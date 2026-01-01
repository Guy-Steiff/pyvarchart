"""
PyVarChart - A Python library for creating variability charts with hierarchical grouping.

This module provides tools for visualizing data variability across multiple categorical
factors with support for custom ordering, color themes, marker styles, and statistical overlays.
"""

from typing import Optional, List, Dict, Tuple, Any, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby, cycle
import matplotlib.colors as mcolors
import matplotlib as mpl
from io import StringIO


# Public API
__all__ = ['PyVarChart']
__version__ = '0.2.0'


# ============================================================================
# Utility Functions - Formatting & Display
# ============================================================================

def legend_label(val: Any) -> str:
    """Convert legend value to display string, handling None values.

    Args:
        val: The value to convert to a label string.

    Returns:
        String representation of the value, or "Unlabeled" if None.
    """
    return "Unlabeled" if val is None else str(val)


# ============================================================================
# Utility Functions - Layout & Spacing
# ============================================================================

def estimate_bottom_margin(num_levels: int,
                          lst_rotations: List[str],
                          lst_spacing: Optional[Union[float, List[float]]] = None,
                          vertical_base: float = 0.12,
                          horizontal_base: float = 0.05,
                          base_margin: float = 0.13,
                          max_margin: float = 0.35) -> float:
    """Estimate the bottom margin needed for multi-level x-axis labels.

    Args:
        num_levels: Number of hierarchical levels in the x-axis.
        lst_rotations: List of rotation specifications ('Vertical' or 'Horizontal').
        lst_spacing: Optional spacing values. If provided as a list, uses actual spacings.
                    If float or None, estimates based on rotation. Default: None
        vertical_base: Margin increment for vertical labels (if lst_spacing not provided). Default: 0.12
        horizontal_base: Margin increment for horizontal labels (if lst_spacing not provided). Default: 0.05
        base_margin: Base margin to start from. Default: 0.13
        max_margin: Maximum allowed margin. Default: 0.35

    Returns:
        Calculated bottom margin value, capped at max_margin.
    """
    # If spacing list is provided, use actual spacings
    if isinstance(lst_spacing, list):
        margin = base_margin + sum(lst_spacing[:num_levels])
        return min(margin, max_margin)

    # Otherwise, estimate based on rotation
    margin = base_margin
    for i in range(num_levels):
        if i < len(lst_rotations):
            if lst_rotations[i].lower() == 'vertical':
                margin += vertical_base
            else:
                margin += horizontal_base
        else:
            margin += horizontal_base
    return min(margin, max_margin)

def add_line(ax, xpos, ypos, spacing):
    line = plt.Line2D(
        [xpos, xpos],
        [ypos + spacing, ypos],
        transform=ax.transAxes,
        color='gray'
    )
    line.set_clip_on(False)
    ax.add_line(line)


def label_len(my_index, level):
    labels = my_index.get_level_values(level)
    return [(k, sum(1 for i in g)) for k, g in groupby(labels)]

def label_group_bar_table(ax: plt.Axes,
                         df: pd.Series,
                         lst_rotation_labels: List[str],
                         spacing: Union[float, List[float]] = 0.15,
                         lst_fontsize: Optional[List[int]] = None) -> None:
    """Create hierarchical grouped labels below the x-axis.

    Args:
        ax: Matplotlib axes object to add labels to.
        df: Series with MultiIndex containing the grouping structure.
        lst_rotation_labels: List of 'Horizontal' or 'Vertical' for each level.
        spacing: Vertical spacing between label levels. Can be a single float for uniform
                spacing, or a list of floats (one per level) for custom spacing. Default: 0.15
        lst_fontsize: Optional list of font sizes for each level.
    """
    # Convert spacing to list if it's a single value
    if isinstance(spacing, (int, float)):
        lst_spacing = [spacing] * df.index.nlevels
    else:
        lst_spacing = spacing

    ypos = 0
    scale = 1. / df.index.size
    num_levels = df.index.nlevels
    index_level_names = df.index.names

    for level in range(num_levels)[::-1]:
        # Get spacing for this level
        current_spacing = lst_spacing[level] if level < len(lst_spacing) else 0.15
        ypos -= current_spacing

        pos = 0
        rotate = lst_rotation_labels[level].lower() == 'vertical' if level < len(lst_rotation_labels) else False

        if index_level_names and level < len(index_level_names):
            ax.text(-0.01, ypos, index_level_names[level],
                    ha='right', va='center',
                    transform=ax.transAxes,
                    fontsize='small', fontweight='bold')

        for label, rpos in label_len(df.index, level):
            lxpos = (pos + .5 * rpos) * scale
            fontsize = lst_fontsize[level] if lst_fontsize and level < len(lst_fontsize) else mpl.rcParams.get(
                "font.size", 10)
            ax.text(
                lxpos, ypos, label,
                ha='center',
                va='top' if rotate else 'center',
                rotation=90 if rotate else 0,
                transform=ax.transAxes,
                fontsize=fontsize
            )
            add_line(ax, pos * scale, ypos, current_spacing)
            pos += rpos

        add_line(ax, pos * scale, ypos, current_spacing)


def normalize_grouping_value(val: Any) -> Any:
    """Normalize float grouping variables to int if they represent whole numbers.

    Args:
        val: Value to normalize.

    Returns:
        Integer if val is a whole number float, otherwise unchanged value.
    """
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val

class ColorMapFactory:
    """Factory class providing various colormap names for matplotlib."""
    def __init__(self):
        self.blue_to_green_to_red = 'blue_to_green_to_red'
        self.Accent = 'Accent'
        self.Accent_r = 'Accent_r'
        self.Blues = 'Blues'
        self.Blues_r = 'Blues_r'
        self.BrBG = 'BrBG'
        self.BrBG_r = 'BrBG_r'
        self.BuGn = 'BuGn'
        self.BuGn_r = 'BuGn_r'
        self.BuPu = 'BuPu'
        self.BuPu_r = 'BuPu_r'
        self.CMRmap = 'CMRmap'
        self.CMRmap_r = 'CMRmap_r'
        self.Dark2 = 'Dark2'
        self.Dark2_r = 'Dark2_r'
        self.GnBu = 'GnBu'
        self.GnBu_r = 'GnBu_r'
        self.Grays = 'Grays'
        self.Grays_r = 'Grays_r'
        self.Greens = 'Greens'
        self.Greens_r = 'Greens_r'
        self.Greys = 'Greys'
        self.Greys_r = 'Greys_r'
        self.OrRd = 'OrRd'
        self.OrRd_r = 'OrRd_r'
        self.Oranges = 'Oranges'
        self.Oranges_r = 'Oranges_r'
        self.PRGn = 'PRGn'
        self.PRGn_r = 'PRGn_r'
        self.Paired = 'Paired'
        self.Paired_r = 'Paired_r'
        self.Pastel1 = 'Pastel1'
        self.Pastel1_r = 'Pastel1_r'
        self.Pastel2 = 'Pastel2'
        self.Pastel2_r = 'Pastel2_r'
        self.PiYG = 'PiYG'
        self.PiYG_r = 'PiYG_r'
        self.PuBu = 'PuBu'
        self.PuBuGn = 'PuBuGn'
        self.PuBuGn_r = 'PuBuGn_r'
        self.PuBu_r = 'PuBu_r'
        self.PuOr = 'PuOr'
        self.PuOr_r = 'PuOr_r'
        self.PuRd = 'PuRd'
        self.PuRd_r = 'PuRd_r'
        self.Purples = 'Purples'
        self.Purples_r = 'Purples_r'
        self.RdBu = 'RdBu'
        self.RdBu_r = 'RdBu_r'
        self.RdGy = 'RdGy'
        self.RdGy_r = 'RdGy_r'
        self.RdPu = 'RdPu'
        self.RdPu_r = 'RdPu_r'
        self.RdYlBu = 'RdYlBu'
        self.RdYlBu_r = 'RdYlBu_r'
        self.RdYlGn = 'RdYlGn'
        self.RdYlGn_r = 'RdYlGn_r'
        self.Reds = 'Reds'
        self.Reds_r = 'Reds_r'
        self.Set1 = 'Set1'
        self.Set1_r = 'Set1_r'
        self.Set2 = 'Set2'
        self.Set2_r = 'Set2_r'
        self.Set3 = 'Set3'
        self.Set3_r = 'Set3_r'
        self.Spectral = 'Spectral'
        self.Spectral_r = 'Spectral_r'
        self.Wistia = 'Wistia'
        self.Wistia_r = 'Wistia_r'
        self.YlGn = 'YlGn'
        self.YlGnBu = 'YlGnBu'
        self.YlGnBu_r = 'YlGnBu_r'
        self.YlGn_r = 'YlGn_r'
        self.YlOrBr = 'YlOrBr'
        self.YlOrBr_r = 'YlOrBr_r'
        self.YlOrRd = 'YlOrRd'
        self.YlOrRd_r = 'YlOrRd_r'
        self.afmhot = 'afmhot'
        self.afmhot_r = 'afmhot_r'
        self.autumn = 'autumn'
        self.autumn_r = 'autumn_r'
        self.berlin = 'berlin'
        self.berlin_r = 'berlin_r'
        self.binary = 'binary'
        self.binary_r = 'binary_r'
        self.bone = 'bone'
        self.bone_r = 'bone_r'
        self.brg = 'brg'
        self.brg_r = 'brg_r'
        self.bwr = 'bwr'
        self.bwr_r = 'bwr_r'
        self.cividis = 'cividis'
        self.cividis_r = 'cividis_r'
        self.cool = 'cool'
        self.cool_r = 'cool_r'
        self.coolwarm = 'coolwarm'
        self.coolwarm_r = 'coolwarm_r'
        self.copper = 'copper'
        self.copper_r = 'copper_r'
        self.cubehelix = 'cubehelix'
        self.cubehelix_r = 'cubehelix_r'
        self.flag = 'flag'
        self.flag_r = 'flag_r'
        self.gist_earth = 'gist_earth'
        self.gist_earth_r = 'gist_earth_r'
        self.gist_gray = 'gist_gray'
        self.gist_gray_r = 'gist_gray_r'
        self.gist_grey = 'gist_grey'
        self.gist_grey_r = 'gist_grey_r'
        self.gist_heat = 'gist_heat'
        self.gist_heat_r = 'gist_heat_r'
        self.gist_ncar = 'gist_ncar'
        self.gist_ncar_r = 'gist_ncar_r'
        self.gist_rainbow = 'gist_rainbow'
        self.gist_rainbow_r = 'gist_rainbow_r'
        self.gist_stern = 'gist_stern'
        self.gist_stern_r = 'gist_stern_r'
        self.gist_yarg = 'gist_yarg'
        self.gist_yarg_r = 'gist_yarg_r'
        self.gist_yerg = 'gist_yerg'
        self.gist_yerg_r = 'gist_yerg_r'
        self.gnuplot = 'gnuplot'
        self.gnuplot2 = 'gnuplot2'
        self.gnuplot2_r = 'gnuplot2_r'
        self.gnuplot_r = 'gnuplot_r'
        self.gray = 'gray'
        self.gray_r = 'gray_r'
        self.grey = 'grey'
        self.grey_r = 'grey_r'
        self.hot = 'hot'
        self.hot_r = 'hot_r'
        self.hsv = 'hsv'
        self.hsv_r = 'hsv_r'
        self.inferno = 'inferno'
        self.inferno_r = 'inferno_r'
        self.jet = 'jet'
        self.jet_r = 'jet_r'
        self.magma = 'magma'
        self.magma_r = 'magma_r'
        self.managua = 'managua'
        self.managua_r = 'managua_r'
        self.nipy_spectral = 'nipy_spectral'
        self.nipy_spectral_r = 'nipy_spectral_r'
        self.ocean = 'ocean'
        self.ocean_r = 'ocean_r'
        self.pink = 'pink'
        self.pink_r = 'pink_r'
        self.plasma = 'plasma'
        self.plasma_r = 'plasma_r'
        self.prism = 'prism'
        self.prism_r = 'prism_r'
        self.rainbow = 'rainbow'
        self.rainbow_r = 'rainbow_r'
        self.seismic = 'seismic'
        self.seismic_r = 'seismic_r'
        self.spring = 'spring'
        self.spring_r = 'spring_r'
        self.summer = 'summer'
        self.summer_r = 'summer_r'
        self.tab10 = 'tab10'
        self.tab10_r = 'tab10_r'
        self.tab20 = 'tab20'
        self.tab20_r = 'tab20_r'
        self.tab20b = 'tab20b'
        self.tab20b_r = 'tab20b_r'
        self.tab20c = 'tab20c'
        self.tab20c_r = 'tab20c_r'
        self.terrain = 'terrain'
        self.terrain_r = 'terrain_r'
        self.turbo = 'turbo'
        self.turbo_r = 'turbo_r'
        self.twilight = 'twilight'
        self.twilight_r = 'twilight_r'
        self.twilight_shifted = 'twilight_shifted'
        self.twilight_shifted_r = 'twilight_shifted_r'
        self.vanimo = 'vanimo'
        self.vanimo_r = 'vanimo_r'
        self.viridis = 'viridis'
        self.viridis_r = 'viridis_r'
        self.winter = 'winter'
        self.winter_r = 'winter_r'

