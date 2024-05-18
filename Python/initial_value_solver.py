from planet import Planet, place_planet
from planet_acceleration import calc_force

from body_problem import body_problem
import numpy as np

def EulersMethod(planet, planets, h):
    planet.position += planet.velocity * h#calculating new position by multiplying the velocity by the time step
    force = calc_force(planet, planets, 0) #Calculating the acceleration
    planet.velocity += force * h #updating the planets velocity by multiplyinh the force byt the timestep
    
    return planet.position

def RungeKutta4_v1(vec0, h, N, C):
    # Use fourth order Runge-Kutta to solve two-body problem with initial state vector vec0
    # Time step = h.
    # Number of steps taken = N.
    Storage = np.zeros((len(vec0), N))  # assign storage for N time steps of data
    v = vec0  # initial conditions
    Storage[:, 0] = v  # store initial time/position in Storage
    
    for count in range(1, N):
        tv = v  # set temporary variable, tv
        k1 = h * body_problem(tv, C)

        tv = v + (0.5 * k1)  # update tv
        k2 = h * body_problem(tv, C)
        
        tv = v + (0.5 * k2)  # update tv
        k3 = h * body_problem(tv, C)
        
        tv = v + k3  # update tv
        k4 = h * body_problem(tv, C)
        
        v = v + ((1/6) * (k1 + 2*k2 + 2*k3 + k4))  # update v
        Storage[:, count] = v  # store new position
    
    return Storage
