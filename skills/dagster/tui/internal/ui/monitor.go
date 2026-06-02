package ui

import (
	"dagster-tui/internal/k8s"
	"fmt"
	"sort"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

const (
	QueueWarning  = 10000
	QueueCritical = 100000
)

type MonitorModel struct {
	client     *k8s.Client
	width      int
	height     int
	lastUpdate time.Time
	loading    bool // true until first data fetch completes

	pods       []k8s.PodInfo
	podMetrics map[string]k8s.PodInfo
	sqsDepths  []k8s.SQSDepth
	dagStats   k8s.DagsterStats
	runsToday  []k8s.RunStats
	err        error

	prevTotalMessages int
	initialSqsDepths  map[string]int // baseline depths from first fetch (for persistent delta)

	kafkaStats         k8s.KafkaStats
	kafkaConsumers     []k8s.KafkaConsumerGroup
	prevKafkaOffset    int64
	kafkaRate          int64 // messages per second
	initialKafkaOffset int64

	// Lag tracking for delta calculation
	prevConsumerLag     map[string]int64 // previous lag per consumer group
	consumerLagDelta    map[string]int64 // lag delta per minute
	prevConsumerFetched map[string]int64 // previous consumed offset per consumer
	consumerConsumed    map[string]int64 // consumed messages since start
	lastFetchTime       time.Time
}

func NewMonitorModel(client *k8s.Client) MonitorModel {
	return MonitorModel{client: client, loading: true}
}

func (m MonitorModel) Init() tea.Cmd {
	return m.fetchData
}

type dataMsg struct {
	pods           []k8s.PodInfo
	podMetrics     map[string]k8s.PodInfo
	sqsDepths      []k8s.SQSDepth
	dagStats       k8s.DagsterStats
	runsToday      []k8s.RunStats
	kafkaStats     k8s.KafkaStats
	kafkaConsumers []k8s.KafkaConsumerGroup
	err            error
}

func (m MonitorModel) fetchData() tea.Msg {
	pods, _ := m.client.GetPods()
	metrics, _ := m.client.GetPodMetrics()
	sqsDepths := m.client.GetAllSQSDepths()
	dagStats, _ := m.client.GetDagsterStats()
	runsToday, _ := m.client.GetRunsToday()
	kafkaStats, _ := m.client.GetKafkaStats()
	kafkaConsumers, _ := m.client.GetKafkaConsumerGroups()

	return dataMsg{
		pods:           pods,
		podMetrics:     metrics,
		sqsDepths:      sqsDepths,
		dagStats:       dagStats,
		runsToday:      runsToday,
		kafkaStats:     kafkaStats,
		kafkaConsumers: kafkaConsumers,
	}
}

func (m MonitorModel) Update(msg tea.Msg) (MonitorModel, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
	case dataMsg:
		// Calculate prev total for throughput indicator
		var total int
		for _, d := range m.sqsDepths {
			total += d.Visible
		}
		m.prevTotalMessages = total

		// Save initial depths only on first fetch (for persistent delta)
		if m.initialSqsDepths == nil {
			m.initialSqsDepths = make(map[string]int)
			for _, d := range msg.sqsDepths {
				m.initialSqsDepths[d.Name] = d.Visible
			}
		}

		// Calculate Kafka rate (messages per second since last fetch)
		if m.prevKafkaOffset > 0 && msg.kafkaStats.TotalOffset > m.prevKafkaOffset {
			// Assume ~5 second interval between fetches
			m.kafkaRate = (msg.kafkaStats.TotalOffset - m.prevKafkaOffset) / 5
		}
		if m.initialKafkaOffset == 0 {
			m.initialKafkaOffset = msg.kafkaStats.TotalOffset
		}
		m.prevKafkaOffset = msg.kafkaStats.TotalOffset
		m.kafkaStats = msg.kafkaStats
		m.kafkaConsumers = msg.kafkaConsumers

		// Track lag deltas per consumer group
		if m.prevConsumerLag == nil {
			m.prevConsumerLag = make(map[string]int64)
			m.consumerLagDelta = make(map[string]int64)
			m.prevConsumerFetched = make(map[string]int64)
			m.consumerConsumed = make(map[string]int64)
		}

		elapsed := time.Since(m.lastFetchTime).Seconds()
		if elapsed > 0 && !m.lastFetchTime.IsZero() {
			for _, cg := range msg.kafkaConsumers {
				if prevLag, ok := m.prevConsumerLag[cg.GroupID]; ok {
					// Calculate lag delta per minute
					lagChange := cg.TotalLag - prevLag
					m.consumerLagDelta[cg.GroupID] = int64(float64(lagChange) / elapsed * 60)

					// Calculate consumed (offset advanced = logEndOffset - lag decreased)
					consumed := msg.kafkaStats.TotalOffset - cg.TotalLag
					if prevConsumed, ok := m.prevConsumerFetched[cg.GroupID]; ok && consumed > prevConsumed {
						m.consumerConsumed[cg.GroupID] += consumed - prevConsumed
					}
					m.prevConsumerFetched[cg.GroupID] = consumed
				}
				m.prevConsumerLag[cg.GroupID] = cg.TotalLag
			}
		} else {
			// First fetch - initialize tracking
			for _, cg := range msg.kafkaConsumers {
				m.prevConsumerLag[cg.GroupID] = cg.TotalLag
				m.prevConsumerFetched[cg.GroupID] = msg.kafkaStats.TotalOffset - cg.TotalLag
			}
		}
		m.lastFetchTime = time.Now()

		m.pods = msg.pods
		m.podMetrics = msg.podMetrics
		m.sqsDepths = msg.sqsDepths
		m.dagStats = msg.dagStats
		m.runsToday = msg.runsToday
		m.err = msg.err
		m.lastUpdate = time.Now()
		m.loading = false
	}
	return m, nil
}

