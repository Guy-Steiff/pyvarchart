"""
PyVarChart - A Python library for creating distribution charts with hierarchical grouping.

This module provides tools for visualizing data distribution across multiple categorical
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
__version__ = '1.0.0'


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
    """A distribution chart creator for visualizing data across multiple categorical factors.
       Allowing breaking down data by different variables to better characterize its nature.

    This class creates sophisticated distribution charts with hierarchical x-axis grouping,
    customizable markers, colors, statistical overlays (means, boxplots), and legend support.

    The chart displays data points across multiple categorical grouping levels with:
    - Hierarchical x-axis labels (e.g., chip → channel → lane → core → cmp)
    - Color-coded legend for categorical differentiation
    - Optional boxplots, cell means, group means, and grand mean overlays
    - Custom ordering of x-axis categories
    - Jittering for overlapping points visualization (jittering results in randomized horizontal positions, such that
      subsequent calls result in slightly different graphs, however, the data is the same)

    Example Output Structure::

        trim_read distribution Across Configs        Legend: lane
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
            Generates a distribution chart from the provided DataFrame.
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
            Create the matplotlib figure and axes for the distribution chart.
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
                 str_yaxis_var_name: str,  # Required - column name for Y-axis
                 lst_xaxis_var_names: List[str],  # Required - list of grouping columns
                 label_spacing: Union[float, List[float]] = 0.15,
                 str_legend: Optional[str] = None,
                 int_jitter_points: int = 1,
                 int_boxplots: int = 1,
                 int_show_points: int = 1,
                 int_marker_size: int = 8,
                 str_marker_theme: str = 'Default',
                 str_color_theme: str = 'blue_to_green_to_red',
                 int_continuous_scale: int = 1,
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
        """Generate a distribution chart from the provided DataFrame.

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
        # Validate required parameters (defensive programming)
        if not self.str_yaxis_var_name:
            raise ValueError("str_yaxis_var_name is required and cannot be empty.")
        if not self.lst_xaxis_var_names or len(self.lst_xaxis_var_names) == 0:
            raise ValueError("lst_xaxis_var_names is required and must contain at least one column name.")

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
            use_continuous_scale = False

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
        """Plot the distribution chart using data from previous analyze() call.

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
        # require applying analysis before changing:
        str_yaxis_var_name = self.str_yaxis_var_name
        lst_xaxis_var_names = self.lst_xaxis_var_names
        str_legend = self.str_legend
        lst_show_group_means = self.lst_show_group_means

        # reapplying analysis isn't required for the following variables:
        label_spacing = self.label_spacing
        int_jitter_points = self.int_jitter_points
        int_boxplots = self.int_boxplots
        int_show_points = self.int_show_points
        int_marker_size = self.int_marker_size
        str_color_theme = self.str_color_theme
        int_reverse_color_scheme = self.int_reverse_color_scheme
        int_show_cell_means = self.int_show_cell_means
        int_show_grand_mean = self.int_show_grand_mean
        int_frame_size_x = self.int_frame_size_x
        int_frame_size_y = self.int_frame_size_y
        str_title = self.str_title
        lst_rotation = self.lst_rotation
        lst_xaxis_font_size = self.lst_xaxis_font_size

        # aren't required for plotting (only for analysis):
        # str_marker_theme = self.str_marker_theme
        # int_continuous_scale = self.int_continuous_scale
        # dict_xaxis_orderings = self.dict_xaxis_orderings

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
        # set limits at 1% above the absolute max and below the absolute min
        ax.set_ylim(f_ylim_min * 0.99 if f_ylim_min > 0 else f_ylim_min * 1.01,
                    f_ylim_max * 1.01 if f_ylim_max > 0 else f_ylim_max * 0.99)

        ax.set_ylabel(str_yaxis_var_name)
        plt.title(str_title if str_title else 'distribution chart')
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

    This example creates a distribution chart showing 'trim_read' values across
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
        str_yaxis_var_name='trim_read',
        lst_xaxis_var_names=['chip', 'channel', 'lane', 'core', 'cmp'],
        label_spacing=0.15,  # [0.05, 0.1, 0.15, 0.1, 0.05],
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
        str_title='trim_read distribution Across Configs',
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


if __name__ == '__main__':
    main_example()
