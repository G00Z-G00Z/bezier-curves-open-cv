import pytest
from ..bezier_calc import BezierPoints_T, from_waypoints_ctr_to_bezier


@pytest.fixture
def waypoints():
    waypoints = [
        (56.0, 263.0),
        (31.0, 280.0),
        (84.0, 419.0),
    ]
    return waypoints


@pytest.fixture
def ctr_points():
    ctr_points = [
        (48.0, 269.0),
        (49.0, 327.0),
        (77.0, 193.0),
    ]
    return ctr_points


def test_waypoints(waypoints, ctr_points):
    correct_bezier: list[BezierPoints_T] = [
        ((56.0, 263.0), (48.0, 269.0), (31.0, 280.0)),
        ((31.0, 280.0), (49.0, 327.0), (84.0, 419.0)),
    ]

    bezier = from_waypoints_ctr_to_bezier(waypoints, ctr_points)

    assert bezier == correct_bezier, "Beziers do not match"
