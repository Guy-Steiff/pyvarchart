from pyvarchart import PyVarChart
import matplotlib.pyplot as plt

def run_pyvarchart(config, df, output_path):
    chart = PyVarChart(
        label_spacing=config.get('label_spacing', 0.05),
        str_yaxis_var_name=config['str_yaxis_var_name'],
        lst_xaxis_var_names=config['lst_xaxis_var_names'],
        str_legend=config.get('str_legend', None),
        b_jitter_points=config.get('b_jitter_points', False),
        int_boxplots=config.get('int_boxplots', 0),
        int_show_points=1,  # as per your note, this is default and unimplemented
        int_marker_size=config.get('int_marker_size', 8),
        str_marker_theme=config.get('str_marker_theme', 'Default'),
        str_color_theme=config.get('str_color_theme', 'pvc light'),
        int_show_cell_means=config.get('int_show_cell_means', 1),
        lst_show_group_means=config.get('lst_show_group_means', []),
        int_show_grand_mean=config.get('int_show_grand_mean', 1),
        int_frame_size_x=config.get('int_frame_size_x', 8),
        int_frame_size_y=config.get('int_frame_size_y', 6),
        str_title=config.get('str_title', None),
        dict_xaxis_orderings=config.get('dict_xaxis_orderings', None),
        lst_rotation=config.get('lst_rotation', None),
        lst_xaxis_font_size=config.get('lst_xaxis_font_size', None)
    )

    fig, ax = chart.analyze(df)
    fig.savefig(output_path, bbox_inches='tight')
    plt.close(fig)
