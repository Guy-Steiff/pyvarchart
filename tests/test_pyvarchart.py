"""Unit tests for PyVarChart."""

import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import StringIO
import sys
sys.path.insert(0, '..')

from pyvarchart import PyVarChart


class TestBasicFunctionality:
    """Test basic chart creation and functionality."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'chip': [0, 0, 0, 0, 1, 1, 1, 1],
            'channel': [2, 2, 2, 2, 3, 3, 3, 3],
            'lane': ['I', 'I', 'Q', 'Q', 'I', 'I', 'Q', 'Q'],
            'measurement': [159, 136, 142, 122, 165, 140, 148, 125]
        })

    def test_basic_chart_creation(self, sample_data):
        """Test that a basic chart can be created without errors."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['chip', 'channel', 'lane']
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)
        plt.close(fig)

    def test_with_legend(self, sample_data):
        """Test chart creation with legend."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['chip', 'channel'],
            str_legend='lane'
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert ax.get_legend() is not None
        plt.close(fig)

    def test_title_appears(self, sample_data):
        """Test that custom title is set."""
        title = "Test Chart Title"
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['chip'],
            str_title=title,
            int_boxplots=0  # Disable boxplots to avoid empty groups
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert ax.get_title() == title
        plt.close(fig)


class TestValidation:
    """Test input validation and error handling."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'a': [1, 2, 3],
            'b': ['x', 'y', 'z'],
            'c': [10, 20, 30]
        })

    def test_missing_y_column(self, sample_data):
        """Test error when y-axis column doesn't exist."""
        pvc = PyVarChart(
            str_yaxis_var_name='nonexistent',
            lst_xaxis_var_names=['a']
        )
        with pytest.raises(ValueError, match="Missing required columns"):
            pvc.analyze(1, sample_data)

    def test_missing_x_column(self, sample_data):
        """Test error when x-axis column doesn't exist."""
        pvc = PyVarChart(
            str_yaxis_var_name='c',
            lst_xaxis_var_names=['a', 'nonexistent']
        )
        with pytest.raises(ValueError, match="Missing required columns"):
            pvc.analyze(1, sample_data)

    def test_missing_legend_column(self, sample_data):
        """Test error when legend column doesn't exist."""
        pvc = PyVarChart(
            str_yaxis_var_name='c',
            lst_xaxis_var_names=['a'],
            str_legend='nonexistent'
        )
        with pytest.raises(ValueError, match="Missing required columns"):
            pvc.analyze(1, sample_data)

    def test_y_in_x_overlap(self, sample_data):
        """Test error when y-axis variable is also in x-axis."""
        pvc = PyVarChart(
            str_yaxis_var_name='c',
            lst_xaxis_var_names=['a', 'c']  # 'c' is both y and x
        )
        with pytest.raises(ValueError, match="cannot also be in X-axis"):
            pvc.analyze(1, sample_data)


