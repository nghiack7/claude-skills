---
name: tui
description: This skill should be used when the user asks to "build a TUI", "create terminal UI", "interactive debugger", "Bubbletea app", or mentions terminal UI, TUI tools, Bubbletea, or interactive monitoring dashboards.
patterns: []
---

# Service Debugger TUI

Interactive terminal UI for inspecting and debugging services with real-time data display, built with Bubbletea.

## Quick Start

```bash
mkdir service-debugger
cd service-debugger
go mod init service-debugger
go get github.com/charmbracelet/bubbletea@latest
go get github.com/charmbracelet/lipgloss@latest
go get github.com/joho/godotenv@latest

go run main.go <entity-id-or-name>
```

## Complete Service Debugger TUI

### Project Structure

```
service-debugger/
├── go.mod
├── go.sum
└── main.go              # Complete TUI application
```

### main.go

```go
package main

import (
	"context"
	"fmt"
	"log"
	"os"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
	"github.com/joho/godotenv"
)

func init() {
	// Load env from project secret or .env file
	godotenv.Load(".env")
}

// Messages
type dataMsg struct {
	data *EntityInfo
	err  error
}

type tickMsg time.Time

// EntityInfo holds all entity data — replace fields to match your domain
type EntityInfo struct {
	Basic      *BasicInfo
	Stats      *Statistics
	SyncStatus *SyncStatus
	Metadata   map[string]int64
}

type BasicInfo struct {
	ID       string
	Name     string
	Domain   string
	Email    string
	Status   string
	Plan     string
	Created  string
	Updated  string
}

type Statistics struct {
	TotalRecords   int64
	Records30d     int64
	Records7d      int64
	Records1d      int64
	DailyAvg       int64
}

type SyncStatus struct {
	LastSync   string
	LastUpdate string
	Connected  bool
	ItemCount  int
}

// Model
type Model struct {
	query      string
	entityData *EntityInfo
	loading    bool
	err        error
	width      int
	height     int
	lastUpdate time.Time
	scrollPos  int
}

func NewModel(query string) Model {
	return Model{
		query:   query,
		loading: true,
	}
}

func (m Model) Init() tea.Cmd {
	return m.fetchData()
}

func (m Model) fetchData() tea.Cmd {
	return func() tea.Msg {
		data, err := fetchEntityData(m.query)
		return dataMsg{data: data, err: err}
	}
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch msg := msg.(type) {
	case tea.KeyMsg:
		return m.handleKeyPress(msg)
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		return m, nil
	case dataMsg:
		m.loading = false
		m.entityData = msg.data
		m.err = msg.err
		m.lastUpdate = time.Now()
		return m, nil
	}
	return m, nil
}

func (m Model) handleKeyPress(msg tea.KeyMsg) (tea.Model, tea.Cmd) {
	switch msg.String() {
	case "q", "ctrl+c":
		return m, tea.Quit
	case "r", "R":
		m.loading = true
		return m, m.fetchData()
	case "up", "k":
		if m.scrollPos > 0 {
			m.scrollPos--
		}
	case "down", "j":
		m.scrollPos++
	}
	return m, nil
}

func (m Model) View() string {
	if m.loading {
		return m.renderLoading()
	}
	if m.err != nil {
		return m.renderError()
	}
	return m.renderView()
}

// fetchEntityData — replace with your actual data source (DB, API, file, etc.)
func fetchEntityData(query string) (*EntityInfo, error) {
	// Example: load from environment-configured data source
	dsn := os.Getenv("DATA_SOURCE_URI")
	if dsn == "" {
		return nil, fmt.Errorf("DATA_SOURCE_URI not set")
	}

	// TODO: connect to your data source and populate EntityInfo
	// This is a stub — replace with real lookup logic
	return &EntityInfo{
		Basic: &BasicInfo{
			ID:      "example-id",
			Name:    query,
			Domain:  "example.com",
			Email:   "admin@example.com",
			Status:  "active",
			Plan:    "pro",
			Created: time.Now().Format("2006-01-02"),
			Updated: time.Now().Format("2006-01-02 15:04"),
		},
		Stats: &Statistics{
			TotalRecords: 12345,
			Records30d:   890,
			Records7d:    210,
			Records1d:    32,
			DailyAvg:     30,
		},
		SyncStatus: &SyncStatus{
			LastSync:   time.Now().Add(-5 * time.Minute).Format("2006-01-02 15:04"),
			LastUpdate: time.Now().Format("2006-01-02 15:04"),
			Connected:  true,
			ItemCount:  42,
		},
		Metadata: map[string]int64{
			"records": 12345,
			"events":  678,
			"errors":  3,
		},
	}, nil
}

// Styles
var (
	Primary   = lipgloss.Color("#7D56F4")
	Secondary = lipgloss.Color("#6C757D")
	Success   = lipgloss.Color("#28A745")
	Warning   = lipgloss.Color("#FFC107")
	Danger    = lipgloss.Color("#DC3545")
	Info      = lipgloss.Color("#17A2B8")
	Dim       = lipgloss.Color("#6C757D")
	Muted     = lipgloss.Color("#ADB5BD")

	TitleStyle   = lipgloss.NewStyle().Bold(true).Foreground(Primary)
	HeaderStyle  = lipgloss.NewStyle().Bold(true).Foreground(Secondary)
	ErrorStyle   = lipgloss.NewStyle().Foreground(Danger)
	WarnStyle    = lipgloss.NewStyle().Foreground(Warning)
	OKStyle      = lipgloss.NewStyle().Foreground(Success)
	LabelStyle   = lipgloss.NewStyle().Foreground(Dim)
	ValueStyle   = lipgloss.NewStyle().Foreground(Primary)
	SectionStyle = lipgloss.NewStyle().Border(lipgloss.NormalBorder()).BorderForeground(Muted).Padding(1, 1)
)

func StatusIcon(ok bool) string {
	if ok {
		return OKStyle.Render("✓")
	}
	return ErrorStyle.Render("✗")
}

func StatusText(ok bool) string {
	if ok {
		return OKStyle.Render("connected")
	}
	return WarnStyle.Render("disconnected")
}

func (m Model) renderView() string {
	sections := []string{
		m.renderHeader(),
		"",
		SectionStyle.Render("ENTITY INFORMATION"),
		m.renderBasicInfo(),
		"",
		SectionStyle.Render("STATISTICS"),
		m.renderStatistics(),
		"",
		SectionStyle.Render("SYNC STATUS"),
		m.renderSyncStatus(),
		"",
		SectionStyle.Render("DATA COLLECTIONS"),
		m.renderMetadata(),
		"",
		m.renderFooter(),
	}

	return lipgloss.JoinVertical(lipgloss.Left, sections...)
}

func (m Model) renderHeader() string {
	title := TitleStyle.Render("SERVICE DEBUGGER")
	timeStr := m.lastUpdate.Format("2006-01-02 15:04:05")

	return lipgloss.JoinHorizontal(lipgloss.Top,
		title,
		lipgloss.NewStyle().Width(m.width-len(title)-len(timeStr)-4).Render(""),
		LabelStyle.Render(timeStr),
	)
}

func (m Model) renderBasicInfo() string {
	info := m.entityData.Basic
	rows := []string{
		keyValue("ID", info.ID, 20),
		keyValue("Name", info.Name, 20),
		keyValue("Domain", info.Domain, 20),
		keyValue("Email", info.Email, 20),
		keyValue("Status", info.Status, 20),
		keyValue("Plan", info.Plan, 20),
		keyValue("Created", info.Created, 20),
		keyValue("Updated", info.Updated, 20),
	}
	return lipgloss.JoinVertical(lipgloss.Left, rows...)
}

func (m Model) renderStatistics() string {
	stats := m.entityData.Stats
	rows := []string{
		keyValue("Total Records", formatInt(stats.TotalRecords), 25),
		keyValue("Records (30d)", formatInt(stats.Records30d), 25),
		keyValue("Records (7d)", formatInt(stats.Records7d), 25),
		keyValue("Daily Avg", formatInt(stats.DailyAvg), 25),
	}
	return lipgloss.JoinVertical(lipgloss.Left, rows...)
}

func (m Model) renderSyncStatus() string {
	sync := m.entityData.SyncStatus
	rows := []string{
		"Last Sync:   " + sync.LastSync + " " + StatusIcon(true),
		"Last Update: " + sync.LastUpdate + " " + StatusIcon(true),
		"Connection:  " + StatusText(sync.Connected),
	}
	return lipgloss.JoinVertical(lipgloss.Left, rows...)
}

func (m Model) renderMetadata() string {
	meta := m.entityData.Metadata
	rows := []string{
		"Records: " + formatInt(meta["records"]) + " docs",
		"Events:  " + formatInt(meta["events"]) + " docs",
		"Errors:  " + formatInt(meta["errors"]) + " docs",
	}
	return lipgloss.JoinVertical(lipgloss.Left, rows...)
}

func (m Model) renderFooter() string {
	help := LabelStyle.Render("[R]efresh  [↑/↓] Scroll  [Q]uit")
	return lipgloss.NewStyle().Width(m.width).Align(lipgloss.Right).Render(help)
}

func (m Model) renderLoading() string {
	loading := TitleStyle.Render("Loading data...")
	return lipgloss.NewStyle().Width(m.width).Align(lipgloss.Center).Height(m.height).Render(loading)
}

func (m Model) renderError() string {
	title := ErrorStyle.Render("Error loading data")
	msg := m.err.Error()
	return lipgloss.NewStyle().Width(m.width).Align(lipgloss.Center).Height(m.height).
		Render(title + "\n\n" + msg + "\n\n" + LabelStyle.Render("[Q]uit"))
}

func keyValue(label, value string, labelWidth int) string {
	labelStyle := lipgloss.NewStyle().Width(labelWidth).Foreground(Dim)
	return labelStyle.Render(label+":") + " " + ValueStyle.Render(value)
}

func formatInt(n int64) string {
	return fmt.Sprintf("%d", n)
}

func main() {
	if len(os.Args) < 2 {
		fmt.Println("Usage: service-debugger <entity-id|name|domain>")
		os.Exit(1)
	}

	query := os.Args[1]

	p := tea.NewProgram(
		NewModel(query),
		tea.WithAltScreen(),
		tea.WithMouseCellMotion(),
	)

	if err := p.Start(); err != nil {
		log.Fatal(err)
	}
}
```

