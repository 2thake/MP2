# %%
import numpy as np
import planet
from planet import Planet
from animation import animate
from initial_value_solver import  RungeKutta4_v1, ABM_4
from body_problem import calculating_C
import os

AU = 149597870700 # astronomical unit in meters

# https://nssdc.gsfc.nasa.gov/planetary/factsheet/
#The following shows the creation of the planets. These values are intial conditions with values from the link above.
scale = 3000000
jupiter = Planet("Jupiter", 1.898e27, [2.657301572545939E+00, 4.244832633235739E+00, -7.706081756999565E-02], [-6.480998680299733E-03, 4.362422858591558E-03, 1.268648293569800E-04], radius=scale*69911/AU, texture= os.path.join("textures", "Jupiter_2k.png"))
saturn  = Planet("Saturn", 5.683e+26, [9.211655736771199E+00, -2.998507001947348E+00, -3.146252679038145E-01], [1.415075980682737E-03, 5.293746502200081E-03, -1.483576235830070E-04], radius=scale*58232/AU, texture=os.path.join("textures", "Saturn_2k.png"))
sun     = Planet("Sun", 1.989e30, [-7.225998149491247E-03, -3.805650685824385E-03, 2.018536538194618E-04], [5.902551462508057E-06, -5.950748571015161E-06, -7.997101158836507E-08], radius=scale/7*6.9634e5/AU, texture=os.path.join("textures", "Sun_2k.png")) # the sun here is assumed to start at zero postion
uranus  = Planet("Uranus", 8.681e25, [1.183100464891022E+01, 1.560581328660078E+01, -9.531293561809405E-02], [-3.163272718481608E-03, 2.192851241912579E-03, 4.915878565000892E-05], radius=scale*2*25362/AU, texture=os.path.join("textures", "Uranus_2k.png"))
neptune = Planet("Neptune", 1.024e+26, [2.985499980827878E+01, -1.358647720327443E+00 , -6.600608487568795E-01], [1.220565817760229E-04, 3.154546893302934E-03, -6.780559909533712E-05], radius=scale*2*24624/AU, texture=os.path.join("textures", "Neptune_2k.png"))

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

N = 2000
distance = np.concatenate(distance).tolist()
velocity = np.concatenate(velocity).tolist()

# Calculating C
C_val = calculating_C(mass)

# Concatenating vector
vector = np.concatenate((distance[3:], velocity)) #not including the sun mass
# print("HIGH")
# print(C_val)
#Applying Runge kutta 
Storage = RungeKutta4_v1(vector, 0.5, N, C_val)

#Applying Adam-Bashfourth Moulton
initial4 =  RungeKutta4_v1(vector, 0.25, 4, C_val) #Initial 4 using Runge Kutta to put into ABM
Storage = ABM_4(initial4, 100, N, C_val)

animate(Storage, planets)