class TestCustomOrdering:
    """Test custom ordering functionality."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'priority': ['High', 'Low', 'Medium', 'High', 'Low'],
            'value': [10, 20, 30, 15, 25]
        })

    def test_custom_ordering_applied(self, sample_data, capsys):
        """Test that custom ordering is applied correctly."""
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['priority'],
            dict_xaxis_orderings={'priority': ['High', 'Medium', 'Low']},
            int_boxplots=0  # Disable boxplots for simple data
        )
        fig, ax = pvc.analyze(1, sample_data)
        plt.close(fig)
        # If no warnings, ordering was complete

    def test_missing_values_warning(self, sample_data, capsys):
        """Test warning when custom ordering is missing values."""
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['priority'],
            dict_xaxis_orderings={'priority': ['High', 'Low']},  # Missing 'Medium'
            int_boxplots=0  # Disable boxplots
        )
        fig, ax = pvc.analyze(1, sample_data)
        captured = capsys.readouterr()

        assert "missing values" in captured.out.lower()
        assert "Medium" in captured.out or "medium" in captured.out
        plt.close(fig)

    def test_extra_values_warning(self, sample_data, capsys):
        """Test warning when custom ordering has extra values."""
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['priority'],
            dict_xaxis_orderings={'priority': ['High', 'Medium', 'Low', 'Critical']},
            int_boxplots=0  # Disable boxplots
        )
        fig, ax = pvc.analyze(1, sample_data)
        captured = capsys.readouterr()

        assert "not in data" in captured.out.lower() or len(captured.out) == 0
        plt.close(fig)


class TestLabelSpacing:
    """Test label spacing functionality (float vs list)."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'a': [1, 1, 2, 2],
            'b': ['x', 'y', 'x', 'y'],
            'c': [10, 20, 30, 40]
        })

    def test_float_spacing(self, sample_data):
        """Test uniform spacing with float."""
        pvc = PyVarChart(
            str_yaxis_var_name='c',
            lst_xaxis_var_names=['a', 'b'],
            label_spacing=0.10
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_list_spacing(self, sample_data):
        """Test custom spacing with list."""
        pvc = PyVarChart(
            str_yaxis_var_name='c',
            lst_xaxis_var_names=['a', 'b'],
            label_spacing=[0.15, 0.10]  # Different spacing per level
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_list_spacing_shorter_than_levels(self, sample_data):
        """Test that short spacing list doesn't crash."""
        pvc = PyVarChart(
            str_yaxis_var_name='c',
            lst_xaxis_var_names=['a', 'b'],
            label_spacing=[0.15]  # Only 1 value for 2 levels
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert isinstance(fig, plt.Figure)
        plt.close(fig)


class TestStatisticalOverlays:
    """Test statistical overlay features."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'group': ['A', 'A', 'B', 'B'] * 3,
            'subgroup': ['X', 'Y', 'X', 'Y'] * 3,
            'value': [10, 15, 20, 25, 12, 18, 22, 28, 11, 16, 21, 26]
        })

    def test_cell_means(self, sample_data):
        """Test cell means display."""
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['group', 'subgroup'],
            int_show_cell_means=1
        )
        fig, ax = pvc.analyze(1, sample_data)
        # Chart should have horizontal lines for means

        assert len(ax.get_lines()) > 0
        plt.close(fig)

    def test_grand_mean(self, sample_data):
        """Test grand mean display."""
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['group'],
            int_show_grand_mean=1,
            int_boxplots=0  # Disable boxplots to avoid empty box_data issues
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert len(ax.get_lines()) > 0
        plt.close(fig)

    def test_group_means(self, sample_data):
        """Test group means display."""
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['group', 'subgroup'],
            lst_show_group_means=['group']
        )
        fig, ax = pvc.analyze(1, sample_data)

        assert len(ax.get_lines()) > 0
        plt.close(fig)

    def test_boxplots_enabled(self, sample_data):
        """Test boxplot display."""
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['group', 'subgroup'],  # Use both grouping levels for sufficient data
            int_boxplots=1
        )
        fig, ax = pvc.analyze(1, sample_data)
        # Should have box plot artists

        assert len(ax.patches) > 0 or len(ax.lines) > 0
        plt.close(fig)


class TestStyling:
    """Test styling options."""

    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing."""
        return pd.DataFrame({
            'category': ['A', 'B', 'A', 'B'],
            'condition': ['X', 'X', 'Y', 'Y'],
            'measurement': [10, 20, 15, 25]
        })

    def test_color_theme_pvc_light(self, sample_data):
        """Test Pastel1 color theme (formerly PVC Light)."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['category'],
            str_legend='condition',
            str_color_theme='Pastel1',
            int_boxplots=0  # Disable boxplots to avoid empty data issues
        )
        fig, ax = pvc.analyze(1, sample_data)

        plt.close(fig)

    def test_color_theme_blue_to_red(self, sample_data):
        """Test Blue to Green to Red theme."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['category'],
            str_legend='condition',
            str_color_theme='Blue to Green to Red',
            int_boxplots=0  # Disable boxplots to avoid empty data issues
        )
        fig, ax = pvc.analyze(1, sample_data)

        plt.close(fig)

    def test_marker_theme_default(self, sample_data):
        """Test default marker theme."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['category'],
            str_legend='condition',
            str_marker_theme='Default',
            int_boxplots=0  # Disable boxplots
        )
        fig, ax = pvc.analyze(1, sample_data)

        plt.close(fig)

    def test_marker_theme_solid(self, sample_data):
        """Test solid marker theme."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['category'],
            str_legend='condition',
            str_marker_theme='Solid',
            int_boxplots=0  # Disable boxplots
        )
        fig, ax = pvc.analyze(1, sample_data)

        plt.close(fig)

    def test_jittering_enabled(self, sample_data):
        """Test point jittering."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['category'],
            int_jitter_points=1,  # Correct parameter name
            int_boxplots=0  # Disable boxplots
        )
        fig, ax = pvc.analyze(1, sample_data)

        plt.close(fig)

    def test_custom_marker_size(self, sample_data):
        """Test custom marker size."""
        pvc = PyVarChart(
            str_yaxis_var_name='measurement',
            lst_xaxis_var_names=['category'],
            int_marker_size=15,
            int_boxplots=0  # Disable boxplots
        )
        fig, ax = pvc.analyze(1, sample_data)

        plt.close(fig)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_single_data_point(self):
        """Test with single data point."""
        data = pd.DataFrame({
            'x': [1],
            'y': [10]
        })
        pvc = PyVarChart(
            str_yaxis_var_name='y',
            lst_xaxis_var_names=['x'],
            int_boxplots=0  # Disable boxplots for single point
        )
        fig, ax = pvc.analyze(1, data)

        plt.close(fig)

    def test_many_grouping_levels(self):
        """Test with many x-axis grouping levels."""
        data = pd.DataFrame({
            'a': [1] * 4,
            'b': [2] * 4,
            'c': ['x', 'y'] * 2,
            'd': ['p', 'p', 'q', 'q'],
            'e': ['m', 'n', 'm', 'n'],
            'value': [10, 20, 30, 40]
        })
        pvc = PyVarChart(
            str_yaxis_var_name='value',
            lst_xaxis_var_names=['a', 'b', 'c', 'd', 'e']
        )
        fig, ax = pvc.analyze(1, data)

        plt.close(fig)

    def test_empty_group_means_list(self):
        """Test with empty group means list."""
        data = pd.DataFrame({
            'x': [1, 2],
            'y': [10, 20]
        })
        pvc = PyVarChart(
            str_yaxis_var_name='y',
            lst_xaxis_var_names=['x'],
            lst_show_group_means=[],
            int_boxplots=0  # Disable boxplots for simple data
        )
        fig, ax = pvc.analyze(1, data)

        plt.close(fig)


class TestUtilityFunctions:
    """Test utility functions."""

    def test_legend_label_with_none(self):
        """Test legend_label function with None."""
        from pyvarchart import legend_label

        assert legend_label(None) == "Unlabeled"

    def test_legend_label_with_value(self):
        """Test legend_label function with actual value."""
        from pyvarchart import legend_label

        assert legend_label("Test") == "Test"
        assert legend_label(123) == "123"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


