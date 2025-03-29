import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from interpolation_lib.Interpolation_2D_Methods import bilinear_interpolation


def apply_bilinear_to_image(image_path, new_height, new_width):
    """
    Загружает изображение и применяет к нему билинейную интерполяцию.
    Аргументы:
        image_path (str): путь к файлу изображения.
        new_height,new_width : новая высота и ширина изображения.
    Вывод:
        numpy.ndarray: Массив с интерполированным изображением.
    """

    print(f"Загрузка изображения: {image_path}")
    img = Image.open(image_path)
    img_arr = np.array(img).astype(float)  # float т.к. элементы могут стать float
    print(f"Исходный размер: {img_arr.shape}")

    if img_arr.ndim == 3:
        old_height, old_width, num_channels = img_arr.shape
        is_color = True  # Цветное
    elif img_arr.ndim == 2:
        old_height, old_width = img_arr.shape
        num_channels = 1  # Черно-белое
        is_color = False
    else:
        print("Error")
        return None

    x = np.arange(old_height)
    y = np.arange(old_width)

    xi = np.linspace(0, old_height - 1, new_height)
    yi = np.linspace(0, old_width - 1, new_width)

    # Массив для результата
    if is_color:
        interpolated_arr = np.zeros((new_height, new_width, num_channels), dtype=float)
    else:
        interpolated_arr = np.zeros((new_height, new_width), dtype=float)

    print("Начат процесс интерполяции")
    if is_color:
        for c in range(num_channels):
            print(f"Канал {c + 1}/{num_channels}...")
            # 2D-срез
            z_channel = img_arr[:, :, c]
            zi_channel = bilinear_interpolation(x, y, z_channel, xi, yi)
            interpolated_arr[:, :, c] = zi_channel
    else:
        z_channel = img_arr
        interpolated_arr = bilinear_interpolation(x, y, z_channel, xi, yi)
    print("Конец интерполяции")

    return np.clip(interpolated_arr, 0, 255).astype(np.uint8)


input_image_file = "test.png"
output_image_file = "interpolated_image.png"
img_test = Image.open(input_image_file)
width, height = img_test.size

# Увеличим размеры в 2 раза
new_w = width * 2
new_h = height * 2

interpolated_result = apply_bilinear_to_image(input_image_file, new_h, new_w)

if interpolated_result is not None:
    print(f"Размер интерполированного изображения: {interpolated_result.shape}")
    result_img = Image.fromarray(interpolated_result)
    result_img.save(output_image_file)
    print(f"Интерполированное изображение сохранено в  файле: {output_image_file}")
    original_img = Image.open(input_image_file)
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(original_img)
    axes[0].set_title("Исходное")
    axes[0].axis("off")
    axes[1].imshow(result_img)
    axes[1].set_title("Билинейная интерполяция")
    axes[1].axis("off")
    plt.show()
