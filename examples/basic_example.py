#!/usr/bin/env python3
"""Basic PyVarChart example - simple usage."""

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving to file

from pyvarchart import PyVarChart
import pandas as pd
from io import StringIO


def main():
    """Run basic example with minimal configuration."""
    # Sample data (smaller subset for basic example)
    str_data = ('chip, channel, lane, core, cmp, trim_read\n'
                '0   , 2      , I   , 0   , 0  , 159\n'
                '0   , 2      , I   , 0   , 1  , 136\n'
                '0   , 2      , I   , 0   , 2  , 167\n'
                '0   , 2      , I   , 0   , 3  , 139\n'
                '0   , 2      , I   , 0   , 4  , 160\n'
                '0   , 2      , I   , 1   , 0  , 167\n'
                '0   , 2      , I   , 1   , 1  , 130\n'
                '0   , 2      , Q   , 0   , 0  , 142\n'
                '0   , 2      , Q   , 0   , 1  , 122\n'
                '0   , 2      , Q   , 0   , 2  , 116\n'
                '0   , 2      , Q   , 1   , 0  , 164\n'
                '0   , 2      , Q   , 1   , 1  , 138'.replace(' ', ''))
    pd_data = pd.read_csv(StringIO(str_data))

    # Create basic variability chart
    pvc = PyVarChart(
        str_yaxis_var_name='trim_read',
        lst_xaxis_var_names=['chip', 'channel', 'lane', 'core', 'cmp'],
        str_color_theme='Blue to Green to Red',
        str_legend='lane',
        str_title='Basic Variability Chart Example',
        int_frame_size_x=10,
        int_frame_size_y=6,
    )

    # Generate chart
    fig, ax = pvc.analyze(1, pd_data)
    ax.set_ylim(0, 200)

    # Save
    fig.savefig('basic_example.png', dpi=150, bbox_inches='tight')
    print("✓ Basic example saved to basic_example.png")


if __name__ == '__main__':
    main()
