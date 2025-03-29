import os
import click
import matplotlib.pyplot as plt
from PIL import Image

from .image_processing import apply_interpolation_to_image
from .Interpolation_2D_Methods import (
    bilinear_interpolation,
    l2_constant_interpolation,
    l2_linear_interpolation,
    l2_mixed_interpolation,
)

INTERPOLATION_ALGORITHMS = {
    "bilinear": bilinear_interpolation,
    "l2_const": l2_constant_interpolation,
    "l2_linear": l2_linear_interpolation,
    "l2_mixed": l2_mixed_interpolation,
}


def _show_images(original_arr, interpolated_arr, method_name):
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].imshow(original_arr)
    ax[0].set_title("Исходное изображение")
    ax[0].axis("off")
    ax[1].imshow(interpolated_arr)
    ax[1].set_title(f"Интерполяция ({method_name})")
    ax[1].axis("off")
    plt.tight_layout()
    plt.show()


@click.command()
@click.argument(
    "input_path", type=click.Path(exists=True, dir_okay=False, readable=True)
)
@click.argument("x_scale", type=click.FLOAT)
@click.argument("y_scale", type=click.FLOAT)
@click.option(
    "--method",
    "-m",
    type=click.Choice(list(INTERPOLATION_ALGORITHMS.keys()), case_sensitive=False),
    default="bilinear",
    show_default=True,
    help="Алгоритм интерполяции",
)
@click.option(
    "--output",
    "-o",
    "output_path",
    type=click.Path(dir_okay=False, writable=True),
    default=None,
    help="Путь для сохранения изображения. Если не указан, не сохраняется",
)
@click.option(
    "--show",
    is_flag=True,
    default=False,
    help="Показать исходное и результат после интерполяции",
)
def interpolate_image_cli(input_path, x_scale, y_scale, method, output_path, show):
    """
    Интерполирует изображение
    input_path: Путь к исходному файлу изображения
    x_scale,y_scale:    Коэффициенты масштабирования по высоте и шширине 
    """
    click.echo(f"Масштаб: {x_scale}x , {y_scale}x")
    click.echo(f"Метод: {method}")
    if x_scale <= 0 or y_scale <= 0:
        click.secho("Коэффициенты масштабирования должны быть положительными!")
        return

    selected_interpolation_func = INTERPOLATION_ALGORITHMS[method.lower()]
    image = Image.open(input_path)
    old_width, old_height = image.size
    new_height = int(old_height * x_scale)
    new_width = int(old_width * y_scale)

    final_interpolated_arr = apply_interpolation_to_image(
        input_path,
        new_height,
        new_width,
        selected_interpolation_func,  
    )
    if final_interpolated_arr is None:
        click.secho("Error")
        return

    click.echo(f"Финальный размер : {final_interpolated_arr.shape}")

    if show:
        click.echo("Показ изображений")
        original_image = Image.open(input_path)
        _show_images(original_image, final_interpolated_arr, method)
    
    if output_path:
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        result_img = Image.fromarray(final_interpolated_arr)
        result_img.save(output_path)
        click.secho(f"Изображение сохранено: {output_path}")

    else:
        click.echo("Путь не указан")


if __name__ == "__main__":
    interpolate_image_cli()
