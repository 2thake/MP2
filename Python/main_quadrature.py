# %%
import numpy as np
import planet
from planet import Planet
# from animation import animate
from initial_value_solver import  RungeKutta4_v1, ABM_4
from body_problem import calculating_C
from num_quadrature_copy import find_dA, triangle_area
import num_quadrature_copy as quad
import matplotlib.pyplot as plt
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

N = 1000
H = 50
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
Storage = ABM_4(initial4, H, N, C_val)


def truncate_path(path, sun_pos, orbital_period, h):
    diff = path[0] - sun_pos
    threshold_angle = 2*np.pi*H/orbital_period
    theta_init = np.arctan2(diff[1], diff[0])
    for i in range(10, len(path)):
        diff = path[i]-sun_pos
        theta = np.arctan2(diff[1], diff[0])
        if np.isclose(theta, theta_init, atol=threshold_angle) and theta < theta_init:
            end_index = i
            break
    
    return path# [:end_index]

sun_2D = np.array([sun.position[0], sun.position[1]])
# sun_2D = np.array([0, 0])



names = ['Jupiter', 'Saturn', 'Uranus', 'Neptune']
orbital_periods = [11.86*365, 29.4*365, 84.0*365, 165.0*365]


paths = []
for i in range(len(names)):
    path = np.array([Storage[3*i], Storage[3*i+1]]).transpose()
    path = truncate_path(path, sun_2D, orbital_periods[i], H)
    paths.append(path)

areas = []
areas_euler = []
# semi_majors = []
for j in range(0, len(names)):
    area_slice = []
    area_slice_euler = []
    semi_major, _ = quad.find_ellipse_axes(paths[j])
    # semi_majors.append(semi_major)
    for i in range(5, int((len(paths[j])-2)/2)):
        area_slice.append(find_dA(sun_2D, paths[j][2*i], paths[j][2*i+1], paths[j][2*i+2]))
        dA_euler = 0
        dA_euler += triangle_area(sun_2D, paths[j][2*i], paths[j][2*i+1])
        dA_euler += triangle_area(sun_2D, paths[j][2*i+2], paths[j][2*i+1])
        area_slice_euler.append(dA_euler)
    areas.append(area_slice)
    areas_euler.append(area_slice_euler)


# plt.plot(np.power(orbital_periods, 2), np.power(semi_majors, 3), 'r-')
# for i in range(0, 4):
#     plt.plot([np.power(np.abs(orbital_periods[i]), 2)], [np.power(semi_majors[i], 3)], 'o', label=names[i])



# plt.title('Verification of Kepler\'s Third Law')
# plt.xlabel('Square of the Orbital Period')
# plt.ylabel('Cube of the Semi-Major Axis')
# plt.legend()
# plt.show()


for i in range(0, len(names)):
    plt.plot(areas[i]-areas[i][0], '-', label=names[i])
    # plt.plot(np.linspace(0, 1, len(areas[i])), areas_euler[i], 'x-', label=names[i])


max_dev = []
max_dev_euler = []
for i in range(0, len(names)):
    max_dev_euler.append(max(areas_euler[i]) - min(areas_euler[i]))
    max_dev.append(max(areas[i]) - min(areas[i]))

print("Max Variation in Areas:")
for i in range(0, len(names)):
    print(names[i]+':')
    print("Euler:", max_dev_euler[i])
    print("Simpson\'s:", max_dev[i])

print("Ratio of Deviations (Euler/Simpson)")
for i, j, p in zip(max_dev_euler, max_dev, names):
    print(p+':', i/j)

plt.title(f'Variation in Area Traced by Each Planet in each {H}-Day Timestep')
plt.ylabel(r'Area ($AU^2$)')
plt.xlabel(r'Timestep (n)')
plt.legend(loc='lower right')
# plt.ylim(0, max([max(ar) for ar in areas])*1.2)
scale = 100
# plt.ylim(min(areas_euler[2])-1/scale, max(areas[2])+1/scale)
plt.ylim(-1/scale, 1/scale)
plt.show()


# %%
