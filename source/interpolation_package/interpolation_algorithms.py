



import numpy as np
import matplotlib.pyplot as plt

def linear_interpolation_1d(x, y, x_new):
    """
    Одномерная линейная интерполяция.
    Аргументы:
        x,y: Массивы известных значений координат x и y 
        x_new: Массив – точки, в которых нужно вычислить новые значения
    Вывод:
        Список – интерполированные значения функции в  x_new
    """

    y_new = []  

    for xi in x_new:  
        # Обработка выхода за границы 
        if xi <= x[0]:
            y_new.append(y[0])  # Если xi меньше первого x, берем первое y
            continue  
        if xi >= x[-1]:
            y_new.append(y[-1]) # Если xi больше последнего x, берем последнее y
            continue

        #  ищем [ x[k], x[k+1] ].
        for k in range(len(x) - 1):
            if x[k] <= xi < x[k+1]:
                #  интерполяция внутри интервала: y = y[k] + (x_new - x[k]) * (y[k+1] - y[k]) / (x[k+1] - x[k])
                y_new.append(y[k] + (xi - x[k]) * (y[k+1] - y[k]) / (x[k+1] - x[k]))
                break  

    return y_new


if __name__ == '__main__':
    x = np.array([0, 2, 4, 6, 8, 10])
    y = np.sin(x)

    x_new = np.linspace(-1, 11, 150) 

    y_original = [np.sin(val) for val in x_new]

    y_new = linear_interpolation_1d(x, y, x_new)
    plt.figure(figsize=(10, 6))  
    plt.plot(x, y, 'o', label='Исходные точки (x, y)', markersize=8)  
    plt.plot(x_new, y_new, '-', label='Линейная интерполяция', linewidth=2) #
    plt.plot(x_new, y_original, '--', label='Исходная функция sin(x)', linewidth=2) 
    plt.title('1D линейная интерполяция')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.grid(True)
    plt.show()