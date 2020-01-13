*TATOO* : Tidal-chronology Age TOOl
==================================

This tool is specifically developed for massive close-in planetary systems: M\ :sub:`p`\  > 0.5 M\ :sub:`jup`\  and 0.5 < M\ :sub:`star`\/M\ :sub:`sun`\  < 1.0

*TATOO* currently only works with python3.5

Input parameter: 

1) Planetary orbital period (P\ :sub:`orb`\) in days
2) Stellar rotation period (P\ :sub:`rot`\) in days
3) Mass of the planet in M\ :sub:`jup`\  
4) Mass of the star in M\ :sub:`sun`\  

Optional:

5) Name of the system
6) Error_Prot in days
7) Error_Porb in days

Return the age of the system!

Example 

python3.5 TATOO.py 0.84 15.6 2.052 0.71 WASP-43 0.4 0.002

Two ways
--------

You can either use *TATOO* in command line using the TATOO folder.

Or to use a Graphical User Interface (GUI) with the GUI folder. 

This latter will need tkinter that is easily installed using Anaconda.

Installation
------------

Currently the best way to install *TATOO* is from github.

.. code-block:: bash
    
    git clone https://github.com/GalletFlorian/TATOO.git
    cd TATOO
    python3.5 setup.py install

Dependencies
------------

The dependencies of *TATOO* are
`NumPy <http://www.numpy.org/>`_,
`scipy <https://www.scipy.org/>`_,
`matplotlib <https://matplotlib.org/>`_ and
`tkinter <https://wiki.python.org/moin/TkInter>`_.


These can be installed using pip:

.. code-block:: bash

    pip install numpy scipy matplotlib

For tkinter (used for the GUI version of *TATOO*) I recommand you to use Anaconda 

.. code-block:: bash

    conda install tkinter

Data
----

You'll also need to download the pre-compiled exploration files (Data.tar.gz | 343.9 Mo).

To download the file from Google Drive via command line, an easy way is to use gdown (https://github.com/circulosmeos/gdown.pl). You can install it via pip:

.. code-block:: bash
    
    pip install gdown
    gdown --id 1VlQa1eEuAZOJp2OXijK8zh5RIvhjCRZO

This file contain six folders (0.5Msol | 0.6Msol | 0.7Msol | 0.8Msol | 0.9Msol | 1.0Msol). 

In each of them there are 480 files named Explo_100_sma_prot_sort.dat

.. https://drive.google.com/open?id=1VlQa1eEuAZOJp2OXijK8zh5RIvhjCRZO

.. The id of the file is

.. id = 1VlQa1eEuAZOJp2OXijK8zh5RIvhjCRZO

It should be extracted in the same folder as the main TATOO folder.

GUI
---

pythin3.5 TATOO_GUI.py 

.. image:: https://raw.githubusercontent.com/GalletFlorian/TATOO/master/docs/GUI.png


