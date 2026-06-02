package k8s

import (
	"context"
	"encoding/json"
	"fmt"
	"os/exec"
	"strings"
	"time"
)

const (
	Context    = "<KUBE_CONTEXT>"
	Namespace  = "dagster"
	AWSProfile = "<AWS_PROFILE>"
	AWSRegion  = "<AWS_REGION>"

	KafkaBroker = "<KAFKA_BROKER_HOST>:9092"
	KafkaTopic  = "order_transaction_create"
)

var SQSQueues = map[string]string{
	"orders_create":      "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeOrdersCreateQueue",
	"orders_update":      "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeOrdersUpdatedV2Queue",
	"orders_delete":      "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeOrdersDeleteQueue",
	"orders_edit":        "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeOrdersEditedQueue",
	"refunds_create":     "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeRefundsCreateQueue",
	"returns_process":    "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeReturnsProcessQueue",
	"returns_approve":    "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeReturnsApproveQueue",
	"returns_cancel":     "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeReturnsCancelQueue",
	"order_transactions": "https://sqs.<AWS_REGION>.amazonaws.com/<AWS_ACCOUNT_ID>/<PREFIX>-DagsterEventBridgeOrderTransactionsCreateQueue",
}

type Client struct {
	daemonPod string
}

func NewClient() *Client {
	return &Client{}
}

type PodInfo struct {
	Name     string
	Ready    bool
	Status   string
	Restarts int
	Age      time.Duration
	CPU      string
	Memory   string
}

type SQSDepth struct {
	Name      string
	Visible   int
	InFlight  int
}

type DagsterStats struct {
	ActiveRuns     int
	SensorsStopped int
	SensorsTotal   int
}

type RunStats struct {
	Status string
	Count  int
}

type KafkaStats struct {
	Topic       string
	Partitions  int
	TotalOffset int64
	Rate        int64 // messages per second (calculated from offset delta)
}

type KafkaConsumerGroup struct {
	GroupID    string
	Topic      string
	TotalLag   int64
	Partitions int
}

func (c *Client) kubectl(args ...string) (string, error) {
	fullArgs := append([]string{"--context", Context, "-n", Namespace}, args...)
	cmd := exec.Command("kubectl", fullArgs...)
	out, err := cmd.Output()
	return string(out), err
}

func (c *Client) GetPods() ([]PodInfo, error) {
	out, err := c.kubectl("get", "pods", "-o", "json")
	if err != nil {
		return nil, err
	}

	var result struct {
		Items []struct {
			Metadata struct {
				Name              string    `json:"name"`
				CreationTimestamp time.Time `json:"creationTimestamp"`
			} `json:"metadata"`
			Status struct {
				Phase             string `json:"phase"`
				ContainerStatuses []struct {
					Ready        bool `json:"ready"`
					RestartCount int  `json:"restartCount"`
				} `json:"containerStatuses"`
			} `json:"status"`
		} `json:"items"`
	}
	if err := json.Unmarshal([]byte(out), &result); err != nil {
		return nil, err
	}

	var pods []PodInfo
	for _, item := range result.Items {
		ready := true
		restarts := 0
		for _, cs := range item.Status.ContainerStatuses {
			if !cs.Ready {
				ready = false
			}
			restarts += cs.RestartCount
		}
		pods = append(pods, PodInfo{
			Name:     item.Metadata.Name,
			Ready:    ready,
			Status:   item.Status.Phase,
			Restarts: restarts,
			Age:      time.Since(item.Metadata.CreationTimestamp),
		})
	}
	return pods, nil
}

func (c *Client) GetPodMetrics() (map[string]PodInfo, error) {
	out, err := c.kubectl("top", "pods", "--no-headers")
	if err != nil {
		return nil, err
	}

	metrics := make(map[string]PodInfo)
	for _, line := range strings.Split(strings.TrimSpace(out), "\n") {
		if line == "" {
			continue
		}
		fields := strings.Fields(line)
		if len(fields) >= 3 {
			metrics[fields[0]] = PodInfo{
				Name:   fields[0],
				CPU:    fields[1],
				Memory: fields[2],
			}
		}
	}
	return metrics, nil
}

