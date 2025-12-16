import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby, cycle
import matplotlib.colors as mcolors
import matplotlib as mpl
from io import StringIO
import os

def legend_label(val):
    return "Unlabeled" if val is None else str(val)

# Estimate bottom margin based on rotation and number of characters
def estimate_bottom_margin(num_levels, lst_rotations, vertical_base=0.12, horizontal_base=0.05, base_margin=0.13, max_margin=0.35):
    margin = base_margin
    # margin = 0.15  # base margin for plot aesthetics
    for i in range(num_levels):
        if i < len(lst_rotations):
            if lst_rotations[i].lower() == 'vertical':
                margin += vertical_base
            else:
                margin += horizontal_base
        else:
            margin += horizontal_base  # default to horizontal if not specified
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

def label_group_bar_table(ax, df, lst_rotation_labels, spacing=0.15, lst_fontsize=None):
    ypos = -spacing
    scale = 1. / df.index.size
    num_levels = df.index.nlevels
    index_level_names = df.index.names  # ← These are your grouping variable names

    for level in range(num_levels)[::-1]:
        pos = 0
        rotate = lst_rotation_labels[level].lower() == 'vertical' if level < len(lst_rotation_labels) else False

        # ⬅️ Draw the group level title on the left
        if index_level_names and level < len(index_level_names):
            ax.text(-0.01, ypos, index_level_names[level],
                    ha='right', va='center',
                    transform=ax.transAxes,
                    fontsize='small', fontweight='bold')

        for label, rpos in label_len(df.index, level):
            lxpos = (pos + .5 * rpos) * scale
            # ax.text(
            #     lxpos, ypos, label,
            #     ha='center',
            #     va='top' if rotate else 'center',
            #     rotation=90 if rotate else 0,
            #     transform=ax.transAxes
            # )
            # fontsize = lst_fontsize[level] if lst_fontsize and level < len(lst_fontsize) else None
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
            add_line(ax, pos * scale, ypos, spacing)
            pos += rpos

        add_line(ax, pos * scale, ypos, spacing)
        ypos -= spacing

# Normalize float grouping variables to int if whole number
def normalize_grouping_value(val):
    if isinstance(val, float) and val.is_integer():
        return int(val)
    return val

