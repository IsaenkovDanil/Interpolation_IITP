import numpy as np
import pytest
from PIL import Image

from interpolation_lib.image_processing import apply_interpolation_to_image
from interpolation_lib.Interpolation_2D_Methods import (
    bilinear_interpolation,
)


def test_bilinear_center():
    """Проверяет билинейную интерполяцию в центре квадрата 2x2"""
    x = np.array([0.0, 1.0])
    y = np.array([0.0, 1.0])
    z_known = np.array([[10.0, 30.0], [20.0, 40.0]])
    xi = np.array([0.5])
    yi = np.array([0.5])
    expected_zi = np.array([[25.0]])
    actual_zi = bilinear_interpolation(x, y, z_known, xi, yi)
    assert np.allclose(actual_zi, expected_zi)


def test_bilinear_grid():
    """Проверяет билинейную интерполяцию что в узлах сетки"""
    x = np.array([0.0, 1.0, 2.0])
    y = np.array([0.0, 1.0])
    # z = x + y
    z_known = np.array([[0.0, 1.0], [1.0, 2.0], [2.0, 3.0]])
    xi = x
    yi = y

    actual_zi = bilinear_interpolation(x, y, z_known, xi, yi)

    assert actual_zi.shape == z_known.shape
    assert np.allclose(actual_zi, z_known)


def test_bilinear_larger_grid():
    """Проверяет билинейную интерполяцию в узлах большой сетки"""
    x = np.linspace(0, 10, 5)
    y = np.linspace(0, 20, 6)
    X_known, Y_known = np.meshgrid(x, y, indexing="ij")
    Z_known = X_known**2 + np.sin(Y_known)
    xi = x
    yi = y

    actual_Zi = bilinear_interpolation(x, y, Z_known, xi, yi)

    assert np.allclose(actual_Zi, Z_known)


def test_bilinear_border():
    """Проверяетзначения на границах"""
    x = np.array([0, 1])
    y = np.array([0, 1])
    z = np.array([[10.0, 30.0], [20.0, 40.0]])
    xi = np.array([-1.0, 0.5, 2.0])
    yi = np.array([-1.0, 0.5, 2.0])

    expected_zi = np.array([[10.0, 20.0, 30.0], [15.0, 25.0, 35.0], [20.0, 30.0, 40.0]])
    actual_zi = bilinear_interpolation(x, y, z, xi, yi)

    assert np.allclose(actual_zi, expected_zi)


@pytest.fixture
def create_temp_image(tmp_path):
    """Вспомогательная фунция для создания изображений"""
    gray_path = tmp_path / "test_gray.png"
    rgb_path = tmp_path / "test_rgb.png"

    gray_arr = np.array([[0, 100], [200, 255]], dtype=np.uint8)

    Image.fromarray(gray_arr).save(gray_path)

    rgb_arr = np.array(
        [[[255, 0, 0], [0, 255, 0]], [[0, 0, 255], [255, 255, 255]]], dtype=np.uint8
    )

    Image.fromarray(rgb_arr).save(rgb_path)

    return {"gray": str(gray_path), "rgb": str(rgb_path)}


def test_apply_interpolation_output_shape_rgb(create_temp_image):
    """Проверяем форму результата для цветного изображения"""

    input_file = create_temp_image["rgb"]
    new_h, new_w = 4, 6

    result_arr = apply_interpolation_to_image(
        input_file, new_h, new_w, bilinear_interpolation
    )

    assert result_arr is not None
    assert result_arr.shape == (new_h, new_w, 3)
    assert result_arr.dtype == np.uint8


def test_apply_interpolation_output_shape_gray(create_temp_image):
    """Проверяет форму результата для черно-белого изображения"""
    input_file = create_temp_image["gray"]
    new_h, new_w = 5, 3
    result_arr = apply_interpolation_to_image(
        input_file, new_h, new_w, bilinear_interpolation
    )
    assert result_arr is not None
    assert result_arr.shape == (new_h, new_w)
    assert result_arr.dtype == np.uint8
