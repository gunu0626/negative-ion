#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np

#######################
## Physical Constant ##
#######################

e = 1.6e-19 # electron charge [C]
epsilon_0 = 8.854e-12 # permittivity of vacuum [F/m]
kB = 1.38e-23 #Bolzmann const [kg m2/s2/K]
Mp = 127*1.67e-27 # mass of positive ion [kg] SF5+
Mn = 127*1.67e-27 # mass of negative ion [kg] SF5-
Me = 9.11e-31 # mass of electron [kg]
hr = 0.6 # h-factor
rp = 25e-6 # probe radius [m]
lp = 6e-3 # probe length [m]
Ap = 2*np.pi*lp*rp + 2*np.pi*rp**2 # probe surface area[m2]