func (c *Client) GetDaemonPod() string {
	if c.daemonPod == "" {
		out, _ := c.kubectl("get", "pods", "-l", "component=dagster-daemon",
			"-o", "jsonpath={.items[0].metadata.name}")
		c.daemonPod = strings.TrimSpace(out)
	}
	return c.daemonPod
}

func (c *Client) QueryDagsterDB(query string) (string, error) {
	daemonPod := c.GetDaemonPod()
	if daemonPod == "" {
		return "", fmt.Errorf("daemon pod not found")
	}

	pythonCode := fmt.Sprintf(`
import os, psycopg2
conn = psycopg2.connect(
    host='<DAGSTER_PG_HOST>',
    database='dagster',
    user='postgres',
    password=os.environ['DAGSTER_PG_PASSWORD'],
    port=5432
)
cur = conn.cursor()
cur.execute('''%s''')
for row in cur.fetchall():
    print('|'.join(str(x) for x in row))
conn.close()
`, query)

	out, err := c.kubectl("exec", daemonPod, "-c", "dagster", "--",
		"python3", "-c", pythonCode)
	return out, err
}

func (c *Client) GetDagsterStats() (DagsterStats, error) {
	query := `
SELECT
    (SELECT COUNT(*) FROM runs WHERE status IN ('STARTED', 'QUEUED', 'STARTING')) as active,
    (SELECT COUNT(*) FROM instigators WHERE instigator_type = 'SENSOR' AND status = 'STOPPED') as sensors_stopped,
    (SELECT COUNT(*) FROM instigators WHERE instigator_type = 'SENSOR') as sensors_total
`
	out, err := c.QueryDagsterDB(query)
	if err != nil {
		return DagsterStats{}, err
	}

	var stats DagsterStats
	parts := strings.Split(strings.TrimSpace(out), "|")
	if len(parts) >= 3 {
		fmt.Sscanf(parts[0], "%d", &stats.ActiveRuns)
		fmt.Sscanf(parts[1], "%d", &stats.SensorsStopped)
		fmt.Sscanf(parts[2], "%d", &stats.SensorsTotal)
	}
	return stats, nil
}

func (c *Client) GetRunsToday() ([]RunStats, error) {
	query := `SELECT status, COUNT(*) FROM runs WHERE create_timestamp > CURRENT_DATE GROUP BY status ORDER BY count DESC`
	out, err := c.QueryDagsterDB(query)
	if err != nil {
		return nil, err
	}

	var runs []RunStats
	for _, line := range strings.Split(strings.TrimSpace(out), "\n") {
		if line == "" {
			continue
		}
		parts := strings.Split(line, "|")
		if len(parts) >= 2 {
			var count int
			fmt.Sscanf(parts[1], "%d", &count)
			runs = append(runs, RunStats{
				Status: parts[0],
				Count:  count,
			})
		}
	}
	return runs, nil
}

func (c *Client) GetSQSDepth(queueURL string) (int, int, error) {
	cmd := exec.Command("aws", "sqs", "get-queue-attributes",
		"--queue-url", queueURL,
		"--attribute-names", "ApproximateNumberOfMessages", "ApproximateNumberOfMessagesNotVisible",
		"--region", AWSRegion,
		"--profile", AWSProfile)
	out, err := cmd.Output()
	if err != nil {
		return 0, 0, err
	}

	var result struct {
		Attributes struct {
			ApproximateNumberOfMessages           string `json:"ApproximateNumberOfMessages"`
			ApproximateNumberOfMessagesNotVisible string `json:"ApproximateNumberOfMessagesNotVisible"`
		} `json:"Attributes"`
	}
	if err := json.Unmarshal(out, &result); err != nil {
		return 0, 0, err
	}

	var visible, inFlight int
	fmt.Sscanf(result.Attributes.ApproximateNumberOfMessages, "%d", &visible)
	fmt.Sscanf(result.Attributes.ApproximateNumberOfMessagesNotVisible, "%d", &inFlight)
	return visible, inFlight, nil
}

