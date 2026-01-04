#!/usr/bin/env python3
"""README Example 1: RF Testing with All Features"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
plt.switch_backend('agg')

from pyvarchart import PyVarChart
import pandas as pd
import numpy as np
from io import StringIO


def main():
    """Generate RF testing example with all features enabled."""
    # Create sample RF test data (simplified version of complex_example)
    str_data = (
        'pin_dbm, tx0_pga_gain, freq, trx_and_sx, standard_and_band, offset_mhz, temp, nf_db\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 1, -30, 12.5\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 9, -30, 12.8\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 19, -30, 13.2\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 29, -30, 14.1\n'
        '-12, 6, 1950.0, TX0_STX0, 4G_FDD_Band01, 1, -30, 11.9\n'
        '-12, 6, 1950.0, TX0_STX0, 4G_FDD_Band01, 9, -30, 12.2\n'
        '-12, 6, 1950.0, TX0_STX0, 4G_FDD_Band01, 19, -30, 12.7\n'
        '-12, 6, 1950.0, TX0_STX0, 4G_FDD_Band01, 29, -30, 13.5\n'
        '-12, 4, 836.5, TX0_STX0, 4G_FDD_Band05, 1, -30, 11.8\n'
        '-12, 4, 836.5, TX0_STX0, 4G_FDD_Band05, 9, -30, 12.1\n'
        '-12, 4, 836.5, TX0_STX0, 4G_FDD_Band05, 19, -30, 12.6\n'
        '-12, 4, 836.5, TX0_STX0, 4G_FDD_Band05, 29, -30, 13.4\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 1, 25, 13.0\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 9, 25, 13.3\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 19, 25, 13.7\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 29, 25, 14.6\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 1, 85, 13.8\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 9, 85, 14.1\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 19, 85, 14.9\n'
        '-12, 4, 1950.0, TX0_STX0, 4G_FDD_Band01, 29, 85, 16.2\n'
    ).replace(' ', '')

    df = pd.read_csv(StringIO(str_data))

    pvc = PyVarChart(
        # Core configuration
        str_yaxis_var_name='nf_db',
        lst_xaxis_var_names=['pin_dbm', 'tx0_pga_gain', 'freq',
                             'standard_and_band', 'offset_mhz'],
        str_legend='temp',

        # Visual customization
        str_color_theme='blue_to_green_to_red',
        str_marker_theme='Solid',
        int_marker_size=8,
        int_jitter_points=1,

        # Statistical overlays
        int_boxplots=1,
        int_show_points=1,
        int_show_cell_means=1,
        lst_show_group_means=['tx0_pga_gain'],
        int_show_grand_mean=1,

        # Layout
        int_frame_size_x=16,
        int_frame_size_y=8,
        label_spacing=[0.06, 0.06, 0.28, 0.06, 0.03],
        lst_rotation=['Horizontal', 'Horizontal', 'Horizontal', 'Vertical', 'Horizontal'],

        # Custom ordering
        dict_xaxis_orderings={
            'temp': [-30, 25, 85]
        },

        str_title='Example 1: RF Noise Figure Variability Analysis'
    )

    # Analyze and plot
    pvc.analyze(df)
    fig, ax = pvc.plot(1)

    # Save
    output_path = '/media/gnew/Mech/Projects/pyvarchart/examples/readme_example_1_rf_testing.png'
    fig.savefig(output_path, dpi=100, bbox_inches='tight')
    plt.close(1)
    print(f"✓ Example 1 (RF Testing with All Features) saved to {output_path}")


if __name__ == '__main__':
    main()

