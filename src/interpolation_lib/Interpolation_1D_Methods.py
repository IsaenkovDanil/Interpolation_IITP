import numpy as np


def linear_interpolation_1d(x, y, x_new):
    """
    Одномерная линейная интерполяция.
    Аргументы:
        x,y: Массивы известных значений координат x и y
        x_new: Массив – точки, в которых нужно вычислить новые значения
    Вывод:
        Список – интерполированные значения функции в  x_new
    """
    x = np.asarray(x)
    y = np.asarray(y)
    is_scalar = not isinstance(x_new, list | tuple | np.ndarray)

    if is_scalar:
        x_new1 = [x_new]
    else:
        x_new1 = np.asarray(x_new)

    y_new = []

    for xi in x_new1:
        # Обработка выхода за границы
        if xi <= x[0]:
            y_new.append(y[0])  # Если xi меньше первого x, берем первое y
            continue
        if xi >= x[-1]:
            y_new.append(y[-1])  # Если xi больше последнего x, берем последнее y
            continue

        #  ищем [ x[k], x[k+1] ].
        for k in range(len(x) - 1):
            if x[k] <= xi < x[k + 1]:
                #  интерполяция внутри интервала:
                # y = y[k] + (x_new1 - x[k]) * (y[k+1] - y[k]) / (x[k+1] - x[k])
                y_new.append(y[k] + (xi - x[k]) * (y[k + 1] - y[k]) / (x[k + 1] - x[k]))
                break

    if is_scalar:
        return y_new[0]
    else:
        if isinstance(x_new, np.ndarray):
            return np.array(y_new)
        else:
            return y_new