# ============================================================================
# Main PyVarChart Class
# ============================================================================

class PyVarChart:
    """A variability chart creator for visualizing data across multiple categorical factors.
       Allowing breaking down data by different variables to better characterize its nature.

    This class creates sophisticated variability charts with hierarchical x-axis grouping,
    customizable markers, colors, statistical overlays (means, boxplots), and legend support.

    The chart displays data points across multiple categorical grouping levels with:
    - Hierarchical x-axis labels (e.g., chip → channel → lane → core → cmp)
    - Color-coded legend for categorical differentiation
    - Optional boxplots, cell means, group means, and grand mean overlays
    - Custom ordering of x-axis categories
    - Jittering for overlapping points visualization (jittering results in randomized horizontal positions, such that
      subsequent calls result in slightly different graphs, however, the data is the same)

    Example Output Structure::

        trim_read Variability Across Configs        Legend: lane
        250 ┤                                        ● I (blue)
            │                                 ●      ● Q (red)
        200 ┤                                 ●
            │    ●     ●      ●     ●     ●
        150 ┤    ●  ●  ●   ●  ●  ●  ●  ●     ●  ●  ●     ●     ●
            │                                    ●       ●
        100 ┤                            ●
            │                         ●
         50 ┤                                          ●
            │
          0 └────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────
            cmp  4  3  2  1  0  4  3  2  1  0  4  3  2  1  0
            core       0              1              0     1
            lane          I                   Q
            channel                2
            chip                   0

    Args:
        label_spacing: Vertical spacing between hierarchical x-axis label levels.
                       Can be a single float for uniform spacing, or a list of floats
                       (one per x-axis level) for custom spacing per level. Default: 0.15

        str_yaxis_var_name: Name of the column to plot on y-axis (must exist in DataFrame). Default: 'y_variable'
        lst_xaxis_var_names: List of column names for hierarchical x-axis grouping. Default: None (empty list)
                             (str_yaxis_var_name mustn't be in lst_xaxis_var_names)

        str_legend: Optional column name for color/marker differentiation. Default: None
        int_jitter_points: If 1, adds horizontal jitter to overlapping points. Default: 0
        int_boxplots: If 1 show boxplots for each x-axis group; if 0, hide them (show means/points only). Default: 1
        int_show_points: If 1, show individual data points; if 0, hide them (show means/boxplots only). Default: 1
        int_marker_size: Size of markers of points. Default: 8
        str_marker_theme: Marker style theme - 'Default' (circles) or 'Solid' (varied shapes). Default: 'Default'

        str_color_theme: Color palette - Default: 'blue_to_green_to_red'
            can be any of the matplotlib colormaps (https://matplotlib.org/stable/tutorials/colors/colormaps.html)
            Popular values:
            Categories of Colormaps:
            Qualitative (best for categorical/legend data like yours):
            Accent, Dark2, Paired, Pastel1, Pastel2, Set1, Set2, Set3
            tab10, tab20, tab20b, tab20c
            Sequential (single hue, good for continuous data):
            Blues, Greens, Reds, Oranges, Purples, Greys, etc.
            viridis, plasma, inferno, magma, cividis
            Diverging (two hues, for data with a midpoint):
            RdBu, RdYlGn, BrBG, PuOr, coolwarm, seismic
            Perceptual (modern, colorblind-friendly):
            viridis, plasma, inferno, magma, cividis, turbo

            also, for plt.cm types, if added a '_r' postfix, it reverses the colormap (in most cases)
            reversing of the colormap can also be done by setting int_reverse_color_scheme=1 (which applies to the
            custom 'blue_to_green_to_red' theme)

        int_continuous_scale: If 1, "quantize the legend" - treats legend as continuous scale with 5-6 representative
                              values shown in legend.
                              Representative values are automatically selected to include endpoints (min/max) and
                              evenly distributed intermediate values (percentiles). Colors smoothly interpolate across range.
                              If 0, treats legend as categorical (shows all unique discrete values).
                              Automatically reverts to 0 if legend contains any non-numeric values. Default: 0
        int_reverse_color_scheme: if 1, reverse the colorscheme intended for the points, if 0 keep as they were. Default: 0
        int_show_cell_means: If 1, display horizontal lines at cell means. Default: 0
        lst_show_group_means: List of grouping variables to show means for. Default: None (empty list)
        int_show_grand_mean: If 1, display grand mean as horizontal dotted line. Default: 0

        int_frame_size_x: Figure width in inches. Default: 20
        int_frame_size_y: Figure height in inches. Default: 6

        str_title: Optional title for the chart, can be changed with plt.title() post figure. Default: None
        dict_xaxis_orderings: Dict mapping column names to custom sort orders, e.g., {'cmp': [4,3,2,1,0]}. Default: None
                              if the dict entry doesn't contain all unique values found in the data column, the missing
                              values are appended at the end in sorted order.
                              if filtering those out is desired, use standard pandas DataFrame filtering prior to passing data to analyze().
                              for example:
                              if 'cmp' is an x-axis variable, and only cmp values 0-4 are desired, do:
                                pvc.analyze(1, dataframe[dataframe['cmp'] < 5])
        lst_rotation: List of 'Horizontal' or 'Vertical' rotation for each x-axis level. Default: None (auto-horizontal)
                      use vertical for long string values or multidigit values, ensure the appropriate label_spacing is set.
        lst_xaxis_font_size: List of font sizes for each x-axis level. Default: None (uses matplotlib default)

    Methods:
        analyze(pd_data: pd.DataFrame) -> pd.DataFrame:
            Generate a variability chart from the provided DataFrame.
            returns the processed DataFrame used for plotting.
            saves the processed DataFrame in self.pd_data_processed for later use.
            also saves other dataframe and variables useful for plotting in self.
            Returns the processed DataFrame used for plotting.
            Must be run prior to plot().
            Must be run at EVERY change of the following variables (in order to .plot() to work correctly):
            str_yaxis_var_name
            lst_xaxis_var_names
            str_legend
            str_marker_theme
            int_continuous_scale
            dict_xaxis_orderings

        plot(int_fig_num: int) -> Tuple[plt.Figure, plt.Axes]:
            Create the matplotlib figure and axes for the variability chart.
            Must be run after analyze().
            Args:
                int_fig_num: Matplotlib figure number for the plot (useful for managing multiple figures).
            Returns:
                Tuple of (figure, axes) matplotlib objects that can be further customized
                or saved to file.

    Example::

        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['chip', 'channel', 'lane'],
            str_legend='condition',
            int_show_cell_means=1
        )
        pvc.analyze(dataframe)
        fig, ax = pvc.plot(1, dataframe)
    """
    def __init__(self,
                 label_spacing: Union[float, List[float]] = 0.15,
                 str_yaxis_var_name: str = 'y_variable',
                 lst_xaxis_var_names: Optional[List[str]] = None,
                 str_legend: Optional[str] = None,
                 int_jitter_points: int = 1,
                 int_boxplots: int = 1,
                 int_show_points: int = 1,
                 int_marker_size: int = 8,
                 str_marker_theme: str = 'Default',
                 str_color_theme: str = 'blue_to_green_to_red',
                 int_continuous_scale: int = 0,
                 int_reverse_color_scheme: int = 0,
                 int_show_cell_means: int = 0,
                 lst_show_group_means: Optional[List[str]] = None,
                 int_show_grand_mean: int = 0,
                 int_frame_size_x: int = 20,
                 int_frame_size_y: int = 6,
                 str_title: Optional[str] = None,
                 dict_xaxis_orderings: Optional[Dict[str, List[Any]]] = None,
                 lst_rotation: Optional[List[str]] = None,
                 lst_xaxis_font_size: Optional[List[int]] = None):
        self.label_spacing = label_spacing
        self.str_yaxis_var_name = str_yaxis_var_name
        self.lst_xaxis_var_names = lst_xaxis_var_names if lst_xaxis_var_names is not None else []
        self.str_legend = str_legend
        self.int_jitter_points = int_jitter_points
        self.int_boxplots = int_boxplots
        self.int_show_points = int_show_points
        self.int_marker_size = int_marker_size
        self.str_marker_theme = str_marker_theme
        self.str_color_theme = str_color_theme
        self.int_continuous_scale = int_continuous_scale
        self.int_reverse_color_scheme = int_reverse_color_scheme
        self.int_show_cell_means = int_show_cell_means
        self.lst_show_group_means = lst_show_group_means if lst_show_group_means is not None else []
        self.int_show_grand_mean = int_show_grand_mean
        self.int_frame_size_x = int_frame_size_x
        self.int_frame_size_y = int_frame_size_y
        self.str_title = str_title
        self.dict_xaxis_orderings = dict_xaxis_orderings
        self.lst_rotation = lst_rotation
        self.lst_xaxis_font_size = lst_xaxis_font_size if lst_xaxis_font_size is not None else []

        self.color_map_factory = ColorMapFactory()

        # analysis quantities:
        self.pd_plot = None
        self.pd_plot_legend_vals = None
        self.pd_data_processed = None
        self.marker_dict = None
        self.normalized_legend_values = None
        self.representative_values = None
        self.use_continuous_scale = False

    def _get_marker_dict(self, values: List[Any], str_marker_theme: str) -> Dict[Any, str]:
        """Generate a mapping of legend values to matplotlib marker styles.

        Args:
            values: List of unique legend values to assign markers to.

        Returns:
            Dictionary mapping each value to a marker style string.
        """
        # theme = self.str_marker_theme.lower()
        theme = str_marker_theme.lower()
        if theme == 'default':
            return {val: 'o' for val in values}
        elif theme == 'solid':
            shapes = ['s', '^', 'D', 'v', '<', '>', 'p', '*', 'X', 'H']
        else:
            shapes = ['o', 's', '^', 'D', 'v', 'P', '*', '<', '>', 'X']
        return {val: shape for val, shape in zip(values, cycle(shapes))}

    def analyze(self, pd_data: pd.DataFrame) -> pd.DataFrame:
        """Generate a variability chart from the provided DataFrame.

        This method creates a matplotlib figure with hierarchical x-axis grouping,
        optional boxplots, means, and customizable visual styling based on the
        instance configuration.

        Args:
            int_fig_num: Matplotlib figure number for the plot (useful for managing multiple figures).
            pd_data: DataFrame containing the data to visualize. Must include columns
                    specified in str_yaxis_var_name, lst_xaxis_var_names, and str_legend.

        Returns:
            dataframe
            Tuple of (figure, axes) matplotlib objects that can be further customized
            or saved to file.

        Raises:
            ValueError: If required columns are missing from pd_data, or if invalid
                       custom orderings are specified.
            KeyError: If specified column names don't exist in the DataFrame.

        Example::

            pvc = PyVarChart(str_yaxis_var_name='value', lst_xaxis_var_names=['group1', 'group2'])
            pd_plot = pvc.analyze(my_dataframe)

        Note:
            Must be run prior to plot().
            Must be run at EVERY change of the following variables (in order to .plot() to work correctly):
            str_yaxis_var_name
            lst_xaxis_var_names
            str_legend
            str_marker_theme
            int_continuous_scale
            dict_xaxis_orderings

        """
        # Validation: Check if required columns exist
        missing_cols = []

        if self.str_yaxis_var_name not in pd_data.columns:
            missing_cols.append(f"Y-axis variable '{self.str_yaxis_var_name}'")

        for var in self.lst_xaxis_var_names:
            if var not in pd_data.columns:
                missing_cols.append(f"X-axis variable '{var}'")

        if self.str_legend and self.str_legend not in pd_data.columns:
            missing_cols.append(f"Legend variable '{self.str_legend}'")

        if missing_cols:
            raise ValueError(
                f"Missing required columns in DataFrame: {', '.join(missing_cols)}. "
                f"Available columns: {list(pd_data.columns)}"
            )

        # Validation: Check for overlap between y-axis and x-axis variables
        if self.str_yaxis_var_name in self.lst_xaxis_var_names:
            raise ValueError(
                f"Y-axis variable '{self.str_yaxis_var_name}' cannot also be in X-axis variables"
            )

        # Validation: Check custom orderings and fix missing/extra values
        if self.dict_xaxis_orderings:
            for col, custom_order in list(self.dict_xaxis_orderings.items()):
                if col not in pd_data.columns:
                    print(f"Warning: Custom ordering specified for column '{col}' which doesn't exist. Ignoring.")
                    continue

                actual_values = set(pd_data[col].unique())
                specified_values = set(custom_order)

                missing_in_order = actual_values - specified_values
                extra_in_order = specified_values - actual_values

                if missing_in_order:
                    print(f"Warning: Custom ordering for '{col}' is missing values: {missing_in_order}. "
                          f"These will be appended at the end in default order.")
                    self.dict_xaxis_orderings[col] = list(custom_order) + sorted(list(missing_in_order), key=lambda x: (isinstance(x, str), x))

                if extra_in_order:
                    print(f"Warning: Custom ordering for '{col}' contains values not in data: {extra_in_order}. "
                          f"These will be ignored.")

        # Validation: Check group means variables
        if self.lst_show_group_means:
            invalid_means = [var for var in self.lst_show_group_means if var not in self.lst_xaxis_var_names]
            if invalid_means:
                print(f"Warning: Group means requested for variables not in x-axis grouping: {invalid_means}. "
                      f"These will be skipped.")

        # inherit only relevant instance variables
        str_yaxis_var_name = self.str_yaxis_var_name
        lst_xaxis_var_names = self.lst_xaxis_var_names
        str_legend = self.str_legend
        str_marker_theme = self.str_marker_theme
        int_continuous_scale = self.int_continuous_scale
        dict_xaxis_orderings = self.dict_xaxis_orderings

        for col in lst_xaxis_var_names:
            # Normalize float grouping variables to int if whole number
            if pd.api.types.is_float_dtype(pd_data[col]):
                with pd.option_context('mode.chained_assignment', None):
                    pd_data[col] = pd_data[col].apply(normalize_grouping_value)

            # Apply category dtype if custom ordering provided
            if dict_xaxis_orderings and col in dict_xaxis_orderings:
                categories = pd.CategoricalDtype(categories=dict_xaxis_orderings[col], ordered=True)
                with pd.option_context('mode.chained_assignment', None):
                    pd_data[col] = pd_data[col].astype(categories)
                # pd_data[col] = pd_data[col].astype(categories)

        # Use grouping vars as MultiIndex
        lst_grouping_vars = lst_xaxis_var_names

        # Select only grouping vars and y-axis var from dataframe
        # (Filtering based on str_filering_string not implemented here)
        # We'll assume full data is used.
        # Get unique combos of grouping variables, sorted
        pd_unique_combos = pd_data[lst_grouping_vars].drop_duplicates()

        pd_unique_combos = pd_unique_combos.sort_values(lst_grouping_vars)

        lst_data, lst_index_levels = [], []
        lst_legend_vals = []

        for index, row in pd_unique_combos.iterrows():
            # pd_ser_conditions = (pd_data[lst_grouping_vars] == row).all(axis=1)
            # This can be fragile if any group column has missing values. Consider using .eq() and .all(axis=1) more robustly:
            pd_ser_conditions = pd.concat([pd_data[col].eq(row[col]) for col in lst_grouping_vars], axis=1).all(axis=1)
            pd_curr = pd_data[pd_ser_conditions]
            if pd_curr.empty:
                continue
            for _, row_match in pd_curr.iterrows():
                lst_data.append(row_match[str_yaxis_var_name])
                lst_index_levels.append(tuple(row))
                lst_legend_vals.append(normalize_grouping_value(row_match[str_legend]) if str_legend else None)

        pd_plot = pd.Series(lst_data, index=pd.MultiIndex.from_tuples(lst_index_levels, names=lst_grouping_vars), name='Data')
        pd_plot_legend_vals = pd.Series(lst_legend_vals, index=pd_plot.index, name='Legend')

        if str_legend and str_legend in pd_data.columns:
            raw_legend_values = pd_data[str_legend].dropna().unique()
            normalized_legend_values = sorted(set(normalize_grouping_value(val) for val in raw_legend_values))

            # Check if continuous scale is enabled and legend values are numeric
            use_continuous_scale = False
            value_to_color_key = {}  # Maps actual value -> color key (for interpolation)
            representative_values = []  # The 5-6 values to show in legend

            if int_continuous_scale == 1 and len(normalized_legend_values) > 0:
                # Check if ALL values are numeric (if any string found, force categorical)
                all_numeric = True
                numeric_values = []

                try:
                    for val in normalized_legend_values:
                        numeric_val = float(val)
                        numeric_values.append(numeric_val)
                except (ValueError, TypeError):
                    # Found a string or non-numeric value - force categorical
                    all_numeric = False

                if all_numeric and len(numeric_values) > 0:
                    use_continuous_scale = True

                    # Select 5-6 representative values using percentiles
                    # Always include min and max as endpoints
                    min_val = min(numeric_values)
                    max_val = max(numeric_values)

                    if min_val == max_val:
                        # All values are the same - just use categorical
                        use_continuous_scale = False
                    else:
                        # Calculate representative values at key percentiles
                        # Using 0%, 20%, 40%, 60%, 80%, 100% for 6 values
                        percentiles = [0, 20, 40, 60, 80, 100]
                        representative_values = [
                            np.percentile(numeric_values, p) for p in percentiles
                        ]

                        # Remove duplicates while preserving order
                        seen = set()
                        representative_values = [
                            x for x in representative_values
                            if not (x in seen or seen.add(x))
                        ]

                        # Create a mapping: each actual value maps to its interpolated position
                        # in the color gradient
                        for val in normalized_legend_values:
                            numeric_val = float(val)
                            # Normalize to 0-1 range for color interpolation
                            normalized_pos = (numeric_val - min_val) / (max_val - min_val)
                            value_to_color_key[val] = normalized_pos

                        # Representative values also need their positions
                        for rep_val in representative_values:
                            normalized_pos = (rep_val - min_val) / (max_val - min_val)
                            value_to_color_key[rep_val] = normalized_pos

            # If not using continuous scale, fall back to categorical
            if not use_continuous_scale:
                # Categorical mode: each unique value gets distinct color
                representative_values = normalized_legend_values

            # Build marker dict
            marker_dict = self._get_marker_dict(representative_values, str_marker_theme)
        else:
            marker_dict = {}
            normalized_legend_values = [None]
            representative_values = []
            value_to_color_key = {}

        # save results to instance variables
        self.pd_plot = pd_plot
        self.pd_plot_legend_vals = pd_plot_legend_vals
        self.pd_data_processed = pd_data
        self.marker_dict = marker_dict
        self.normalized_legend_values = normalized_legend_values
        self.representative_values = representative_values
        self.use_continuous_scale = use_continuous_scale
        self.value_to_color_key = value_to_color_key
        return pd_plot

    def plot(self, int_fig_number=1) -> Tuple[plt.Figure, plt.Axes]:
        """Plot the variability chart using data from previous analyze() call.

        Args:
            int_fig_number: Matplotlib figure number for the plot.

        Returns:
            Tuple of (figure, axes) matplotlib objects.

        Raises:
            ValueError: If analyze() hasn't been called yet.

        Example:
        fig, ax = pvc.plot(1)
            fig.savefig('output.png')

        """
        # Check if analyze was called
        if self.pd_plot is None:
            raise ValueError("Must call analyze() with the data before plot()")

        # Retrieve stored data from analyze()
        pd_plot = self.pd_plot
        pd_plot_legend_vals = self.pd_plot_legend_vals
        pd_data = self.pd_data_processed
        marker_dict = self.marker_dict
        normalized_legend_values = self.normalized_legend_values
        representative_values = self.representative_values
        use_continuous_scale = self.use_continuous_scale
        value_to_color_key = self.value_to_color_key

        # inherit only relevant instance variables
        label_spacing = self.label_spacing
        str_yaxis_var_name = self.str_yaxis_var_name
        lst_xaxis_var_names = self.lst_xaxis_var_names
        str_legend = self.str_legend
        int_jitter_points = self.int_jitter_points
        int_boxplots = self.int_boxplots
        int_show_points = self.int_show_points
        int_marker_size = self.int_marker_size
        # str_marker_theme = self.str_marker_theme
        str_color_theme = self.str_color_theme
        # int_continuous_scale = self.int_continuous_scale
        int_reverse_color_scheme = self.int_reverse_color_scheme
        int_show_cell_means = self.int_show_cell_means
        lst_show_group_means = self.lst_show_group_means
        int_show_grand_mean = self.int_show_grand_mean
        int_frame_size_x = self.int_frame_size_x
        int_frame_size_y = self.int_frame_size_y
        str_title = self.str_title
        # dict_xaxis_orderings = self.dict_xaxis_orderings
        lst_rotation = self.lst_rotation
        lst_xaxis_font_size = self.lst_xaxis_font_size

        if lst_rotation is None:
            lst_rotation = ['Horizontal'] * len(lst_xaxis_var_names)

        # Build color dict based on representative values
        if str_legend:
            # Handle custom 'Blue to Green to Red' gradient (normalize by removing spaces and lowercasing)
            normalized_theme = str_color_theme.lower().replace(' ', '_')
            if normalized_theme == 'blue_to_green_to_red':
                color_list = ['blue', 'green', 'red']
                if int_reverse_color_scheme == 1:
                    color_list = color_list[::-1]
                cmap = mcolors.LinearSegmentedColormap.from_list('custom', color_list)
            else:
                # Try to get colormap from matplotlib
                theme_name = str_color_theme
                base_theme_name = theme_name

                # Try to get the colormap
                try:
                    cmap = mpl.colormaps[base_theme_name]
                except (ValueError, KeyError):
                    # Fallback to blue_to_green_to_red if colormap not found
                    print(f"Warning: Colormap '{str_color_theme}' not found. Falling back to 'blue_to_green_to_red'.")
                    color_list = ['blue', 'green', 'red']
                    if int_reverse_color_scheme == 1:
                        color_list = color_list[::-1]
                    cmap = mcolors.LinearSegmentedColormap.from_list('custom', color_list)
                else:
                    # Apply reversal if requested
                    should_reverse = int_reverse_color_scheme == 1
                    if should_reverse:
                        cmap = cmap.reversed()

            # Generate colors based on mode
            if use_continuous_scale:
                # Continuous mode: use interpolated colors
                # Create color dict for all actual values using interpolation
                color_dict = {}
                for val, normalized_pos in value_to_color_key.items():
                    color_dict[val] = cmap(normalized_pos)

                # Also ensure representative values have colors
                for rep_val in representative_values:
                    if rep_val not in color_dict:
                        normalized_pos = value_to_color_key.get(rep_val, 0.5)
                        color_dict[rep_val] = cmap(normalized_pos)
            else:
                # Categorical mode: discrete colors
                n_colors = len(representative_values)
                colors = [cmap(i / (n_colors - 1 if n_colors > 1 else 1)) for i in range(n_colors)]
                color_dict = dict(zip(representative_values, colors))

            # marker_dict = self._get_marker_dict(representative_values)
        else:
            color_dict = {}
            marker_dict = {}
            normalized_legend_values = [None]

        fig = plt.figure(int_fig_number, figsize=(int_frame_size_x, int_frame_size_y))
        ax = plt.gca()

        # Build mapping from unique group index -> x-position
        unique_index_order = list(dict.fromkeys(pd_plot.index.to_list()))  # preserve order
        index_to_xpos = {idx: i for i, idx in enumerate(unique_index_order)}

        # BOX DATA for optional boxplot
        if int_boxplots in [1, 2]:
            grouped = pd_data.groupby(lst_xaxis_var_names, observed=False)[str_yaxis_var_name]
            box_data = [grouped.get_group(idx).dropna().values for idx in unique_index_order if idx in grouped.groups]
            ax.boxplot(box_data, positions=range(len(box_data)), widths=0.5, patch_artist=True,
                       boxprops=dict(facecolor='lightgray', color='black'),
                       medianprops=dict(color='black'),
                       whiskerprops=dict(color='black'),
                       capprops=dict(color='black'),
                       flierprops=dict(marker='o', markersize=4, linestyle='none', markerfacecolor='gray'))


        if int_show_grand_mean:
            grand_mean = pd_plot.mean()
            ax.axhline(grand_mean, color='black', linestyle=':', linewidth=1.5, label='Grand Mean')

        if lst_show_group_means:
            for level_name in lst_show_group_means:
                if level_name not in lst_xaxis_var_names:
                    continue  # Skip invalid groupings

                level_idx = lst_xaxis_var_names.index(level_name)
                grouped = pd_plot.groupby(level=level_idx)

                for group_val, group_data in grouped:
                    mean_val = group_data.mean()

                    # Get x positions matching this group value at the level
                    matching_indices = [idx for idx in pd_plot.index if idx[level_idx] == group_val]
                    matching_positions = [index_to_xpos[idx] for idx in matching_indices]

                    if matching_positions:
                        # Old Behavior (Bug):
                        # min_pos, max_pos = min(matching_positions), max(matching_positions)
                        # ax.hlines(mean_val, min_pos - 0.3, max_pos + 0.3, colors='blue', linewidth=1.2, linestyles='--')
                        # reasoning for the example of:
                        # lst_xaxis_var_names = ['chip', 'channel', 'lane', 'core', 'cmp']
                        # lst_show_group_means = ['lane']  # Show mean for each lane value
                        # For lane='I', the grouped data appears at these x-positions:
                        # matching_positions = [0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17]
                        #                       ^^^^^^^^^^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^
                        #                       First group (core=0)   Second group (core=1)
                        #                       Gap between position 5 and 12!
                        # When using lst_show_group_means, the code incorrectly drew a single continuous line across
                        # discontinuous x-axis positions, creating visual artifacts that spanned gaps where no data exists.
                        # Drew ONE line from x=-0.3 to x=17.3, spanning the gap!

                        # Fix:
                        # Split positions into continuous segments when gaps (Δ > 1) are detected, then draw separate
                        # lines for each segment.
                        sorted_pos = np.array(sorted(matching_positions))
                        # [0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16, 17]
                        breaks = np.where(np.diff(sorted_pos) > 1)[0] + 1
                        # np.diff → [1, 1, 1, 1, 1, 7, 1, 1, 1, 1, 1]
                        # np.where(... > 1) → finds index where diff > 1 → [5]
                        # breaks = [6] (split after index 5)
                        segments = np.split(sorted_pos, breaks)
                        # [[0,1,2,3,4,5], [12,13,14,15,16,17]]

                        for segment in segments:
                            min_pos, max_pos = segment[0], segment[-1]
                            ax.hlines(mean_val, min_pos - 0.3, max_pos + 0.3, colors='blue', linewidth=1.2,
                                      linestyles='--')
                        # Draws TWO lines: 0→5 and 12→17

        # POINTS
        if int_boxplots in [0, 1] and int_show_points:
            for (idx_val, y_val), legend_val in zip(pd_plot.items(), pd_plot_legend_vals):
                x_base = index_to_xpos[idx_val]
                x_pos = x_base + np.random.uniform(-0.2, 0.2) if int_jitter_points else x_base

                if str_legend:
                    norm_val = normalize_grouping_value(legend_val)

                    # Use the normalized value directly as color key
                    # In continuous mode, all actual values are in color_dict
                    # In categorical mode, only unique values are in color_dict
                    color = color_dict.get(norm_val, 'blue')

                    # For markers, use representative values in continuous mode
                    if use_continuous_scale and representative_values:
                        # Find closest representative value for marker
                        if norm_val in value_to_color_key:
                            # Use the first representative value's marker (continuous uses same marker)
                            marker_key = representative_values[0]
                        else:
                            marker_key = representative_values[0] if representative_values else norm_val
                    else:
                        marker_key = norm_val

                    marker = marker_dict.get(marker_key, 'o')
                else:
                    color = 'blue'
                    marker = 'o'

                ax.plot(x_pos, y_val, marker=marker, color=color, linestyle='none', markersize=int_marker_size)

        if int_show_cell_means:
            cell_means = pd_plot.groupby(level=list(range(pd_plot.index.nlevels))).mean()
            for idx, mean_val in cell_means.items():
                xpos = index_to_xpos.get(idx, None)
                if xpos is not None:
                    ax.hlines(mean_val, xpos - 0.2, xpos + 0.2, colors='black', linewidth=1.5, linestyles='-')

        # Annotate grouped x-axis with rotation if too many groups
        ax.set_xticks(range(len(unique_index_order)))
        ax.set_xticklabels('')
        ax.set_xlabel('')

        # if lst_rotation is None:
        #     lst_rotation = ['Vertical'] * len(lst_xaxis_var_names)

        unique_index = pd.MultiIndex.from_tuples(unique_index_order, names=lst_xaxis_var_names)
        label_group_bar_table(ax,
                              pd.Series(index=unique_index, dtype='object'),
                              lst_rotation,
                              spacing=label_spacing,
                              lst_fontsize=lst_xaxis_font_size)

        ax.set_xlim(-0.5, len(unique_index_order) - 0.5)
        f_ylim_min = pd_data[str_yaxis_var_name].min()
        f_ylim_max = pd_data[str_yaxis_var_name].max()
        ax.set_ylim(f_ylim_min * 0.99 if f_ylim_min > 0 else f_ylim_min * 1.01,
                    f_ylim_max * 1.01 if f_ylim_max > 0 else f_ylim_max * 0.99)

        ax.set_ylabel(str_yaxis_var_name)
        plt.title(str_title if str_title else 'Variability Chart')
        plt.grid(True)

        if str_legend:
            handles = []
            labels = []
            for val in representative_values:
                h, = ax.plot([], [], marker=marker_dict.get(val, 'o'), color=color_dict.get(val, 'blue'),
                             linestyle='none', markersize=int_marker_size)
                handles.append(h)

                # Format the label appropriately
                if use_continuous_scale:
                    # Format numeric values nicely
                    if abs(val) >= 1000:
                        labels.append(f"{val:.0f}")
                    elif abs(val) >= 10:
                        labels.append(f"{val:.1f}")
                    else:
                        labels.append(f"{val:.2f}")
                else:
                    labels.append(legend_label(val))

            ax.legend(handles=handles, labels=labels, title=str_legend)

        bottom_margin = estimate_bottom_margin(len(lst_xaxis_var_names), lst_rotation, label_spacing)
        plt.subplots_adjust(bottom=bottom_margin)
        plt.tight_layout()
        plt.tight_layout()

        return fig, ax


