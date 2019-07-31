"""
mc_lj_potential.py
A python package for Monte Carlo simulation of Lennard Jones particles.

Handles the primary functions
"""


import numpy as np

class Box:
    def __init__(self, box_length, coordinates=None):
        self.box_length=box_length
        self.coordinates=coordinates
    def wrap(self, coordinates,box_length):
        """
        This is for wrapping all particles in the box, updating the coordinates.

        Parameters
        ----------
        coordinates : np.array
            Original coordinates from the generate_initial_state function.
        box_length : float
            Side of cubic simulation box.

        """
        if (coordinates is not None):
            self.coordinates = self.coordinates - self.box_length*np.round(self.coordinates/self.box_length)
    def minimum_image_distance(self, r_i, r_j, box_length):
        """
        Computes the minimum image distance between two particles.

        Parameters
        ----------
        r_i : float
            Position of particle i
        r_j : float
            Position of particle j
        box_length : float
            Side of cubic simulation box.

        Returns
        -------
        rij2 :  float
            Square of minimum image distance between an atom pair.
        """
        rij = r_i - r_j
        rij = rij - self.box_length * np.round(rij / self.box_length)
        rij2 = np.dot(rij, rij)
        return rij2
        
    @property
    def volume(self):
        """ Property decorator function which calculates the volume of the cubic simulation box.
        
        Parameters
        ----------
        box_length : float
            Side of cubic simulation box.
        
        Returns
        -------
        volume=box_length**3 : float
        """
        return self.box_length**3
    
    @property
    def num_particles(self):
        """ Property decorator function which calculates the number of particles in the cubic simulation box.
        
        Parameters
        ----------
        coordinates : np.array(num_particles,3)
            A numpy array with the x, y and z coordinates of each atom in the simulation box.
       
       Returns
        -------
        num_particles=number of particles in the simulation box : integer
        """
        if (isinstance(self.coordinates,type(None))):
            return None
        else:
            return len(self.coordinates)

    #self.box_length=np.cbrt(self.num_particles / reduced_density)
            
