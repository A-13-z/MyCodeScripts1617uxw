import numpy as np
import time
import cython

def trap(f, a, b, n):
    res = 0
    for i in range(1, n+1):
        x1 = a + (i-1)*(b-a)/n
        x2 = a + i*(b-a)/n

        y1, y2 = f(x1), f(x2)
        res += 0.5*(x2 - x1)*(y1 + y2)

    return res

def f1(x):
    return x**2

def trap(f, a, b, n):
    res = 0
    for i in range(1, n+1):
        x1 = a + (i-1)*(b-a)/n
        x2 = a + i*(b-a)/n

        y1, y2 = f(x1), f(x2)
        res += 0.5*(x2 - x1)*(y1 + y2)

    return res
trap(f1, 0, 10, 10**7)
