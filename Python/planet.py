# %%
import numpy as np
import os
import matplotlib.pyplot as plt

# Class that represent planets
class Planet:
    # Contructs the planet based on what has been initial given
    def __init__(self, name, mass, position, velocity, radius, texture):
        self.name = name
        self.mass = mass
        self.position = np.array(position)
        self.velocity = np.array(velocity)  
        self.path = []
        self.texture = texture
        self.radius = radius
    
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
    plot.plot_surface(x.T, y.T, z.T, facecolors=img, cstride=1, rstride=1, shade=True, edgecolor='none', alpha=0.5) # we've already pruned ourselves
    # plt.show()