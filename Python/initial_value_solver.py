from planet import Planet, place_planet
from planet_acceleration import calc_force

def EulersMethod(planet, planets, h):
    planet.position += planet.velocity * h#calculating new position by multiplying the velocity by the time step
    force = calc_force(planet, planets, 0) #Calculating the acceleration
    planet.velocity += force * h #updating the planets velocity by multiplyinh the force byt the timestep
    
    return planet.position

def RungeKutta4_v1(planet, planets, h):
    # Calculate acceleration
    k1_a = calc_force(planet, planets, 0)
    k2_a = calc_force(planet, planets, 0.5 *  k1_a)
    k3_a = calc_force(planet, planets,0.5 *  k2_a)
    k4_a = calc_force(planet, planets, k3_a)

    # Find new velocity and update
    planet.velocity +=(k1_a + 2 * k2_a + 2 * k3_a + k4_a) / 6*h

    # Calculate velocity
    k1_v = planet.velocity
    k2_v = planet.velocity + (0.5 *  k1_v)
    k3_v = planet.velocity + (0.5 * k2_v)
    k4_v = planet.velocity + (k3_v)

    # Find new position and update   
    planet.position += (k1_v + 2 * k2_v + 2 * k3_v + k4_v) / 6 *h  

    return planet.position