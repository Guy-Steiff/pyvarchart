# PyVarChart

A Python library for creating sophisticated variability charts with hierarchical grouping.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

PyVarChart creates professional variability charts that visualize data distribution across multiple categorical factors. It's perfect for:

- **Quality Control**: Analyzing manufacturing variation across multiple factors
- **A/B Testing**: Comparing performance across different configurations
- **Scientific Research**: Visualizing experimental results with hierarchical grouping
- **Data Exploration**: Understanding patterns in multi-dimensional categorical data

## Features

✨ **Hierarchical X-Axis Grouping** - Display data across multiple categorical levels  
📊 **Statistical Overlays** - Cell means, group means, grand mean, boxplots  
🎨 **Flexible Colormaps** - Support for 100+ matplotlib colormaps (viridis, plasma, tab10, etc.)  
🌈 **Continuous Scale** - Auto-select representative values for cleaner legends  
🎨 **Customizable Styling** - Color themes, marker styles, jittering  
📐 **Flexible Layout** - Custom spacing, rotation, and font sizes per level  
🔧 **Custom Ordering** - Control sort order of categorical variables  
⚡ **Type-Safe** - Full type hints for better IDE support  
✅ **Validated** - Comprehensive input validation with helpful error messages

## Installation

```bash
# From source
git clone https://github.com/Guy-Steiff/pyvarchart.git
cd pyvarchart
pip install -e .
```

## Quick Start

```python
from pyvarchart import PyVarChart
import pandas as pd

# Your data
data = pd.DataFrame({
    'chip': [0, 0, 0, 0],
    'channel': [2, 2, 2, 2],
    'lane': ['I', 'I', 'Q', 'Q'],
    'measurement': [159, 136, 142, 122]
})

# Create chart
pvc = PyVarChart(
    str_yaxis_var_name='measurement',
    lst_xaxis_var_names=['chip', 'channel', 'lane'],
    str_legend='lane',
    int_show_cell_means=1
)

fig, ax = pvc.analyze(1, data)
fig.savefig('variability_chart.png')
```

## Examples

### Basic Variability Chart

```python
from pyvarchart import PyVarChart
import pandas as pd

# Sample data
data = pd.DataFrame({
    'part': ['A', 'A', 'B', 'B'] * 3,
    'operator': [1, 2, 1, 2] * 3,
    'measurement': [10.2, 10.5, 9.8, 10.1, 10.3, 10.4, 9.9, 10.2, 10.1, 10.6, 9.7, 10.0]
})

pvc = PyVarChart(
    str_yaxis_var_name='measurement',
    lst_xaxis_var_names=['part', 'operator'],
    int_show_cell_means=1,
    int_show_grand_mean=1
)

fig, ax = pvc.analyze(1, data)
```

### Advanced: Custom Styling with NEW v0.2.0 Features

```python
pvc = PyVarChart(
    # Data configuration
    str_yaxis_var_name='temperature',
    lst_xaxis_var_names=['site', 'operator', 'batch', 'replicate'],
    str_legend='temperature',  # Continuous numeric values
    
    # NEW v0.2.0: Flexible colormaps (100+ options!)
    str_color_theme='viridis',           # Use any matplotlib colormap
    int_reverse_color_scheme=0,          # Set to 1 to reverse colors
    int_continuous_scale=1,              # Auto-select 5-6 representative values
    
    # Visual styling
    str_marker_theme='Solid',
    int_marker_size=10,
    b_jitter_points=True,
    
    # Statistical overlays
    int_boxplots=1,
    int_show_cell_means=1,
    lst_show_group_means=['site', 'operator'],
    int_show_grand_mean=1,
    
    # Layout customization
    label_spacing=[0.10, 0.08, 0.06, 0.05],  # Custom spacing per level
    lst_rotation=['Horizontal', 'Horizontal', 'Vertical', 'Horizontal'],
    lst_xaxis_font_size=[12, 11, 10, 9],
    
    # Custom ordering
    dict_xaxis_orderings={'site': ['North', 'South', 'East', 'West']},
    
    # Figure size
    int_frame_size_x=14,
    int_frame_size_y=8,
    str_title='Temperature Analysis with Viridis Colormap'
)

fig, ax = pvc.analyze(1, data)
```

### Example Outputs

**Basic Variability Chart:**

![Basic Example](examples/basic_example.png)

**Advanced Chart with Custom Styling:**

