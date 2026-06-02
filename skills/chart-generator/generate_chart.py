#!/usr/bin/env python3
"""
Chart Generator - Creates publication-quality charts using matplotlib.
Output directory: ./charts/ by default (configurable via --outdir or CHART_OUTPUT_DIR env var).
"""

import argparse
import json
import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for image generation

# Default output directory — can be overridden by --outdir or CHART_OUTPUT_DIR env var
_DEFAULT_OUTPUT_DIR = Path(os.environ.get("CHART_OUTPUT_DIR", "./charts"))

# Default colors palette
DEFAULT_COLORS = [
    '#4ECDC4', '#FF6B6B', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9'
]


def ensure_output_dir(output_dir: Path):
    """Ensure the output directory exists."""
    output_dir.mkdir(parents=True, exist_ok=True)


def parse_data(data_str: str) -> dict:
    """Parse JSON data string."""
    try:
        return json.loads(data_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON data: {e}", file=sys.stderr)
        sys.exit(1)


def parse_colors(colors_str: str) -> list:
    """Parse colors JSON array or return default."""
    if not colors_str:
        return DEFAULT_COLORS
    try:
        return json.loads(colors_str)
    except json.JSONDecodeError:
        return DEFAULT_COLORS


def setup_style(style: str):
    """Set matplotlib style."""
    try:
        plt.style.use(style)
    except OSError:
        # Fallback to default if style not found
        plt.style.use('seaborn-v0_8-whitegrid')


def create_bar_chart(data: dict, ax, colors: list, horizontal: bool = False):
    """Create a bar chart."""
    labels = data.get('labels', [])

    if 'series' in data:
        # Multi-series bar chart
        series_list = data['series']
        n_series = len(series_list)
        n_labels = len(labels)
        width = 0.8 / n_series

        for i, series in enumerate(series_list):
            positions = [x + i * width for x in range(n_labels)]
            values = series['values']
            color = colors[i % len(colors)]

            if horizontal:
                ax.barh(positions, values, height=width, label=series.get('name', f'Series {i+1}'), color=color)
            else:
                ax.bar(positions, values, width=width, label=series.get('name', f'Series {i+1}'), color=color)

        # Adjust tick positions
        tick_positions = [x + width * (n_series - 1) / 2 for x in range(n_labels)]
        if horizontal:
            ax.set_yticks(tick_positions)
            ax.set_yticklabels(labels)
        else:
            ax.set_xticks(tick_positions)
            ax.set_xticklabels(labels)
        ax.legend()
    else:
        # Single series bar chart
        values = data.get('values', [])
        color_list = [colors[i % len(colors)] for i in range(len(labels))]

        if horizontal:
            ax.barh(labels, values, color=color_list)
        else:
            ax.bar(labels, values, color=color_list)


def create_line_chart(data: dict, ax, colors: list):
    """Create a line chart."""
    labels = data.get('labels', [])

    if 'series' in data:
        # Multi-series line chart
        for i, series in enumerate(data['series']):
            values = series['values']
            color = colors[i % len(colors)]
            ax.plot(labels, values, marker='o', label=series.get('name', f'Series {i+1}'),
                   color=color, linewidth=2, markersize=6)
        ax.legend()
    else:
        # Single series line chart
        values = data.get('values', [])
        ax.plot(labels, values, marker='o', color=colors[0], linewidth=2, markersize=6)

    # Rotate labels if many points
    if len(labels) > 6:
        plt.xticks(rotation=45, ha='right')


def create_pie_chart(data: dict, ax, colors: list):
    """Create a pie chart."""
    labels = data.get('labels', [])
    values = data.get('values', [])
    color_list = [colors[i % len(colors)] for i in range(len(labels))]

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        colors=color_list,
        autopct='%1.1f%%',
        startangle=90,
        explode=[0.02] * len(values)
    )
    ax.axis('equal')

    # Style the percentage text
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')


def create_scatter_chart(data: dict, ax, colors: list):
    """Create a scatter chart."""
    if 'series' in data:
        # Multi-series scatter
        for i, series in enumerate(data['series']):
            x = series['x']
            y = series['y']
            color = colors[i % len(colors)]
            ax.scatter(x, y, label=series.get('name', f'Series {i+1}'),
                      color=color, s=60, alpha=0.7)
        ax.legend()
    else:
        # Single series scatter
        x = data.get('x', [])
        y = data.get('y', [])
        ax.scatter(x, y, color=colors[0], s=60, alpha=0.7)


