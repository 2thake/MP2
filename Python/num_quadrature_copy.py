# %%

import numpy as np
import matplotlib.pyplot as plt
import math

# %%
def rotate_points(x, y, rad):
    cos_a, sin_a = np.cos(rad), np.sin(rad)
    x_new = cos_a * np.array(x) - sin_a * np.array(y)
    y_new = sin_a * np.array(x) + cos_a * np.array(y)
    return x_new.tolist(), y_new.tolist()

# sample unit circle path to show the area comes out to pi

N = 101
theta = np.linspace(0, 2*np.pi, N)

a = 1
b = 1.5
c = np.sqrt(a*a+b*b)

x = a*np.cos(theta)
y = b*np.sin(theta)

x, y = rotate_points(x, y, np.pi/4)

sun = np.array([c, 0])

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

# points need to be in a certain order here: left to right. I'll fix this later
def simpsons_area(p1, p2, p3):
    return np.abs(p3[0]-p1[0])/6 * (p1[1] + 4*p2[1] + p3[1])

def rectangle_area(x, y):
    return x*y

# Final function: putting it all together
# finds the area of the triangle between the three points, along with the area under simpsons curve using
# his rule, and a trapezoid which is below that curve.
# subtracts the trapezoid from the sum of Simpsons rule and 
def find_dA(sun, p1, p2, p3):
    p1, p2, p3 = p1+sun, p2+sun, p3+sun
    result = rotate_to_x_axis(p1 - sun, p2 - sun, p3 - sun)
    triangle = triangle_area(sun, p1, p3)
    simpsons = simpsons_area(result[2], result[1], result[0])
    trapezoid = rectangle_area(np.abs(result[0][0]-result[2][0]), result[0][1])

    return triangle + simpsons - trapezoid


# print(triangle_area(sun, ps[0], ps[1])*2)
# sample usage, find the area of the entire circle. Just as accurate with 100 samples as with 10 samples :)
tot_area = 0
for i in range(0, int(N/2)):
    # print(ps[i])

    tot_area += find_dA(sun, ps[i], ps[i+1], ps[i+2])
    # v1, v2, v3 = ps[i] + sun, ps[i+1] + sun, ps[i+2] + sun
    # tot_area += find_dA(sun, v1, v2, v3)


print("Area of the ellipse:", (np.pi*a*b))
print("Approximation using Simpson's rule:", (tot_area))
print("Accuracy:", (tot_area/np.pi/a/b * 100), "%")