![Advanced Example](examples/advanced_example.png)

*See the `examples/` folder for more demonstrations including colormap showcase and continuous scale examples.*

## API Reference

### PyVarChart

```python
PyVarChart(
    # Core parameters
    str_yaxis_var_name='y_variable',
    lst_xaxis_var_names=None,
    str_legend=None,
    
    # Display options
    int_boxplots=1,              # 0: points only, 1: points+boxes, 2: boxes only
    int_show_points=1,
    int_show_cell_means=0,
    int_show_grand_mean=0,
    lst_show_group_means=None,
    
    # Styling
    str_color_theme='tab10',     # Any matplotlib colormap (see below)
    int_reverse_color_scheme=0,  # 1 to reverse colors, 0 for normal
    int_continuous_scale=0,      # 1: auto-select 5-6 values for cleaner legends
    str_marker_theme='Default',  # or 'Solid'
    int_marker_size=8,
    b_jitter_points=False,
    
    # Layout
    label_spacing=0.15,          # float or list of floats
    lst_rotation=None,
    lst_xaxis_font_size=None,
    dict_xaxis_orderings=None,
    int_frame_size_x=20,
    int_frame_size_y=6,
    str_title=None
)
```

### Methods

#### `analyze(int_fig_num, pd_data)`

Generate the variability chart.

**Parameters:**
- `int_fig_num` (int): Matplotlib figure number
- `pd_data` (pd.DataFrame): Data to visualize

**Returns:**
- `Tuple[plt.Figure, plt.Axes]`: Matplotlib figure and axes objects

**Example:**
```python
fig, ax = pvc.analyze(1, dataframe)
ax.set_ylim(0, 100)  # Customize further
fig.savefig('output.png', dpi=300)
```

## Parameter Guide

### Layout Customization

#### `label_spacing`
Control vertical spacing between x-axis label levels.

```python
# Uniform spacing
label_spacing=0.15

# Custom spacing per level (bottom to top)
label_spacing=[0.10, 0.08, 0.06, 0.05]
```

#### `lst_rotation`
Control label orientation per level.

```python
lst_rotation=['Horizontal', 'Horizontal', 'Vertical', 'Vertical']
```

#### `dict_xaxis_orderings`
Specify custom sort order for categorical variables.

```python
dict_xaxis_orderings={
    'priority': ['High', 'Medium', 'Low'],
    'status': ['Complete', 'In Progress', 'Pending']
}
```

### Statistical Overlays

```python
int_show_cell_means=1          # Horizontal line at each cell's mean
int_show_grand_mean=1          # Overall dataset mean (dotted line)
lst_show_group_means=['part']  # Group means across (a) specific parameter(s)
int_boxplots=1                 # 0: off, 1: with points, 2: only boxes
```

### Color Themes

PyVarChart supports **any matplotlib colormap**! You can use:

#### Custom Gradient
- `'Blue to Green to Red'` - Custom three-color gradient (special case)

#### Qualitative (Best for Categorical Data)
Perfect for legend-based differentiation:
- `'tab10'`, `'tab20'`, `'tab20b'`, `'tab20c'` - Tableau palettes
- `'Set1'`, `'Set2'`, `'Set3'` - ColorBrewer sets
- `'Paired'`, `'Accent'` - ColorBrewer paired colors
- `'Pastel1'`, `'Pastel2'` - Soft pastel colors
- `'Dark2'` - Darker, high-contrast colors

#### Sequential (Single Hue)
Good for ordered categories:
- `'Blues'`, `'Greens'`, `'Reds'`, `'Oranges'`, `'Purples'`, `'Greys'`
- `'viridis'`, `'plasma'`, `'inferno'`, `'magma'`, `'cividis'` - Perceptually uniform

#### Diverging (Two Hues)
For data with a meaningful midpoint:
- `'RdBu'`, `'RdYlGn'`, `'RdYlBu'`, `'BrBG'`, `'PuOr'`
- `'coolwarm'`, `'seismic'`, `'bwr'`

#### Reversing Colors
You can reverse any colormap in two ways:
1. **Add `_r` suffix**: `'viridis_r'`, `'tab10_r'`, etc.
2. **Use parameter**: Set `int_reverse_color_scheme=1`

