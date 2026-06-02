---
name: chart-generator
description: This skill should be used when the user asks to "generate a chart", "create a graph", "plot data", "make a bar chart", "draw a pie chart", "visualize data", or mentions matplotlib, data visualization, or chart generation.
---

## Related Skills

- **mongodb** - Query data for charts
- **starrocks** - OLAP queries for analytics
- **bigquery** - Big data analysis
- **amplitude** - Product analytics data

# Chart Generator

Generate publication-quality chart images using Python and matplotlib.

## Quick Start

```bash
python3 .claude/skills/chart-generator/generate_chart.py \
  --type bar \
  --data '{"labels": ["A", "B", "C"], "values": [10, 20, 15]}' \
  --title "My Chart" \
  --output "my_chart.png"
```

## Chart Types

| Type | Use Case |
|------|----------|
| `bar` | Comparing categories |
| `line` | Trends over time |
| `pie` | Part-to-whole relationships |
| `scatter` | Correlation between variables |
| `area` | Cumulative trends |
| `hbar` | Horizontal bar comparison |

## Data Formats

**Single series (bar, line, pie, area, hbar):**
```json
{"labels": ["Q1", "Q2", "Q3", "Q4"], "values": [100, 150, 130, 180]}
```

**Multi-series (bar, line, area):**
```json
{
  "labels": ["Jan", "Feb", "Mar"],
  "series": [
    {"name": "Sales", "values": [100, 120, 140]},
    {"name": "Costs", "values": [80, 90, 100]}
  ]
}
```

**Scatter plot:**
```json
{"x": [1, 2, 3, 4, 5], "y": [2, 4, 5, 4, 5]}
```

**Multi-series scatter:**
```json
{
  "series": [
    {"name": "Group A", "x": [1, 2, 3], "y": [2, 4, 3]},
    {"name": "Group B", "x": [1, 2, 3], "y": [1, 3, 5]}
  ]
}
```

## Command Options

```
--type       Chart type (bar, line, pie, scatter, area, hbar)
--data       JSON data string
--title      Chart title
--output     Output filename (e.g. my_chart.png)
--outdir     Output directory (default: ./charts/ or CHART_OUTPUT_DIR env var)
--xlabel     X-axis label
--ylabel     Y-axis label
--width      Figure width in inches (default: 10)
--height     Figure height in inches (default: 6)
--colors     JSON array of colors (e.g., '["#FF6B6B", "#4ECDC4"]')
--style      Matplotlib style (default: seaborn-v0_8-whitegrid)
```

## Examples

**Bar chart:**
```bash
python3 .claude/skills/chart-generator/generate_chart.py \
  --type bar \
  --data '{"labels": ["Product A", "Product B", "Product C"], "values": [45000, 32000, 28000]}' \
  --title "Revenue by Product" \
  --ylabel "Revenue ($)" \
  --output "revenue_chart.png"
```

**Line chart with multiple series:**
```bash
python3 .claude/skills/chart-generator/generate_chart.py \
  --type line \
  --data '{"labels": ["Jan", "Feb", "Mar", "Apr"], "series": [{"name": "2024", "values": [100, 120, 110, 140]}, {"name": "2025", "values": [120, 150, 140, 180]}]}' \
  --title "Monthly Trend Comparison" \
  --xlabel "Month" \
  --ylabel "Sales" \
  --output "trend_comparison.png"
```

**Pie chart:**
```bash
python3 .claude/skills/chart-generator/generate_chart.py \
  --type pie \
  --data '{"labels": ["Desktop", "Mobile", "Tablet"], "values": [55, 35, 10]}' \
  --title "Traffic by Device" \
  --output "device_traffic.png"
```

**Scatter plot:**
```bash
python3 .claude/skills/chart-generator/generate_chart.py \
  --type scatter \
  --data '{"x": [1, 2, 3, 4, 5, 6], "y": [2.1, 3.9, 6.2, 7.8, 10.1, 12.0]}' \
  --title "Correlation Analysis" \
  --xlabel "Input" \
  --ylabel "Output" \
  --output "correlation.png"
```

## Output

Charts are saved to `./charts/` by default. Override with `--outdir <path>` or the `CHART_OUTPUT_DIR` environment variable. The directory is created automatically if it does not exist.

The script prints the absolute local file path of the generated chart on success (e.g., `/home/user/project/charts/my_chart.png`).
