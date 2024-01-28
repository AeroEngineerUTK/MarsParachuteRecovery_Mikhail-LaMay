# -*- coding: utf-8 -*-

# Author: Mikhail LaMay

# --------------------------------------------------------------------
# MARS_ATM_P_ENT_TRAJ contains scripts to read MARS_ATM_P_ENT_TRAJ.txt
# and perform various calculations for MARS probe Re-Entry. It is used
# seperatley from Spacecraft_Reentry_Trajectory_Code.pynb and differs
# with it being a sandbox for calculations.
# --------------------------------------------------------------------




#pyspread is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyspread is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyspread.  If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------


# Enter Below Functions Used Within This Python Script
"""

**Provides**

* :func: ' ': 

"""

# Define Libraries
import numpy as np
from numpy import diff
import pandas as pd
import matplotlib.pyplot as plt

# Define Debug Variables
printData_Active = False
printOutput_Active = False

# --------------------------------------------------------------------
# Accessing Mars Atmospheric Model
""" Atmopsheric Model Variables:
    
    t(s)
    Alt(m)
    Vel(m/s)
    Gamma
    Den(kg/m^3)

"""
# --------------------------------------------------------------------

# Open MARS_ATM_P_ENT_TRAJ.txt and Print To Terminal
if printData_Active:
    with open('MARS_ATM_P_ENT_TRAJ.txt', 'r') as reader:
        print(reader.read())

# Read MARS_ATM_P_ENT_TRAJ.txt into a DataFrame
dataFrame = pd.read_csv('MARS_ATM_P_ENT_TRAJ.txt', sep='\t', lineterminator='\n')
#print(dataFrame)

# Define Variables From MARS_ATM_P_ENT_TRAJ.txt
time = dataFrame['t(s)']    # time(sec)
alt = dataFrame['Alt(m)']   # altitude(m)
vel = dataFrame['Vel(m/s)'] # velocity(m/s)
gamma = dataFrame['Gamma']  # gamma(degree)    
den = dataFrame['Den(kg/m^3)\r']    # density(kg/m^3)

# Define Constants
G = 3.711   # gravity(m/s^2)
R_Mars = 3389.5e3   # Mar's Radius(m)
Mass_Pr = 300   # ProbeMass(kg)
Area_Pr = 3.14  # ProbeArea(m^2)

# --------------------------------------------------------------------
# Re-entry Calculations
# --------------------------------------------------------------------

# Calculate Dynamic Pressue
q = (den*(vel**2))/2  # Pa

# Calculate Acceleration
def acceleration(velocity):

    acceleration = -1*(velocity.diff())    # m/s^2

    return acceleration
accel_Pr = acceleration(vel)    # m/s^2

# Calculate Force
def Force(Mass_Probe,acceleration):

    Force = Mass_Probe * acceleration    # N @ alt
    
    return Force
F = Force(Mass_Pr, accel_Pr)    # N @ alt

# Calculate Gravity
G_alt = G * (R_Mars**2)/((R_Mars + alt)**2)         # m/s^2 @ alt

# Calculate Weight of Probe
W_alt = G_alt * Mass_Pr                             # N @ alt

# Calculate Drag Coefficient
gamma_rad = np.deg2rad(gamma)
C_1 = np.sin(gamma_rad)
C_2 = np.cos(2*gamma_rad)
C_3 = 2*W_alt*C_1
C_4 = np.sqrt(2)
C_5 = np.sqrt(np.absolute((2*(F**2) - (W_alt**2)*(C_2) - (W_alt**2))))
C_6 = den * vel**2 * Area_Pr
C_D = (-1* ((C_3 - (C_4 * C_5)) / C_6)) #C_D @ Alt

if printOutput_Active:
    print("----Dynamic Pressure----")
    print(q)
    print("----Re-Entry Probe Acceleration----")
    print(accel_Pr)
    print("----Re-Entry Probe Force----")
    print(F)
    print("----Re-Entry Mars Gravity----")
    print(G_alt)
    print("----Re-Entry Weight of Probe---")
    print(W_alt)
    print("----Drag Coefficient----")
    print(C_D)

# --------------------------------------------------------------------
# Plot Data
# --------------------------------------------------------------------

# Clean Up Time/Acceleration Data From NAN Data
updatedTime = time.drop(index=0)
updatedAccel = accel_Pr.drop(index=0)

# Plot Acceleration v. Time
plt.figure()
plt.plot(updatedTime,updatedAccel, 'g')
plt.xlabel('Time, s', fontsize=10)
plt.ylabel('Acceleration, m/s^2', fontsize=10)
plt.show()