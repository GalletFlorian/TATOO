import numpy as np
from scipy.interpolate import griddata
import matplotlib as mpl
import matplotlib.pyplot as plt
from math import log10
from scipy import interpolate
from scipy import interp
import random
import math
import sys
import os
import os.path
from scipy import stats
from scipy.optimize import curve_fit
from Function import Find_4
from Function import func_sq 
from Function import func_lin
from Function import linear
from Function import clean
from Function import Control_file
from Function import rsquared
from Function import Is_empty
from Function import Find_age
import argparse

np.seterr(divide='ignore', invalid='ignore')


def floatt(number) :
    return "%.3f"%number
    
def floatt2(number) :
    return "%.2f"%number
    
def floatt3(number) :
	return "%.1f"%number
	
#List of pre-compiled age estimate couples 
massstar = np.array([0.5,0.6,0.7,0.8,0.9,1.0])
prot = np.array([2,4,6,8,10,11,12,13,14,15,16,17,18,19,20,22,24,26,28,30])
sma = np.array([0.08,0.09,0.010,0.011,0.012,0.013,0.014,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095])

size_mass = len(massstar)
size_prot = len(prot)
size_sma = len(sma)

#Input parameter: 
# 1) Semi-major axis (SMA) in au 
# 2) Stellar rotation period (Prot) in days
# 3) Mass of the planet in Mjup
# 4) Mass of the star in Msun
# 5) Name of the system
# 6) Error_Prot in days
# 7) Error_SMA in au

if len(sys.argv) < 4:
	print "Not enouth information"
	print "TATOO needs: SMA_obs |  Prot_obs | M_planet | M_star | Name of the system | Error_P_rot | Error_SMA"
	sys.exit()
	

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs=4)
parser.add_argument('system',nargs='?')
parser.add_argument('error_prot',nargs='?')
parser.add_argument('error_sma',nargs='?')

args = parser.parse_args()

smaobs = float(args.input[0])
protobs = float(args.input[1])
mp = float(args.input[2])
mstarobs = float(args.input[3])


if (args.system == None):
	system = "Unknown_system"
else:	
	system = args.system


if (args.error_prot == None):
	print "Standard Error_Prot = 0.4 days"
	sigmarot = 0.4	
else:
	sigmarot = float(args.error_prot)


if (args.error_sma == None):
	print "Standard Error_SMA = 0.002 au"
	sigmasma = 0.002	
else:
	sigmasma = float(args.error_sma)		


#Number of age estimations for a given system. 
nstep = 100

#Nbtest_limit indicate the maximum number of iterations without finding any good enough age. 
Nbtest_limit = 100

#Assess the robustness of the age estimation? When robust = 1, TATOO will randomly explore the vicinity of the 4
#corner points. 
robust = 0

#The minimum value of the spearmanr coefficient.
coeflim = 0.5

arr_agemod_min = []
arr_agemod_max = []

arr_agemod_min_rand = []
arr_agemod_max_rand = []

#Find the two stellar mass around the mass of the required star
for index_mass in range(0,size_mass-1):
	if mstarobs >= massstar[index_mass]:
		massstarmin = massstar[index_mass]
		massstarmax = massstar[index_mass+1]
		
		
