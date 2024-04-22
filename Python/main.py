# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import planet
from planet import Planet, place_planet
from planet_movement import calc_force
from initial_value_solver import  RungeKutta4_v1, EulersMethod

# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
#The following shows the creation of the planets. These values are intial conditions with values from the link above.
v_mw = 720000# * 60 * 60 # m/s
jupiter = Planet("Jupiter", 1.898e27, [778.5e13, 0, 0], [0, 13.1e6, v_mw], radius=1.42984e8/2, texture='Jupiter_2k.png')
saturn  = Planet("Saturn", 5.683e+26, [0.0, 1432.0e13, 0], [-9.7e6, 0, v_mw], radius=1.20536e8/2, texture='Saturn_2k.png')
sun     = Planet("Sun", 1.989e30, [0.0, 0, 0], [0.0, 0, v_mw], radius=6.96e8, texture='Venus_2k.png') # the sun here is assumed to start at zero postion
uranus  = Planet("Uranus", 86.8e24, [2867.0e13, 0.0, 0.0], [0.0, 6.8e6, v_mw], radius=5.1e7/2, texture='Uranus_2k.png')
neptune = Planet("Neptune", 102e24, [4515.0e13, 0.0, 0.0], [0.0, 64.7e5 / 1.1, v_mw], radius=4.95e7/2, texture='Neptune_2k.png')

# Storing the created planets into a list named planets
planets = [
    jupiter,
    saturn,
    uranus,
    neptune,
    sun
]

max_orbit = 0 #initialising max orbit to 0
              #This accounts for the maximum deviation from the centre of the planets orbits
for planet in planets: #iterating through all of the planets and calculating the euclidian distance, if this passes the max, set as new max
    d = np.linalg.norm(planet.position)
    if d > max_orbit:
        max_orbit = d
# max_orbit = np.max(neptune.position) * 1.5

max_t = 20000000000 # maximum time 
h = 1000000 #time step

# Initial Value Problem
for i in range(0, int(max_t/h)):
    for planet in planets:
        planet.path.append(planet.position.copy())  
        # planet.position = RungeKutta4_v1(planet, planets, h)
        planet.position = EulersMethod(planet, planets, h)

fig = plt.figure(figsize=[8, 8])
ax = fig.add_subplot(111, projection='3d')
ax.set_box_aspect([1,1,1])
ax.set_xlim(-max_orbit, max_orbit)
ax.set_ylim(-max_orbit, max_orbit)
ax.set_zlim(-max_orbit, max_orbit)
ax.grid(False)
plt.title('Solar System')

plt.figure(figsize=[6, 6])
for planet in planets:
    transpose = np.transpose(planet.path)
    ax.plot(transpose[0], transpose[1], transpose[2])
    place_planet(planet.radius * 5000000, planet.texture, ax, planet.position, 60)
# %%

plt.show()