class MCState:
    def __init__(self,box1,cutoff):
        self.box1=box1
        self.cutoff=cutoff
        self.total_pair_energy=0.0
        self.particle_energy=0.0
        self.tail_correction=0.0
        self.unit_energy=0.0
    
    def calculate_total_pair_energy(self):
        """Computes the total energy of the system.
    
        Parameters
        ----------
        coordinates : np.array(num_particles,3)
            A numpy array with the x, y and z coordinates of each atom in the simulation box.
        box_length : float
            Side of cubic simulation box.
        cutoff2: float 
            Square of cutoff value for Lennard Jones potential.
        
        Returns
        -------
        e_total : float
            Total energy of the system.
        """
        self.total_pair_energy=0.0
        particle_count = len(self.box1.coordinates)
        for i_particle in range(particle_count):
            for j_particle in range(i_particle):
                r_i = self.box1.coordinates[i_particle]
                r_j = self.box1.coordinates[j_particle]
                rij2 = self.box1.minimum_image_distance(r_i, r_j, self.box1.box_length)
                if rij2 < self.cutoff**2:
                    self.total_pair_energy += self.lennard_jones_potential(rij2)
        return self.total_pair_energy
        
    def calculate_tail_correction(self):
        """
        Computes the standard tail correction for Lennard Jones potential.

        Parameters
        ----------
        box_length : float
            Side of cubic simulation box.
        cutoff : float
            Cutoff value for LJ potential.
        num_particles : integer
            Number of particles in the simulation box.

        Returns
        -------
        e_correction : float
            Energy correction term to compensate for Lennard Jones cutoff.
        """

        sig_by_cutoff3 = np.power(1.0 / self.cutoff, 3)
        sig_by_cutoff9 = np.power(sig_by_cutoff3, 3)
        self.tail_correction = sig_by_cutoff9 - 3.0 * sig_by_cutoff3
        self.tail_correction *= (8.0 / 9.0) * np.pi * self.box1.num_particles * self.box1.num_particles/ self.box1.volume
        return self.tail_correction

    def calculate_unit_energy(self):
        """
        Computes the unit energy per particle in the system.

        Parameters
        ----------
        total_pair_energy : float
            Total pair energy calculated by calculate_total_pair_energy().
        tail_correction : float
            Tail correction calculated by calculate_tail_correction()
        
        Returns
        -------
        unit_energy : float
            The total unit energy per particle.
        
        """
        self.unit_energy = (self.total_pair_energy + self.tail_correction)/self.box1.num_particles
        return self.unit_energy
    
    def get_particle_energy(self, i_particle):
        """
        Computes the energy of a particle with respect to the rest of the system.
    
        Parameters
        ----------
        coordinates : np.array(num_particles,3)
            A numpy array with the x, y and z coordinates of each atom in the simulation box.
        box_length : float
            Side of cubic simulation box.
        i_particle : integer
            Particle whose energy is computed.
        cutoff2: float 
            Square of cutoff value for Lennard Jones potential.
        
        Returns
        -------
        e_total : float
            Total energy of particle_i.
        """
        self.particle_energy = 0.0
        i_position = self.box1.coordinates[i_particle]
        particle_count = len(self.box1.coordinates)
        for j_particle in range(particle_count):
            if i_particle != j_particle:
                j_position = self.box1.coordinates[j_particle]
                rij2 = self.box1.minimum_image_distance(i_position, j_position, self.box1.box_length)
                if rij2 < self.cutoff**2:
                    e_pair = self.lennard_jones_potential(rij2) 
                    self.particle_energy += e_pair
        return self.particle_energy
    
    def lennard_jones_potential(self, rij2):
        """
        Computes the Lennard Jones potential between an atom pair.

        Parameters
        ----------
        rij2 : float
            Square of minimum image distance between an atom pair.

        Returns
        -------
        Lennard Jones potential : float
            Lennard Jones potential between an atom pair.    
        """
        
        sig_by_r6 = np.power(1 / rij2, 3)
        sig_by_r12 = np.power(sig_by_r6, 2)
        return 4.0 * (sig_by_r12  - sig_by_r6)
    
def generate_initial_state(method = 'random', file_name = None, num_particles = None, box_length = None):
    """ 
    Generates initial state of the system.

    Generates the initial coordinates of all the atoms in the simulation box. If the method is random, the atoms are assigned a random set of coordinates.
    If method is File, coordinates are loaded from a file.

    Parameters
    ----------
    method : string. Either 'random' or 'file'.
        Flag which is either set to random or file depending on whether we need random coordinates or load coordinates from a file.
    file_name :  string. Default is None.
        File name to load coordinates from if method is file.
    num_particles : integer. Default is none.
        Number of particles in the simulation box.
    box_length : float. Default is None
        Side of cubic simulation box.
    
    Returns
    -------
    coordinates : np.array(num_particles,3)
        A numpy array with the x, y and z coordinates of each atom in the simulation box.
    """
    if method is 'random':
        coordinates = (0.5 - np.random.rand(num_particles, 3)) * box_length
    
    elif method is 'file':
        coordinates = np.loadtxt(file_name, skiprows = 2, usecols=(1, 2, 3))
    return coordinates

def accept_or_reject(delta_e, beta):
    """
    Accepts or rejects a move based on the energy difference between initial and updated state along with system temperature.
    
    Parameters
    ----------
    delta_e : float
        Energy difference between initial and updated state of the system.
    beta : float
        Inverse reduced temperature, a general constant in canonical ensemble.

    Returns
    -------
    accept : boolean
        If true, trial move is accepted, else it is rejected.

    """
    if delta_e < 0.0:
        accept = True
    
    else:
        random_number = np.random.rand(1)
        p_acc = np.exp(-beta * delta_e)
        if random_number < p_acc:
            accept = True
        else:
            accept = False
    return accept

