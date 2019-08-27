# TATOO
Tidal-chronology Age esTimation tOOl

This tool is specifically developped for massive close-in planetary systems => Mass planet > 0.5 M_jup and 0.5 < M_star/Msun < 1.0

Input parameter: 
1) Semi-major axis (SMA) in au 
2) Stellar rotation period (Prot) in days
3) Mass of the planet in Mjup
4) Mass of the star in Msun

Optional

5) Name of the system
6) Error_Prot in days
7) Error_SMA in au


Return the age of the system!


Example 

python TATOO.py 0.01560 15.6 2.052 0.71 WASP-43 0.4 0.002

________________  Resquested file  ________________

Dowload the pre-compiled exploration files here (Data.tar.gz | 343.9 Mo).

https://share.orange.fr/#yBC3ycDIV23f0e138a24


Its in French: first clic on the file, then on the "Télécharger" button.

This file contain six folders (0.5Msol | 0.6Msol | 0.7Msol | 0.8Msol | 0.9Msol | 1.0Msol). 

In each of them there are 480 files named Explo_100_sma_prot_sort.dat
