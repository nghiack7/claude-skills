package ui

import "github.com/charmbracelet/lipgloss"

type Column struct {
	Width int
	Align lipgloss.Position
}

type Table struct {
	columns []Column
}

func NewTable(columns []Column) *Table {
	return &Table{columns: columns}
}

func (t *Table) Row(cells ...string) string {
	var rendered []string
	for i, cell := range cells {
		if i >= len(t.columns) {
			break
		}
		col := t.columns[i]
		style := lipgloss.NewStyle().Width(col.Width)
		if col.Align == lipgloss.Right {
			style = style.Align(lipgloss.Right)
		} else {
			style = style.Align(lipgloss.Left)
		}
		rendered = append(rendered, style.Render(cell))
	}
	return lipgloss.JoinHorizontal(lipgloss.Top, rendered...)
}

func (t *Table) Header(cells ...string) string {
	var rendered []string
	for i, cell := range cells {
		if i >= len(t.columns) {
			break
		}
		col := t.columns[i]
		style := lipgloss.NewStyle().
			Width(col.Width).
			Foreground(Dim)
		if col.Align == lipgloss.Right {
			style = style.Align(lipgloss.Right)
		}
		rendered = append(rendered, style.Render(cell))
	}
	return lipgloss.JoinHorizontal(lipgloss.Top, rendered...)
}

func KeyValue(label string, value string, labelWidth int) string {
	labelStyle := lipgloss.NewStyle().Width(labelWidth).Foreground(Dim)
	return labelStyle.Render(label+":") + " " + value
}
