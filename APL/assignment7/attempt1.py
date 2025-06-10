import numpy as np
import matplotlib.pyplot as plt

s = np.loadtxt("rx3.txt")
Nmics, Nsamp = s.shape
src = (0,0)

#spacing between microphones
pitch = 0.1

#proxy for sampling rate
dist_per_samp = 0.1

#speed of sound 
C = 2.0

SincP = 5       #sincP = 1 we get the first figure sincP = 5, we get the second figure

mics = [(0, i*pitch) for i in range(1, Nmics + 1)]
obstacle = (3, 3)

sampling_rate = C/dist_per_samp

def wsrc(t):
    return np.sinc(SincP*t)

def dist(src, pt, mic):
    #distance from src to pt
    d1 = np.sqrt((src[0]-pt[0])**2 + (src[1]-pt[1])**2)
    #distance from mic to pt
    d2 = np.sqrt((mic[0]-pt[0])**2 + (mic[1]-pt[1])**2)

    return d1 + d2

x_axis = np.linspace(0, 200/sampling_rate, 200)
#print(mics)
#plt.plot(x_axis, wsrc(x_axis))
for i in range(1, len(mics) + 1):
    plt.plot(x_axis, pitch*wsrc(x_axis- dist(src, obstacle, mics[i-1])/C)  - i*pitch)
plt.show()