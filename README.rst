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

Return the age of the system in Myr.

Example: 

.. code-block:: bash

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

You'll also need to download the pre-compiled exploration files (Data.tar.gz | 344.4 Mo).

To download the file from Google Drive via command line, an easy way is to use gdown (https://github.com/circulosmeos/gdown.pl). You can install it via pip:

.. code-block:: bash
    
    pip install gdown
    cd ./Data/
    gdown --id 10SCb8cfI3o86AQiiM9_-itCF1PZUtT7v
    tar zxvf Data.tar.gz
    rm Data.tar.gz
    cd ../

This file contain six folders (0.5Msol | 0.6Msol | 0.7Msol | 0.8Msol | 0.9Msol | 1.0Msol). 

In each of them there are 480 files named Explo_100_sma_prot_sort.dat

.. https://drive.google.com/open?id=10SCb8cfI3o86AQiiM9_-itCF1PZUtT7v

.. The id of the file is

.. id = 10SCb8cfI3o86AQiiM9_-itCF1PZUtT7v

It should be extracted in the Data folder.

GUI
---

python3.5 TATOO_GUI.py 

.. image:: https://raw.githubusercontent.com/GalletFlorian/TATOO/master/docs/GUI.png

+------------------------------------------------------+-----------------------------------------------------+
|                          Star                        | Planet                                              | 
+======================================================+=====================================================+
| Mstar: Mass of the star in solar mass unit           | Mp: Mass of the planet in Jupiter mass unit         | 
+------------------------------------------------------+-----------------------------------------------------+
| Prot: Rotation period of the star in days            | Porb: Orbital period of the planet in days          |
+------------------------------------------------------+-----------------------------------------------------+
| Errot_prot: RMS error of the rotation period in days | Error_porb: RMS error of the orbital period in days | 
+------------------------------------------------------+-----------------------------------------------------+

| Gyro: when checked, *TATOO* will give the gyrochronological age of the star
| Robust: when checked, *TATOO* will explore the vicinity of the properties of the requested system to check the robustness of the age estimation

|

| Coef limit: Value of the requested coefficient for the Pearson correlation coefficient test
| Nb_step: Number of age estimations for the standard deviation of the age


Acknowledgements
----------------

Please cite Gallet 2020 if you use this tool.


References
----------


Gallet, F., Bolmont, E., Bouvier, J., Mathis, S., & Charbonnel, C. 2018, A&A, 619, A80

Gallet, F. & Delorme, P. 2019, A&A, 626, A120
