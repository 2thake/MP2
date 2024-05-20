# %%
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# %%
p1 = np.array([0, 1])
p2 = np.array([4, 4])

points_x = [1, 4, 4]
points_y = [2, 3, 6]

# %%
sun = np.array([2, 3])

def find_dist(p1, p2):
    return np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)

def point_line_distance(x0, y0, x1, y1, x2, y2):
    """Calculate the perpendicular distance from a point to a line."""
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    return numerator / denominator

def furthest_point_distance(x_points, y_points, line_start, line_end):
    """Find the distance from the line to the furthest point in arrays."""
    distances = [point_line_distance(x, y, line_start[0], line_start[1], line_end[0], line_end[1])
                 for x, y in zip(x_points, y_points)]
    max_distance = np.max(distances)
    return max_distance

closest_dist = np.inf
furthest_dist = 0

for i in range(0, len(points_x)):
    dist = find_dist([points_x[i], points_y[i]], sun)
    # print(dist)
    if dist < closest_dist:
        p1 = np.array([points_x[i], points_y[i]])
        closest_dist = dist
    if dist > furthest_dist:
        p2 = np.array([points_x[i], points_y[i]])
        furthest_dist = dist

print(p1, p2)

dist = p2-p1

dist_sq = dist*dist
a = np.sqrt(sum(dist_sq)) / 2
b = furthest_point_distance(points_x, points_y, p1, p2)

rotation_angle = np.arctan(dist[1]/dist[0])

# Calculating the distance from the center to the foci
c = np.sqrt(a**2 - b**2)
# Coordinates of the foci
foci_x = [a+c, a-c]
foci_y = [0, 0]

# Parametric equations for the ellipse
theta = np.linspace(0, 2 * np.pi, 100)
x = a * np.cos(theta) + a
y = b * np.sin(theta)

R = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)],
              [np.sin(rotation_angle),  np.cos(rotation_angle)]])

xy_rotated = R @ np.array([x, y])
x = xy_rotated[0] + p1[0]
y = xy_rotated[1] + p1[1]

foci_rotated = R @ np.array([foci_x, foci_y])
foci_x = foci_rotated[0] + p1[0]
foci_y = foci_rotated[1] + p1[1]

# Plotting the ellipse and the foci
plt.figure(figsize=(8, 6))
plt.plot(x, y)
plt.scatter([sun[0]], [sun[1]], marker='x')
plt.scatter(foci_x, foci_y)
plt.scatter(points_x, points_y)
plt.scatter(points_x, points_y)
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.grid(color='gray', linestyle='--', linewidth=0.5)
plt.legend()
plt.axis('equal')  # Ensures the aspect ratio is equal
plt.show()