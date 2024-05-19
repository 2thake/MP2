# %%
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import planet
from planet import Planet, place_planet
from planet_acceleration import calc_force
from initial_value_solver import  RungeKutta4_v1, ABM_4
from body_problem import r_values, calculating_C
import csv 
import os

AU = 149597870700 # astronomical unit in meters

# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
#The following shows the creation of the planets. These values are intial conditions with values from the link above.
v_mw = 400000000/AU# * 60 * 60 # m/s
jupiter = Planet("Jupiter", 1.898e27, [2.657301572545939E+00, 4.244832633235739E+00, -7.706081756999565E-02], [-6.480998680299733E-03, 4.362422858591558E-03, 1.268648293569800E-04+v_mw], radius=2000000*69911/AU, texture= os.path.join("textures", "Jupiter_2k.png"))
# jupiter = Planet("Jupiter", 1.898e27, [2.660511872500166e+00, 4.246331340893854e+00, -7.683955467163552e-02], [-5.923603532402550e-03, 3.369365015933616e-03, 2.621050098384081e-05], radius=10000000*69911/AU, texture= os.path.join("textures", "Jupiter_2k.png"))
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

# bary_distance = r_values(mass, distance)
C_val = calculating_C(mass)

vector = np.concatenate((distance[3:], velocity)) #not including the sun mass
Storage = RungeKutta4_v1(vector, 0.5, N, C_val)
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


# print(jupiter.position)
initial4 =  RungeKutta4_v1(vector, 0.025, 4, C_val)
#print(ABM_4(initial4, 0.025, 40, C_val))


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
