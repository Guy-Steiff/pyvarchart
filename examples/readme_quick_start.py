#!/usr/bin/env python3
"""README Quick Start Example"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
plt.switch_backend('agg')

from pyvarchart import PyVarChart
import pandas as pd
from io import StringIO


def main():
    """Generate quick start example figure."""
    # Sample data from README quick start
    str_data = (
        'measurement, chip, channel, condition\n'
        '10, 0, A, X\n'
        '15, 0, A, Y\n'
        '20, 0, A, X\n'
        '12, 1, B, Y\n'
        '18, 1, B, X\n'
        '22, 1, B, Y\n'
    ).replace(' ', '')

    df = pd.read_csv(StringIO(str_data))

    # Create chart exactly as shown in quick start
    pvc = PyVarChart(
        str_yaxis_var_name='measurement',
        lst_xaxis_var_names=['chip', 'channel'],
        str_legend='condition',
        int_show_cell_means=1,
        int_frame_size_x=8,
        int_frame_size_y=6,
        str_title='Quick Start Example'
    )

    # Analyze and plot
    pvc.analyze(df)
    fig, ax = pvc.plot(1)

    # Save
    fig.savefig('readme_quick_start.png', dpi=100, bbox_inches='tight')
    plt.close(1)
    print("✓ Quick Start Example saved to readme_quick_start.png")


if __name__ == '__main__':
    main()

