# PyVarChart Examples

This directory contains example scripts demonstrating PyVarChart features and capabilities.

## Quick Start Examples

### Quick Start (`readme_quick_start.py`)
Minimal example showing basic chart creation with 3-level grouping.

**Features:** Basic hierarchical grouping, legend, cell means  
**Output:** `readme_quick_start.png`

### Basic Example (`basic_example.py`)
Simple distribution chart with 5-level hierarchical grouping and minimal configuration.

**Features:** 5-level grouping, lane-based coloring, blue→green→red gradient  
**Output:** `basic_example.png`

### Advanced Example (`advanced_example.py`)
Chart with all features enabled including custom ordering, jittering, and custom styling.

**Features:** Custom label spacing, point jittering, reversed cmp ordering, varied rotations, font sizes  
**Output:** `advanced_example.png`

### Complex Example (`complex_example.py`)
Full-featured RF testing analysis with 6 levels of hierarchical grouping.

**Features:** RF test data, 6-level grouping, boxplots, statistical overlays (cell/group/grand means), vertical labels  
**Output:** `complex_example.png`

## README Examples

The following examples generate figures used in the main README.md:

### RF Testing Example (`readme_example_1_rf_testing.py`)
Demonstrates RF noise figure analysis across multiple test parameters.

**Output:** `readme_example_1_rf_testing.png`

### Continuous Scale Example (`readme_example_2_continuous_scale.py`)
Shows continuous scale legend feature for cleaner visualization of continuous data.

**Output:** `readme_example_2_continuous_scale.png`

### Custom Ordering Example (`readme_example_3_custom_ordering.py`)
Demonstrates custom categorical ordering (prioritizing problem areas first).

**Output:** `readme_example_3_custom_ordering.png`

## Feature Showcases (v0.2.0)

### Colormap Showcase (`colormap_showcase.py`)
Demonstrates the flexible colormap system with 12 different matplotlib colormaps.

**Features:**
- Custom gradient (blue_to_green_to_red)
- Qualitative maps (tab10, Set1, Dark2, Pastel1)
- Sequential maps (viridis, plasma)
- Diverging maps (RdYlBu, coolwarm)
- Reversed colormaps (tab10_r, viridis_r)

**Generates:** 12 PNG files showing different colormaps

### Continuous Scale Demo (`continuous_scale_demo.py`)
Shows how continuous scale feature creates cleaner legends for continuous numeric data.

**Features:**
- Comparison: categorical vs continuous mode
- Multiple colormaps (viridis, plasma, coolwarm)
- Auto-revert behavior (strings detected)

**Generates:** 5 PNG files comparing modes

## Running Examples

### Run individual examples:
```bash
# From project root
python examples/basic_example.py
python examples/advanced_example.py
python examples/complex_example.py
python examples/colormap_showcase.py
python examples/continuous_scale_demo.py

# Or using module syntax
python -m examples.basic_example
```

### Run all examples:
```bash
# Unix/Linux/Mac
for f in examples/*.py; do python "$f"; done

# Windows PowerShell
Get-ChildItem examples\*.py | ForEach-Object { python $_.FullName }
```

### Generate all README figures:
```bash
python examples/readme_quick_start.py
python examples/readme_example_1_rf_testing.py
python examples/readme_example_2_continuous_scale.py
python examples/readme_example_3_custom_ordering.py
```

## Requirements

All examples use the non-interactive `Agg` backend to save directly to files. 

### Install PyVarChart:
```bash
# From PyPI (once published)
pip install pyvarchart

# Or from source (development)
pip install -e .
```

### Dependencies:
- pandas >= 1.3.0
- numpy >= 1.20.0
- matplotlib >= 3.3.0

All dependencies are installed automatically with PyVarChart.

## Output Files

All examples generate PNG files in the `examples/` directory:
- Resolution: 100 DPI
- Format: PNG with `bbox_inches='tight'`
- No interactive display (uses Agg backend)

## Notes

- Examples are read-only and serve as reference implementations
- All examples include embedded test data (no external files required)
- Complex example demonstrates real-world RF testing scenario
- Colormap showcase generates the most files (12 colormaps × 1 figure each)


