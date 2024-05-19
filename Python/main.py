# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import planet
from planet import Planet, place_planet
from planet_acceleration import calc_force
from initial_value_solver import  RungeKutta4_v1, EulersMethod
from body_problem import r_values, calculating_C

# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
#The following shows the creation of the planets. These values are intial conditions with values from the link above.
v_mw = 720000# * 60 * 60 # m/s
jupiter = Planet("Jupiter", 1.898e27, [2.660511872500166e+00, 4.246331340893854e+00, -7.683955467163552e-02], [-5.923603532402550e-03, 3.369365015933616e-03, 2.621050098384081e-05], radius=69911, texture='Jupiter_2k.png')
saturn  = Planet("Saturn", 5.683e+26, [9.214866036725425, -2.997008294289234, -3.144040050054544e-01], [1.972471128579921e-03, 4.300688659542139e-03, -2.490119519561464e-04], radius=58232, texture='Saturn_2k.png')
sun     = Planet("Sun", 1.989e30, [0.0, 0, 0], [0.0, 0, v_mw], radius=6.96e8, texture='Venus_2k.png') # the sun here is assumed to start at zero postion
uranus  = Planet("Uranus", 8.681e25, [1.18342149488644e+01, 1.560731199425889e+01, -9.509167271973212e-02], [-2.605877570584423e-03, 1.19979339925463e-03, -5.149554272313025e-05], radius=25362, texture='Uranus_2k.png')
neptune = Planet("Neptune", 1.024e+26, [2.985821010823300E+01, -1.357149012669329E+00, -6.598395858585192E-01], [6.794517296732074E-04, 2.161489050644991E-03, -1.684599274684762E-04], radius=24624, texture='Neptune_2k.png')

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
velocity = [jupiter.position, saturn.position, uranus.position, neptune.position]

distance = np.concatenate(distance).tolist()
velocity = np.concatenate(velocity).tolist()

bary_distance = r_values(mass, distance)
C_val = calculating_C(mass)
vector = np.concatenate((bary_distance[3:], velocity)) #not including the sun mass
print(RungeKutta4_v1(vector, 1, 5, C_val))

# max_orbit = 0 #initialising max orbit to 0
#               #This accounts for the maximum deviation from the centre of the planets orbits
# for planet in planets: #iterating through all of the planets and calculating the euclidian distance, if this passes the max, set as new max
#     d = np.linalg.norm(planet.position)
#     if d > max_orbit:
#         max_orbit = d
# # max_orbit = np.max(neptune.position) *  5

# max_t = 20000000000 # maximum time 
# h = 1000000 #time step

# # Initial Value Problem
# for i in range(0, int(max_t/h)):
#     for planet in planets:
#         planet.path.append(planet.position.copy())  
#         RungeKutta4_v1(planet, planets, h)
#         # planet.position = EulersMethod(planet, planets, h)

# fig = plt.figure(figsize=[8, 8])
# ax = fig.add_subplot(111, projection='3d')
# ax.set_box_aspect([1,1,1])
# ax.set_xlim(-max_orbit, max_orbit)
# ax.set_ylim(-max_orbit, max_orbit)
# ax.set_zlim(-max_orbit, max_orbit)
# ax.grid(False)
# plt.title('Solar System')

# plt.figure(figsize=[6, 6])
# for planet in planets:
#     transpose = np.transpose(planet.path)
#     ax.plot(transpose[0], transpose[1], transpose[2])
#     place_planet(planet.radius * 5000000, planet.texture, ax, planet.position, 60)
# # %%

# plt.show()