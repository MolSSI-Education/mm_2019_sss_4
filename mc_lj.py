import mc_lj_potential as mc
import numpy as np
np.random.seed(123)
num_particles = 100
box_length = 10.0
coordinates =  mc.generate_initial_state(method = 'random', num_particles = num_particles, box_length = box_length)
#print(coordinates)
box = mc.Box(coordinates = coordinates, box_length = box_length)
#print(box.coordinates) 
mcs = mc.MCState(box1 = box, cutoff = 3.0)
total_pair_energy = mcs.calculate_total_pair_energy()
#print(total_pair_energy)
#print(mcs.calculate_tail_correction())
#print(mcs.calculate_unit_energy())
#print(mcs.get_particle_energy(0))

                                    
