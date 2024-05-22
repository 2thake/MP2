# %%

import numpy as np
import matplotlib.pyplot as plt
import math

# %%

# sample unit circle path to show the area comes out to pi
sun = np.array([0, 0])

N = 100
theta = np.linspace(0, 2*np.pi, N)

x = np.cos(theta)
y = np.sin(theta)

ps = np.array([x, y]).transpose()

# %%


# dont remember what I even wrote this for
# def find_area(sun_path, path, start, end): 
#     start = int(start)
#     end = int(end)
#     area = 0
#     focus = path[start:end]
#     for i in range(end-start):
#         area += triangle_area(sun_path[i], path[i], path[i+1])
    
#     return area


# dont remember what I wrote this for either
# def find_area_simpsons(sun_path, path, start_ind, end_ind):
#     start = int(start)
#     end = int(end)
#     area = 0
#     focus = path[start_ind:end_ind]
#     for i in range(end-start):
#         area += triangle_area(sun_path[i], path[i], path[i+1])


# old unused version of the rotate_to_y_axis function
# def rotate_vectors(v1, v2, v3):
#     angle = np.arctan2(v2[0], v2[1])
#     print(angle)
#     rotation_matrix = np.array([[np.cos(-angle), -np.sin(-angle)], [np.sin(-angle), np.cos(-angle)]])
#     return [np.dot(rotation_matrix, v1), np.dot(rotation_matrix, v2), np.dot(rotation_matrix, v3)]

def calculate_angle(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def triangle_area(v1, v2, v3):
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2)

# rotate 3 vectors so the middle one points directly upwards. Simpson rule can be applied after this
def rotate_to_y_axis(p1, p2, p3):
    angle = math.atan2(p2[0], p2[1])
    
    p1p = rotate_vector(p1, angle)
    p2p = rotate_vector(p2, angle)
    p3p = rotate_vector(p3, angle)
    
    return [rotate_vector(p1, angle), rotate_vector(p2, angle), rotate_vector(p3, angle)]

# function to simply rotate a vector by an angle
def rotate_vector(vector, angle):
    x, y = vector
    cos_theta = math.cos(angle)
    sin_theta = math.sin(angle)
    return (x * cos_theta - y * sin_theta, x * sin_theta + y * cos_theta)

# points need to be in a certain order here: left to right. I'll fix this later
def simpsons_area(p1, p2, p3):
    return (p3[0]-p1[0])/6 * (p1[1] + 4*p2[1] + p3[1])

# Final function: putting it all together
# finds the area of the triangle between the three points, along with the area under simpsons curve using
# his rule, and a trapezoid which is below that curve.
# subtracts the trapezoid from the sum of Simpsons rule and 
def find_dA(sun, p1, p2, p3):
    result = rotate_to_y_axis(p1 - sun, p2 - sun, p3 - sun)
    triangle = triangle_area(sun, p1, p3)
    simpsons = simpsons_area(result[2], result[1], result[0])
    sq = np.abs((result[0][0]-result[2][0]) * min(result[0][1], result[2][1]))
    trapezoid = sq + np.abs((result[0][0]-result[2][0])*(result[0][1]-result[2][1])/2)

    return simpsons - trapezoid + triangle


# sample usage, find the area of the entire circle. Just as accurate with 100 samples as with 10 samples :)
tot_area = 0
for i in range(0, int(N/2)):
    tot_area += find_dA(sun, ps[i], ps[i+1], ps[i+2])

print(tot_area)


sun_path = [sun for i in range(N)]
