package ui

import "github.com/charmbracelet/lipgloss"

var (
	Primary   = lipgloss.Color("#7D56F4")
	Secondary = lipgloss.Color("#6C757D")
	Success   = lipgloss.Color("#28A745")
	Warning   = lipgloss.Color("#FFC107")
	Error     = lipgloss.Color("#DC3545")
	Info      = lipgloss.Color("#17A2B8")
	Dim       = lipgloss.Color("#6C757D")
	Magenta   = lipgloss.Color("#E040FB")

	TitleStyle  = lipgloss.NewStyle().Bold(true).Foreground(Primary)
	HeaderStyle = lipgloss.NewStyle().Bold(true).Foreground(Secondary)
	ErrorStyle  = lipgloss.NewStyle().Foreground(Error)
	WarnStyle   = lipgloss.NewStyle().Foreground(Warning)
	OKStyle     = lipgloss.NewStyle().Foreground(Success)
	InfoStyle   = lipgloss.NewStyle().Foreground(Info)
	LabelStyle  = lipgloss.NewStyle().Foreground(Dim)
	ValueStyle  = lipgloss.NewStyle().Foreground(lipgloss.Color("#FFFFFF"))
	ChangeStyle = lipgloss.NewStyle().Foreground(Magenta)

	BoxStyle = lipgloss.NewStyle().
			Border(lipgloss.RoundedBorder()).
			BorderForeground(Dim).
			Padding(0, 1)
)

func StatusIcon(ready bool) string {
	if ready {
		return OKStyle.Render("●")
	}
	return ErrorStyle.Render("●")
}

func StatusText(status string) string {
	switch status {
	case "Running":
		return OKStyle.Render(status)
	case "Pending":
		return WarnStyle.Render(status)
	case "CrashLoopBackOff", "Error", "Failed":
		return ErrorStyle.Render(status)
	default:
		return status
	}
}

func FormatChange(value string, prev string, isUp bool) string {
	if prev == "" || value == prev {
		return value
	}
	if isUp {
		return ChangeStyle.Render(value) + " " + OKStyle.Render("▲")
	}
	return ChangeStyle.Render(value) + " " + ErrorStyle.Render("▼")
}
