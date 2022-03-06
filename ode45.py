# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 19:56:28 2021

@author: Connor
"""
import numpy as np

def ode45_step(f, x, t, dt, *args):
    """
    One step of 4th Order Runge-Kutta method
    """
    k1 = dt * f(t, x, *args)
    k2 = dt * f(t + 0.5*dt, x + 0.5*k1, *args)
    k3 = dt * f(t + 0.5*dt, x + 0.5*k2, *args)
    k4 = dt * f(t + dt, x + k3, *args)
    return x + 1/6. * (k1 + 2*k2 + 2*k3 + k4)

def ode45(f, t, x0, *args):
    """
    4th Order Runge-Kutta method
    """
    n = len(t)
    x = np.zeros((n, len(x0)))
    x[0] = x0
    for i in range(n-1):
        dt = t[i+1] - t[i] 
        x[i+1] = ode45_step(f, x[i], t[i], dt, *args)
    return x
