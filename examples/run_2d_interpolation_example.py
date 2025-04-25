import matplotlib.pyplot as plt
import numpy as np

from interpolation_lib.Interpolation_2D_Methods import bilinear_interpolation


def sin_cos_function(x, y):
    return np.sin(x) * np.cos(y)


x = np.linspace(0, 2 * np.pi, 10)
y = np.linspace(0, 2 * np.pi, 10)

X, Y = np.meshgrid(x, y, indexing="ij")
Z = sin_cos_function(X, Y)

# 50 точек по x и 60 точек по y (с выходом за границы)
xi = np.linspace(-0.5, 2 * np.pi + 0.5, 50)
yi = np.linspace(-0.5, 2 * np.pi + 0.5, 60)
Xi, Yi = np.meshgrid(xi, yi, indexing="ij")


Zi = bilinear_interpolation(x, y, Z, xi, yi)

fig = plt.figure(figsize=(12, 5))
# Исходная функция
ax1 = fig.add_subplot(1, 2, 1, projection="3d")
ax1.plot_surface(X, Y, Z, cmap="viridis", alpha=0.8)  # Поверхность
ax1.scatter(
    X.ravel(), Y.ravel(), Z.ravel(), color="red", s=20
)  #  ravel() для показа точек
ax1.set_title("Исходная функция (узлы сетки)")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("z")

# Интерполированная функция
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
ax2.plot_surface(Xi, Yi, Zi, cmap="viridis")
ax2.set_title("Билинейная интерполяция")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_zlabel("z")

plt.tight_layout()
plt.show()

# для одной точки
x_test = np.pi / 4
y_test = np.pi / 3
z_test = bilinear_interpolation(x, y, Z, x_test, y_test)
print(f"Инетрполированное значение ({x_test:.3f}, {y_test:.3f}): {z_test:.4f}")

(
    f"Фактическое значение ({x_test:.3f}, {y_test:.3f}): "
    f"{sin_cos_function(x_test, y_test):.4f}"
)
