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

    def __init__(self, name, mass, position, velocity, radius=142984000/2, texture='Venus_2k.png'):
        self.name = name
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity) * 1.1
        self.path = []
        self.texture = texture
        self.radius = radius

    def print_params(self):
        print(self.name, self.mass, self.position, self.velocity)


# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
v_mw = 0 #720000# * 60 * 60 # m/s
jupiter = Planet("Jupiter", 1.898e27, [778.5e13, 0, 0], [0, 13.1e6, v_mw], radius=1.42984e8/2, texture='Jupiter_2k.png')
saturn  = Planet("Saturn", 5.683e+26, [0.0, 1432.0e13, 0], [-9.7e6, 0, v_mw], radius=1.20536e8/2, texture='Saturn_2k.png')
sun     = Planet("Sun", 1.989e30, [0.0, 0, 0], [0.0, 0, v_mw], radius=6.96e8, texture='Venus_2k.png')
uranus  = Planet("Uranus", 86.8e24, [2867.0e13, 0.0, 0.0], [0.0, 6.8e6, v_mw], radius=5.1e7/2, texture='Uranus_2k.png')
neptune = Planet("Neptune", 102e24, [4515.0e13, 0.0, 0.0], [0.0, 64.7e5 / 1.1, v_mw], radius=4.95e7/2, texture='Neptune_2k.png')

planets = [
    jupiter,
    saturn,
    uranus,
    neptune,
    sun
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


def place_planet(R, image, plot, position=[0,0,0], count=20):
    img = plt.imread(image)

    # define a grid matching the map size, subsample along with pixels
    theta = np.linspace(0, np.pi, img.shape[0])
    phi = np.linspace(0, 2*np.pi, img.shape[1])

    theta_inds = np.linspace(0, img.shape[0] - 1, count).round().astype(int)
    phi_inds = np.linspace(0, img.shape[1] - 1, count).round().astype(int)
    theta = theta[theta_inds]
    phi = phi[phi_inds]
    img = img[np.ix_(theta_inds, phi_inds)]

    theta,phi = np.meshgrid(theta, phi)

    # sphere
    x = R * np.sin(theta) * np.cos(phi)
    y = R * np.sin(theta) * np.sin(phi)
    z = R * np.cos(theta)

    x += position[0]
    y += position[1]
    z += position[2]

    # create 3d Axes
    plot.plot_surface(x.T, y.T, z.T, facecolors=img, cstride=1, rstride=1, shade=True, edgecolor='none', alpha=1) # we've already pruned ourselves


max_orbit = 0
for planet in planets:
    d = np.linalg.norm(planet.position)
    if d > max_orbit:
        max_orbit = d*1.5
# max_orbit = np.max(neptune.position) * 1.5

max_t = 40000000000
h = 100000000
for i in range(0, int(max_t/h)):
    for planet in planets:
        planet.path.append(planet.position.copy())
        planet.position += planet.velocity * h
        force = calc_force(planet, planets)
        planet.velocity += force * h



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
    #ax.plot(transpose[0], transpose[1], transpose[2])
    place_planet(planet.radius * 5000000, planet.texture, ax, planet.position, 50)