def create_area_chart(data: dict, ax, colors: list):
    """Create an area chart."""
    labels = data.get('labels', [])

    if 'series' in data:
        # Multi-series area chart (stacked)
        cumulative = [0] * len(labels)
        for i, series in enumerate(data['series']):
            values = series['values']
            color = colors[i % len(colors)]
            ax.fill_between(range(len(labels)), cumulative,
                           [c + v for c, v in zip(cumulative, values)],
                           label=series.get('name', f'Series {i+1}'),
                           color=color, alpha=0.7)
            cumulative = [c + v for c, v in zip(cumulative, values)]
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)
        ax.legend()
    else:
        # Single series area chart
        values = data.get('values', [])
        ax.fill_between(range(len(labels)), values, color=colors[0], alpha=0.7)
        ax.plot(range(len(labels)), values, color=colors[0], linewidth=2)
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels)

    if len(labels) > 6:
        plt.xticks(rotation=45, ha='right')


def generate_chart(args):
    """Generate the chart based on arguments."""
    output_dir = Path(args.outdir) if args.outdir else _DEFAULT_OUTPUT_DIR
    ensure_output_dir(output_dir)

    # Parse inputs
    data = parse_data(args.data)
    colors = parse_colors(args.colors)

    # Setup style
    setup_style(args.style)

    # Create figure
    fig, ax = plt.subplots(figsize=(args.width, args.height))

    # Generate chart based on type
    chart_type = args.type.lower()

    if chart_type == 'bar':
        create_bar_chart(data, ax, colors)
    elif chart_type == 'hbar':
        create_bar_chart(data, ax, colors, horizontal=True)
    elif chart_type == 'line':
        create_line_chart(data, ax, colors)
    elif chart_type == 'pie':
        create_pie_chart(data, ax, colors)
    elif chart_type == 'scatter':
        create_scatter_chart(data, ax, colors)
    elif chart_type == 'area':
        create_area_chart(data, ax, colors)
    else:
        print(f"Unknown chart type: {chart_type}", file=sys.stderr)
        print("Supported types: bar, hbar, line, pie, scatter, area", file=sys.stderr)
        sys.exit(1)

    # Set labels and title
    if args.title:
        ax.set_title(args.title, fontsize=14, fontweight='bold', pad=15)

    if args.xlabel and chart_type != 'pie':
        ax.set_xlabel(args.xlabel, fontsize=11)

    if args.ylabel and chart_type != 'pie':
        ax.set_ylabel(args.ylabel, fontsize=11)

    # Add grid for non-pie charts
    if chart_type != 'pie':
        ax.grid(True, alpha=0.3)

    # Tight layout
    plt.tight_layout()

    # Save chart
    output_path = output_dir / args.output
    fig.savefig(output_path, dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)

    # Print the local file path
    print(str(output_path.resolve()))
    return str(output_path.resolve())


def main():
    parser = argparse.ArgumentParser(
        description='Generate publication-quality charts',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--type', '-t', required=True,
                       choices=['bar', 'hbar', 'line', 'pie', 'scatter', 'area'],
                       help='Chart type')
    parser.add_argument('--data', '-d', required=True,
                       help='JSON data string')
    parser.add_argument('--title', default='',
                       help='Chart title')
    parser.add_argument('--output', '-o', required=True,
                       help='Output filename (e.g. my_chart.png)')
    parser.add_argument('--outdir', default='',
                       help='Output directory (default: ./charts/ or CHART_OUTPUT_DIR env var)')
    parser.add_argument('--xlabel', default='',
                       help='X-axis label')
    parser.add_argument('--ylabel', default='',
                       help='Y-axis label')
    parser.add_argument('--width', type=float, default=10,
                       help='Figure width in inches (default: 10)')
    parser.add_argument('--height', type=float, default=6,
                       help='Figure height in inches (default: 6)')
    parser.add_argument('--colors', default='',
                       help='JSON array of colors')
    parser.add_argument('--style', default='seaborn-v0_8-whitegrid',
                       help='Matplotlib style')

    args = parser.parse_args()
    generate_chart(args)


if __name__ == '__main__':
    main()
