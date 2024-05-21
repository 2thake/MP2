# %%

import numpy as np
import matplotlib.pyplot as plt

# %%

# sample unit circle path to show the area comes out to pi
sun = np.array([0, 0])

N = 100
theta = np.linspace(0, 2*np.pi, N)

x = np.cos(theta)
y = np.sin(theta)

ps = np.array([x, y]).transpose()

# %%
def triangle_area(v1, v2, v3):
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2)

def find_area(sun_path, path, start, end): 
    start = int(start)
    end = int(end)
    area = 0
    focus = path[start:end]
    for i in range(end-start):
        area += triangle_area(sun_path[i], path[i], path[i+1])
    
    return area

sun_path = [sun for i in range(N)]

# finding the area of 1 quarter of the path. comes out to pi/4
print(find_area(sun_path, ps, 0, N/4-1))