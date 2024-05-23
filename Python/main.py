# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import planet
from planet import Planet, place_planet
from planet_acceleration import calc_force
from initial_value_solver import  RungeKutta4_v1, ABM_4
from body_problem import r_values, calculating_C
from num_quadrature import find_dA
import os

AU = 149597870700 # astronomical unit in meters

# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
#The following shows the creation of the planets. These values are intial conditions with values from the link above.
v_mw = 0# * 60 * 60 # m/s
jupiter = Planet("Jupiter", 1.898e27, [2.657301572545939E+00, 4.244832633235739E+00, -7.706081756999565E-02], [-6.480998680299733E-03, 4.362422858591558E-03, 1.268648293569800E-04+v_mw], radius=2000000*69911/AU, texture= os.path.join("textures", "Jupiter_2k.png"))
saturn  = Planet("Saturn", 5.683e+26, [9.211655736771199E+00, -2.998507001947348E+00, -3.146252679038145E-01], [1.415075980682737E-03, 5.293746502200081E-03, -1.483576235830070E-04+v_mw], radius=2000000*58232/AU, texture=os.path.join("textures", "Saturn_2k.png"))
sun     = Planet("Sun", 1.989e30, [-7.225998149491247E-03, -3.805650685824385E-03, 2.018536538194618E-04], [5.902551462508057E-06, -5.950748571015161E-06, -7.997101158836507E-08+v_mw], radius=500000*6.9634e5/AU, texture=os.path.join("textures", "Venus_2k.png")) # the sun here is assumed to start at zero postion
uranus  = Planet("Uranus", 8.681e25, [1.183100464891022E+01, 1.560581328660078E+01, -9.531293561809405E-02], [-3.163272718481608E-03, 2.192851241912579E-03, 4.915878565000892E-05+v_mw], radius=2000000*25362/AU, texture=os.path.join("textures", "Uranus_2k.png"))
neptune = Planet("Neptune", 1.024e+26, [2.985499980827878E+01, -1.358647720327443E+00 , -6.600608487568795E-01], [1.220565817760229E-04, 3.154546893302934E-03, -6.780559909533712E-05+v_mw], radius=2000000*24624/AU, texture=os.path.join("textures", "Neptune_2k.png"))

# Storing the created planets into a list named planets
planets = [
    sun,
    jupiter,
    saturn,
    uranus,
    neptune
]

mass = [sun.mass, jupiter.mass, saturn.mass, uranus.mass, neptune.mass]
distance = [sun.position, jupiter.position, saturn.position, uranus.position, neptune.position]
velocity = [jupiter.velocity, saturn.velocity, uranus.velocity, neptune.velocity]

N=10000
distance = np.concatenate(distance).tolist()
velocity = np.concatenate(velocity).tolist()

#Calculating C
C_val = calculating_C(mass)

#Concatenating vector
vector = np.concatenate((distance[3:], velocity)) #not including the sun mass
print("HIGH")
print(C_val)
#Applying Runge kutta 
Storage = RungeKutta4_v1(vector, 0.5, N, C_val)

#Applying Adam-Bashfourth Moulton
# initial4 =  RungeKutta4_v1(vector, 0.05, 4, C_val) #Initial 4 using Runge Kutta to put into ABM
# Storage = ABM_4(initial4, 0.5, N, C_val)

i = 0
j = 12
sun_values = 0.5 * np.arange(N)
for planet in planets:

    if planet == sun:
        continue
        # planet.position = planet.position + (planet.velocity * sun_values.reshape((-1,1)))
    else:
        planet.position = np.vstack((Storage[i,N-1], Storage[i+1,N-1], Storage[i+2,N-1]))
        planet.velocity = np.vstack((Storage[j,N-1], Storage[j+1,N-1], Storage[j+2,N-1]))
        i += 3
        j += 3

max_orbit = 0 #initialising max orbit to 0
               #This accounts for the maximum deviation from the centre of the planets orbits
for planet in planets: #iterating through all of the planets and calculating the euclidian distance, if this passes the max, set as new max
    d = np.linalg.norm(planet.position)
    if d > max_orbit:
        max_orbit = d
max_orbit = np.max(neptune.position)

# max_t = 20000000000 # maximum time 
# h = 1000000 #time step

#Initial Value Problem
for j, planet in enumerate(planets):
   for i in range(0, N):
        planet.path.append(Storage[0+3*j:3+3*j, i])  
        # RungeKutta4_v1(planet, planets, h)
        # planet.position = EulersMethod(planet, planets, h)

fig = plt.figure(figsize=[8, 8])
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1,1,1])
ax.set_xlim(-max_orbit, max_orbit)
ax.set_ylim(-max_orbit, max_orbit)
ax.set_zlim(-max_orbit, max_orbit)
ax.grid(False)
plt.title('Solar System')

for planet in planets:
    transpose = np.transpose(planet.path)
    ax.plot(transpose[0], transpose[1], transpose[2])
    place_planet(planet.radius, planet.texture, ax, planet.position, 60)
plt.show()
# %%

# %%
p1 = np.array([0, 1])
p2 = np.array([4, 4])

points_x = Storage[0]
points_y = Storage[1]

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

# print(p1, p2)

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
