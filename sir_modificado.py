# -*- coding: utf-8 -*-
"""SIR_modificado

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jQ6bWMzdNdmRSsmv1Kfr_UbtkOjHndgb
"""

import numpy as np
from numpy import linalg
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Total population, N.
N = 200000000
# número inicial de infectados e mortos
I0, M0 = 1, 0
# Everyone else, S0, is susceptible to infection initially.
S0 = N - I0 - M0
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
#beta, gamma = 1.0E-3,1.0E-3 
# A grid of time points (in days)
xdata = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35])
ydata = np.array([1,1,1,2,2,2,2,3,8,13,25,25,25,34,52,77,98,98,98,234,291,428,621,978,1178,1604,1960,2271,2555,2988,3477,3928,4313,4661,5786])
mortos =np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,4,7,11,18,25,34,47,59,77,93,113,139,165,200])
t = np.linspace(start = 1, stop = 35, num = 35)

print(t)
print(ydata.shape[0])

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, M = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dMdt = gamma * I
    return dSdt, dIdt, dMdt

def obj(x):
  y0 = S0, I0, M0
  ret = odeint(deriv, y0, t, args=(N, x[0], x[1]))
  S, I, M = ret.T  
  return linalg.norm(I-ydata) +linalg.norm(M-mortos)

x0 = np.array([10,10])
result = minimize(obj, x0, method='Nelder-Mead', tol=1e-7)
print(result.fun,result.x)

beta = result.x[0]
gamma = result.x[1]
# Initial conditions vector
y0 = S0, I0, M0
#time
t2 = np.linspace(start = 1, stop = 32, num = 32)
ret = odeint(deriv, y0, t, args=(N, beta, gamma))
S, I, M = ret.T
print(t)
print(t2)
print(I)
print()
print(M)
print(mortos)
print(np.sum(M))

# Plot the data on three separate curves for S(t), I(t) and M(t)
fig = plt.figure(facecolor='w')
ax = fig.add_subplot(111, axisbelow=True)
#ax.plot(t, S/N, 'b', alpha=0.5, lw=2, label='Susceptible')
ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infectado S')
ax.plot(t, M, 'g', alpha=0.5, lw=2, label='Morto S')
ax.plot(t, ydata, 'b', alpha=0.5, lw=2, label='Infectado R')
ax.plot(t, mortos, 'p', alpha=0.5, lw=2, label='Morto R')
ax.set_xlabel('Tempo /dias')
ax.set_ylabel('Núúmero de pessoas')
#ax.set_ylim(0,1.2)
ax.yaxis.set_tick_params(length=0)
ax.xaxis.set_tick_params(length=0)
ax.grid(b=True, which='major', c='w', lw=2, ls='-')
legend = ax.legend()
legend.get_frame().set_alpha(0.5)
for spine in ('top', 'right', 'bottom', 'left'):
    ax.spines[spine].set_visible(False)
plt.show()

