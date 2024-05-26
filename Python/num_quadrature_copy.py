# %%

import numpy as np
import matplotlib.pyplot as plt
import math

# %%

if __name__ == '__main__':
    def rotate_points(x, y, rad):
        cos_a, sin_a = np.cos(rad), np.sin(rad)
        x_new = cos_a * np.array(x) - sin_a * np.array(y)
        y_new = sin_a * np.array(x) + cos_a * np.array(y)
        return x_new.tolist(), y_new.tolist()

    # sample unit circle path to show the area comes out to pi

    N = 9
    theta = np.linspace(0, 2*np.pi, N)

    a = 1.5
    b = 1
    c = np.sqrt(a*a-b*b)

    x = a*np.cos(theta)
    y = b*np.sin(theta)

    # x, y = rotate_points(x, y, np.pi/4)

    # sun = np.array([c, 0])
    sun = np.array([1, 0])

    ps = np.array([x, y]).transpose()

# %%

def triangle_area(v1, v2, v3):
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2)

# rotate 3 vectors so the middle one points directly upwards. Simpson rule can be applied after this
def rotate_to_x_axis(p1, p2, p3):
    diff = p3-p1
    angle = math.atan2(diff[0], diff[1]) + np.pi/2
    
    return [rotate_vector(p1, angle), rotate_vector(p2, angle), rotate_vector(p3, angle)]

# function to simply rotate a vector by an angle
def rotate_vector(vector, angle):
    x, y = vector
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    return (x * cos_theta - y * sin_theta, x * sin_theta + y * cos_theta)

def perpendicular_distance(v1, v2, v3):
    line_vec = np.array(v2) - np.array(v1)
    point_vec = np.array(v3) - np.array(v1)
    proj_len = np.dot(point_vec, line_vec) / np.sqrt(np.dot(line_vec, line_vec))
    proj_vec = (proj_len / np.sqrt(np.dot(line_vec, line_vec))) * line_vec
    dist_vec = point_vec - proj_vec
    return np.sqrt(np.dot(dist_vec, dist_vec))

def distance_between_vectors(v1, v2):
    diff_vec = np.array(v2) - np.array(v1)
    return np.sqrt(np.dot(diff_vec, diff_vec))


# function to calculate Simpson's rule. Vectors are split so default values can be included.
# all values default to zero
def simpsons_area(x1=0, x2=0, x3=0, y1=0, y2=0, y3=0):
    return np.abs(x3-x1)/6 * (y1 + 4*y2 + y3)


# Final function: putting it all together
# finds the area of the triangle between the three points, along with the area under simpsons curve using
# his rule, and a trapezoid which is below that curve.
# subtracts the trapezoid from the sum of Simpsons rule and 
def find_dA(sun, p1, p2, p3):
    d1 = distance_between_vectors(p1, p2)
    d2 = perpendicular_distance(p1, p2, p3)
    triangle = triangle_area(sun, p1, p3)
    simpsons = simpsons_area(x1=-d1/2, y2=d2, x3=d1/2)

    return triangle + simpsons

def find_tot_area(sun, path):
    tot_area = 0
    for i in range(0, int(N/2)):
        tot_area += find_dA(sun, ps[2*i], ps[2*i+1], ps[2*i+2])

def furthest_point_from_line(v1, v2, points):
    distances = [perpendicular_distance(v1, v2, point) for point in points]
    max_index = np.argmax(distances)
    return points[max_index], distances[max_index]


def furthest_points(points):
    max_distance = 0
    point_pair = (points[0], points[1])
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = distance_between_vectors(points[i], points[j])
            if dist > max_distance:
                max_distance = dist
                point_pair = (points[i], points[j])
    return point_pair, max_distance

def find_ellipse_axes(points):
    vertices, semi_major = furthest_points(points)
    _, semi_minor = furthest_point_from_line(vertices[0], vertices[1], points)
    return semi_major/2, semi_minor

def points_x_units_away(point1, point2, x):
    midpoint = ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)
    dir_vector1 = (point1[0] - midpoint[0], point1[1] - midpoint[1])
    dir_vector2 = (point2[0] - midpoint[0], point2[1] - midpoint[1])
    length1 = np.sqrt(dir_vector1[0]**2 + dir_vector1[1]**2)
    length2 = np.sqrt(dir_vector2[0]**2 + dir_vector2[1]**2)
    unit_vector1 = (dir_vector1[0] / length1, dir_vector1[1] / length1)
    unit_vector2 = (dir_vector2[0] / length2, dir_vector2[1] / length2)
    displacement1 = (unit_vector1[0] * x, unit_vector1[1] * x)
    displacement2 = (unit_vector2[0] * x, unit_vector2[1] * x)
    final_point1 = (midpoint[0] + displacement1[0], midpoint[1] + displacement1[1])
    final_point2 = (midpoint[0] + displacement2[0], midpoint[1] + displacement2[1])
    return [final_point1, final_point2]

def find_foci(path):
    vertices, semi_major = furthest_points(path)
    semi_major /= 2
    _, semi_minor = furthest_point_from_line(vertices[0], vertices[1], path)
    c = np.sqrt(semi_major*semi_major - semi_minor*semi_minor)

    return points_x_units_away(vertices[0], vertices[1], c)

def dist_to_closest_focus(sun, path):
    foci = np.array(find_foci(path))
    d0 = distance_between_vectors(sun, foci[0])
    d1 = distance_between_vectors(sun, foci[1])

    if d0 < d1:
        return d0
    else:
        return d1





if __name__ == '__main__':
    # print(triangle_area(sun, ps[0], ps[1])*2)
    # sample usage, find the area of the entire circle. Just as accurate with 100 samples as with 10 samples :)
    tot_area = 0
    tot_area_euler = 0
    for i in range(0, int(N/2)):
        tot_area += find_dA(sun, ps[2*i], ps[2*i+1], ps[2*i+2])
        tot_area_euler += triangle_area(sun, ps[2*i], ps[2*i+1])
        tot_area_euler += triangle_area(sun, ps[2*i+1], ps[2*i+2])

    vertices, semi_major = furthest_points(ps)
    semi_major /= 2
    _, semi_minor = furthest_point_from_line(vertices[0], vertices[1], ps)
    # print(semi_minor, semi_major)
    c = np.sqrt(semi_major*semi_major - semi_minor*semi_minor)

    # print(c)

    # print(points_x_units_away(vertices[0], vertices[1], c))

    print(find_foci(ps))
    print(dist_to_closest_focus(sun, ps))

    

    

    # h, j = furthest_points(ps)
    # print(h, j)
    # print(furthest_point_from_line(h[0], h[1], ps))



    # print(f'Number of samples: {N-1}')
    # print("Area of the ellipse:", (np.pi*a*b))
    # print("Approximation using Simpson's rule:", tot_area)
    # print("Approximation using Euler's Method Exclusively:", tot_area_euler)
    # print("Accuracy:", (tot_area/np.pi/a/b * 100), "%")
    # print("Exclusive Euler Accuracy:", tot_area_euler/np.pi/a/b * 100, "%")

    # plt.scatter(sun[0], sun[1])
    # plt.axis('equal')
    # plt.plot(ps.transpose()[0], ps.transpose()[1])
    # plt.show()

