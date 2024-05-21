# %%
import numpy as np
import matplotlib.pyplot as plt


# %%

sun = np.array([0, 0])

theta = np.linspace(0, 2*np.pi, 9)

x = np.cos(theta)
y = np.sin(theta)

ps = np.array([x, y]).transpose()

# %%

def simpsons_rule(a, b, c):
    x0, y0 = a
    x1, y1 = b
    x2, y2 = c

    h = (x2 - x0) / 2

    area = (h / 3) * (y0 + 4 * y1 + y2)

    A = np.array([
        [a[0]**2, a[0], 1],
        [b[0]**2, b[0], 1],
        [c[0]**2, c[0], 1]
    ])
    y = np.array([a[1], b[1], c[1]])
    coefficients = np.linalg.solve(A, y)
    def quadratic(x):
        return coefficients[0]*x**2 + coefficients[1]*x + coefficients[2]
    
    x_simpson = np.linspace(a[0], c[0], 100)
    y_simpson = quadratic(x_simpson)
    plt.plot(x_simpson, y_simpson, 'r--', label="Simpson's Rule Polynomial")
    
    return area


def plot_triangle(v1, v2, v3):
    x = [v1[0], v2[0], v3[0], v1[0]]
    y = [v1[1], v2[1], v3[1], v1[1]]
    plt.plot(x, y, 'r-')
    plt.fill(x, y, 'r', alpha=0.5)

# %%


def simpsons_area(p1, p2, p3):
    return (p3[0]-p1[0])/6 * (p1[1] + 4*p2[1] + p3[1])

def triangle_area(v1, v2, v3):
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2)



area = simpsons_area(ps[2], ps[1], ps[0]) - ps[2][1]*ps[0][0]/2
tri_area = triangle_area(sun, ps[0], ps[2])

print("Simpsons Rule:")
print(area + tri_area)

print("Analytical Solution:")
print(np.pi/4)


# %%

def simpsons_rule(a, b, c):
    x0, y0 = a
    x1, y1 = b
    x2, y2 = c

    h = (x2 - x0) / 2

    area = (h / 3) * (y0 + 4 * y1 + y2)
    
    # Calculate coefficients of the quadratic polynomial
    A = np.array([
        [a[0]**2, a[0], 1],
        [c[0]**2, c[0], 1],
        [b[0]**2, b[0], 1]
    ])
    y = np.array([a[1], c[1], b[1]])
    coefficients = np.linalg.solve(A, y)
    
    # Define the quadratic polynomial
    def quadratic(x):
        return coefficients[0]*x**2 + coefficients[1]*x + coefficients[2]
    
    # Plot the quadratic polynomial
    x_simpson = np.linspace(a[0], b[0], 100)
    y_simpson = quadratic(x_simpson)
    plt.plot(x_simpson, y_simpson, 'r--', label="Simpson's Rule Polynomial")
    
    return area

a = (0, 0)
b = (2, 0)
c = (1, 1)

area = simpsons_rule(a, b, c)
print("Area below the points:", area)

plt.xlabel('X')
plt.ylabel('Y')
plt.title('Simpson\'s Rule Approximation')
plt.legend()
plt.grid(True)
plt.show()


# %%

# sample unit circle path to show the area comes out to pi
sun = np.array([0, 0])

N = 100
theta = np.linspace(0, 2*np.pi, N)

x = np.cos(theta)
y = np.sin(theta)

ps = np.array([x, y]).transpose()

# %%
def triangle_area(v1, v2, v3):
    x1, y1 = v1
    x2, y2 = v2
    x3, y3 = v3
    return abs((x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2)) / 2)

def find_area(sun_path, path, start, end): 
    start = int(start)
    end = int(end)
    area = 0
    focus = path[start:end]
    for i in range(end-start):
        area += triangle_area(sun_path[i], path[i], path[i+1])
    
    return area

sun_path = [sun for i in range(N)]

# finding the area of 1 quarter of the path. comes out to pi/4
print(find_area(sun_path, ps, 0, N/4-1))