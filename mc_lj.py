import mc_lj_potential as mc
import numpy as np
np.random.seed(123)
num_particles = 100
box_length = 10.0
coordinates =  mc.generate_initial_state(method = 'random', num_particles = num_particles, box_length = box_length)
print(coordinates)
mcs = mc.Box(coordinates = coordinates, box_length = box_length)
print(mcs.coordinates)                                     
