import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import math

def planck(t, c, h, kbt):
    t_ = [math.pow(i, 5) for i in t]
    return (2*h*c*c)/(t_*(np.exp(h*c/(np.multiply(kbt, t))) - 1))

def partial_planck1(t, c, h = 6.6*math.pow(10, -34), kbt = 5.53*math.pow(10, -20)):
    t_ = [math.pow(i, 5) for i in t]
    return (2*h*c*c)/(t_*(np.exp(h*c/(np.multiply(kbt, t))) - 1))

def partial_planck2(t, h, c = 3*math.pow(10, 8), kbt = 5.552*math.pow(10, -20)):
    t_ = [math.pow(i, 5) for i in t]
    return (2*h*c*c)/(t_*(np.exp(h*c/(np.multiply(kbt, t))) - 1))

def partial_planck3(t, kbt, h = 6.6*math.pow(10, -34), c = 3*math.pow(10, 8)):
    t_ = [math.pow(i, 5) for i in t]
    return (2*h*c*c)/(t_*(np.exp(h*c/(np.multiply(kbt, t))) - 1))

fle = open("d2.txt")
lnes = fle.readlines()
lbda = [float(i.split(',')[0]) for i in lnes]
b_val = [float(i.split(',')[-1][:-1]) for i in lnes]

# plt.plot(lbda, b_val)
# plt.show()

#popt, pcov = curve_fit(planck, lbda, b_val, p0=[3*math.pow(10, 8), 6.6*math.pow(10, -34), 4*math.pow(10, -20)])
popt, pcov = curve_fit(partial_planck3, lbda, b_val, p0 = [5*math.pow(10, -20)])
print(popt)
plt.plot(lbda, b_val)
plt.plot(lbda, partial_planck3(lbda, *popt))
plt.show()