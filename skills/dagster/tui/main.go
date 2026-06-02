package main

import (
	"dagster-tui/internal/k8s"
	"dagster-tui/internal/ui"
	"flag"
	"fmt"
	"os"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

var version = "1.0.0"

type mainModel struct {
	monitor  ui.MonitorModel
	width    int
	height   int
	interval time.Duration
}

func newMainModel(interval time.Duration) mainModel {
	client := k8s.NewClient()
	return mainModel{
		monitor:  ui.NewMonitorModel(client),
		interval: interval,
	}
}

type tickMsg time.Time

func tickCmd(interval time.Duration) tea.Cmd {
	return tea.Tick(interval, func(t time.Time) tea.Msg {
		return tickMsg(t)
	})
}

func (m mainModel) Init() tea.Cmd {
	return tea.Batch(m.monitor.Init(), tickCmd(m.interval))
}

func (m mainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "q", "ctrl+c":
			return m, tea.Quit
		case "r":
			return m, m.monitor.RefreshCmd()
		case "+", "=":
			// Increase interval
			if m.interval < 60*time.Second {
				m.interval += time.Second
			}
		case "-", "_":
			// Decrease interval
			if m.interval > time.Second {
				m.interval -= time.Second
			}
		}
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		m.monitor, _ = m.monitor.Update(msg)
	case tickMsg:
		return m, tea.Batch(m.monitor.RefreshCmd(), tickCmd(m.interval))
	default:
		var cmd tea.Cmd
		m.monitor, cmd = m.monitor.Update(msg)
		return m, cmd
	}
	return m, nil
}

func (m mainModel) View() string {
	content := m.monitor.Render(m.width, m.height-2)
	footer := lipgloss.NewStyle().Foreground(lipgloss.Color("#6C757D")).
		Render(fmt.Sprintf("[r] Refresh  [+/-] Interval  [q] Quit  Auto-refresh: %ds", int(m.interval.Seconds())))
	return lipgloss.JoinVertical(lipgloss.Left, content, "", footer)
}

func printHelp() {
	fmt.Printf(`dagster-tui v%s - Dagster Production Monitor

USAGE:
    dagster-tui [OPTIONS]

OPTIONS:
    -i, --interval <seconds>    Refresh interval in seconds (default: 5, range: 1-60)
    -h, --help                  Show this help message
    -v, --version               Show version

RUNTIME KEYS:
    r         Manual refresh
    +/=       Increase refresh interval by 1s
    -/_       Decrease refresh interval by 1s
    q         Quit

EXAMPLES:
    dagster-tui                 Start with 5s refresh interval
    dagster-tui -i 10           Start with 10s refresh interval
    dagster-tui --interval 2    Start with 2s refresh interval

`, version)
}

func main() {
	var interval int
	var showHelp, showVersion bool

	flag.IntVar(&interval, "i", 5, "Refresh interval in seconds")
	flag.IntVar(&interval, "interval", 5, "Refresh interval in seconds")
	flag.BoolVar(&showHelp, "h", false, "Show help")
	flag.BoolVar(&showHelp, "help", false, "Show help")
	flag.BoolVar(&showVersion, "v", false, "Show version")
	flag.BoolVar(&showVersion, "version", false, "Show version")

	flag.Usage = printHelp
	flag.Parse()

	if showHelp {
		printHelp()
		return
	}

	if showVersion {
		fmt.Printf("dagster-tui v%s\n", version)
		return
	}

	// Validate interval
	if interval < 1 {
		interval = 1
	} else if interval > 60 {
		interval = 60
	}

	p := tea.NewProgram(newMainModel(time.Duration(interval)*time.Second), tea.WithAltScreen())
	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error: %v\n", err)
		os.Exit(1)
	}
}
