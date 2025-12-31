# PyVarChart Examples

This directory contains example scripts demonstrating PyVarChart usage.

## Examples

### Basic Example (`basic_example.py`)
Simple variability chart with minimal configuration.

**Output:** `basic_example.png`

### Advanced Example (`advanced_example.py`)
Chart with all features enabled (custom ordering, multiple statistical overlays, custom styling).

**Output:** `advanced_example.png`

### Colormap Showcase (`colormap_showcase.py`) - NEW in v0.2.0
Demonstrates the flexible colormap system with 10+ different matplotlib colormaps.

**Generates:** Multiple PNG files showing different colormaps

### Continuous Scale Demo (`continuous_scale_demo.py`) - NEW in v0.2.0
Shows how continuous scale feature creates cleaner legends for continuous numeric data.

**Generates:** Multiple PNG files comparing categorical vs continuous modes

## Running Examples

```bash
# Run all examples
python examples/basic_example.py
python examples/advanced_example.py
python examples/colormap_showcase.py
python examples/continuous_scale_demo.py

# Or from project root
python -m examples.basic_example
```

## Requirements

All examples use the non-interactive `Agg` backend to save directly to files. Make sure PyVarChart is installed:

```bash
pip install -e .
```

