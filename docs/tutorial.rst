.. _Tutorial:

========
Tutorial
========

**mc_lj_potential** is a python package to carry out Monte Carlo simulation of Lennard Jones particles. By calling different functions in the package, users can get the total pair energy, tail correction, particle energy and unit energy of a defined system with specific cubic box size, number of particles and their coordinates.

generate_initial_state
++++++++++++++++++++++

.. code-block:: python

    #mc_lj.py
    import mc_lj_potential as mci
    import numpy as np
    np.random.seed(123)
    num_particles = 100
    box_length = 10.0
    coordinates =  mc.generate_initial_state(method = 'random', num_particles = num_particles, box_length = box_length)
    print(coordinates)

.. note::
    
    Attention: The ``np.random.seed(123)`` here is used to make sure users can get the same results by following  the tutorials below. There is no need to generate the random seed forcely in users' simulation.
 
save the script as mc_lj.py, run it, then the output is 100 random coordinates:

.. code-block:: bash

    ~/my_project$ python mc_lj.py
    [[-6.46469186e+00 -2.36139335e+00 -1.76851454e+00]
     [-5.01314769e+00 -6.69468970e+00 -3.73106460e+00]
     [-9.30764198e+00 -6.34829739e+00 -4.30931901e+00]
     [-3.42117518e+00 -2.93178016e+00 -6.79049707e+00]
     [-3.88572245e+00 -9.67789661e-02 -3.48044255e+00]
     [-6.87995406e+00 -1.32491730e+00 -1.25451756e+00]
     [-4.81551374e+00 -4.81827587e+00 -5.84400959e+00]
     ...

.. note::

    User are allow to import coordinates from a file as well. Instead of ``mc.generate_initial_state(method = 'random', 
    num_particles = num_particles, box_length = box_length)``, use 
    ``mc.generate_initial_state(method = 'file', box_length = box_length)``.

calculate energy in the system
++++++++++++++++++++++++++++++

In order to calculate the energy in the system, we need to initialize our box into unit box with ``wrap()`` and ``minimum_image_distance()``.

.. code-block:: python

    box = mc.Box(coordinates = coordinates, box_length = box_length)
    print(box.coordinates)

add this into mc_lj.py, run it:

.. code-block:: bash

    ~/my_project$ python mc_lj.py
    [[-6.46469186e+00 -2.36139335e+00 -1.76851454e+00]
     [-5.01314769e+00 -6.69468970e+00 -3.73106460e+00]
     [-9.30764198e+00 -6.34829739e+00 -4.30931901e+00]
     [-3.42117518e+00 -2.93178016e+00 -6.79049707e+00]
     [-3.88572245e+00 -9.67789661e-02 -3.48044255e+00]
     [-6.87995406e+00 -1.32491730e+00 -1.25451756e+00]
     [-4.81551374e+00 -4.81827587e+00 -5.84400959e+00]
     ...

it will update our coordinates into the box.

calculate total pair energy
---------------------------

.. code-block:: python

    mcs = mc.MCState(box1 = box, cutoff = 3.0)
    total_pair_energy = mcs.calculate_total_energy()
    print("total pair energy of the system is",total_pair_energy)

The output is:

.. code-block:: bash

    ~/my_project$ python mc_lj.py
    total pair energy of the system is 18677707323853.145


calculate tail correction
-------------------------

.. code-block:: python
     
    tail_correction = mcs.calculate_tail_correction()
    print("tail correction of the system is", tail_correction)
 
The output is:
 
.. code-block:: bash

     ~/my_project$ python mc_lj.py
     tail correction of the system is -3.101388808502446


calculate unit energy
---------------------

.. code-block:: python

    unit_energy = mcs.calculate_unit_energy()
    print("unit energy of the system is",unit_energy)
  
The output is:
  
.. code-block:: bash

    ~/my_project$ python mc_lj.py
    unit energy of the system is 186777073238.50043


get particle energy
-------------------

For example, the particle energy of the first particle can be obtained by ``mcs.get_particle_energy(0)`` where the **index 0** means the first particle in the system. 

.. code-block:: python
     
    particle_energy = mcs.get_particle_energy(0)
    print("particle energy of the first particle is",particle_energy)
    
The output is:
   
.. code-block:: bash
 
    ~/my_project$ python mc_lj.py
    particle energy of the first particle is 12.663401162199152