#For each requested systems, performs nstep loops to generate random SMA and Prot within their uncertainties
#It is used to get the median and the standard deviation for the age estimation 
Nb = 0
Nbtest = 0
Nbtest_step = 0
#for Nb in range(0,nstep):
while Nb < nstep:

	arr_ai = []
	arr_roti = []
	arr_chi2 = []
	arr_massp = []
	arr_age = []

	
	flag_max = 0
	flag_min = 0
	
	sma_list = [0.0,0.0,0.0,0.0]
	prot_list = [0.0,0.0,0.0,0.0] 
	age_list = [0.0,0.0,0.0,0.0] 
	massp_list = [0.0,0.0,0.0,0.0]  
	masss_list = [0.0,0.0,0.0,0.0] 	
	coef_min = [0.0,0.0,0.0,0.0] 	
	coef_max = [0.0,0.0,0.0,0.0] 	
	
	#random exploration on P_rot and SMA given Error_Prot and Error_SMA
	protrand = random.uniform(protobs-sigmarot,protobs+sigmarot)
	smarand = random.uniform(smaobs-sigmasma, smaobs+sigmasma)	
	
	#Find the four couples that encompass the observed (random) couple protrand-smarand
	for index_sma in range(0,size_sma-1):
		if smarand >= sma[index_sma]:
			smamin = sma[index_sma]
			smamax = sma[index_sma+1] 
			index_ref_sma = index_sma
				
				
	for index_prot in range(0,size_prot-1):
		if protrand >= prot[index_prot]:
			protmin = prot[index_prot]
			protmax = prot[index_prot+1]
			index_ref_prot = index_prot
					
	#Cleaning the useful arrays  
	sma_list=clean(sma_list)
	prot_list=clean(prot_list)
	age_list=clean(age_list)
	massp_list=clean(massp_list)
	masss_list=clean(masss_list)
	
	#Control on the content of the Explo_* files. If empty, try to find the next non empty file.
	smamin,protmin,smamax,protmax= Control_file(prot,sma,index_ref_prot,index_ref_sma,massstarmin,smamin,protmin,smamax,protmax)

	#Estimating the spearman correlation coefficient + the age of each corner pre-compiled Explo_* files. Here for massstarmin 
	coef_min[0] = Find_4(floatt(smamin),floatt2(protmin),mp,massstarmin,0,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_min[1] = Find_4(floatt(smamax),floatt2(protmin),mp,massstarmin,1,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_min[2] = Find_4(floatt(smamin),floatt2(protmax),mp,massstarmin,2,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_min[3] = Find_4(floatt(smamax),floatt2(protmax),mp,massstarmin,3,sma_list,prot_list,age_list,massp_list,masss_list)
	
	#Calling Find_age to perform the 3D interpolation
	age_min = Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)
	
	if age_min >= 0.0:
		flag_min = 1
		arr_agemod_min.append(age_min) #for massstarmin

	coef_min_f = np.mean(coef_min)


	#Same procedure as above but for massstarmax
	sma_list=clean(sma_list)
	prot_list=clean(prot_list)
	age_list=clean(age_list)
	massp_list=clean(massp_list)
	masss_list=clean(masss_list)
	
	smamin,protmin,smamax,protmax= Control_file(prot,sma,index_ref_prot,index_ref_sma,massstarmax,smamin,protmin,smamax,protmax)

	coef_max[0] = Find_4(floatt(smamin),floatt2(protmin),mp,massstarmax,0,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_max[1] = Find_4(floatt(smamax),floatt2(protmin),mp,massstarmax,1,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_max[2] = Find_4(floatt(smamin),floatt2(protmax),mp,massstarmax,2,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_max[3] = Find_4(floatt(smamax),floatt2(protmax),mp,massstarmax,3,sma_list,prot_list,age_list,massp_list,masss_list)

	age_max = Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)
	
	if age_max >= 0.0:
		flag_max = 1
		arr_agemod_max.append(age_max) #for massstarmax
	
	coef_max_f = np.mean(coef_max)
	
	#Control on the spearman averaged coefficient. It is used to ensure a good enough linear relation between the estimated age and the 
	#mass of the planet?
	Nbtest = Nbtest + 1
	if (abs(coef_min_f) > coeflim and abs(coef_max_f) > coeflim) and flag_max*flag_min == 1:
		print Nb,arr_agemod_min[Nb],arr_agemod_max[Nb]
		Nb = Nb + 1
		Nbtest = 0

	
	if Nbtest == Nbtest_limit:
		print "Limit of",Nbtest_limit,"iterations reached for", system,". No linear relation between the age and the mass of the planet found!"
		print "Try with reduced coeflim.", coeflim * 0.8
		Nbtest = 0
		coeflim = coeflim * 0.8
		Nbtest_step = Nbtest_step + 1
		if Nbtest_step > 2:
			sys.exit()

	
################### Robustness ###################

	if robust == 1:
	
	
		for index_sma in range(0,size_sma-1):
			if smarand >= sma[index_sma]:
				index_ref_sma = index_sma
			
				rand1 = random.uniform(0,1)
				rand2 = random.uniform(0,1)
				if rand1 >= 0.5 and index_sma>0:
					rand1 = 1
				else:
					rand1 = 0		
				if rand2 >= 0.5 and index_sma<size_sma-2 :
					rand2 = 1
				else:
					rand2 = 0	
	
				smaminrand = sma[index_sma-int(rand1)]
				smamaxrand = sma[index_sma+1+int(rand2)]	
				
		for index_prot in range(0,size_prot-1):
			if protrand >= prot[index_prot]:
				index_ref_prot = index_prot
			
				rand1 = random.uniform(0,1)
				rand2 = random.uniform(0,1)
				if rand1 >= 0.5 and index_prot>0 :
					rand1 = 1
				else:
					rand1 = 0
				if rand2 >= 0.5 and index_prot<size_prot-2:
					rand2 = 1
				else:
					rand2 = 0	
					
				protminrand = prot[index_prot-int(rand1)]
				protmaxrand = prot[index_prot+1+int(rand2)]
			
		sma_list=clean(sma_list)
		prot_list=clean(prot_list)
		age_list=clean(age_list)
		massp_list=clean(massp_list)
		masss_list=clean(masss_list)

		coef2_1 = Find_4(floatt(smaminrand),floatt2(protminrand),mp,massstarmin,0,sma_list,prot_list,age_list,massp_list,masss_list)
		coef2_2 = Find_4(floatt(smamaxrand),floatt2(protminrand),mp,massstarmin,1,sma_list,prot_list,age_list,massp_list,masss_list)
		coef2_3 = Find_4(floatt(smaminrand),floatt2(protmaxrand),mp,massstarmin,2,sma_list,prot_list,age_list,massp_list,masss_list)
		coef2_4 = Find_4(floatt(smamaxrand),floatt2(protmaxrand),mp,massstarmin,3,sma_list,prot_list,age_list,massp_list,masss_list)

		coef1 = (coef1_1 + coef1_2 + coef1_3 + coef1_4)/4.0
	

		arr_agemod_min_rand.append(Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)) #for massstarmin

		sma_list=clean(sma_list)
		prot_list=clean(prot_list)
		age_list=clean(age_list)
		massp_list=clean(massp_list)
		masss_list=clean(masss_list)


		coef2_1 = Find_4(floatt(smaminrand),floatt2(protminrand),mp,massstarmax,0,sma_list,prot_list,age_list,massp_list,masss_list)
		coef2_2 = Find_4(floatt(smamaxrand),floatt2(protminrand),mp,massstarmax,1,sma_list,prot_list,age_list,massp_list,masss_list)
		coef2_3 = Find_4(floatt(smaminrand),floatt2(protmaxrand),mp,massstarmax,2,sma_list,prot_list,age_list,massp_list,masss_list)
		coef2_4 = Find_4(floatt(smamaxrand),floatt2(protmaxrand),mp,massstarmax,3,sma_list,prot_list,age_list,massp_list,masss_list)

		coef2 = (coef2_1 + coef2_2 + coef2_3 + coef2_4)/4.0

		arr_agemod_max_rand.append(Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)) #for massstarmax
		
		
	
##################################################

age_med_min = np.median(arr_agemod_min, 0)
std_age_min = np.std(arr_agemod_min)

age_med_max = np.median(arr_agemod_max, 0)
std_age_max = np.std(arr_agemod_max,0)

arr_avgage = []

for i in range(0,Nb):
	arr_age = [arr_agemod_min[i],arr_agemod_max[i]]
	arr_masss = [massstarmin,massstarmax]
	popt, pcov = curve_fit(linear, np.array(arr_masss), np.array(arr_age))
	a = popt[0]
	b = popt[1]
	arr_avgage.append(a*mstarobs + b)
	
age_med_avg = np.median(arr_avgage, 0)
std_age_avg = np.std(arr_avgage)


tablefile = open("age.dat",'a')
tablefile.write("{}$\pm${}\n".format(floatt3(age_med_avg),floatt3(std_age_avg)))

agefile = open("table.dat",'a')
agefile.write("{} & {} & {} & {} & {} & {} & {}$\pm${} & {} \\ \n".format(system,mstarobs,mp,protobs,smaobs,0.000,floatt3(age_med_avg),floatt3(std_age_avg), 0.000))

print 'Estimated averaged age for',system,"=",age_med_avg,'+-',std_age_avg,'Myr'


##################################################

if robust == 1:
	arr_avgage = []

	for i in range(0,Nb):
		arr_age = [arr_agemod_min_rand[i],arr_agemod_max_rand[i]]
		arr_masss = [massstarmin,massstarmax]
		popt, pcov = curve_fit(linear, np.array(arr_masss), np.array(arr_age))
		a = popt[0]
		b = popt[1]
		arr_avgage.append(a*mstarobs + b)
	
	age_med_avg = np.median(arr_avgage, 0)
	std_age_avg = np.std(arr_avgage)


	print 'Robustness => estimated averaged age for',system,"=",age_med_avg,'+-',std_age_avg,'Myr'

	
