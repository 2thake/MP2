from planet import Planet, place_planet
from planet_movement import calc_force

def EulersMethod(planet, planets, h):
    planet.position += planet.velocity * h#calculating new position by multiplying the velocity by the time step
    force = calc_force(planet, planets, 0) #Calculating the acceleration
    planet.velocity += force * h #updating the planets velocity by multiplyinh the force byt the timestep
    
    return planet.position

def RungeKutta4_v1(planet, planets, h):
    k1_v = calc_force(planet, planets, 0)
    k2_v = calc_force(planet, planets, 0.5 *  k1_v)
    k3_v = calc_force(planet, planets,0.5 *  k2_v)
    k4_v = calc_force(planet, planets, k3_v)

    planet.velocity +=(k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6*h

    k1_p= planet.velocity
    k2_p = planet.velocity + (0.5 *  k1_p)
    k3_p = planet.velocity + (0.5 * k2_p)
    k4_p = planet.velocity + (k3_p)
            
    planet.position += (k1_p + 2 * k2_p + 2 * k3_p + k4_p) / 6 *h  

    return planet.position