#!/usr/bin/env python3
"""Showcase of PyVarChart's flexible colormap system.

This example demonstrates how to use any matplotlib colormap with PyVarChart,
including reversing colormaps using either the _r suffix or the parameter.
"""

import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyvarchart import PyVarChart
import pandas as pd
from io import StringIO


def create_sample_data():
    """Create sample data with multiple categories."""
    str_data = ('category, subcategory, value\n'
                'A, X, 10\n'
                'A, X, 12\n'
                'A, Y, 15\n'
                'A, Y, 14\n'
                'A, Z, 8\n'
                'A, Z, 9\n'
                'B, X, 20\n'
                'B, X, 22\n'
                'B, Y, 18\n'
                'B, Y, 19\n'
                'B, Z, 25\n'
                'B, Z, 23'.replace(' ', ''))
    return pd.read_csv(StringIO(str_data))


def main():
    """Demonstrate various colormap options."""
    pd_data = create_sample_data()

    print("PyVarChart Colormap Showcase")
    print("=" * 60)

    # Define colormap examples to showcase
    examples = [
        # (colormap_name, description, filename)
        ('Blue to Green to Red', 'Custom gradient', 'colormap_custom_gradient.png'),
        ('tab10', 'Qualitative - Tableau 10', 'colormap_tab10.png'),
        ('Set1', 'Qualitative - ColorBrewer Set1', 'colormap_set1.png'),
        ('Dark2', 'Qualitative - Dark high-contrast', 'colormap_dark2.png'),
        ('Pastel1', 'Qualitative - Soft pastels', 'colormap_pastel1.png'),
        ('viridis', 'Sequential - Perceptually uniform', 'colormap_viridis.png'),
        ('plasma', 'Sequential - Perceptually uniform', 'colormap_plasma.png'),
        ('RdYlBu', 'Diverging - Red-Yellow-Blue', 'colormap_rdylbu.png'),
        ('coolwarm', 'Diverging - Cool to warm', 'colormap_coolwarm.png'),
        ('tab10_r', 'Reversed with _r suffix', 'colormap_tab10_reversed.png'),
    ]

    for i, (cmap_name, description, filename) in enumerate(examples, start=1):
        print(f"\n{i}. {description}")
        print(f"   Colormap: '{cmap_name}'")

        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['category', 'subcategory'],
            str_legend='subcategory',
            str_color_theme=cmap_name,
            str_title=f'{description} ({cmap_name})',
            int_frame_size_x=8,
            int_frame_size_y=6,
            int_marker_size=10,
        )
        pvc.analyze(pd_data)
        fig, ax = pvc.plot(i)
        fig.savefig(filename, dpi=100, bbox_inches='tight')
        plt.close(i)
        print(f"   ✓ Saved to {filename}")

    # Demonstrate color reversal with parameter
    print(f"\n{len(examples) + 1}. Color Reversal Demo")
    print("   Using int_reverse_color_scheme=1")
    pvc_rev = PyVarChart(
        str_yaxis_var_name='value',
        lst_xaxis_var_names=['category', 'subcategory'],
        str_legend='subcategory',
        str_color_theme='viridis',
        int_reverse_color_scheme=1,  # Reverse the colormap
        str_title='Reversed viridis (using parameter)',
        int_frame_size_x=8,
        int_frame_size_y=6,
        int_marker_size=10,
    )
    pvc.analyze(pd_data)
    fig_rev, ax_rev = pvc.plot(len(examples) + 1)
    fig_rev.savefig('colormap_viridis_reversed_param.png', dpi=100, bbox_inches='tight')
    plt.close(len(examples) + 1)
    print("   ✓ Saved to colormap_viridis_reversed_param.png")

    print("\n" + "=" * 60)
    print("✓ Colormap showcase completed!")
    print("\nAll matplotlib colormaps are supported:")
    print("  - Qualitative: tab10, Set1, Dark2, Pastel1, etc.")
    print("  - Sequential: viridis, plasma, Blues, Greens, etc.")
    print("  - Diverging: RdYlBu, coolwarm, seismic, etc.")
    print("\nReverse any colormap by:")
    print("  1. Adding '_r' suffix (e.g., 'viridis_r')")
    print("  2. Setting int_reverse_color_scheme=1")


if __name__ == '__main__':
    main()