func (c *Client) GetAllSQSDepths() []SQSDepth {
	var depths []SQSDepth
	for name, url := range SQSQueues {
		visible, inFlight, _ := c.GetSQSDepth(url)
		depths = append(depths, SQSDepth{
			Name:     name,
			Visible:  visible,
			InFlight: inFlight,
		})
	}
	return depths
}

func FormatNumber(n int) string {
	if n >= 1000000 {
		return fmt.Sprintf("%.1fM", float64(n)/1000000)
	} else if n >= 1000 {
		return fmt.Sprintf("%.1fK", float64(n)/1000)
	}
	return fmt.Sprintf("%d", n)
}

func FormatNumber64(n int64) string {
	if n >= 1000000 {
		return fmt.Sprintf("%.1fM", float64(n)/1000000)
	} else if n >= 1000 {
		return fmt.Sprintf("%.1fK", float64(n)/1000)
	}
	return fmt.Sprintf("%d", n)
}

func (c *Client) GetKafkaStats() (KafkaStats, error) {
	// Use kafka-debug pod with kafka-consumer-groups to get offsets
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "kubectl", "--context", Context, "-n", Namespace,
		"exec", "kafka-debug", "--",
		"kafka-consumer-groups",
		"--bootstrap-server", KafkaBroker,
		"--group", "<KAFKA_CONSUMER_GROUP>",
		"--describe",
		"--timeout", "5000")
	out, err := cmd.Output()
	if err != nil {
		return KafkaStats{}, err
	}

	var totalOffset int64
	partitions := 0
	for _, line := range strings.Split(string(out), "\n") {
		if line == "" || strings.HasPrefix(line, "GROUP") || strings.HasPrefix(line, "Consumer group") {
			continue
		}
		// Parse: GROUP TOPIC PARTITION CURRENT-OFFSET LOG-END-OFFSET LAG ...
		parts := strings.Fields(line)
		if len(parts) >= 5 {
			var logEndOffset int64
			fmt.Sscanf(parts[4], "%d", &logEndOffset)
			totalOffset += logEndOffset
			partitions++
		}
	}

	return KafkaStats{
		Topic:       KafkaTopic,
		Partitions:  partitions,
		TotalOffset: totalOffset,
	}, nil
}

func (c *Client) GetKafkaConsumerGroups() ([]KafkaConsumerGroup, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "kubectl", "--context", Context, "-n", Namespace,
		"exec", "kafka-debug", "--",
		"kafka-consumer-groups",
		"--bootstrap-server", KafkaBroker,
		"--list",
		"--timeout", "5000")
	out, err := cmd.Output()
	if err != nil {
		return nil, err
	}

	var groups []KafkaConsumerGroup
	for _, groupID := range strings.Split(strings.TrimSpace(string(out)), "\n") {
		if groupID == "" || strings.HasPrefix(groupID, "amazon.msk.canary") {
			continue
		}

		// Get lag for this group
		lag, partitions := c.getConsumerGroupLag(groupID)
		groups = append(groups, KafkaConsumerGroup{
			GroupID:    groupID,
			Topic:      KafkaTopic,
			TotalLag:   lag,
			Partitions: partitions,
		})
	}
	return groups, nil
}

func (c *Client) getConsumerGroupLag(groupID string) (int64, int) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "kubectl", "--context", Context, "-n", Namespace,
		"exec", "kafka-debug", "--",
		"kafka-consumer-groups",
		"--bootstrap-server", KafkaBroker,
		"--group", groupID,
		"--describe",
		"--timeout", "5000")
	out, err := cmd.Output()
	if err != nil {
		return 0, 0
	}

	var totalLag int64
	partitions := 0
	for _, line := range strings.Split(string(out), "\n") {
		if line == "" || strings.HasPrefix(line, "GROUP") || strings.HasPrefix(line, "Consumer group") {
			continue
		}
		parts := strings.Fields(line)
		if len(parts) >= 6 {
			var lag int64
			fmt.Sscanf(parts[5], "%d", &lag)
			totalLag += lag
			partitions++
		}
	}
	return totalLag, partitions
}