class PyVarChart:
    '''
    arguments:
        1) label_spacing, can be set to be "0.05" as defualt.
        2) str_yaxis_var_name, the variable name to be plotted with the later introduced function "analyze", must exist as a title in the analyze's input "pd_data", also must not exist in the input "lst_xaxis_var_names"
        3) lst_xaxis_var_names, the variable names where "str_yaxis_var_name" is broken down accross, with the later introduced function "analyze", all members must exist as a title in the analyze's input "pd_data", also must not exist in the input "str_yaxis_var_name"
        4) str_legend, default: None, will serve as a coloring classifier based on any title over analyze's pd_data, must be a column's title of pd_data.
        5) b_jitter_points, possible values: True or False, will cause points to artifically jitter horizontally so that the observer can get a sense of how many points are present at the same x/y location.
        6) int_boxplots, possible values 1 or 0, prints in addition to the points, boxplots based on their statistics.
        7) int_show_points, possible values 1 or 0, 1 for the points to be shown, 0 for omitting them (if only boxplots or averages are desired visually). can be default 1 (not implemented yet, can be ignored)
        8) int_marker_size, all integers are allowed, get be default 8. 
        9) str_marker_theme, theme of markers, currently supports "Default" (which should be the default value) and "Solid".
        10) str_color_theme, color theme of markers, currently supports 'pvc light' (which should be the default value) and "blue to green to red".
        11) int_continuous_scale, (not implemented yet, can be ignored)
        12) int_reverse_scale, (not implemented yet, can be ignored)
        13) int_show_range_bars, (not implemented yet, can be ignored)
        14) int_show_cell_means, 1 or 0, should be 1 by default, prints cell means in addition to the points.
        15) lst_show_group_means, can default to [], must be a list of 0 or more titles appearing as column titles in pd_data, prints a mean over the grouping variable desired.
        16) int_show_grand_mean, 1 or 0, should be 1 by default, prints a grand mean overall.
        17) int_frame_size_x, can be any integer, default to 8, the x width of the printed figure.
        18) int_frame_size_y, can be any integer, default to 6, the 6 width of the printed figure.
        19) f_hline_value, (not implemented yet, can be ignored set to None)
        20) lst_hlines, (not implemented yet, can be ignored set to None)
        21) lst_axis_control, set to None, not required.
        22) str_title, default: None, can be text, will serve as the title of the figure.
        21) dict_xaxis_orderings, default: None, a dictionary like {'cmp': [4, 3, 2, 1, 0]} or {'skew': ['FF2_FF', 'TT_TT', 'SS2_SS']}, can be used to change the print ordering of xaxis grouping variables, can be done to multiple grouping variables, keys must be titles of pd_data, the values should be values which exist under said title in the same column of pd_data. 
        22) lst_rotation, default None, otherwise, a list of values "Horizontal" or "Vertical", causing the grouping variables of lst_xaxis_var_names to rotate 90deg in the figure, generally should be a list of the same length of lst_xaxis_var_names.
        23) lst_xaxis_font_size, default None, otherwise, a list of integers determining the font size of each of the grouping variables of lst_xaxis_var_names, generally should be a list of the same length of lst_xaxis_var_names.
    '''
    def __init__(self,
                 label_spacing=0.15,
                 str_yaxis_var_name='clock_shift_rise_after_fall_cycle_fixed',
                 lst_xaxis_var_names=['ClockUnderTest', 'ProcessSkew', 'LO_Freq_MHz'],
                 str_legend=None,
                 b_jitter_points=False,  # Not implemented, placeholder
                 int_boxplots=1,         # Not implemented, placeholder
                 int_show_points=1,      # Not implemented, placeholder
                 int_marker_size=8,
                 str_marker_theme='Default',
                 str_color_theme='PVC Light',
                 int_continuous_scale=0,  # Not implemented, placeholder
                 int_reverse_scale=0,     # Not implemented, placeholder
                 int_show_range_bars=0,   # Not implemented, placeholder
                 int_show_cell_means=0,   # Not implemented, placeholder
                 lst_show_group_means=[], # Not implemented, placeholder
                 int_show_grand_mean=0,   # Not implemented, placeholder
                 int_frame_size_x=20,
                 int_frame_size_y=6,
                 f_hline_value=None,      # Not implemented, placeholder
                 lst_hlines=None,         # Not implemented, placeholder
                 lst_axis_control=None,   # Not implemented, placeholder
                 str_title=None,
                 dict_xaxis_orderings=None,
                 lst_rotation=None,
                 lst_xaxis_font_size=None):
        self.label_spacing = label_spacing
        self.str_yaxis_var_name = str_yaxis_var_name
        self.lst_xaxis_var_names = lst_xaxis_var_names
        self.str_legend = str_legend
        self.b_jitter_points = b_jitter_points
        self.int_boxplots = int_boxplots
        self.int_show_points = int_show_points
        self.int_marker_size = int_marker_size
        self.str_marker_theme = str_marker_theme
        self.str_color_theme = str_color_theme
        self.int_continuous_scale = int_continuous_scale
        self.int_reverse_scale = int_reverse_scale
        self.int_show_range_bars = int_show_range_bars
        self.int_show_cell_means = int_show_cell_means
        self.lst_show_group_means = lst_show_group_means
        self.int_show_grand_mean = int_show_grand_mean
        self.int_frame_size_x = int_frame_size_x
        self.int_frame_size_y = int_frame_size_y
        self.f_hline_value = f_hline_value
        self.lst_hlines = lst_hlines
        self.lst_axis_control = lst_axis_control
        self.str_title = str_title
        self.dict_xaxis_orderings = dict_xaxis_orderings
        self.lst_rotation = lst_rotation
        self.lst_xaxis_font_size = lst_xaxis_font_size if lst_xaxis_font_size is not None else []

    def _get_marker_dict(self, values):
        theme = self.str_marker_theme.lower()
        if theme == 'default':
            return {val: 'o' for val in values}
        elif theme == 'solid':
            shapes = ['s', '^', 'D', 'v', '<', '>', 'p', '*', 'X', 'H']
        else:
            shapes = ['o', 's', '^', 'D', 'v', 'P', '*', '<', '>', 'X']
        return {val: shape for val, shape in zip(values, cycle(shapes))}

    def analyze(self, int_fig_num, pd_data: pd.DataFrame) -> plt.Axes:
        label_spacing = self.label_spacing
        str_yaxis_var_name = self.str_yaxis_var_name
        lst_xaxis_var_names = self.lst_xaxis_var_names
        str_legend = self.str_legend
        b_jitter_points = self.b_jitter_points
        int_boxplots = self.int_boxplots
        int_show_points = self.int_show_points
        int_marker_size = self.int_marker_size
        str_marker_theme = self.str_marker_theme
        str_color_theme = self.str_color_theme
        int_continuous_scale = self.int_continuous_scale
        int_reverse_scale = self.int_reverse_scale
        int_show_range_bars = self.int_show_range_bars
        int_show_cell_means = self.int_show_cell_means
        lst_show_group_means = self.lst_show_group_means
        int_show_grand_mean = self.int_show_grand_mean
        int_frame_size_x = self.int_frame_size_x
        int_frame_size_y = self.int_frame_size_y
        f_hline_value = self.f_hline_value
        lst_hlines = self.lst_hlines
        lst_axis_control = self.lst_axis_control
        str_title = self.str_title
        dict_xaxis_orderings = self.dict_xaxis_orderings
        lst_rotation = self.lst_rotation
        lst_xaxis_font_size = self.lst_xaxis_font_size

        if lst_rotation is None:
            lst_rotation = ['Vertical'] * len(lst_xaxis_var_names)

        for col in lst_xaxis_var_names:
            # Normalize float grouping variables to int if whole number
            if pd.api.types.is_float_dtype(pd_data[col]):
                with pd.option_context('mode.chained_assignment', None):
                    pd_data[col] = pd_data[col].apply(normalize_grouping_value)
                # for index, row in pd_data.iterrows():
                #     pd_data.at[index, col] = normalize_grouping_value(row[col])

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

        # Apply custom order if specified
        # if dict_xaxis_orderings:
        #     for var in lst_grouping_vars:
        #         if var in dict_xaxis_orderings:
        #             categories = pd.CategoricalDtype(categories=dict_xaxis_orderings[var], ordered=True)
        #             pd_unique_combos[var] = pd_unique_combos[var].astype(categories)

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

            # Build color dict and marker dict keyed by normalized values:
            # cmap = mcolors.LinearSegmentedColormap.from_list('BlueGreenRed', ['blue', 'green', 'red'])
            if str_color_theme.lower() == 'blue to green to red':
                cmap = mcolors.LinearSegmentedColormap.from_list('custom', ['blue', 'green', 'red'])
            elif str_color_theme.lower() == 'pvc light':
                cmap = plt.cm.Pastel1
            else:
                cmap = plt.cm.tab10
            n_colors = len(normalized_legend_values)
            colors = [cmap(i / (n_colors - 1 if n_colors > 1 else 1)) for i in range(n_colors)]
            color_dict = dict(zip(normalized_legend_values, colors))
            marker_dict = self._get_marker_dict(normalized_legend_values)
        else:
            color_dict = {}
            marker_dict = {}
            normalized_legend_values = [None]


        # # Setup marker style mapping based on str_marker_theme
        # if str_legend:
        #     legend_values_in_plot = sorted(pd_data[str_legend].dropna().unique())
        # else:
        #     legend_values_in_plot = [None]

        fig = plt.figure(int_fig_num, figsize=(int_frame_size_x, int_frame_size_y))
        ax = plt.gca()

        # Build mapping from unique group index -> x-position
        unique_index_order = list(dict.fromkeys(pd_plot.index.to_list()))  # preserve order
        index_to_xpos = {idx: i for i, idx in enumerate(unique_index_order)}

        # for (idx_val, y_val), legend_val in zip(pd_plot.items(), pd_plot_legend_vals):
        #     x_base = index_to_xpos[idx_val]
        #     x_pos = x_base + np.random.uniform(-0.2, 0.2) if b_jitter_points else x_base
        #
        #     if str_legend:
        #         norm_val = normalize_grouping_value(legend_val)
        #         color = color_dict.get(norm_val, 'blue')
        #         marker = marker_dict.get(norm_val, 'o')
        #     else:
        #         color = 'blue'
        #         marker = 'o'
        #
        #     ax.plot(x_pos, y_val, marker=marker, color=color, linestyle='none', markersize=int_marker_size)
        # BOX DATA for optional boxplot
        if int_boxplots in [1, 2]:
            grouped = pd_data.groupby(lst_xaxis_var_names)[str_yaxis_var_name]
            box_data = [grouped.get_group(idx).dropna().values for idx in unique_index_order if idx in grouped.groups]
            ax.boxplot(box_data, positions=range(len(box_data)), widths=0.5, patch_artist=True,
                       boxprops=dict(facecolor='lightgray', color='black'),
                       medianprops=dict(color='black'),
                       whiskerprops=dict(color='black'),
                       capprops=dict(color='black'),
                       flierprops=dict(marker='o', markersize=4, linestyle='none', markerfacecolor='gray'))

        if int_show_cell_means:
            cell_means = pd_plot.groupby(level=list(range(pd_plot.index.nlevels))).mean()
            for idx, mean_val in cell_means.items():
                xpos = index_to_xpos.get(idx, None)
                if xpos is not None:
                    ax.hlines(mean_val, xpos - 0.2, xpos + 0.2, colors='black', linewidth=1.5, linestyles='-')

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
                        min_pos, max_pos = min(matching_positions), max(matching_positions)
                        ax.hlines(mean_val, min_pos - 0.3, max_pos + 0.3, colors='blue', linewidth=1.2, linestyles='--')

        # POINTS
        if int_boxplots in [0, 1]:
            for (idx_val, y_val), legend_val in zip(pd_plot.items(), pd_plot_legend_vals):
                x_base = index_to_xpos[idx_val]
                x_pos = x_base + np.random.uniform(-0.2, 0.2) if b_jitter_points else x_base

                if str_legend:
                    norm_val = normalize_grouping_value(legend_val)
                    color = color_dict.get(norm_val, 'blue')
                    marker = marker_dict.get(norm_val, 'o')
                else:
                    color = 'blue'
                    marker = 'o'

                ax.plot(x_pos, y_val, marker=marker, color=color, linestyle='none', markersize=int_marker_size)

        # Annotate grouped x-axis with rotation if too many groups
        ax.set_xticks(range(len(unique_index_order)))
        ax.set_xticklabels('')
        ax.set_xlabel('')

        # if lst_rotation is None:
        #     lst_rotation = ['Vertical'] * len(lst_xaxis_var_names)

        unique_index = pd.MultiIndex.from_tuples(unique_index_order, names=lst_xaxis_var_names)
        # label_group_bar_table(ax, pd.Series(index=unique_index), lst_rotation, spacing=label_spacing)
        # label_group_bar_table(ax, pd.Series(index=unique_index, dtype='object'), lst_rotation, spacing=label_spacing)
        label_group_bar_table(ax,
                              pd.Series(index=unique_index, dtype='object'),
                              lst_rotation,
                              spacing=label_spacing,
                              lst_fontsize=lst_xaxis_font_size)

        ax.set_xlim(-0.5, len(unique_index_order) - 0.5)
        ax.set_ylim(pd_data[str_yaxis_var_name].min() * 0.99,
                    pd_data[str_yaxis_var_name].max() * 1.005)

        ax.set_ylabel(str_yaxis_var_name)
        plt.title(str_title if str_title else 'Variability Chart')
        plt.grid(True)

        # if str_legend:
        #     for val in normalized_legend_values:
        #         ax.plot([], [], marker=marker_dict[val], color=color_dict.get(val, 'blue'),
        #                 linestyle='none', label=str(val), markersize=int_marker_size)
        #     #ax.legend(title=str_legend)
        #     ax.legend(title=str_legend, labels=[legend_label(v) for v in normalized_legend_values])

        if str_legend:
            handles = []
            labels = []
            for val in normalized_legend_values:
                h, = ax.plot([], [], marker=marker_dict[val], color=color_dict.get(val, 'blue'),
                             linestyle='none', markersize=int_marker_size)
                handles.append(h)
                labels.append(legend_label(val))
            ax.legend(handles=handles, labels=labels, title=str_legend)


        # Increase bottom margin to fit multi-level x-axis labels
        plt.tight_layout()
        # bottom_margin = estimate_bottom_margin(len(lst_xaxis_var_names), lst_rotation, vertical_base=0.18, max_margin=0.5)
        bottom_margin = estimate_bottom_margin(len(lst_xaxis_var_names), lst_rotation)
        # plt.subplots_adjust(bottom=bottom_margin-0.13)
        plt.subplots_adjust(bottom=bottom_margin)

        return fig, ax