## Key Controls

- **q/ctrl+c**: Quit
- **r**: Refresh data
- **up/k**: Scroll up
- **down/j**: Scroll down

## Color Scheme

- **Purple (#7D56F4)**: Primary, titles
- **Green (#28A745)**: Success, active items
- **Yellow (#FFC107)**: Warnings
- **Red (#DC3545)**: Errors
- **Blue (#17A2B8)**: Info
- **Gray**: Labels, muted text

## Extending the TUI

### Add tabs for multiple views:

```go
type tabsModel struct {
    tabs      []string
    activeTab int
    models    map[string]TabModel
}

func (m tabsModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tea.KeyMsg:
        switch msg.String() {
        case "tab", "right":
            m.activeTab = (m.activeTab + 1) % len(m.tabs)
        case "left":
            m.activeTab = (m.activeTab - 1 + len(m.tabs)) % len(m.tabs)
        }
    }
    return m, nil
}
```

### Add auto-refresh:

```go
type tickMsg time.Time

func (m Model) Init() tea.Cmd {
    return tea.Batch(
        m.fetchData(),
        tea.Tick(30*time.Second, func(t time.Time) tea.Msg {
            return tickMsg(t)
        }),
    )
}

func (m Model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
    switch msg := msg.(type) {
    case tickMsg:
        return m, tea.Batch(m.fetchData(), tea.Tick(30*time.Second, func(t time.Time) tea.Msg {
            return tickMsg(t)
        }))
    }
    return m, nil
}
```

## Building

```bash
go build -o service-debugger main.go
./service-debugger my-entity-name
```