func (m MonitorModel) View() string {
	if m.loading {
		return BoxStyle.Render(TitleStyle.Render("DAGSTER PRODUCTION MONITOR") + "\n\n" + LabelStyle.Render("  Loading..."))
	}

	var sections []string

	sections = append(sections, m.renderHeader())
	sections = append(sections, m.renderCodeServers())
	sections = append(sections, m.renderDagsterCore())
	sections = append(sections, m.renderKafka())
	sections = append(sections, m.renderSQSQueues())
	sections = append(sections, m.renderThroughput())

	return strings.Join(sections, "\n")
}

func (m MonitorModel) renderHeader() string {
	title := TitleStyle.Render("DAGSTER PRODUCTION MONITOR")
	timeStr := LabelStyle.Render("Time: ") + ValueStyle.Render(m.lastUpdate.Format("2006-01-02 15:04:05"))
	return BoxStyle.Render(title + "    " + timeStr)
}

func (m MonitorModel) renderCodeServers() string {
	var lines []string
	lines = append(lines, HeaderStyle.Render("CODE SERVERS"))

	table := NewTable([]Column{
		{Width: 3},  // icon
		{Width: 36}, // name
		{Width: 12}, // cpu
		{Width: 12}, // mem
	})

	codeServers := []string{"code-marketing", "code-payment", "code-sync-shopify-webhook-order"}
	for _, prefix := range codeServers {
		pod := m.findPodByPrefix(prefix)
		if pod == nil {
			lines = append(lines, table.Row(
				WarnStyle.Render("○"),
				prefix,
				"-",
				"-",
			))
			continue
		}

		icon := StatusIcon(pod.Ready && pod.Status == "Running")
		if m.hasCrashLoop(prefix) {
			icon = ErrorStyle.Render("●")
		}

		metrics := m.podMetrics[pod.Name]
		cpuStr := metrics.CPU
		if cpuStr == "" {
			cpuStr = "-"
		}
		memStr := metrics.Memory
		if memStr == "" {
			memStr = "-"
		}

		lines = append(lines, table.Row(
			icon,
			prefix,
			LabelStyle.Render("CPU: ")+cpuStr,
			LabelStyle.Render("MEM: ")+memStr,
		))
	}

	return BoxStyle.Render(strings.Join(lines, "\n"))
}

func (m MonitorModel) renderKafka() string {
	var sections []string

	// Topic section
	sections = append(sections, m.renderKafkaTopics())
	// Consumer Groups section
	sections = append(sections, m.renderKafkaConsumers())

	return strings.Join(sections, "\n")
}

func (m MonitorModel) renderKafkaTopics() string {
	var lines []string
	lines = append(lines, HeaderStyle.Render("KAFKA TOPICS (MSK)"))

	if m.kafkaStats.Partitions == 0 {
		lines = append(lines, WarnStyle.Render("  Failed to fetch Kafka data (check kafka-debug pod)"))
		return BoxStyle.Render(strings.Join(lines, "\n"))
	}

	table := NewTable([]Column{
		{Width: 28}, // topic
		{Width: 12}, // total offset
		{Width: 10}, // partitions
		{Width: 12}, // rate
	})

	lines = append(lines, table.Header("TOPIC", "OFFSET", "PARTITIONS", "RATE"))

	rateStr := "-"
	if m.kafkaRate > 100 {
		rateStr = OKStyle.Render(fmt.Sprintf("%d/s", m.kafkaRate))
	} else if m.kafkaRate > 0 {
		rateStr = ValueStyle.Render(fmt.Sprintf("%d/s", m.kafkaRate))
	}

	lines = append(lines, table.Row(
		m.kafkaStats.Topic,
		k8s.FormatNumber64(m.kafkaStats.TotalOffset),
		fmt.Sprintf("%d", m.kafkaStats.Partitions),
		rateStr,
	))

	return BoxStyle.Render(strings.Join(lines, "\n"))
}