def main_example():
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

    pvc = PyVarChart(label_spacing=0.05,
                     str_yaxis_var_name='trim_read',
                     lst_xaxis_var_names=['chip', 'channel', 'lane', 'core', 'cmp'],
                     str_legend='lane',  #'skew_sn',  #   ,
                     b_jitter_points=True,
                     int_marker_size=7,
                     str_marker_theme='Default',  # 'Solid',
                     str_color_theme='Blue to Green to Red',
                     str_title='trim_read Variability Across Configs',
                     int_frame_size_x=8,
                     int_frame_size_y=6,
                     dict_xaxis_orderings={'cmp': [4, 3, 2, 1, 0]},  # None,  # {'skew': ['FF2_FF', 'TT_TT', 'SS2_SS']},
                     lst_rotation=['Horizontal', 'Horizontal', 'Horizontal', 'Horizontal', 'Horizontal'],
                     lst_xaxis_font_size=[10, 10, 10, 10, 10],
                     )
    int_fig_num = 1
    fig, ax = pvc.analyze(int_fig_num, pd_data)
    ax.set_ylim(0, 255)
    # Increase bottom margin to fit multi-level x-axis labels
    plt.tight_layout()
    plt.tight_layout()
    
if __name__ == '__main__':
    # pd_data = pd.concat([pd_data1, pd_data2, pd_data3], ignore_index=True)
    # 
    #     pvc = PyVarChart(label_spacing=0.08,
    #                      str_yaxis_var_name='ENOB_SNDR_FS',
    #                      lst_xaxis_var_names=['skew', 'sn', 'channel', 'lane', 'f_sampling_rate_MHz', 'sar_config_string', 'cal_config'],
    #                      str_legend='temp_oven_degc',  # 'skew_sn',  #   ,
    #                      b_jitter_points=True,
    #                      int_marker_size=7,
    #                      str_marker_theme='Default',  # 'Solid',
    #                      str_color_theme='Blue to Green to Red',
    #                      str_title='trim_read Variability Across Configs',
    #                      int_frame_size_x=8,
    #                      int_frame_size_y=9,
    #                      dict_xaxis_orderings={'cal_config': ['allperms', '25degc', 'alltemps']},  #{'cmp': [4, 3, 2, 1, 0]},  # None,  # {'skew': ['FF2_FF', 'TT_TT', 'SS2_SS']},
    #                      lst_rotation=['Horizontal', 'Horizontal', 'Horizontal', 'Horizontal', 'Horizontal', 'Horizontal', 'vertical'],
    #                      lst_xaxis_font_size=[10, 10, 10, 10, 10, 10, 6],
    #                      int_boxplots=1,
    #                      int_show_cell_means=1,
    #                      int_show_grand_mean=0,
    #                      lst_show_group_means=['f_sampling_rate_MHz']
    #                      )
    #     # pvc.int_boxplots = 0
    #     fig, ax = pvc.analyze(1, pd_data)
	main_example()