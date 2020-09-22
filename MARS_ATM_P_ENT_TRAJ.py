# -*- coding: utf-8 -*-
"""
Created on Thu Sep 17 12:21:23 2020

@author: Mikhail LaMay
"""
# Modules
import pandas as pd
import matplotlib.pyplot as plt
from numpy import diff
import numpy as np
import math

# Open's MARS_ATM_P_ENT_TRAJ_v2.txt & RR Variables
#with open('MARS_ATM_P_ENT_TRAJ.txt', 'r') as reader:
    # Read & print the entire file
    #print(reader.read())
df = pd.read_csv('MARS_ATM_P_ENT_TRAJ_v2.txt', sep='\t', lineterminator='\n')
#print(df)

# Variables
time = df['t(s)']                                   # sec
alt = df['Alt(m)']                                  # m
vel = df['Vel(m/s)']                                # m/s
gamma = df['Gamma']                                 # degree    
den = df['Den(kg/m^3)\r']                           # kg/m^3

G = 3.711                                           # m/s^2
R_Mars = 3389.5e3                                   # m
Mass_Pr = 300                                       # kg
Area_Pr = 3.14                                      # m^2


# Re - Entry

# Dynamic Pressue
q = (den * vel**2) / 2                              # Pa

# Acceleration
x = df['t(s)']                                      # s
y = df['Vel(m/s)']                                  # m/s
#accel = np.diff(y)/np.diff(x)                      # m/s^2
accel = -1*(y.diff())
#accel_corrected = np.insert(accel,0,[0])
#print(accel_corrected)

# Force
F = (Mass_Pr * accel)                                 # N @ alt

# Weight
G_alt = G * (R_Mars**2)/((R_Mars + alt)**2)         # m/s^2 @ alt
W_alt = G_alt * Mass_Pr                             # N @ alt

# Drag Coefficient
gamma_rad = np.deg2rad(gamma)
C_1 = np.sin(gamma_rad)
C_2 = np.cos(2*gamma_rad)


A = 2*W_alt*C_1
B = np.sqrt(2)
C = np.sqrt(np.absolute((2*(F**2) - (W_alt**2)*(C_2) - (W_alt**2))))
D = den * vel**2 * Area_Pr

C_D = -1* ((A - (B * C)) / D)
print(C_D)
#C_D = (2*W_alt * C_1 - ((np.sqrt(2)*np.sqrt((2*F**2) - ((W_alt**2) * C_2) - W_alt))) / (den * vel**2 * Area_Pr)

#gamma_rad = np.deg2rad(gamma)


time_accel = plt.plot(time, accel)
plt.show(time_accel)

# Re-Entry Trajectory Plot
#df.plot(kind='scatter', x='t(s)', y='Alt(m)')
#plt.show()