# ============================================================================
# Example & Demo
# ============================================================================

def main_example() -> None:
    """Demonstrate PyVarChart usage with example data.

    This example creates a variability chart showing 'trim_read' values across
    multiple hardware configuration factors (chip, channel, lane, core, cmp).
    The output displays:
    - Data points colored by 'lane' (I=blue, Q=red)
    - Hierarchical x-axis with 5 levels of grouping
    - Custom ordering for 'cmp' (reversed: 4,3,2,1,0)
    - Jittered points to show overlapping values
    - Y-axis range: 0-255
    """
    str_data = ('chip, channel, lane, core, cmp, trim_read\n'
                '0   , 2      , I   , 0   , 0  , 159\n'
                '0   , 2      , I   , 0   , 1  , 136\n'
                '0   , 2      , I   , 0   , 2  , 167\n'
                '0   , 2      , I   , 0   , 3  , 139\n'
                '0   , 2      , I   , 0   , 4  , 160\n'
                '0   , 2      , I   , 0   , 5  , 152\n'
                '0   , 2      , I   , 1   , 0  , 167\n'
                '0   , 2      , I   , 1   , 1  , 130\n'
                '0   , 2      , I   , 1   , 2  , 143\n'
                '0   , 2      , I   , 1   , 3  , 158\n'
                '0   , 2      , I   , 1   , 4  , 142\n'
                '0   , 2      , I   , 1   , 5  , 56\n'
                '0   , 2      , Q   , 0   , 0  , 142\n'
                '0   , 2      , Q   , 0   , 1  , 122\n'
                '0   , 2      , Q   , 0   , 2  , 116\n'
                '0   , 2      , Q   , 0   , 3  , 135\n'
                '0   , 2      , Q   , 0   , 4  , 96\n'
                '0   , 2      , Q   , 0   , 5  , 130\n'
                '0   , 2      , Q   , 1   , 0  , 164\n'
                '0   , 2      , Q   , 1   , 1  , 138\n'
                '0   , 2      , Q   , 1   , 2  , 168\n'
                '0   , 2      , Q   , 1   , 3  , 148\n'
                '0   , 2      , Q   , 1   , 4  , 60\n'
                '0   , 2      , Q   , 1   , 5  , 135'.replace(' ', ''))
    pd_data = pd.read_csv(StringIO(str_data))

    pvc = PyVarChart(
        label_spacing=0.15,  # [0.05, 0.1, 0.15, 0.1, 0.05],
        str_yaxis_var_name='trim_read',
        lst_xaxis_var_names=['chip', 'channel', 'lane', 'core', 'cmp'],
        str_legend='lane',  #'lane',
        int_jitter_points=1,
        int_show_points=1,
        int_marker_size=8,
        int_reverse_color_scheme=0,
        lst_show_group_means=['core'],
        int_continuous_scale=0,
        int_show_cell_means=1,
        int_boxplots=0,
        str_marker_theme='Default',  # 'Solid',
        str_color_theme='blue_to_green_to_red',
        str_title='trim_read Variability Across Configs',
        int_frame_size_x=8,
        int_frame_size_y=6,
        dict_xaxis_orderings={'cmp': [5, 4, 3, 2, 1, 0]},  # Include all values: 0-5
        lst_rotation=['Horizontal', 'Horizontal', 'Horizontal', 'Horizontal', 'Horizontal'],
        lst_xaxis_font_size=[10, 10, 10, 10, 10],
    )
    int_fig_num = 1
    pvc.analyze(pd_data)
    fig, ax = pvc.plot(int_fig_num)
    ax.set_ylim(0, 255)
    # plt.tight_layout()
    # plt.show()

