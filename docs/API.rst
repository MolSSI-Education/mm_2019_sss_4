.. _API:

=================
API Documentation
=================

Initialize the system
+++++++++++++++++++++

For initialize the sysetm, the ``generate_initial_state()`` will generate an initial state either in a random way or import from a *.xyz* file.

.. autosummary::
    :toctree: autosummary
    
    mc_lj_potential.generate_initial_state

.. tip::

    The *.xyz* file will give the coordinates of all the particles. If the method is *random*, num_particles and box_length are required arguments.

Class Box
+++++++++

This is the class to generate a box, with the particles parameters.

.. autosummary::
    :toctree: autosummary

    mc_lj_potential.Box

In the class, we have functions as follows:

.. autosummary::
    :toctree: autosummary

    mc_lj_potential.Box.wrap
    mc_lj_potential.Box.minimum_image_distance

And we set the volume and num_particles as properties, can be called as:

.. autosummary::
    :toctree: autosummary

    mc_lj_potential.Box.volume
    mc_lj_potential.Box.num_particles    


Class MCState
+++++++++++++

In the class ``MCState``, we will have functions for the energies in the defined system:

.. autosummary::
    :toctree: autosummary

    mc_lj_potential.MCState

In the class, we can calculate total pair energy, tail correction, unit energy and particle energy by functions as follows:
 
.. autosummary::
    :toctree: autosummary

    mc_lj_potential.MCState.calculate_total_pair_energy
    mc_lj_potential.MCState.calculate_tail_correction
    mc_lj_potential.MCState.calculate_unit_energy
    mc_lj_potential.MCState.get_particle_energy


Monte Carlo Steps
+++++++++++++++++

After that the Monte Carlo will determine the acceptance of each movement with ``accept_or_reject()``:

.. autosummary::
    :toctree: autosummary
  
    mc_lj_potential.accept_or_reject


Optimization
++++++++++++

Optimization of the scale of displacement can be done by ``adjust_displacement()``:

.. autosummary::
    :toctree: autosummary
 
    mc_lj_potential.adjust_displacement