func (m MonitorModel) renderKafkaConsumers() string {
	var lines []string
	lines = append(lines, HeaderStyle.Render("KAFKA CONSUMER GROUPS"))

	if m.kafkaStats.Partitions == 0 {
		return "" // No data yet
	}

	table := NewTable([]Column{
		{Width: 32}, // consumer group
		{Width: 12}, // consumed
		{Width: 10}, // lag
		{Width: 14}, // lag delta/min
	})

	lines = append(lines, table.Header("CONSUMER GROUP", "CONSUMED", "LAG", "LAG Δ/min"))

	for _, cg := range m.kafkaConsumers {
		name := cg.GroupID
		if len(name) > 32 {
			name = name[:29] + "..."
		}

		// Consumed count
		consumed := m.consumerConsumed[cg.GroupID]
		consumedStr := k8s.FormatNumber64(consumed)

		// Lag with color coding
		var lagStr string
		if cg.TotalLag > 10000 {
			lagStr = ErrorStyle.Render(k8s.FormatNumber64(cg.TotalLag))
		} else if cg.TotalLag > 1000 {
			lagStr = WarnStyle.Render(k8s.FormatNumber64(cg.TotalLag))
		} else {
			lagStr = OKStyle.Render(k8s.FormatNumber64(cg.TotalLag))
		}

		// Lag delta per minute
		delta := m.consumerLagDelta[cg.GroupID]
		var deltaStr string
		if delta > 0 {
			deltaStr = ErrorStyle.Render(fmt.Sprintf("↑%s", k8s.FormatNumber64(delta)))
		} else if delta < 0 {
			deltaStr = OKStyle.Render(fmt.Sprintf("↓%s", k8s.FormatNumber64(-delta)))
		} else {
			deltaStr = ValueStyle.Render("→0")
		}

		lines = append(lines, table.Row(name, consumedStr, lagStr, deltaStr))
	}

	return BoxStyle.Render(strings.Join(lines, "\n"))
}

func (m MonitorModel) renderDagsterCore() string {
	var lines []string
	lines = append(lines, HeaderStyle.Render("DAGSTER CORE")+"                                      "+HeaderStyle.Render("OPERATIONS"))

	// Left: core pods, Right: operations
	coreComponents := []string{"dagster-daemon", "dagster-workers-worker-dagster"}
	table := NewTable([]Column{
		{Width: 3},  // icon
		{Width: 20}, // name
		{Width: 12}, // pods
		{Width: 5},  // spacer
		{Width: 20}, // ops label
		{Width: 15}, // ops value
	})

	for i, prefix := range coreComponents {
		running, total := m.countPodsByPrefix(prefix)
		icon := StatusIcon(running == total && total > 0)

		displayName := strings.Replace(prefix, "dagster-", "", 1)
		displayName = strings.Replace(displayName, "-worker-dagster", "", 1)

		podsStr := fmt.Sprintf("%d/%d pods", running, total)

		// Operations on right side
		var opsLabel, opsValue string
		if i == 0 {
			opsLabel = "Active Runs:"
			opsValue = fmt.Sprintf("%d", m.dagStats.ActiveRuns)
		} else if i == 1 {
			opsLabel = "Sensors:"
			sensorsRunning := m.dagStats.SensorsTotal - m.dagStats.SensorsStopped
			if m.dagStats.SensorsStopped > 20 {
				opsValue = ErrorStyle.Render(fmt.Sprintf("%d/%d running", sensorsRunning, m.dagStats.SensorsTotal))
			} else if m.dagStats.SensorsStopped > 5 {
				opsValue = WarnStyle.Render(fmt.Sprintf("%d/%d running", sensorsRunning, m.dagStats.SensorsTotal))
			} else {
				opsValue = OKStyle.Render(fmt.Sprintf("%d/%d running", sensorsRunning, m.dagStats.SensorsTotal))
			}
		}

		lines = append(lines, table.Row(
			icon,
			displayName,
			podsStr,
			"",
			LabelStyle.Render(opsLabel),
			opsValue,
		))
	}

	return BoxStyle.Render(strings.Join(lines, "\n"))
}

