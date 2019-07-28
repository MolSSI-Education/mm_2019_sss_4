"""
Unit and regression test for the mc_lj_potential package.
"""

# Import package, test suite, and other packages as needed
import mc_lj_potential
import pytest
import sys
import os


# Dependencies
import numpy as np

def test_mc_lj_potential_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "mc_lj_potential" in sys.modules


def test_generate_intial_state():
    coordinates = mc_lj_potential.generate_initial_state("random", num_particles = 100, box_length = 10.0)
    assert len(coordinates) == 100


def test_get_particle_energy_cutoff():
    coordinates = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,4.0])]
    box_length = 10.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = 3.0)
    expected_vaule = 0.0
    calculated_value = mcs.get_particle_energy(0)
    assert np.isclose(expected_vaule, calculated_value)

def test_get_particle_energy_equi():
    coordinates = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,1.0])]
    box_length = 10.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = 3.0)
    expected_vaule = 0.0
    calculated_value = mcs.get_particle_energy(0)
    assert np.isclose(expected_vaule, calculated_value)

def test_lennard_jones_potential():
    coordinates = [np.array([0.0,0.0,0.0]),np.array([0.0,0.0,1.0])]
    box_length = 10.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = 3.0)
    expected_vaule = 224.0
    calculated_value = mcs.lennard_jones_potential(0.5)
    assert np.isclose(expected_vaule, calculated_value)

def test_energy():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_directory, "sample_config.xyz")
    coordinates = mc_lj_potential.generate_initial_state(method = "file", file_name=file_path)
    box_length = 10.0
    cutoff = 3.0
    box = mc_lj_potential.Box(box_length=box_length, coordinates=coordinates)
    mcs = mc_lj_potential.MCState(box, cutoff = cutoff)

    # test the calcualte_total_pair_energy
    calculated_pair_energy = mcs.calculate_total_pair_energy()
    assert np.isclose(calculated_pair_energy, -4.3515E+03)

    # test the calculate_tail_correction
    calculated_tail_correction = mcs.calculate_tail_correction()
    assert np.isclose(calculated_tail_correction, -198.488258)

    # test the get_particle_energy
    calculated_particle_energy = mcs.get_particle_energy(0)
    assert np.isclose(calculated_particle_energy, -10.877945)

    # test the calculate_unit_energy
    calculated_unit_energy = mcs.calculate_unit_energy()
    assert np.isclose(calculated_unit_energy, -5.687536)

def test_accpet_or_reject_true():
    """Test the accept_or_reject function when it is true."""
    expected_vaule1 = True
    calculated_value1 = mc_lj_potential.accept_or_reject(-1.0,0.10)
    assert expected_vaule1 == calculated_value1

def test_accpet_or_reject_false():
    """Test the accept_or_reject function when it is False."""
    np.random.seed(10)
    expected_vaule2 = False
    calculated_value2 = mc_lj_potential.accept_or_reject(6.0, 0.10)
    print(calculated_value2)
    try:
        assert expected_vaule2 == calculated_value2
    finally:
        np.random.seed()


def test_adjust_displacement():
    """Test the accept_or_reject function."""
    n_trials = 100.0
    n_accept1 = 37.0
    n_accept2 = 40.0
    n_accept3 = 43.0
    max_displacement = 1.0
    expected_vaule1 = 0.8

    # test if its movement is too large
    cal_max_displacement1, n_trials1, n_accept1 = mc_lj_potential.adjust_displacement(n_trials = n_trials, n_accept = n_accept1, max_displacement = max_displacement)
    assert expected_vaule1 == cal_max_displacement1
    
    # test if its movement is reasonable
    cal_max_displacement2, n_trials2, n_accept1 = mc_lj_potential.adjust_displacement(n_trials = n_trials, n_accept = n_accept2, max_displacement = max_displacement)
    expected_value2 = 1.0
    assert expected_value2 == cal_max_displacement2
    
    # test if its movement is too small
    cal_max_displacement3, n_trials3, n_accept1 = mc_lj_potential.adjust_displacement(n_trials = n_trials, n_accept = n_accept3, max_displacement = max_displacement)
    expected_value3 = 1.2
    assert expected_value3 == cal_max_displacement3
