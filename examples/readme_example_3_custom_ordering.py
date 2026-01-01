#!/usr/bin/env python3
"""README Example 3: Minimal Chart with Custom Ordering"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
# plt.switch_backend('agg')  # Non-interactive backend

from pyvarchart import PyVarChart
import pandas as pd
import numpy as np
from io import StringIO


def main():
    """Generate minimal chart with custom ordering example."""
    # Create sample production yield data
    str_data = (
        'production_line, shift, date, operator, yield_percent\n'
        'Line_A, Day, 2026-01-01, OpA, 95.2\n'
        'Line_A, Day, 2026-01-01, OpB, 94.8\n'
        'Line_A, Day, 2026-01-01, OpA, 96.1\n'
        'Line_A, Evening, 2026-01-01, OpA, 92.3\n'
        'Line_A, Evening, 2026-01-01, OpB, 93.1\n'
        'Line_A, Evening, 2026-01-01, OpA, 91.8\n'
        'Line_A, Night, 2026-01-01, OpA, 88.5\n'
        'Line_A, Night, 2026-01-01, OpB, 89.2\n'
        'Line_A, Night, 2026-01-01, OpA, 87.9\n'
        'Line_B, Day, 2026-01-01, OpA, 97.1\n'
        'Line_B, Day, 2026-01-01, OpB, 96.8\n'
        'Line_B, Day, 2026-01-01, OpA, 97.5\n'
        'Line_B, Evening, 2026-01-01, OpA, 94.2\n'
        'Line_B, Evening, 2026-01-01, OpB, 95.0\n'
        'Line_B, Evening, 2026-01-01, OpA, 93.8\n'
        'Line_B, Night, 2026-01-01, OpA, 91.3\n'
        'Line_B, Night, 2026-01-01, OpB, 90.8\n'
        'Line_B, Night, 2026-01-01, OpA, 92.1\n'
        'Line_C, Day, 2026-01-01, OpA, 89.2\n'
        'Line_C, Day, 2026-01-01, OpB, 88.5\n'
        'Line_C, Day, 2026-01-01, OpA, 90.1\n'
        'Line_C, Evening, 2026-01-01, OpA, 85.3\n'
        'Line_C, Evening, 2026-01-01, OpB, 86.2\n'
        'Line_C, Evening, 2026-01-01, OpA, 84.8\n'
        'Line_C, Night, 2026-01-01, OpA, 81.5\n'
        'Line_C, Night, 2026-01-01, OpB, 82.3\n'
        'Line_C, Night, 2026-01-01, OpA, 80.9\n'
        'Line_A, Day, 2026-01-02, OpA, 94.9\n'
        'Line_A, Evening, 2026-01-02, OpA, 92.7\n'
        'Line_A, Night, 2026-01-02, OpA, 88.8\n'
        'Line_B, Day, 2026-01-02, OpB, 97.3\n'
        'Line_B, Evening, 2026-01-02, OpA, 94.5\n'
        'Line_B, Night, 2026-01-02, OpB, 91.0\n'
        'Line_C, Day, 2026-01-02, OpA, 89.5\n'
        'Line_C, Evening, 2026-01-02, OpB, 85.7\n'
        'Line_C, Night, 2026-01-02, OpA, 81.8\n'
    ).replace(' ', '')

    df = pd.read_csv(StringIO(str_data))

    pvc = PyVarChart(
        str_yaxis_var_name='yield_percent',
        lst_xaxis_var_names=['production_line', 'shift', 'date'],
        str_legend='operator',  # Add legend to avoid bug

        # Custom order: prioritize problem areas
        dict_xaxis_orderings={
            'production_line': ['Line_C', 'Line_A', 'Line_B'],  # Worst first
            'shift': ['Night', 'Evening', 'Day']  # Worst first
        },

        int_boxplots=1,
        int_show_points=0,  # Hide individual points, show only boxplots
        int_marker_size=8,

        int_frame_size_x=12,
        int_frame_size_y=7,

        # Layout
        label_spacing=[0.06        , 0.25        ,  0.06     ],
        lst_rotation= ['Horizontal', 'Horizontal', 'Vertical'],

        str_title='Example 3: Production Yield by Line, Shift, and Date'
    )

    pvc.analyze(df)
    fig, ax = pvc.plot(1)

    # Save
    fig.savefig('readme_example_3_custom_ordering.png', dpi=100, bbox_inches='tight')
    print("✓ Example 3 (Custom Ordering) saved to readme_example_3_custom_ordering.png")


if __name__ == '__main__':
    main()

