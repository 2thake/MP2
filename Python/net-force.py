# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# %%
class Planet:
    name = ""
    mass = 0
    position = [0, 0, 0]
    velocity = [0, 0, 0]

    def __init__(self, name, mass, position, velocity):
        self.name = name
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity) * 1.1
        self.path = []

    def print_params(self):
        print(self.name, self.mass, self.position, self.velocity)


# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
v_mw = 0 #720000 # m/s
jupiter = Planet("Jupiter", 1.898e27, [778.5e13, 0, 0], [0, 13.1e6, v_mw])
saturn  = Planet("Saturn", 5.683e+26, [0.0, 1432.0e13, 0], [-9.7e6, 0, v_mw])
sun     = Planet("Sun", 1.989e30, [0.0, 0, 0], [0.0, 0, v_mw])
uranus  = Planet("Uranus", 86.8e24, [2867.0e13, 0.0, 0.0], [0.0, 6.8e6, v_mw])
neptune = Planet("Neptune", 102e24, [4515.0e13, 0.0, 0.0], [0.0, 64.7e5 / 1.1, v_mw])
planets = [
    jupiter,
    saturn,
    sun,
    uranus,
    neptune
]


def calc_force(planet_obj, planets):
    total_force = np.array([0.0, 0.0, 0.0])
    for planet in planets:
        if planet != planet_obj:
            position = planet.position - planet_obj.position
            direction = normalize(position)
            distance = np.linalg.norm(position)
            total_force += direction * planet.mass / (distance * distance)
    return total_force


def normalize(v):
    mag = np.linalg.norm(v)
    if mag == 0:
        return v
    return v/mag


max_orbit = 0
for planet in planets:
    d = np.linalg.norm(planet.position) * 1.5
    if d > max_orbit:
        max_orbit = d
# max_orbit = np.max(neptune.position) * 1.5

max_t = 40000000000
h = 100000000
for i in range(0, int(max_t/h)):
    for planet in planets:
        planet.path.append(planet.position.copy())
        planet.position += planet.velocity * h
        force = calc_force(planet, planets)
        planet.velocity += force * h



fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

plt.figure(figsize=[6, 6])
for planet in planets:
    transpose = np.transpose(planet.path)
    ax.plot(transpose[0], transpose[1], transpose[2])


plt.show()

# plt.plot(np.transpose(sun.path)[0])
# plt.show()

