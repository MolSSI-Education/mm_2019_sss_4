"""
Unit and regression test for the mc_lj_potential package.
"""

# Import package, test suite, and other packages as needed
import mc_lj_potential
import pytest
import sys
import numpy as np
import random
import os
import random
import math
def test_generate_initial_state():
    """Tests initial state if the length of the coordinates matches the number of the particles provided.
    Parameters
    ----------
    method : str
    num_particles : int
    box_length : float
    
    Returns
    -------
    size of coordinates : int
    """
    expected = 30
    calculated = mc_lj_potential.generate_initial_state(method = 'random', num_particles = 30, box_length = 10.0)
    calculated = len(calculated)
    assert expected == calculated

def test_total_pair_energy():
    """Tests the total pair energy
    Parameters
    ----------
    num_particles : int
    box_length : float
    method : str

    Returns
    -------
    e_total : float
        Returns the total pair energy of the system
    """
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "sample_config.xyz")
    coordinates = mc_lj_potential.generate_initial_state(method = "file", file_name=file_path)
    box_length = 10.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = 4.0)

    calculated_value = mcs.calculate_total_pair_energy()

    assert np.isclose(calculated_value, -4.4675E+03)

def test_minimum_image_distance():
    """Tests if the particle is bounded with in the box
    Parameters
    ----------
    coordinates : np.array
    box_length : float
    
    Returns
    -------
    minimum image distance : float

    """
    r_i = np.array([2.08728997, -0.60907129, -1.75467417])
    r_j = np.array([1.91098003, 0.8518106,  2.06060399])
    box_length = 4.0

    bx = mc_lj_potential.Box(box_length)
    calculated = bx.minimum_image_distance(r_i, r_j, box_length)
    calculated = math.sqrt(calculated)
    assert calculated < box_length
