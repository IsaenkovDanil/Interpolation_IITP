import numpy as np
import pytest

from interpolation_lib.Interpolation_1D_Methods import linear_interpolation_1d

def test_linear_1d_basic_interpolation():
    """
    проверяем интерполяцию в одной точке
    """
    x_known = [0.0, 10.0]
    y_known = [0.0, 20.0]
    x_to_interpolate = [5.0]
    expected_y = [10.0]
    actual_y = linear_interpolation_1d(x_known, y_known, x_to_interpolate)
    assert np.allclose(actual_y, expected_y)
def test_linear_1d_multiple_points():
    """
    Проверяем интерполяцию сразу для нескольких точек.
    """
    x_known = [0.0, 10.0]
    y_known = [0.0, 20.0]
    x_interpolate = [2.0, 4.0, 6.0, 8.0] 
    expected_y = [4.0, 8.0, 12.0, 16.0]
    actual_y = linear_interpolation_1d(x_known, y_known, x_interpolate)
    assert np.allclose(actual_y, expected_y)
def test_linear_1d_known_points():
    """
    Проверяем, что интерполяция в старых точках их не изменит

    """
    x_known =[0,2,4,6,8,10]
    y_known=[np.sin(val) for val in x_known]
    x_interpolate= [2,6,10]
    excepted_y=[y_known[1],y_known[3],y_known[5]]
    actual_y=linear_interpolation_1d(x_known,y_known,x_interpolate)
    assert np.allclose(actual_y,excepted_y)

def test_linear_1d_left_outside():
    """
    Проверяем, если точка левее самой левой точки.
    Ожидание :  вернется значение самой левой точки.
    """
    x_known = [5.0, 10.0] 
    y_known = [15.0, 25.0]
    x_to_interpolate = [0.0, 3.0] 
    expected_y = [15.0, 15.0]
    actual_y = linear_interpolation_1d(x_known, y_known, x_to_interpolate)
    assert np.allclose(actual_y, expected_y)
def test_linear_1d_right_outside():
    """
    Проверяем, если точка правее самой правой точки.
    Ожидание :  вернется значение самой правой точки.
    """
    x_known = [5.0, 10.0] 
    y_known = [15.0, 25.0]
    x_to_interpolate = [11.0, 20.0] 
    expected_y = [25.0, 25.0]
    actual_y = linear_interpolation_1d(x_known, y_known, x_to_interpolate)
    assert np.allclose(actual_y, expected_y)
def test_linear_1d_scalar():
    x_known = [0, 10]
    y_known = [0, 100]
    x_scalar = 7
    expected_y_scalar = 70.0
    actual_y = linear_interpolation_1d(x_known, y_known, x_scalar)
    assert isinstance(actual_y, (float, int)) 
    assert np.isclose(actual_y, expected_y_scalar)
