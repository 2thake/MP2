# %%
import numpy as np
import matplotlib.pyplot as plt

# %%

import numpy as np

def rotate_points(x, y, rad):
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    x_new = cos_a * np.array(x) - sin_a * np.array(y)
    y_new = sin_a * np.array(x) + cos_a * np.array(y)
    return x_new.tolist(), y_new.tolist()

# %%

# Define a quadratic function that fits the specified points
def quadratic_function_adjusted(x, p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    # Solve for the coefficients of the quadratic function y = ax^2 + bx + c
    A = np.array([
        [x1**2, x1, 1],
        [x2**2, x2, 1],
        [x3**2, x3, 1]
    ])
    b = np.array([y1, y2, y3])
    a, b, c = np.linalg.solve(A, b)
    
    return a * x**2 + b * x + c

# Parameters for the ellipse
a_ellipse = 1.5  # Major axis
b_ellipse = 1.0  # Minor axis
N = 9  # Number of points

# Parametric equations for the ellipse
theta_ellipse = np.linspace(0, 2 * np.pi, N)
x_ellipse = a_ellipse * np.cos(theta_ellipse)
y_ellipse = b_ellipse * np.sin(theta_ellipse)

# Adjusted points for the quadratic function
p1_ellipse_adjusted = (-a_ellipse * np.cos(np.pi / 4), b_ellipse * np.sin(np.pi / 4))  # Point between the leftmost and the topmost
p2_ellipse_adjusted = (0, b_ellipse)  # Topmost point
p3_ellipse_adjusted = (a_ellipse * np.cos(np.pi / 4), b_ellipse * np.sin(np.pi / 4))  # Point between the rightmost and the topmost



# x values for the quadratic function plot
x_quad_ellipse_adjusted = np.linspace(p1_ellipse_adjusted[0], p3_ellipse_adjusted[0], 100)
y_quad_ellipse_adjusted = quadratic_function_adjusted(x_quad_ellipse_adjusted, p1_ellipse_adjusted, p2_ellipse_adjusted, p3_ellipse_adjusted)

# Calculate the foci of the ellipse
c = np.sqrt(a_ellipse**2 - b_ellipse**2)  # Distance from center to each focus
focus1 = (c, 0)
focus2 = (-c, 0)

# Use one of the foci as the vertex of the blue triangle
focus_vertex = focus1

# Coordinates for the blue triangle with one focus as the vertex
triangle_x_focus = [focus_vertex[0], p1_ellipse_adjusted[0], p3_ellipse_adjusted[0], focus_vertex[0]]
triangle_y_focus = [focus_vertex[1], p1_ellipse_adjusted[1], p3_ellipse_adjusted[1], focus_vertex[1]]

# Plot the ellipse and the approximations with the quadratic function using adjusted points
# Add the blue triangle with an outline and remove the yellow background in the ellipse
plt.figure(figsize=(10, 6))

theta = 0 #-np.pi/4

print(x_ellipse)
x_ellipse, y_ellipse = rotate_points(x_ellipse, y_ellipse, theta)
print(x_ellipse)
plt.plot(x_ellipse, y_ellipse, label="Ellipse")

x_quad_ellipse_adjusted, y_quad_ellipse_adjusted = rotate_points(x_quad_ellipse_adjusted, y_quad_ellipse_adjusted, theta)
plt.plot(x_quad_ellipse_adjusted, y_quad_ellipse_adjusted, color='green')
plt.scatter(x_ellipse, y_ellipse, color='red')

triangle_x_focus, triangle_y_focus = rotate_points(triangle_x_focus, triangle_y_focus, theta)
plt.fill(triangle_x_focus, triangle_y_focus, color='blue', alpha=0.3, edgecolor='black', linewidth=1)

plt.title("Approximating the Area of an Ellipse Using Simpson's Rule")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.grid(True)
plt.axis('equal')
plt.show()
