import os

import numpy as np
import pytest
from click.testing import CliRunner
from PIL import Image

from interpolation_lib.cli import interpolate_image_cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def create_test_image(tmp_path):
    test_array = np.array(
        [
            [[255, 0, 0], [0, 255, 0], [0, 0, 255], [0, 0, 0]],
            [[255, 255, 0], [0, 255, 255], [255, 0, 255], [128, 128, 128]],
            [[255, 255, 255], [100, 50, 0], [50, 0, 100], [0, 50, 100]],
        ],
        dtype=np.uint8,
    )
    img = Image.fromarray(test_array)
    file_path = tmp_path / "test_input.png"
    img.save(file_path)
    print(f"\nСоздан временный файл: {file_path}")
    return str(file_path)


def test_cli_without_args(runner):
    result = runner.invoke(interpolate_image_cli, [])
    assert result.exit_code != 0
    assert "Missing argument" in result.output


def test_cli_help_option(runner):
    """Проверяем help."""
    result = runner.invoke(interpolate_image_cli, ["--help"])

    assert result.exit_code == 0  #
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "--method" in result.output
    assert "--output" in result.output
    assert "--show" in result.output
    assert "INPUT_PATH" in result.output


def test_cli_bilinear_save(runner, create_test_image, tmp_path):
    """
    Проверяет б билинейную интерполяцию, сохранение файла
    """
    input_file = create_test_image
    output_file = tmp_path / "output_bilinear.png"
    args = [
        input_file,
        "2.0",
        "1.5",
        "--method",
        "bilinear",
        "--output",
        str(output_file),
    ]

    result = runner.invoke(interpolate_image_cli, args)

    print(f"CLI: \n{result.output}")
    assert result.exit_code == 0, f"Error: {result.exception}"
    assert "Метод: bilinear" in result.output
    assert f"Изображение сохранено: {output_file}" in result.output
    assert os.path.exists(output_file)

    if os.path.exists(output_file):
        saved_img = Image.open(output_file)
        original_img = Image.open(input_file)

        orig_w, orig_h = original_img.size
        saved_w, saved_h = saved_img.size
        expected_w = int(orig_w * 1.5)
        expected_h = int(orig_h * 2.0)

        assert saved_h == expected_h
        assert saved_w == expected_w


def test_cli_show_option(runner, create_test_image, mocker):
    """Проверяет --show"""
    input_file = create_test_image
    mocked_show = mocker.patch("matplotlib.pyplot.show")
    args = [input_file, "1.2", "1.2", "--show"]

    result = runner.invoke(interpolate_image_cli, args)

    print(f"CLI :\n{result.output}")

    assert result.exit_code == 0
    assert "Показ изображений" in result.output

    mocked_show.assert_called_once()


def test_cli_invalid_scale_factor(runner, create_test_image):
    """Проверяет нулевой масштаб"""
    input_file = create_test_image
    args = [
        input_file,
        "0.0",  #
        "1.5",
    ]

    result = runner.invoke(interpolate_image_cli, args)

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code == 0
    assert "Коэффициенты масштабирования должны быть положительными!" in result.output


def test_cli_input_file_not_found(runner):
    """Проверяет обработку несуществующего входного файла"""
    args = ["nonexistent_image.png", "2.0", "2.0"]

    result = runner.invoke(interpolate_image_cli, args)

    print(f"CLI :\n{result.output}")
    assert result.exit_code != 0
    assert (
        "Invalid value for 'INPUT_PATH'" in result.output
        or "does not exist" in result.output
    )


def test_cli_unknown_method(runner, create_test_image):
    """Проверяет на неизвестный метод интерполяции"""
    # Arrange
    input_file = create_test_image
    args = [input_file, "1.0", "1.0", "--method", "unknown_method"]

    result = runner.invoke(interpolate_image_cli, args)

    print(f"CLI Output:\n{result.output}")
    assert result.exit_code != 0
    assert "Invalid value for '--method' / '-m'" in result.output
