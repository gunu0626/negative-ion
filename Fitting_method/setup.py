import numpy as np

### PROBE SETUP ###
H_FACTOR = 0.6 # h-factor
PROBE_RADIUS = 25e-6 # probe radius [m]
PROBE_LENGTH = 6e-3 # probe length [m]
PROBE_AREA = 2*np.pi*PROBE_RADIUS*PROBE_LENGTH + 2*np.pi*PROBE_RADIUS**2 # probe surface area [m2]

### PHYSICAL CONSTANTS ###
ELECTRON_CHARGE = 1.6e-19 # electron charge [C]
EPSILON_0 = 8.854e-12 # permittivity of vacuum [F/m]
BOLTZMANN_CONST = 1.38e-23 #Bolzmann const [kg m2/s2/K]
POSITIVE_ION_MASS= 127*1.67e-27 # mass of positive ion [kg] SF5+
NEGATIVE_ION_MASS = 127*1.67e-27 # mass of negative ion [kg] SF5-
ELECTRON_MASS = 9.11e-31 # mass of electron [kg]