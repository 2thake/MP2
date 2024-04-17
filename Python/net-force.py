# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# %%Class that represents the planet
class Planet:
    name = "" #name of plane
    mass = 0 #intial mass
    position = [0, 0, 0] #initial position of planet
    velocity = [0, 0, 0] #initial velocity of the planet

    # Contructs the planet based on what has been initial given
    def __init__(self, name, mass, position, velocity, radius=142984000/2, texture='Venus_2k.png'):
        self.name = name
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity) * 1.1 #scaling velocity by 1.1. After some experimentation, this value worked best
        self.path = []
        self.texture = texture
        self.radius = radius

    def print_params(self):
        print(self.name, self.mass, self.position, self.velocity)

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

# This function calulates the total gravitations force acting on a given planet 
# It takes in two arguments:
#   - planet_obj = the planet that werecalcualting gravitational force for
#   - planets - A list of all the planets, as previously defined above
def calc_force(planet_obj, planets):
    total_force = np.array([0.0, 0.0, 0.0]) #Initialising the total force
    G = 6.67430e-11 #gravitational constant
    for planet in planets: #iterating through all the other planets (only calculate the force wtr to curretn planet)
        if planet != planet_obj: 
            position = planet.position - planet_obj.position #Position of the planet of interest wit respect to the other planets
            direction = normalize(position) #Fidningnthe direction by finding the unit vecotr 
            distance = np.linalg.norm(position) #findign the distance by finding the magnitude of the positios
           # total_force += direction * planet.mass / (distance * distance) # 
            total_force += G*direction * planet.mass / (distance * distance) # 
    return total_force

# performs normalization on a vector
#id rather call this unit vecotr actually
def normalize(v):
    mag = np.linalg.norm(v)
    if mag == 0:
        return v
    return v/mag

#Plotting planet onto a 3D surface 
#This function takes in 5 arguments
#   -R = radius of the planet in question 
#   -image = texture image of the planet in question
#   -plot = 
#   -position = The position of the coneter of the planet which has been initialised to zero
#   -count = Number of points to sample (QUESTION: is this two cylces of neptune??)
def place_planet(R, image, plot, position=[0,0,0], count=180):
    img = plt.imread(image) #Reading the 

    # define a grid matching the map size, subsample along with pixels
    # These are grids covering the spherical coordinate space.
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


max_orbit = 0 #initialising max orbit to 0
              #This accounts for the maximum deviation from the centre of the planets orbits
for planet in planets: #iterating through all of the planets and calculating the euclidian distance, if this passes the max, set as new max
    d = np.linalg.norm(planet.position)
    if d > max_orbit:
        max_orbit = d
# max_orbit = np.max(neptune.position) * 1.5

max_t = 20000000000 # maximum time 
h = 1000000 #time step

#for each time step
for i in range(0, int(max_t/h)):
    for planet in planets:
        planet.path.append(planet.position.copy())#appending the new position of the planet into planet path
        planet.position += planet.velocity * h#calculating new position by multiplying the velocity by the time step
        force = calc_force(planet, planets) #Calculating the acceleration
        planet.velocity += force * h #updating the planets velocity by multiplyinh the force byt the timestep


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
