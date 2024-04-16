import numpy as np
import matplotlib.pyplot as plt


# def dydt(t, y):
#     return -y





def euler(df, t0, f0, xrange=5, h = 0.2):
    t = [t0]
    y = [f0]

    for i in range(0, int(xrange / h)):
        t.append((i + 1) * h)
        y.append(y[i] + h * df(t[i], y[i]))

    return t, y


def runge_kutta(f, t0, f0, xrange=5, h=0.2):
    t = [t0]
    y = [f0]

    for i in range(0, int(xrange / h)):
        tn, yn = runge_kutta_step(f, t[i], y[i])

        t.append(tn)
        y.append(yn)

    return t, y


def runge_kutta_step(f, t, y, h=0.2):
    k1 = f(t, y)
    k2 = f(t + h/2, y + h*k1/2)
    k3 = f(t + h/2, y + h*k2/2)
    k4 = f(t + h,   y + h*k3)

    return t+h, y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)


def rk_shm(t0, v0, x0, y0, h=0.2):
    kx1 = dx(v0)
    kp1 = dv(x0, y0)
    kx2 = dx(v0 + h*kp1/2)
    kp2 = dv(x0 + h*kx1/2, y0)
    kx3 = dx(v0 + h*kp2/2)
    kp3 = dv(x0 + h*kx2/2, y0)
    kx4 = dx(v0 + h*kp3)
    kp4 = dv(x0 + h*kp3, y0)

    x1 = x0 + (h/6) * (kx1 + 2*kx2 + 2*kx3 + kx4)
    v1 = v0 + (h/6) * (kp1 + 2*kp2 + 2*kp3 + kp4)

    return t0 + h, x1, v1


def dx(v):
    return v


def dv(x, y):
    d = np.sqrt(x*x + y*y)
    return -1/d/d * (x/d)


t = [0]
x = [2]
y = [0]
vx = [0]
vy = [1]

xrange = 1*np.pi
h = 0.2
for i in range(0, int(xrange / h)):
    r = np.sqrt(x[i]*x[i] + y[i] * y[i])
    tn, xn, vn = rk_shm(t[i], vx[i], x[i], y[i])
    t.append(tn)
    vx.append(vn)
    x.append(xn)
    tn, yn, vn = rk_shm(t[i], vy[i], y[i], y[i])
    y.append(xn)
    vy.append(vn)


plt.figure(figsize=(6, 6))
# plt.xlim(-2, 2)
# plt.ylim(-2, 2)
plt.plot(x, y)
plt.scatter([0], [0])
# t, y = euler(dydt, 0, 2)
# plt.plot(t, y, label='euler')
# t, y = runge_kutta(dydt, 0, 2)
# plt.plot(t, y, label='runge-kutta')
plt.grid(True)
# plt.legend()
plt.show()
