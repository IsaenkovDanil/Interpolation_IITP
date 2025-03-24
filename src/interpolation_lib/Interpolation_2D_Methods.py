import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  

def bilinear_interpolation(x, y, z, xi, yi):
    """
      Двумерная билинейная интерполяция (еще обрабатывется случай, если нужно 
      интерполировать только в одной точке(скалярный случай))
    Аргументы:
        x,y:  1D массив координат x,y узлов сетки .
        z:  2D массив значений функции в узлах сетки z[i,j] = f(x[i],y[j])
        xi,yi: 1D массив или скаляр – x,y-координаты точек, в которых нужно
            вычислить интерполированные значения.
    Вывод:
        2D массив или скаляр – интерполированные значения  в точках (xi, yi)
    """

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    xi = np.array(xi)
    yi = np.array(yi)

    # Проверка, являются ли xi и yi скалярами
    scalar_input = False
    if xi.ndim == 0 and yi.ndim == 0:
        scalar_input = True
        xi = xi.reshape(1)  
        yi = yi.reshape(1)

    if z.shape != (x.size, y.size):
         raise ValueError(f"Размерность z {z.shape} должна быть ({x.size}, {y.size})")


    zi = np.zeros((xi.size, yi.size))

    # Цикл по точкам интерполяции
    for i in range(xi.size):
        for j in range(yi.size):

            x_idx = np.searchsorted(x, xi[i])
            y_idx = np.searchsorted(y, yi[j])

            #Обработка выхода за границы , индексы для z должны быть между 0 и size-1
            x1_idx = max(0, min(x_idx - 1, x.size - 1))
            x2_idx = max(0, min(x_idx,     x.size - 1))
            y1_idx = max(0, min(y_idx - 1, y.size - 1))
            y2_idx = max(0, min(y_idx,     y.size - 1))
            x1, x2 = x[x1_idx], x[x2_idx]
            y1, y2 = y[y1_idx], y[y2_idx]

            #Углы 
            z11 = z[x1_idx, y1_idx]
            z21 = z[x2_idx, y1_idx]
            z12 = z[x1_idx, y2_idx]
            z22 = z[x2_idx, y2_idx]

            # Проверка ,если узлы сетки будут совпадать (тогда может произойти деление на 0)
            if x1 == x2:
                if y1 == y2: 
                    zi[i,j] = z11
                    continue
                else: 
                    t = (yi[j] - y1) / (y2 - y1)
                    zi[i, j] = (1 - t) * z11 + t * z12
                    continue
            if y1 == y2:   
                s = (xi[i] - x1) / (x2 - x1)
                zi[i, j] = (1-s) * z11 + s* z21
                continue
            s = (xi[i] - x1) / (x2 - x1)
            t = (yi[j] - y1) / (y2 - y1)
            zi[i, j] = (1 - s) * (1 - t) * z11 + s * (1 - t) * z21 + (1 - s) * t * z12 + s * t * z22
            
            #Здесь вместо этой фомрулы можно использовать просто подряд две одномерные интерполяции:
            #z_interp1 = linear_interpolation_1d([x1, x2], [z11, z21], xi[i])
            #z_interp2 = linear_interpolation_1d([x1, x2], [z12, z22], xi[i])
            #zi[i, j] = linear_interpolation_1d([y1, y2], [z_interp1, z_interp2], yi[j])

    if scalar_input:
        return zi[0, 0]
    else:
        return zi




def l2_constant_interpolation(x, y, z, xi, yi):
    print("заглушка:  L2 (константные базисные) ")
    return bilinear_interpolation(x, y, z, xi, yi)

def l2_linear_interpolation(x, y, z, xi, yi):
    print("заглушка:  L2 (линейные базисные) ")
    return bilinear_interpolation(x, y, z, xi, yi)

def l2_mixed_interpolation(x, y, z, xi, yi):
    print("заглушка:  L2 (смешанные базисные) ")
    return bilinear_interpolation(x, y, z, xi, yi)

