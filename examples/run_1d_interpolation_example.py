import numpy as np
import matplotlib.pyplot as plt
from interpolation_lib.Interpolation_1D_Methods import linear_interpolation_1d


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