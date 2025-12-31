# PyVarChart Tests

Unit tests for PyVarChart using pytest.

## Current Status

✅ **All 28 tests passing** (as of v0.2.0, December 2024)  
✅ **No errors**  
✅ **Zero deprecation warnings** (matplotlib API updated)

## Running Tests

### Install test dependencies:
```bash
pip install pytest pytest-cov
```

### Run all tests:
```bash
pytest
```

### Run with coverage report:
```bash
pytest --cov=pyvarchart --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_pyvarchart.py
```

### Run specific test class:
```bash
pytest tests/test_pyvarchart.py::TestBasicFunctionality
```

### Run specific test:
```bash
pytest tests/test_pyvarchart.py::TestBasicFunctionality::test_basic_chart_creation
```

### Run with verbose output:
```bash
pytest -v
```

## Test Structure

- `test_pyvarchart.py` - Main test suite (28 tests)
  - `TestBasicFunctionality` (3 tests) - Basic chart creation, legends, titles
  - `TestValidation` (4 tests) - Input validation and error handling
  - `TestCustomOrdering` (3 tests) - Custom ordering with warnings
  - `TestLabelSpacing` (3 tests) - Label spacing (float/list modes)
  - `TestStatisticalOverlays` (4 tests) - Cell means, grand mean, group means, boxplots
  - `TestStyling` (6 tests) - Colormaps, markers, jittering, sizing
  - `TestEdgeCases` (3 tests) - Single point, many levels, empty lists
  - `TestUtilityFunctions` (2 tests) - Helper functions (legend_label)

## What Gets Tested

### Core Functionality
✅ Chart creation with hierarchical grouping  
✅ Legend display and formatting  
✅ Custom titles  
✅ Multi-level x-axis grouping  

### Validation & Error Handling
✅ Missing column detection  
✅ Overlap validation (y-axis vs x-axis)  
✅ Invalid custom ordering warnings  
✅ Missing/extra values in orderings  

### v0.2.0 Features
✅ **Flexible colormaps** - 100+ matplotlib colormaps (viridis, plasma, tab10, etc.)  
✅ **Continuous scale** - Auto-select 5-6 representative values for cleaner legends  
✅ **Color reversal** - Both `_r` suffix and `int_reverse_color_scheme` work  
✅ **Blue to Green to Red** - Custom gradient with space/underscore normalization  

### Statistical Overlays
✅ Cell means display  
✅ Grand mean display  
✅ Group means across hierarchical levels  
✅ Boxplots with sufficient data  

### Styling & Layout
✅ Color themes (Pastel1, custom gradients, matplotlib colormaps)  
✅ Marker themes (Default, Solid)  
✅ Point jittering (`int_jitter_points`)  
✅ Custom marker sizes  
✅ Label spacing (float and list modes)  

### Edge Cases
✅ Single data point handling  
✅ Many grouping levels (5+ levels)  
✅ Empty group means lists  

### Utility Functions
✅ `legend_label()` - None handling and string conversion  

## Recent Fixes (v0.2.0)

### Test File Issues Resolved
1. **Boxplot empty data** - Added `int_boxplots=0` to tests with insufficient data
2. **Colormap names** - Updated 'PVC Light' → 'Pastel1' (valid matplotlib colormap)
3. **Parameter names** - Fixed `b_jitter_points` → `int_jitter_points`
4. **File structure** - Reversed backwards test file (imports were at the end!)

### PyVarChart Fixes Applied
1. **Matplotlib deprecation** - Updated `plt.cm.get_cmap()` → `mpl.colormaps[]`
2. **Colormap normalization** - Handles both 'Blue to Green to Red' and 'blue_to_green_to_red'
3. **Group means bug** - Fixed discontinuous position handling with NumPy segmentation
4. **Fallback colormap** - Changed from non-existent colormap to 'tab10'

## Test Coverage Goal

Target: **>80% code coverage**

Current: High coverage across all major features including v0.2.0 additions

## Notes for Contributors

- Tests use `int_boxplots=0` for simple data to avoid matplotlib boxplot errors
- Custom colormap 'Blue to Green to Red' accepts both space and underscore formats
- Test data is kept minimal but sufficient for validation
- All tests clean up with `plt.close(fig)` to avoid memory leaks