def adjust_displacement(n_trials, n_accept, max_displacement):
    """Adjusts the maximum value allowed for a displacement move.
    
    This function adjusts the maximum displacement to obtain a suitable acceptance of trial moves. That is, when the acceptance is too high, the maximum displacement is increased and when the acceptance is too low, the maximum displacement is decreased.
    
    Parameters
    ----------
    n_trials : integer
        Number of trials that have been performed when the funtction is called.
    n_accept: integer
        Number of current accepted trials when the function is called.
    max_displacement: float
        Maximum displacement allowed for any step in the simulation.
    
    Returns
    -------
    n_trials: integer
        Number of trials. Updated to zero if maximum displacement is updated.
    n_accept: integer
        Number of trials. Updated to zero if maximum displacement is updated.
    max_displacemnt: float
        Maximum displacement allowed for any step in the simulation. 
    """
    acc_rate = float(n_accept)/float(n_trials)
    if (acc_rate < 0.38):
        max_displacement *= 0.8
    
    elif (acc_rate > 0.42):
        max_displacement *= 1.2

    n_trials = 0
    n_accept = 0
    return max_displacement, n_trials, n_accept
    
if __name__ == "__main__":

    #------------------
    # Parameter setup
    #------------------

    reduced_temperature = 0.9
    reduced_density = 0.9

    n_steps = 50000
    freq = 1000
    simulation_cutoff = 3.0
    max_displacement = 0.1
    tune_displacement = True
    build_method = 'random'
    num_particles=100

    box_length = np.cbrt(num_particles / reduced_density)
    beta = 1.0 / reduced_temperature
    simulation_cutoff2 = np.power(simulation_cutoff, 2)
    n_trials = 0
    n_accept = 0
    energy_array = np.zeros(n_steps)

    #-----------------------
    # Monte Carlo Simulation
    #-----------------------
    if (build_method == 'random'):
        coordinates = generate_initial_state(method = build_method, num_particles = num_particles, box_length = box_length)
    elif(build_method == 'file'):
        coordinates = generate_initial_state(method = build_method, file_name='sample_config1.xyz')
    num_particles = len(coordinates)
    box_length = np.cbrt(num_particles / reduced_density)
    mcs=MCState(Box(box_length,coordinates),simulation_cutoff)
    total_pair_energy = mcs.calculate_total_pair_energy()
    tail_correction = mcs.calculate_tail_correction()

    for i_step in range(n_steps):
        n_trials += 1
        i_particle = np.random.randint(num_particles)
        random_displacement = (2.0 * np.random.rand(3) - 1.0) * max_displacement
        current_energy = mcs.get_particle_energy(i_particle)
        proposed_coordinates = coordinates.copy()
        proposed_coordinates[i_particle] += random_displacement 
        mcs_check=MCState(Box(box_length,proposed_coordinates),simulation_cutoff)
        proposed_energy = mcs_check.get_particle_energy(i_particle)
        delta_e = proposed_energy - current_energy
        accept = accept_or_reject(delta_e, beta)
        if accept:
            mcs.total_pair_energy += delta_e
            n_accept += 1
            coordinates[i_particle] += random_displacement
             
        total_energy = mcs.calculate_unit_energy()
        energy_array[i_step] = total_energy

        if np.mod(i_step + 1, freq) == 0:
            print(i_step + 1, energy_array[i_step])
            if tune_displacement:
                max_displacement, n_trials, n_accept = adjust_displacement(n_trials, n_accept, max_displacement)
    #print(coordinates)
    #print(calculate_total_pair_energy(coordinates, 10.0, 9.0))
    #print(calculate_tail_correction(10.0, 3.0, len(coordinates)))

    #plt.plot(energy_array[100:], 'o')
    #plt.xlabel('Monte Carlo steps')
    #plt.ylabel('Energy (reduced units)')
    #plt.grid(True)
    #plt.show()

    #plt.figure()
    #ax = plt.axes(projection='3d')
    #ax.plot3D(coordinates[:,0], coordinates[:,1], coordinates[:,2], 'o')
    #plt.show()
