
Installation
============

To install our package, users can clone it from GitHub:

.. code-block:: bash
 
    $ git clone https://github.com/MolSSI-Education/mm_2019_sss_4.git

There will come a new folder named *mm_2019_sss_4* in the users' path.

.. code-block:: bash

    $ cd mm_2019_sss_4
    $ pip install -e .

Use pip to install the whole package to your ``$PYTHONPATH``.

.. Tip::

    Users can go to **docs** folder, make html and open the html to preview the documentation.

.. code-block:: bash

    $ cd docs/
    $ make html
    $ open _build/html/index.html

And the documentation will pop up.

.. Attention::
    
    In ordert to make html, the user should first install *sphinx* and *sphinx_rtd_theme*. Use conda to install,

.. code-block::
 
    $ conda install sphinx sphinx_rtd_theme
