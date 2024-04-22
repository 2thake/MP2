import numpy as np

# performs normalization on a vector
#id rather call this unit vecotr actually
def normalize(v):
    mag = np.linalg.norm(v)
    if mag == 0:
        return v
    return v/mag

# This function calulates the total gravitations force acting on a given planet 
# It takes in two arguments:
#   - planet_obj = the planet that werecalcualting gravitational force for
#   - planets - A list of all the planets, as previously defined above
def calc_force(planet_obj, planets, update):

    total_force = np.array([0.0, 0.0, 0.0]) #Initialising the total force
    G = 6.67430e-11 #gravitational constant

    total_force += update

    for planet in planets: #iterating through all the other planets (only calculate the force wtr to curretn planet)
        if planet != planet_obj: 
            position = (planet.position - planet_obj.position)#Position of the planet of interest wit respect to the other planets
            direction = normalize(position) #Fidningnthe direction by finding the unit vecotr 
            distance = np.linalg.norm(position)#findign the distance by finding the magnitude of the positios
            total_force += ((direction * planet.mass / (distance * distance)))# 
#            total_force += G*direction * planet.mass / (distance * distance) # 
    
    return total_force
