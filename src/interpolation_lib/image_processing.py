import numpy as np
from PIL import Image


def apply_interpolation_to_image(image_path, new_height, new_width, interpolation_func):
    """
    Загружает изображение и применяет к нему ЗАДАННУЮ функцию 2D интерполяции.
    Аргументы:
        image_path (str): путь к файлу изображения.
        new_height,new_width : новая высота и ширина изображения.
        interpolation_func (x, y, z, xi, yi): Функция 2D интерполяции.

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

    print(
        f"Новый размер: ({new_height}, {new_width}, {num_channels if is_color else 1})"
    )
    x = np.arange(old_height)
    y = np.arange(old_width)

    xi = np.linspace(0, old_height - 1, new_height)
    yi = np.linspace(0, old_width - 1, new_width)

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
            zi_channel = interpolation_func(x, y, z_channel, xi, yi)
            interpolated_arr[:, :, c] = zi_channel
    else:
        z_channel = img_arr
        interpolated_arr = interpolation_func(x, y, z_channel, xi, yi)
    print("Конец интерполяции")

    return np.clip(interpolated_arr, 0, 255).astype(np.uint8)
