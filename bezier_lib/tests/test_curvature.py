import pytest
import bezier
import numpy as np
from ..bezier_calc import calculate_curvature


@pytest.fixture
def curve():
    """
    Create a quadratic Bezier curve with nodes at (0, 0), (1, 1), and (2, 0).
    """
    nodes = np.asfortranarray([[0, 1, 2], [0, 1, 0]])
    curve = bezier.Curve(nodes, degree=2)
    return curve


@pytest.fixture
def straight_line():
    """
    Quadratic straight line
    """
    nodes = np.asfortranarray([[0, 1, 2], [0, 1, 2]])
    curve = bezier.Curve(nodes, degree=2)
    return curve


def test_curvature(curve: bezier.Curve):
    """
    Test if function runs
    """
    s_values = np.linspace(0, 1, 10)  # Array of s values
    curvitances = calculate_curvature(curve, s_values)
    assert len(curvitances) == len(
        s_values
    ), "Length of curvitances and s_values must match"


def test_curvitance_of_straight_line(straight_line: bezier.Curve):
    """
    Test if function runs
    """
    s_values = np.linspace(0, 1, 10)  # Array of s values
    curvitances = calculate_curvature(straight_line, s_values)
    assert len(curvitances) == len(
        s_values
    ), "Length of curvitances and s_values must match"
