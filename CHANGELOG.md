# Changelog
All notable changes to PyVarChart will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-04

### Added
- **First stable public release** - Production-ready with comprehensive features
- **Flexible Colormap System**: Support for ALL matplotlib colormaps (100+ options)
  - Users can now specify any colormap from `plt.cm` (e.g., 'viridis', 'plasma', 'Set1', 'tab20', etc.)
  - Intelligent handling of `_r` suffix for reversed colormaps
  - `int_reverse_color_scheme=1` works with ALL colormaps
  - Graceful fallback to 'blue_to_green_to_red' if colormap not found
  - Custom 'Blue to Green to Red' gradient with flexible naming (spaces/underscores)
  
- **Continuous Scale for Legends**: Clean legend display for continuous numeric data
  - `int_continuous_scale=0`: Show all unique values (categorical mode)
  - `int_continuous_scale=1`: Auto-select 5-6 representative values using percentiles
  - Representative values include: min, 20th, 40th, 60th, 80th, 100th percentiles
  - Smooth color gradient interpolation across the full range
  - Auto-detection: Reverts to categorical if any string values detected
  - Works seamlessly with all colormaps
  
- **Separated analyze() and plot() methods**: Better workflow and performance
  - `analyze()` processes data once
  - `plot()` can be called multiple times with different display parameters
  - Allows modification of visual parameters without re-processing data

### Fixed
- **Group means discontinuity bug**: Fixed horizontal lines spanning gaps in x-axis positions
  - Now correctly segments continuous position ranges
  - Draws separate lines for each continuous segment
- **Missing legend handling**: Fixed crash when `str_legend` is None
  - Properly initializes `use_continuous_scale=False` in no-legend case
- **Matplotlib deprecation warnings**: Updated to modern API
  - `plt.cm.get_cmap()` → `mpl.colormaps[]`
  
### Changed
- Color theme system redesigned for maximum flexibility
- Continuous scale uses percentile-based representative value selection
- Required parameters (`str_yaxis_var_name`, `lst_xaxis_var_names`) now have no defaults
  - Fail-fast with clear error messages at initialization
- Label rotation default changed from 'Vertical' to 'Horizontal' for better readability

## [0.1.0] - 2024-12-28

### Added
- Initial release of PyVarChart
- Hierarchical x-axis grouping with unlimited levels
- Statistical overlays (cell means, group means, grand mean, boxplots)
- Visual customization (color themes, marker themes, marker size control, point jittering)
- Layout control (custom label spacing, label rotation, font size, custom categorical ordering)
- Comprehensive input validation with helpful error messages
- Full type hints for better IDE support
- Detailed docstrings (Google style)

[Unreleased]: https://github.com/Guy-Steiff/pyvarchart/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Guy-Steiff/pyvarchart/releases/tag/v1.0.0
[0.1.0]: https://github.com/Guy-Steiff/pyvarchart/releases/tag/v0.1.0


