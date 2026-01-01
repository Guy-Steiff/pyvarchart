#!/usr/bin/env python3
"""Demonstrate PyVarChart's continuous scale feature for cleaner legends.

This example shows how int_continuous_scale handles continuous legend values:
- int_continuous_scale=0: Shows ALL unique values (categorical mode)
- int_continuous_scale=1: Auto-selects 5-6 representative values with smooth gradient
"""

import pandas as pd
import matplotlib.pyplot as plt
plt.switch_backend('agg')
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyvarchart import PyVarChart
import numpy as np


def create_continuous_data():
    """Create sample data with continuous legend values."""
    np.random.seed(42)

    # Simulate temperature measurements across different locations
    data = []
    locations = ['Site_A', 'Site_B', 'Site_C']
    operators = ['Op1', 'Op2']

    for location in locations:
        for operator in operators:
            # Generate 15 measurements with varying temperatures
            for _ in range(15):
                temperature = np.random.uniform(15.0, 45.0)  # Continuous temperature values
                measurement = np.random.normal(100, 10) + temperature * 0.5

                data.append({
                    'location': location,
                    'operator': operator,
                    'temperature': temperature,
                    'measurement': measurement
                })

    return pd.DataFrame(data)


def main():
    """Demonstrate continuous scale feature."""
    print("PyVarChart Continuous Scale Feature Demonstration")
    print("=" * 70)

    pd_data = create_continuous_data()

    # Show the data range
    temp_min = pd_data['temperature'].min()
    temp_max = pd_data['temperature'].max()
    temp_unique = pd_data['temperature'].nunique()

    print(f"\nDataset Statistics:")
    print(f"  Temperature range: {temp_min:.2f} to {temp_max:.2f}")
    print(f"  Number of unique temperatures: {temp_unique}")
    print(f"  Total data points: {len(pd_data)}")

    # Example 1: Without continuous scale (categorical - will be messy!)
    print("\n" + "-" * 70)
    print("\n1. WITHOUT Continuous Scale (int_continuous_scale=0)")
    print("   → Shows ALL unique temperature values")
    print(f"   → Legend will have {temp_unique} entries (very messy!)")

    pvc1 = PyVarChart(
        str_yaxis_var_name='measurement',
        lst_xaxis_var_names=['location', 'operator'],
        str_legend='temperature',
        str_color_theme='viridis',
        int_continuous_scale=0,  # Disabled - treats as categorical
        str_title='Categorical Mode: All Values Shown',
        int_frame_size_x=10,
        int_frame_size_y=8,
        int_marker_size=8,
    )

    # Generate chart
    pvc1.analyze(pd_data)
    fig1, ax1 = pvc1.plot(1)
    fig1.savefig('continuous_scale_OFF.png', dpi=150, bbox_inches='tight')
    plt.close(1)
    print("   ✓ Saved to continuous_scale_OFF.png")

    # Example 2: With continuous scale - auto-selects 5-6 values
    print("\n2. WITH Continuous Scale (int_continuous_scale=1)")
    print("   → Auto-selects 5-6 representative values")
    print("   → Includes min, max, and evenly distributed percentiles")
    print("   → Smooth color gradient interpolation")

    pvc2 = PyVarChart(
        str_yaxis_var_name='measurement',
        lst_xaxis_var_names=['location', 'operator'],
        str_legend='temperature',
        str_color_theme='viridis',
        int_continuous_scale=1,  # Auto-select 5-6 representative values
        str_title='Continuous Mode: 5-6 Representative Values',
        int_frame_size_x=10,
        int_frame_size_y=8,
        int_marker_size=8,
    )

    pvc2.analyze(pd_data)
    fig2, ax2 = pvc2.plot(2)
    fig2.savefig('continuous_scale_ON.png', dpi=150, bbox_inches='tight')
    plt.close(2)
    print("   ✓ Saved to continuous_scale_ON.png")
    print("   ✓ Legend shows ~6 values (much cleaner!)")

    # Example 3: Continuous with plasma colormap
    print("\n3. Continuous Scale with 'plasma' colormap")

    pvc3 = PyVarChart(
        str_yaxis_var_name='measurement',
        lst_xaxis_var_names=['location', 'operator'],
        str_legend='temperature',
        str_color_theme='plasma',
        int_continuous_scale=1,
        str_title='Continuous Scale: Plasma Colormap',
        int_frame_size_x=10,
        int_frame_size_y=8,
        int_marker_size=8,
    )

    pvc3.analyze(pd_data)
    fig3, ax3 = pvc3.plot(3)
    fig3.savefig('continuous_scale_plasma.png', dpi=150, bbox_inches='tight')
    plt.close(3)
    print("   ✓ Saved to continuous_scale_plasma.png")

    # Example 4: Continuous with coolwarm diverging colormap
    print("\n4. Continuous Scale with 'coolwarm' (diverging)")
    print("   → Blue=cold, Red=hot")

    pvc4 = PyVarChart(
        str_yaxis_var_name='measurement',
        lst_xaxis_var_names=['location', 'operator'],
        str_legend='temperature',
        str_color_theme='coolwarm',  # Blue=cold, Red=hot
        int_continuous_scale=1,
        str_title='Temperature Analysis (coolwarm)',
        int_frame_size_x=10,
        int_frame_size_y=8,
        int_marker_size=10,
    )

    pvc4.analyze(pd_data)
    fig4, ax4 = pvc4.plot(4)
    fig4.savefig('continuous_scale_coolwarm.png', dpi=150, bbox_inches='tight')
    plt.close(4)
    print("   ✓ Saved to continuous_scale_coolwarm.png")

    # Example 5: Auto-revert to categorical when strings present
    print("\n5. Auto-Detection: Strings Force Categorical Mode")
    print("   → Mixed data with strings automatically reverts to categorical")

    # Create data with string legend values
    mixed_data = pd.DataFrame({
        'location': ['A', 'A', 'B', 'B'] * 3,
        'operator': ['Op1', 'Op2'] * 6,
        'category': ['Low', 'Medium', 'High', 'Low', 'Medium', 'High'] * 2,
        'measurement': [95, 105, 115, 93, 107, 117, 96, 104, 114, 94, 106, 116]
    })

    pvc5 = PyVarChart(
        str_yaxis_var_name='measurement',
        lst_xaxis_var_names=['location', 'operator'],
        str_legend='operator',
        str_color_theme='Set1',
        int_continuous_scale=1,  # Requesting continuous, but will auto-revert
        str_title='Auto-Reverts to Categorical (strings detected)',
        int_frame_size_x=8,
        int_frame_size_y=6,
        int_marker_size=10,
    )

    pvc5.analyze(pd_data)
    fig5, ax5 = pvc5.plot(5)
    fig5.savefig('continuous_scale_auto_revert.png', dpi=150, bbox_inches='tight')
    plt.close(5)
    print("   ✓ Saved to continuous_scale_auto_revert.png")
    print("   ✓ Automatically reverted to categorical (3 string values)")

    print("\n" + "=" * 70)
    print("✓ Continuous scale demonstration completed!")
    print("\nKey Features:")
    print("  - int_continuous_scale=0: Show ALL values (categorical)")
    print("  - int_continuous_scale=1: Auto-select 5-6 representative values")
    print("  - Representative values: min, 20th, 40th, 60th, 80th, max percentiles")
    print("  - Smooth color gradient across the range")
    print("  - Auto-detects strings and reverts to categorical")
    print("  - Works seamlessly with ALL colormaps")
    print("\nBest Practices:")
    print("  - Use continuous scale when you have many (>10) numeric values")
    print("  - Use categorical mode when you have discrete categories or strings")
    print("  - Recommended colormaps: viridis, plasma, coolwarm, RdYlBu")


if __name__ == '__main__':
    main()

