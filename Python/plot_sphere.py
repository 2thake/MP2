# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from itertools import product, combinations
from matplotlib.colors import LightSource
from matplotlib.image import imread

# %%
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.set_aspect("equal")

# draw sphere
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_wireframe(x, y, z, color="r")

plt.show()


# Create a meshgrid for the spherical coordinates
phi = np.linspace(0, np.pi, 20)  # Azimuthal angle
theta = np.linspace(0, 2 * np.pi, 40)  # Polar angle
phi, theta = np.meshgrid(phi, theta)

# Convert spherical coordinates to Cartesian coordinates
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the mesh sphere
ax.plot_surface(x, y, z, color='b', alpha=0.5)

# Set the aspect ratio of the plot to be equal
ax.set_box_aspect([1,1,1])

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()

# %%

earth_texture = imread('Earth_4k.png')

# Create a meshgrid for the spherical coordinates
phi = np.linspace(0, np.pi, 20)  # Azimuthal angle
theta = np.linspace(0, 2 * np.pi, 40)  # Polar angle
phi, theta = np.meshgrid(phi, theta)

# Convert spherical coordinates to Cartesian coordinates
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a light source
ls = LightSource(azdeg=0, altdeg=45)

# Plot the mesh sphere with lighting
ax.plot_surface(x, y, z, rstride=1, cstride=1, color='b', alpha=1, facecolors=earth_texture)
# ax.plot_surface(x, y, z, color='b', alpha=0.5)

# Set the aspect ratio of the plot to be equal
ax.set_box_aspect([1,1,1])

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()

# %%

# Create a meshgrid for the spherical coordinates
phi = np.linspace(0, np.pi, 20)  # Azimuthal angle
theta = np.linspace(0, 2 * np.pi, 40)  # Polar angle
phi, theta = np.meshgrid(phi, theta)

# Convert spherical coordinates to Cartesian coordinates
x = np.sin(phi) * np.cos(theta)
y = np.sin(phi) * np.sin(theta)
z = np.cos(phi)

# Load the texture image
earth_texture = imread('Earth_4k.png')  # Replace 'texture.png' with the path to your PNG image
plt.imshow(earth_texture)

# %%

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the mesh sphere with texture
ax.plot_surface(x, y, z, rstride=1, cstride=1, facecolors=earth_texture, alpha=0.5, 
                shade=False)

# Set the aspect ratio of the plot to be equal
ax.set_box_aspect([1, 1, 1])

# Set labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the plot
plt.show()


# %%
image = imread('Earth_4k.png')

plt.imshow(image)

# %%
img = plt.imread('Jupiter_2k.png')

# define a grid matching the map size, subsample along with pixels
theta = np.linspace(0, np.pi, img.shape[0])
phi = np.linspace(0, 2*np.pi, img.shape[1])

count = 180 # keep 180 points along theta and phi
theta_inds = np.linspace(0, img.shape[0] - 1, count).round().astype(int)
phi_inds = np.linspace(0, img.shape[1] - 1, count).round().astype(int)
theta = theta[theta_inds]
phi = phi[phi_inds]
img = img[np.ix_(theta_inds, phi_inds)]

theta,phi = np.meshgrid(theta, phi)
R = 2

# sphere
x = R * np.sin(theta) * np.cos(phi)
y = R * np.sin(theta) * np.sin(phi)
z = R * np.cos(theta)

z += 1


# %%
# create 3d Axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x.T, y.T, z.T, facecolors=img, cstride=1, rstride=1, shade=True, edgecolor='none', alpha=1) # we've already pruned ourselves

# make the plot more spherical
ax.axis('scaled')

# %%
def place_planet(R, image, position=[0,0,0], count=20):
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
    R = 1

    # sphere
    x = R * np.sin(theta) * np.cos(phi)
    y = R * np.sin(theta) * np.sin(phi)
    z = R * np.cos(theta)

    x += position[0]
    y += position[1]
    z += position[2]

    # create 3d Axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x.T, y.T, z.T, facecolors=img, cstride=1, rstride=1, shade=True, edgecolor='none', alpha=1) # we've already pruned ourselves

    # make the plot more spherical
    ax.axis('scaled')

# %%
place_planet(0.5, 'Jupiter_2k.png', [0, 5, 5])