```python
# These are equivalent:
pvc = PyVarChart(str_color_theme='viridis_r', ...)
pvc = PyVarChart(str_color_theme='viridis', int_reverse_color_scheme=1, ...)

# Also works with custom gradient:
pvc = PyVarChart(str_color_theme='Blue to Green to Red', int_reverse_color_scheme=1, ...)
# This gives you 'Red to Green to Blue'
```

**Note**: If colormap name is not found, falls back to `'tab10'` with a warning.

### Continuous Scale

For cleaner legends when dealing with many continuous numeric values:

```python
int_continuous_scale=0  # Default: Show all unique values (categorical)
int_continuous_scale=1  # Auto-select 5-6 representative values (continuous)
```

**When to use continuous scale:**
- Legend has many unique numeric values (>10)
- Values are continuous (temperature, pressure, time, etc.)
- You want a cleaner, more professional legend

**How it works:**
- Automatically selects 5-6 values using percentiles (0%, 20%, 40%, 60%, 80%, 100%)
- Includes endpoints (min/max) and evenly distributed intermediate values
- Smooth color gradient interpolation across the full range
- Auto-detects strings and reverts to categorical mode

**Example:**
```python
# Instead of showing all 90 unique temperatures in legend,
# show 6 representative values: 15.2, 21.1, 27.0, 32.9, 38.8, 44.8
pvc = PyVarChart(
    str_legend='temperature',
    str_color_theme='coolwarm',    # Blue=cold, Red=hot
    int_continuous_scale=1,
)
```

### Marker Themes

- `'Default'` - All circles
- `'Solid'` - Varied shapes (squares, triangles, diamonds, etc.)

## Requirements

```
python>=3.8
pandas>=1.3.0
numpy>=1.20.0
matplotlib>=3.3.0
```

## Use Cases

### Manufacturing Quality Control

```python
# Analyze part variation across multiple factors
pvc = PyVarChart(
    str_yaxis_var_name='dimension',
    lst_xaxis_var_names=['machine', 'shift', 'operator', 'lot'],
    int_show_cell_means=1,
    lst_show_group_means=['machine', 'shift']
)
```

### A/B Testing

```python
# Compare test variants across segments
pvc = PyVarChart(
    str_yaxis_var_name='conversion_rate',
    lst_xaxis_var_names=['variant', 'segment', 'platform'],
    str_legend='variant',
    str_color_theme='Blue to Green to Red'
)
```

### Scientific Experiments

```python
# Visualize experimental results with replicates
pvc = PyVarChart(
    str_yaxis_var_name='response',
    lst_xaxis_var_names=['treatment', 'replicate', 'timepoint'],
    int_boxplots=1,
    int_show_grand_mean=1
)
```

## Tips & Best Practices

1. **Start Simple**: Begin with 2-3 grouping variables before adding more
2. **Use Jittering**: Enable `b_jitter_points=True` when points overlap
3. **Custom Spacing**: Adjust `label_spacing` for cleaner layouts with many levels
4. **Rotation**: Use vertical rotation for long label names
5. **Validation**: PyVarChart will warn about missing values in custom orderings

## Troubleshooting

### "Missing required columns in DataFrame"
Ensure all column names in `lst_xaxis_var_names` and `str_yaxis_var_name` exist in your data.

### "Custom ordering missing values"
Your `dict_xaxis_orderings` doesn't include all values present in the data. PyVarChart will auto-append missing values.

### Overlapping labels
Increase `label_spacing` or use a list with larger values for crowded levels.

### Plot too small/large
Adjust `int_frame_size_x` and `int_frame_size_y` parameters.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Changelog

## Changelog

### v0.2.0 (2024-12-29)
- **Flexible Colormap System**: Support for ALL matplotlib colormaps (100+ options)
- **Continuous Scale**: Auto-select 5-6 representative values for cleaner legends
- **Enhanced Color Reversal**: XOR logic for `_r` suffix and `int_reverse_color_scheme`
- Smooth color gradient interpolation for continuous data
- Auto-detection and fallback for string/categorical data
- Comprehensive colormap documentation and examples

### v0.1.0 (2024-12-28)
- Initial release
- Hierarchical x-axis grouping
- Statistical overlays (means, boxplots)
- Custom ordering and styling
- Comprehensive validation
- Full type hints
- List-based label spacing

## Acknowledgments

Inspired by variability chart functionality in statistical analysis software.

## Contact

For questions, issues, or suggestions, please [open an issue on GitHub](https://github.com/Guy-Steiff/pyvarchart/issues).