func (m MonitorModel) renderSQSQueues() string {
	var lines []string
	lines = append(lines, HeaderStyle.Render("SQS QUEUE DEPTH")+"                                   "+HeaderStyle.Render("RUNS (Today)"))

	table := NewTable([]Column{
		{Width: 18}, // queue name
		{Width: 8},  // visible
		{Width: 10}, // delta
		{Width: 6},  // spacer
		{Width: 3},  // run icon
		{Width: 12}, // run status
		{Width: 8},  // run count
	})

	// Sort SQS by visible descending
	sqsSorted := make([]k8s.SQSDepth, len(m.sqsDepths))
	copy(sqsSorted, m.sqsDepths)
	sort.Slice(sqsSorted, func(i, j int) bool {
		return sqsSorted[i].Visible > sqsSorted[j].Visible
	})

	// Display queues (show top 4 by depth)
	displayQueues := []string{"orders_create", "orders_update", "refunds_create", "order_transactions"}
	for i, qName := range displayQueues {
		var depth k8s.SQSDepth
		for _, d := range m.sqsDepths {
			if d.Name == qName {
				depth = d
				break
			}
		}

		displayName := strings.ReplaceAll(qName, "_", " ")
		visibleStr := k8s.FormatNumber(depth.Visible)
		if depth.Visible > QueueCritical {
			visibleStr = ErrorStyle.Render(visibleStr)
		} else if depth.Visible > QueueWarning {
			visibleStr = WarnStyle.Render(visibleStr)
		}

		// Calculate delta from initial (persistent)
		deltaStr := ""
		if initial, ok := m.initialSqsDepths[qName]; ok {
			delta := depth.Visible - initial
			if delta > 0 {
				deltaStr = WarnStyle.Render(fmt.Sprintf("↑%s", k8s.FormatNumber(delta)))
			} else if delta < 0 {
				deltaStr = OKStyle.Render(fmt.Sprintf("↓%s", k8s.FormatNumber(-delta)))
			}
		}

		// Runs on right
		var runIcon, runStatus, runCount string
		if i < len(m.runsToday) {
			run := m.runsToday[i]
			switch run.Status {
			case "SUCCESS":
				runIcon = OKStyle.Render("✓")
			case "FAILURE":
				runIcon = ErrorStyle.Render("✗")
			case "CANCELED":
				runIcon = WarnStyle.Render("⊘")
			default:
				runIcon = LabelStyle.Render("●")
			}
			runStatus = run.Status
			runCount = fmt.Sprintf("%d", run.Count)
		}

		lines = append(lines, table.Row(
			displayName,
			visibleStr,
			deltaStr,
			"",
			runIcon,
			runStatus,
			runCount,
		))
	}

	return BoxStyle.Render(strings.Join(lines, "\n"))
}

func (m MonitorModel) renderThroughput() string {
	var lines []string
	lines = append(lines, HeaderStyle.Render("THROUGHPUT"))

	var totalVisible, totalInFlight int
	for _, d := range m.sqsDepths {
		totalVisible += d.Visible
		totalInFlight += d.InFlight
	}

	totalStr := k8s.FormatNumber(totalVisible)
	if totalVisible > 500000 {
		totalStr = ErrorStyle.Render(totalStr)
	} else if totalVisible > 100000 {
		totalStr = WarnStyle.Render(totalStr)
	}

	lines = append(lines, fmt.Sprintf("%s %s    %s %s",
		LabelStyle.Render("Total SQS pending:"),
		totalStr,
		LabelStyle.Render("In-flight:"),
		fmt.Sprintf("%d", totalInFlight),
	))

	// Processing rate
	if m.prevTotalMessages > 0 && m.prevTotalMessages != totalVisible {
		diff := m.prevTotalMessages - totalVisible
		if diff > 0 {
			lines = append(lines, OKStyle.Render("↓")+" Processing: queue shrinking")
		} else {
			lines = append(lines, WarnStyle.Render("↑")+" Incoming: queue growing")
		}
	}

	// Warning if sensors stopped
	if m.dagStats.SensorsStopped > 20 {
		lines = append(lines, ErrorStyle.Render("⚠ SENSORS STOPPED!")+" Check dagster webserver")
	}

	return BoxStyle.Render(strings.Join(lines, "\n"))
}

func (m MonitorModel) findPodByPrefix(prefix string) *k8s.PodInfo {
	for i, pod := range m.pods {
		if strings.HasPrefix(pod.Name, prefix) && pod.Status == "Running" {
			return &m.pods[i]
		}
	}
	return nil
}

func (m MonitorModel) hasCrashLoop(prefix string) bool {
	for _, pod := range m.pods {
		if strings.HasPrefix(pod.Name, prefix) && pod.Status == "CrashLoopBackOff" {
			return true
		}
	}
	return false
}

func (m MonitorModel) countPodsByPrefix(prefix string) (running, total int) {
	for _, pod := range m.pods {
		if strings.HasPrefix(pod.Name, prefix) {
			total++
			if pod.Ready && pod.Status == "Running" {
				running++
			}
		}
	}
	return
}

func (m MonitorModel) RefreshCmd() tea.Cmd {
	return m.fetchData
}

func (m MonitorModel) Render(width, height int) string {
	m.width = width
	m.height = height
	return lipgloss.NewStyle().Width(width).Render(m.View())
}
