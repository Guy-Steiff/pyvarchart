#!/usr/bin/env python3
"""Advanced PyVarChart example - all features enabled."""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving to file

from pyvarchart import PyVarChart
import pandas as pd
from io import StringIO


def main():
    """Run advanced example with full dataset and all features."""
    # Full sample data from main_example
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

    # Create advanced chart with all features
    pvc = PyVarChart(
        # Custom label spacing per level
        label_spacing=[0.10, 0.08, 0.06, 0.05, 0.04],

        # Data configuration
        str_yaxis_var_name='trim_read',
        lst_xaxis_var_names=['chip', 'channel', 'lane', 'core', 'cmp'],
        str_legend='lane',

        # Visual styling
        b_jitter_points=True,
        int_marker_size=7,
        str_marker_theme='Default',
        str_color_theme='Blue to Green to Red',

        # Layout
        str_title='trim_read Variability Across Configs - Advanced Example',
        int_frame_size_x=12,
        int_frame_size_y=7,

        # Custom ordering (reversed)
        dict_xaxis_orderings={'cmp': [5, 4, 3, 2, 1, 0]},

        # Label control
        lst_rotation=['Horizontal', 'Horizontal', 'Vertical', 'Vertical', 'Horizontal'],
        lst_xaxis_font_size=[11, 10, 9, 8, 9],
    )

    # Generate chart
    fig, ax = pvc.analyze(1, pd_data)
    ax.set_ylim(0, 255)

    # Save with high quality
    fig.savefig('advanced_example.png', dpi=300, bbox_inches='tight')
    print("✓ Advanced example saved to advanced_example.png")
    print(f"✓ Chart shows {len(pd_data)} data points")
    print(f"✓ Grouped by {len(pvc.lst_xaxis_var_names)} factors")
    print("✓ Features: custom spacing, jittering, custom ordering, color theme")


if __name__ == '__main__':
    main()

