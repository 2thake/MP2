import numpy as np

#This might be a boy problem

def body_problem(vector, C):
    F = np.zeros(24)
    F[0:11] = vector[12:23]  # Velocity components

    for n in np.arange(int(np.sqrt(len(C))+1)):
        r = np.linalg.norm(vector[3*n:2+3*n])  # Distance
        F[12+3*n:14+n*3] = np.sum(- (C[4*n:3+4*n] / (r**3))) * vector[3*n:2+3*n] # Acceleration components
    return F

# C = 2.953485975463116e-04
# vector = np.array([
#     -5.109860226922701, -1.892671882214539, 0.122138159013022,  # Position components (replace with actual values if needed)
#     2.533876190218832, -6.718255014466351, -0.028731841357519   # Velocity components (replace with actual values if needed)
# ])
# body_problem(vector, C)

def calculating_C(M):
    C = []
    AU = 149597870700
    TU = 86400
    G = 6.67430e-11

    for reference_planet in range(len(M)-1):
        for planet in range(len(M)):
            if reference_planet == planet:
                continue
            else:
                C.append(((G * M[reference_planet]) * (TU ** 2) / (((M[planet] / M[reference_planet]) + 1) ** 2)) / (AU ** 3))
    return C

M = [1.98855e30, 1.898e27, 3, 4, 5]
test = calculating_C(M)
# print(len(test))
# print(test)

import numpy as np

def r_values(M, distance_vec):
    M = np.array(M)
    distance_vec = np.array(distance_vec)
    
    sum1 = np.sum(M * distance_vec[::3])
    sum2 = np.sum(M * distance_vec[1::3])
    sum3 = np.sum(M * distance_vec[2::3])

    sum_mass = np.sum(M)

    x_bary = sum1 / sum_mass
    y_bary = sum2 / sum_mass
    z_bary = sum3 / sum_mass

    bary_coord = np.array([x_bary, y_bary, z_bary])

    result_array = []
    truncated = [distance_vec[i:i+3] for i in range(0,len(distance_vec),3)]
    for subset in truncated:
        result_array.extend(subset - bary_coord)

    return np.array(result_array)

# M = [1.98855e30, 1.898e27, 3, 4, 5]  # Example masses
# d = [1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]  # Example distance vector

# b = r_values(M, d)
# print("Modified Distance Vector:", b)
