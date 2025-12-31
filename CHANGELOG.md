# Changelog
All notable changes to PyVarChart will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
## [0.2.0] - 2024-12-29
### Added
- **Flexible Colormap System**: Support for ALL matplotlib colormaps
  - Users can now specify any colormap from `plt.cm` (e.g., 'viridis', 'plasma', 'Set1', 'tab20', etc.)
  - Intelligent handling of `_r` suffix for reversed colormaps
  - XOR logic: `_r` suffix and `int_reverse_color_scheme=1` work independently or together
  - Graceful fallback to 'tab10' if colormap not found
  - Custom 'Blue to Green to Red' gradient still supported as special case
- **Enhanced Color Control**: Better color reversal with XOR logic
  - `int_reverse_color_scheme=1` now works with ALL colormaps
  - Combining `_r` suffix + `int_reverse_color_scheme=1` cancels out (returns to original)
- **Continuous Scale for Legends**: Clean legend display for continuous numeric data
  - `int_continuous_scale=0`: Show all unique values (categorical mode)
  - `int_continuous_scale=1`: Auto-select 5-6 representative values using percentiles
  - Representative values include: min, 20th, 40th, 60th, 80th, 100th percentiles
  - Smooth color gradient interpolation across the full range
  - Auto-detection: Reverts to categorical if any string values detected
  - Works seamlessly with all colormaps
### Changed
- Color theme system redesigned for maximum flexibility
- Continuous scale uses percentile-based representative value selection
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
