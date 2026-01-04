#!/usr/bin/env python3
"""README Example 2: Continuous Scale for Power Measurements"""

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
    """Generate continuous scale legend example."""
    # Create sample power measurement data
    str_data = (
        'frequency, temperature, gain_setting, input_power_dbm, output_power_dbm\n'
        '1900, -40, Low, -20, 5.2\n'
        '1900, -40, Low, -15, 7.8\n'
        '1900, -40, Low, -10, 10.5\n'
        '1900, -40, Low, -5, 13.2\n'
        '1900, -40, Low, 0, 15.8\n'
        '1900, -40, Mid, -20, 8.3\n'
        '1900, -40, Mid, -15, 10.9\n'
        '1900, -40, Mid, -10, 13.6\n'
        '1900, -40, Mid, -5, 16.2\n'
        '1900, -40, Mid, 0, 18.9\n'
        '1900, 25, Low, -20, 5.5\n'
        '1900, 25, Low, -15, 8.1\n'
        '1900, 25, Low, -10, 10.8\n'
        '1900, 25, Low, -5, 13.4\n'
        '1900, 25, Low, 0, 16.1\n'
        '1900, 25, Mid, -20, 8.6\n'
        '1900, 25, Mid, -15, 11.2\n'
        '1900, 25, Mid, -10, 13.9\n'
        '1900, 25, Mid, -5, 16.5\n'
        '1900, 25, Mid, 0, 19.2\n'
        '2400, -40, Low, -20, 4.9\n'
        '2400, -40, Low, -15, 7.5\n'
        '2400, -40, Low, -10, 10.2\n'
        '2400, -40, Low, -5, 12.9\n'
        '2400, -40, Low, 0, 15.5\n'
        '2400, 25, Low, -20, 5.2\n'
        '2400, 25, Low, -15, 7.8\n'
        '2400, 25, Low, -10, 10.5\n'
        '2400, 25, Low, -5, 13.1\n'
        '2400, 25, Low, 0, 15.8\n'
    ).replace(' ', '')

    df = pd.read_csv(StringIO(str_data))

    pvc = PyVarChart(
        str_yaxis_var_name='output_power_dbm',
        lst_xaxis_var_names=['frequency', 'temperature', 'gain_setting'],
        str_legend='input_power_dbm',

        # Enable continuous scale for legend
        int_continuous_scale=1,  # Quantizes legend to 5-6 values
        str_color_theme='plasma',  # Sequential colormap
        int_reverse_color_scheme=0,

        int_boxplots=0,  # Hide boxplots
        int_show_points=1,
        int_show_cell_means=1,
        int_jitter_points=1,
        int_marker_size=10,

        int_frame_size_x=12,
        int_frame_size_y=7,

        str_title='Example 2: Continuous Scale - Power Output vs Input Power'
    )

    pvc.analyze(df)
    fig, ax = pvc.plot(1)

    # Save
    fig.savefig('readme_example_2_continuous_scale.png', dpi=100, bbox_inches='tight')
    plt.close(1)
    print("✓ Example 2 (Continuous Scale) saved to readme_example_2_continuous_scale.png")


if __name__ == '__main__':
    main()