def complex_example():
    str_data = (
        'skew_sn, skew, sn, temp, pin_dbm  , tx0_pga_gain, freq  , trx_and_sx, standard_and_band , offset_mhz  , nf_db  , snr_db  , pout_dbm  \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 38.207 , 82.032  , -12.875   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 37.644 , 82.595  , -13.197   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 38.688 , 81.552  , -13.973   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 39.112 , 81.127  , -15.355   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 36.896 , 77.343  , -12.869   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 36.031 , 78.208  , -13.183   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 37.413 , 76.826  , -13.962   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 38.394 , 75.845  , -15.334   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 35.514 , 84.725  , -11.88    \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 37.375 , 82.864  , -12.296   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 38.448 , 81.791  , -13.152   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 38.484 , 81.755  , -14.541   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 34.649 , 79.59   , -11.845   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 34.103 , 80.136  , -12.256   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 34.837 , 79.402  , -13.113   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 37.516 , 76.723  , -14.512   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 37.985 , 82.254  , -13.255   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 38.655 , 81.585  , -13.619   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 40.032 , 80.207  , -14.433   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.854 , 79.385  , -15.802   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 35.496 , 78.743  , -13.269   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 36.802 , 77.437  , -13.633   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 36.872 , 77.367  , -14.427   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.291 , 73.948  , -15.795   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 36.21  , 84.029  , -11.95    \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 36.197 , 84.042  , -12.344   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 37.939 , 82.3    , -13.183   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 38.979 , 81.261  , -14.567   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 33.926 , 80.313  , -11.924   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 35.36  , 78.879  , -12.314   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 36.162 , 78.077  , -13.147   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 37.277 , 76.962  , -14.528   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 40.401 , 79.838  , -13.541   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 40.594 , 79.645  , -13.914   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 40.737 , 79.502  , -14.783   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 42.542 , 77.697  , -16.221   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.641 , 76.598  , -13.529   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 38.892 , 75.348  , -13.905   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 38.4   , 75.839  , -14.769   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 40.808 , 73.431  , -16.22    \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 37.039 , 83.2    , -12.254   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 38.507 , 81.732  , -12.707   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 39.065 , 81.174  , -13.667   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 39.336 , 80.903  , -15.186   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 36.187 , 78.052  , -12.217   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 36.143 , 78.096  , -12.666   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 36.022 , 78.217  , -13.626   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 38.64  , 75.599  , -15.156   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 39.827 , 80.412  , -13.975   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 40.173 , 80.066  , -14.399   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 41.094 , 79.145  , -15.321   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 42.044 , 78.195  , -16.821   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 37.768 , 76.471  , -13.978   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 37.674 , 76.565  , -14.403   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 40.237 , 74.003  , -15.323   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.949 , 73.29   , -16.823   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 38.287 , 81.952  , -12.341   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 38.164 , 82.075  , -12.78    \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 38.713 , 81.526  , -13.718   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 39.865 , 80.374  , -15.222   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 35.682 , 78.557  , -12.327   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 37.225 , 77.014  , -12.759   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 36.173 , 78.066  , -13.689   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 39.155 , 75.084  , -15.187   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 39.923 , 80.316  , -13.245   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 40.394 , 79.846  , -13.592   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 39.595 , 80.644  , -14.394   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 40.397 , 79.842  , -15.792   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.013 , 77.226  , -13.225   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 37.228 , 77.011  , -13.575   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 38.143 , 76.096  , -14.384   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 38.815 , 75.424  , -15.784   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 35.61  , 84.629  , -12.096   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 37.724 , 82.515  , -12.528   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 38.094 , 82.145  , -13.431   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 40.045 , 80.194  , -14.882   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 34.538 , 79.701  , -12.058   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 34.853 , 79.386  , -12.49    \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 36.376 , 77.863  , -13.397   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 37.93  , 76.309  , -14.851   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 38.659 , 81.58   , -13.659   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 39.401 , 80.839  , -14.056   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 41.183 , 79.056  , -14.887   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 42.355 , 77.884  , -16.311   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 37.235 , 77.004  , -13.636   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 37.699 , 76.54   , -14.031   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 38.54  , 75.7    , -14.886   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.371 , 73.868  , -16.308   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 36.803 , 83.436  , -12.159   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 37.086 , 83.153  , -12.577   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 38.479 , 81.761  , -13.461   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 39.608 , 80.631  , -14.899   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 34.291 , 79.948  , -12.138   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 35.686 , 78.553  , -12.552   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 36.065 , 78.174  , -13.427   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 38.718 , 75.521  , -14.857   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 36.559 , 83.68   , -12.615   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 36.854 , 83.386  , -12.935   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 38.564 , 81.675  , -13.699   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 39.329 , 80.91   , -15.045   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 35.953 , 78.286  , -12.606   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 35.013 , 79.226  , -12.929   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 35.934 , 78.305  , -13.691   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 37.755 , 76.484  , -15.048   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 37.437 , 82.802  , -13.06    \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 38.153 , 82.086  , -13.43    \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 38.426 , 81.813  , -14.222   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 40.108 , 80.131  , -15.557   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 36.269 , 77.97   , -13.073   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 36.887 , 77.352  , -13.441   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 37.436 , 76.803  , -14.228   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 40.036 , 74.203  , -15.562   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.513 , 84.726  , -11.461   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.435 , 84.804  , -11.868   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 38.194 , 82.045  , -12.748   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.242 , 80.997  , -14.194   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.389 , 79.851  , -11.433   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 34.207 , 80.032  , -11.832   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 34.565 , 79.674  , -12.706   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.268 , 77.971  , -14.152   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.212 , 84.027  , -11.465   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.86  , 84.379  , -11.874   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.052 , 84.188  , -12.752   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.109 , 81.13   , -14.198   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 33.208 , 81.031  , -11.438   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 33.781 , 80.458  , -11.834   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.464 , 77.776  , -12.708   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.199 , 78.04   , -14.153   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 40.488 , 79.751  , -14.275   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 39.198 , 81.041  , -14.542   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 40.411 , 79.828  , -15.326   \n'
        'TT_3   , TT  , 3 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 41.537 , 78.702  , -16.796   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 36.777 , 77.462  , -14.279   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 38.018 , 76.221  , -14.547   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 38.494 , 75.745  , -15.316   \n'
        'TT_3   , TT  , 3 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 39.941 , 74.298  , -16.777   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 38.568 , 81.672  , -13.202   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 39.078 , 81.161  , -13.581   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 40.269 , 79.971  , -14.462   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 41.313 , 78.926  , -15.954   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 37.442 , 76.797  , -13.195   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 37.881 , 76.358  , -13.573   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 38.033 , 76.206  , -14.458   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 39.762 , 74.477  , -15.956   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 39.665 , 80.574  , -13.599   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 39.789 , 80.45   , -14.037   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 40.985 , 79.254  , -14.984   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 42.341 , 77.898  , -16.503   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.213 , 76.026  , -13.606   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 40.729 , 73.51   , -14.048   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 38.777 , 75.462  , -14.989   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 40.561 , 73.678  , -16.506   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.807 , 83.432  , -11.808   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.635 , 82.604  , -12.272   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 38.953 , 81.287  , -13.283   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 40.966 , 79.273  , -14.874   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.916 , 78.323  , -11.788   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 36.892 , 77.347  , -12.239   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.582 , 77.657  , -13.234   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 37.509 , 76.73   , -14.829   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 37.805 , 82.435  , -11.812   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.218 , 83.021  , -12.272   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 39.033 , 81.206  , -13.278   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 40.202 , 80.037  , -14.871   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.309 , 77.93   , -11.795   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 34.91  , 79.329  , -12.245   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.983 , 77.256  , -13.24    \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 37.293 , 76.946  , -14.835   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 41.501 , 78.738  , -15.095   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 42.28  , 77.959  , -15.412   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 43.618 , 76.621  , -16.296   \n'
        'TT_3   , TT  , 3 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 44.624 , 75.615  , -17.877   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 40.802 , 73.437  , -15.1     \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 40.535 , 73.704  , -15.42    \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 42.571 , 71.668  , -16.307   \n'
        'TT_3   , TT  , 3 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 42.352 , 71.887  , -17.867   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 38.586 , 81.654  , -12.932   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 39.56  , 80.679  , -13.283   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 39.747 , 80.492  , -14.097   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 41.052 , 79.188  , -15.505   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 36.452 , 77.787  , -12.906   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 36.855 , 77.384  , -13.262   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 36.511 , 77.728  , -14.08    \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 39.162 , 75.077  , -15.498   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.596 , 81.643  , -13.321   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 38.921 , 81.318  , -13.733   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 40.122 , 80.117  , -14.6     \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 42.041 , 78.198  , -16.02    \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.125 , 76.114  , -13.331   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 38.327 , 75.912  , -13.739   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 39.248 , 74.991  , -14.603   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 41.013 , 73.226  , -16.027   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.529 , 83.71   , -11.645   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 38.523 , 81.716  , -12.077   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.484 , 82.755  , -12.991   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 38.976 , 81.263  , -14.508   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.196 , 80.043  , -11.599   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.304 , 78.935  , -12.025   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 35.616 , 78.623  , -12.955   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.872 , 77.367  , -14.465   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 37.331 , 82.908  , -11.626   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.666 , 82.574  , -12.058   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.984 , 82.255  , -12.995   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.518 , 80.721  , -14.511   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.995 , 79.244  , -11.603   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 34.737 , 79.502  , -12.028   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.729 , 77.51   , -12.958   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 37.577 , 76.662  , -14.468   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 40.515 , 79.724  , -14.673   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 41.322 , 78.917  , -14.966   \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 42.199 , 78.04   , -15.78    \n'
        'TT_3   , TT  , 3 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 43.339 , 76.9    , -17.279   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 39.032 , 75.207  , -14.689   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 39.779 , 74.46   , -14.974   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 42.208 , 72.031  , -15.776   \n'
        'TT_3   , TT  , 3 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 43.064 , 71.175  , -17.267   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.254 , 82.985  , -13.188   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 38.712 , 81.527  , -13.491   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 38.395 , 81.844  , -14.21    \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 39.261 , 80.978  , -15.51    \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 36.132 , 78.107  , -13.174   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 36.528 , 77.711  , -13.477   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 35.661 , 78.578  , -14.192   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 38.582 , 75.657  , -15.491   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 36.368 , 83.871  , -12.201   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 36.085 , 84.154  , -12.589   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 38.294 , 81.945  , -13.395   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 38.428 , 81.811  , -14.706   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 33.435 , 80.804  , -12.166   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 34.092 , 80.147  , -12.556   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 35.543 , 78.696  , -13.347   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 36.203 , 78.036  , -14.663   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 38.382 , 81.857  , -13.557   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 38.691 , 81.548  , -13.902   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 39.758 , 80.481  , -14.655   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 39.845 , 80.394  , -15.953   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 36.906 , 77.333  , -13.563   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 37.215 , 77.024  , -13.903   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 37.211 , 77.028  , -14.648   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 38.924 , 75.315  , -15.918   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 36.174 , 84.065  , -12.244   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 36.925 , 83.314  , -12.621   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 37.714 , 82.525  , -13.409   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 39.293 , 80.946  , -14.714   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 33.402 , 80.837  , -12.211   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 34.98  , 79.259  , -12.583   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 35.462 , 78.777  , -13.363   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 37.332 , 76.907  , -14.666   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 39.589 , 80.65   , -13.885   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 39.414 , 80.825  , -14.23    \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 40.551 , 79.688  , -15.024   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 42.933 , 77.306  , -16.394   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.47  , 76.769  , -13.874   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 37.902 , 76.337  , -14.215   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 37.726 , 76.513  , -15.013   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 40.3   , 73.939  , -16.389   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 39.269 , 80.97   , -12.585   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 38.459 , 81.78   , -13.016   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 39.08  , 81.159  , -13.914   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 40.594 , 79.646  , -15.347   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 36.841 , 77.398  , -12.543   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 36.551 , 77.688  , -12.976   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 37.207 , 77.032  , -13.874   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 38.597 , 75.642  , -15.318   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 39.326 , 80.913  , -14.312   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 40.808 , 79.432  , -14.714   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 41.304 , 78.935  , -15.58    \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 42.525 , 77.715  , -17.0     \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 37.944 , 76.295  , -14.313   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 38.129 , 76.11   , -14.723   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 40.239 , 74.001  , -15.589   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.872 , 73.367  , -17.002   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 38.011 , 82.228  , -12.677   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 39.163 , 81.076  , -13.097   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 39.136 , 81.104  , -13.978   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 40.093 , 80.146  , -15.399   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 35.8   , 78.439  , -12.652   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 36.525 , 77.715  , -13.066   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 36.16  , 78.079  , -13.938   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 38.019 , 76.22   , -15.358   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 39.098 , 81.141  , -13.558   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 38.316 , 81.923  , -13.881   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 39.936 , 80.304  , -14.622   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 42.339 , 77.9    , -15.938   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 35.89  , 78.349  , -13.531   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 37.356 , 76.883  , -13.858   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 38.309 , 75.93   , -14.606   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 39.071 , 75.168  , -15.924   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 37.103 , 83.136  , -12.394   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 37.394 , 82.845  , -12.808   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 37.403 , 82.836  , -13.65    \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 39.798 , 80.441  , -15.018   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 34.804 , 79.435  , -12.346   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 35.535 , 78.704  , -12.757   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 36.85  , 77.389  , -13.604   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 36.612 , 77.627  , -14.978   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 38.861 , 81.378  , -13.94    \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 38.585 , 81.654  , -14.316   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 41.851 , 78.388  , -15.117   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 41.746 , 78.493  , -16.461   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 36.776 , 77.464  , -13.933   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 37.751 , 76.489  , -14.31    \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 38.907 , 75.332  , -15.108   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 39.506 , 74.733  , -16.453   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 36.714 , 83.526  , -12.471   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 36.966 , 83.273  , -12.872   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 38.436 , 81.804  , -13.699   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 39.832 , 80.407  , -15.057   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 35.376 , 78.864  , -12.436   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 34.984 , 79.255  , -12.832   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 36.183 , 78.056  , -13.653   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 38.5   , 75.739  , -15.008   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 37.169 , 83.07   , -12.799   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 39.525 , 80.714  , -13.096   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 39.134 , 81.105  , -13.8     \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 38.935 , 81.304  , -15.093   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 34.842 , 79.397  , -12.783   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 35.23  , 79.009  , -13.08    \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 36.017 , 78.222  , -13.788   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 37.663 , 76.576  , -15.071   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.312 , 81.927  , -13.193   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 38.496 , 81.743  , -13.541   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 39.158 , 81.081  , -14.279   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 39.567 , 80.672  , -15.546   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 36.02  , 78.22   , -13.197   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 35.35  , 78.889  , -13.544   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 38.252 , 75.987  , -14.28    \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 37.716 , 76.523  , -15.545   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.459 , 84.78   , -11.655   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 36.091 , 84.148  , -12.047   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.578 , 82.661  , -12.871   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 38.119 , 82.12   , -14.24    \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.432 , 79.807  , -11.62    \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.147 , 79.092  , -12.005   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 35.392 , 78.847  , -12.824   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.061 , 78.178  , -14.192   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.904 , 84.335  , -11.663   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 36.506 , 83.733  , -12.054   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.493 , 83.746  , -12.879   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 38.558 , 81.681  , -14.247   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.444 , 79.796  , -11.628   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 33.598 , 80.641  , -12.011   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 34.355 , 79.884  , -12.829   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.786 , 77.453  , -14.195   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 39.984 , 80.255  , -14.439   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 39.718 , 80.521  , -14.692   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 39.925 , 80.314  , -15.427   \n'
        'TT_8   , TT  , 8 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 42.286 , 77.953  , -16.831   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 37.748 , 76.491  , -14.448   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 37.193 , 77.046  , -14.696   \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 38.633 , 75.606  , -15.42    \n'
        'TT_8   , TT  , 8 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 41.377 , 72.862  , -16.799   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 38.742 , 81.497  , -13.392   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 40.234 , 80.005  , -13.737   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 40.265 , 79.974  , -14.557   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 41.182 , 79.058  , -15.976   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 37.414 , 76.825  , -13.365   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 36.764 , 77.475  , -13.721   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 38.362 , 75.877  , -14.547   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 40.196 , 74.043  , -15.971   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 40.57  , 79.669  , -13.75    \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 40.888 , 79.351  , -14.164   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 41.092 , 79.147  , -15.056   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 41.928 , 78.311  , -16.495   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.775 , 75.464  , -13.752   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 37.677 , 76.562  , -14.167   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 39.492 , 74.747  , -15.05    \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 40.552 , 73.687  , -16.499   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.837 , 83.403  , -12.004   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.418 , 82.821  , -12.447   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 39.509 , 80.731  , -13.389   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.422 , 80.817  , -14.902   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.953 , 79.287  , -11.969   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.475 , 78.764  , -12.402   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.548 , 76.691  , -13.34    \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 38.579 , 75.66   , -14.857   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 37.651 , 82.588  , -12.001   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.669 , 82.57   , -12.442   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 38.152 , 82.088  , -13.389   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 40.753 , 79.486  , -14.905   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.0   , 78.239  , -11.976   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.889 , 78.35   , -12.406   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.78  , 77.459  , -13.345   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 37.65  , 76.589  , -14.861   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 42.608 , 77.631  , -15.243   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 42.141 , 78.098  , -15.538   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 43.663 , 76.576  , -16.375   \n'
        'TT_8   , TT  , 8 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 44.629 , 75.61   , -17.883   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 39.529 , 74.71   , -15.24    \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 40.488 , 73.751  , -15.542   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 40.34  , 73.9    , -16.378   \n'
        'TT_8   , TT  , 8 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 42.951 , 71.288  , -17.871   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 38.07  , 82.169  , -13.086   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 38.207 , 82.032  , -13.418   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 38.44  , 81.799  , -14.176   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 40.013 , 80.226  , -15.512   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 35.369 , 78.87   , -13.062   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 36.912 , 77.327  , -13.393   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 37.329 , 76.91   , -14.156   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 38.659 , 75.58   , -15.502   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 39.299 , 80.94   , -13.444   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 39.436 , 80.803  , -13.835   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 40.542 , 79.697  , -14.649   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 40.929 , 79.31   , -15.996   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 37.568 , 76.671  , -13.45    \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 37.764 , 76.475  , -13.838   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 37.761 , 76.478  , -14.652   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 39.45  , 74.79   , -16.004   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.555 , 83.684  , -11.82    \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 36.939 , 83.3    , -12.236   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 38.328 , 81.912  , -13.12    \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.052 , 81.187  , -14.558   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.929 , 79.31   , -11.791   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.271 , 78.968  , -12.201   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.338 , 77.901  , -13.074   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 37.896 , 76.343  , -14.51    \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 38.024 , 82.215  , -11.826   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.268 , 82.971  , -12.242   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 38.606 , 81.633  , -13.126   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.405 , 80.834  , -14.563   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.513 , 79.726  , -11.795   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 34.486 , 79.753  , -12.204   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.127 , 78.112  , -13.076   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.85  , 77.39   , -14.513   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 41.103 , 79.136  , -14.84    \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 40.548 , 79.691  , -15.115   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 41.4   , 78.839  , -15.874   \n'
        'TT_8   , TT  , 8 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 43.306 , 76.933  , -17.295   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 39.197 , 75.042  , -14.848   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 37.951 , 76.288  , -15.115   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 40.609 , 73.63   , -15.864   \n'
        'TT_8   , TT  , 8 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 40.981 , 73.258  , -17.274   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.478 , 82.762  , -13.111   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 38.326 , 81.913  , -13.398   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 37.963 , 82.276  , -14.077   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 40.783 , 79.456  , -15.32    \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 35.852 , 78.387  , -13.098   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 35.488 , 78.751  , -13.392   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 36.688 , 77.551  , -14.074   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 39.534 , 74.705  , -15.312   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 35.787 , 84.452  , -12.07    \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 36.826 , 83.413  , -12.455   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 37.742 , 82.497  , -13.226   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 38.521 , 81.718  , -14.503   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 34.151 , 80.088  , -12.039   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 34.367 , 79.873  , -12.429   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 35.075 , 79.164  , -13.212   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 37.287 , 76.952  , -14.482   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 38.245 , 81.994  , -13.545   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 38.638 , 81.601  , -13.862   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 40.404 , 79.836  , -14.555   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.719 , 79.52   , -15.78    \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 36.536 , 77.703  , -13.556   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 36.763 , 77.476  , -13.869   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 37.73  , 76.509  , -14.558   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.156 , 74.083  , -15.782   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 36.025 , 84.214  , -12.106   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 37.506 , 82.734  , -12.479   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 37.157 , 83.082  , -13.248   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 37.601 , 82.638  , -14.528   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 35.472 , 78.767  , -12.072   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 34.652 , 79.587  , -12.44    \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 34.614 , 79.625  , -13.207   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 36.348 , 77.891  , -14.49    \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 39.743 , 80.496  , -13.772   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 39.291 , 80.948  , -14.113   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 40.649 , 79.591  , -14.875   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 41.41  , 78.83   , -16.199   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.622 , 76.617  , -13.763   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 37.703 , 76.536  , -14.103   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 38.42  , 75.82   , -14.87    \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 39.384 , 74.855  , -16.198   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 37.462 , 82.777  , -12.409   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 38.528 , 81.711  , -12.838   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 39.03  , 81.209  , -13.714   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 40.912 , 79.327  , -15.118   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 35.183 , 79.056  , -12.38    \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 35.334 , 78.905  , -12.81    \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 36.313 , 77.926  , -13.69    \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 38.111 , 76.128  , -15.101   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 39.124 , 81.115  , -14.238   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 41.099 , 79.14   , -14.618   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 40.758 , 79.481  , -15.434   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 42.071 , 78.168  , -16.786   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 37.921 , 76.318  , -14.234   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 38.912 , 75.327  , -14.62    \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 40.856 , 73.383  , -15.438   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 40.718 , 73.521  , -16.797   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 37.447 , 82.792  , -12.473   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 38.73  , 81.509  , -12.891   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 38.984 , 81.255  , -13.76    \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 40.978 , 79.261  , -15.163   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 35.117 , 79.122  , -12.452   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 36.124 , 78.115  , -12.862   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 37.271 , 76.968  , -13.726   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 38.83  , 75.409  , -15.131   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.878 , 82.361  , -13.474   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 39.08  , 81.159  , -13.793   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 38.878 , 81.361  , -14.5     \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 41.199 , 79.04   , -15.769   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 1           , 37.562 , 76.677  , -13.452   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 9           , 37.224 , 77.015  , -13.769   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 19          , 37.82  , 76.419  , -14.485   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX0_STX0  , 4G_FDD_Band01_DIV3, 29          , 38.942 , 75.298  , -15.76    \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 36.736 , 83.503  , -12.251   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 37.944 , 82.295  , -12.658   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 37.844 , 82.395  , -13.483   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 39.793 , 80.446  , -14.817   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 1           , 34.47  , 79.769  , -12.221   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 9           , 36.014 , 78.225  , -12.631   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 19          , 36.185 , 78.054  , -13.455   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 836.5 , TX0_STX0  , 4G_FDD_Band05_DIV6, 29          , 37.572 , 76.667  , -14.794   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 39.366 , 80.873  , -13.908   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 39.494 , 80.745  , -14.268   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 40.322 , 79.918  , -15.02    \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 42.45  , 77.789  , -16.294   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 1           , 37.464 , 76.775  , -13.881   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 9           , 37.67  , 76.57   , -14.238   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 19          , 39.705 , 74.534  , -14.988   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX0_STX0  , 4G_FDD_Band07_DIV2, 29          , 39.617 , 74.622  , -16.265   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 38.18  , 82.059  , -12.279   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 37.539 , 82.7    , -12.675   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 39.586 , 80.653  , -13.492   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 40.164 , 80.075  , -14.829   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 1           , 35.274 , 78.965  , -12.251   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 9           , 35.744 , 78.495  , -12.641   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 19          , 36.264 , 77.975  , -13.449   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX0_STX0  , 4G_FDD_Band08_DIV8, 29          , 37.599 , 76.64   , -14.79    \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 37.31  , 82.929  , -12.688   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 37.958 , 82.281  , -12.982   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 38.993 , 81.246  , -13.681   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 41.2   , 79.039  , -14.96    \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 35.528 , 78.712  , -12.684   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 36.091 , 78.148  , -12.977   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 35.315 , 78.925  , -13.676   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 37.487 , 76.752  , -14.951   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.407 , 81.832  , -13.176   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 38.495 , 81.744  , -13.496   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 38.219 , 82.02   , -14.209   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 39.221 , 81.019  , -15.454   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 36.531 , 77.709  , -13.174   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 37.001 , 77.238  , -13.507   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 37.89  , 76.349  , -14.219   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 38.802 , 75.437  , -15.459   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.972 , 83.267  , -11.582   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.952 , 84.287  , -11.974   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.57  , 82.669  , -12.793   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 38.074 , 82.165  , -14.143   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.644 , 79.596  , -11.55    \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.166 , 79.073  , -11.933   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 34.329 , 79.91   , -12.75    \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.02  , 78.219  , -14.106   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.137 , 85.102  , -11.592   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.248 , 82.991  , -11.982   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.283 , 82.956  , -12.8     \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 38.54  , 81.699  , -14.149   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 33.45  , 80.789  , -11.554   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 34.752 , 79.487  , -11.939   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 34.731 , 79.508  , -12.755   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.778 , 77.461  , -14.11    \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 39.496 , 80.743  , -14.361   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 40.153 , 80.086  , -14.613   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 41.093 , 79.146  , -15.349   \n'
        'TT_2   , TT  , 2 , -30 , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 41.407 , 78.832  , -16.735   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 38.77  , 75.469  , -14.38    \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 38.007 , 76.232  , -14.618   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 38.368 , 75.871  , -15.336   \n'
        'TT_2   , TT  , 2 , -30 , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 39.389 , 74.85   , -16.712   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 39.984 , 80.255  , -13.272   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 40.216 , 80.024  , -13.633   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 39.911 , 80.328  , -14.449   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 40.767 , 79.472  , -15.866   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 37.945 , 76.294  , -13.263   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 38.375 , 75.864  , -13.621   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 37.653 , 76.586  , -14.452   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 39.572 , 74.667  , -15.866   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.958 , 81.281  , -13.74    \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 39.707 , 80.532  , -14.142   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 41.482 , 78.757  , -15.007   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 41.585 , 78.654  , -16.43    \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 37.379 , 76.86   , -13.755   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 39.03  , 75.209  , -14.148   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 38.619 , 75.621  , -15.012   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 41.483 , 72.756  , -16.44    \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 37.126 , 83.113  , -11.921   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 38.322 , 81.917  , -12.365   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 39.315 , 80.924  , -13.311   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 40.285 , 79.954  , -14.817   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.436 , 78.803  , -11.912   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.569 , 78.67   , -12.344   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.172 , 77.067  , -13.277   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.521 , 74.718  , -14.782   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 37.8   , 82.439  , -11.927   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 38.969 , 81.27   , -12.371   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 38.414 , 81.826  , -13.315   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 40.382 , 79.857  , -14.817   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 34.913 , 79.326  , -11.906   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.933 , 78.306  , -12.341   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 36.88  , 77.359  , -13.278   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 37.441 , 76.798  , -14.782   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 40.535 , 79.705  , -15.172   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 41.398 , 78.841  , -15.488   \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 43.891 , 76.348  , -16.34    \n'
        'TT_2   , TT  , 2 , 85  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 44.233 , 76.006  , -17.833   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 40.773 , 73.466  , -15.188   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 41.303 , 72.937  , -15.496   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 41.382 , 72.857  , -16.323   \n'
        'TT_2   , TT  , 2 , 85  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 42.709 , 71.53   , -17.818   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 39.284 , 80.955  , -12.982   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 38.406 , 81.833  , -13.313   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 39.461 , 80.778  , -14.07    \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 40.493 , 79.746  , -15.397   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 1           , 36.042 , 78.197  , -12.968   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 9           , 37.298 , 76.942  , -13.299   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 19          , 36.728 , 77.511  , -14.052   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 1950.0, TX1_STX1  , 4G_FDD_Band01_DIV4, 29          , 38.145 , 76.094  , -15.385   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 39.357 , 80.882  , -13.44    \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 39.284 , 80.955  , -13.816   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 39.668 , 80.571  , -14.601   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 40.882 , 79.357  , -15.92    \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 1           , 38.119 , 76.12   , -13.449   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 9           , 36.448 , 77.791  , -13.823   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 19          , 38.029 , 76.21   , -14.603   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 2535.0, TX1_STX1  , 4G_FDD_Band07_DIV2, 29          , 39.911 , 74.328  , -15.923   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 36.619 , 83.62   , -11.753   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.82  , 82.419  , -12.167   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.267 , 82.972  , -13.04    \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 38.802 , 81.437  , -14.457   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 33.952 , 80.288  , -11.721   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 34.476 , 79.763  , -12.132   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 35.735 , 78.504  , -13.001   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.899 , 77.34   , -14.419   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.969 , 84.27   , -11.758   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 37.305 , 82.934  , -12.174   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 37.882 , 82.357  , -13.046   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 39.203 , 81.036  , -14.465   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 1           , 35.64  , 78.599  , -11.727   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 9           , 35.827 , 78.412  , -12.137   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 19          , 35.355 , 78.884  , -13.006   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 897.5 , TX1_STX1  , 4G_FDD_Band08_DIV8, 29          , 36.615 , 77.624  , -14.423   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 40.852 , 79.387  , -14.772   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 41.488 , 78.751  , -15.048   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 42.783 , 77.457  , -15.805   \n'
        'TT_2   , TT  , 2 , 25  , -12      , 4           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 42.394 , 77.845  , -17.217   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 1           , 39.509 , 74.73   , -14.788   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 9           , 39.159 , 75.08   , -15.055   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 19          , 40.015 , 74.224  , -15.801   \n'
        'TT_2   , TT  , 2 , 25  , -18      , 6           , 3625.0, TX1_SRX2_3, 4G_TDD_Band48_DIV2, 29          , 42.191 , 72.048  , -17.199     ').replace(' ', '')
    pd_data = pd.read_csv(StringIO(str_data))
    pvc = PyVarChart(
        label_spacing=[0.025, 0.06, 0.07, 0.28, 0.02, 0.025],  # [0.05, 0.1, 0.15, 0.1, 0.05],
        str_yaxis_var_name='nf_db',  #'SNR (dB)',  #'Pout (dBm)',
        lst_xaxis_var_names=['pin_dbm', 'tx0_pga_gain', 'freq', 'trx_and_sx', 'standard_and_band', 'offset_mhz'],  #['pin_dbm', 'tx0_pga_gain', 'Freq', 'TRX & SX', 'Standard & Band', 'Offset (MHz)']
        str_legend='temp',
        int_jitter_points=1,
        int_boxplots=1,
        int_show_points=1,
        int_marker_size=8,
        str_marker_theme='Solid',  # 'Default',
        str_color_theme='blue_to_green_to_red',
        str_title='Sample RF PyVarChart',
        int_continuous_scale=0,
        int_reverse_color_scheme=0,
        int_show_cell_means=1,
        lst_show_group_means=['tx0_pga_gain'],
        int_show_grand_mean=1,
        int_frame_size_x=17,
        int_frame_size_y=10,
        dict_xaxis_orderings={'freq': np.sort(pd_data['freq'].unique()).tolist()},
        lst_rotation=['Horizontal', 'Horizontal', 'Horizontal', 'Horizontal', 'Vertical', 'Horizontal'],
        lst_xaxis_font_size=[10, 10, 10, 10, 10, 10],
    )
    pvc.analyze(pd_data)
    fig, ax = pvc.plot(1)
    # fig.savefig('/tmp/pyvarchart_test.png', dpi=100, bbox_inches='tight')
    # print("Plot saved to /tmp/pyvarchart_test.png")
    # plt.show()
    # return pvc, fig, ax


if __name__ == '__main__':
    main_example()
    # complex_example()



