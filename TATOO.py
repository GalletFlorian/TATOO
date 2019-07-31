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


def floatt(number) :
    return "%.3f"%number
    
def floatt2(number) :
    return "%.2f"%number
    
def floatt3(number) :
	return "%.1f"%number
	
#List of pre-compiled age estimate couples 
massstar = np.array([0.5,0.6,0.7,0.8,0.9,1.0])
prot = np.array([2,4,6,8,10,11,12,13,14,15,16,17,18,19,20,22,24,26,30])
sma = np.array([0.010,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095])

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

smaobs = float(sys.argv[1])
protobs = float(sys.argv[2])
mp = sys.argv[3]
mstarobs = float(sys.argv[4])
system = sys.argv[5]
 
sigmarot = float(sys.argv[6])
sigmasma = float(sys.argv[7])

#Number of age estimations for a given system. 
nstep = 100

#Nbtest limit
Nbtest_limit = 100

#Assess the robustness?
robust = 0

#Useful functions
def func_sq(x,a,b,c):
	return a*x**2.0+ b*x + c
	
def func_lin(x,a,b):
	return a*x + b

def linear(x,a,b):
	return a*x + b
	
	
def clean(array):
	array = [0.0,0.0,0.0,0.0]
	return array
	
x = []
y = []	
def rsquared(x, y):
	""" Return R^2 where x and y are array-like."""
	slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
	return r_value**2


#Function used to get the age estimation, at the selected planetary mass, of the 4 couples that surround the observed couple.
def Find_4(sma,prot,mp,mstar,i,sma_list,prot_list,age_list,massp_list,masss_list):

	arr_ai = []
	arr_roti = []
	arr_chi2 = []
	arr_massp = []
	arr_age = []
	
	#chi2 threshold
	chi2lim = 1.0
	
	filename = "./%sMsol/Explo_100_%s_%s_sort.dat" %(mstar,sma,prot)
	
	count = 0
	xyzfile = open(filename)
	next(xyzfile)
	for line in xyzfile:
		age,ai,roti,chi2,massp = line.split()
		if float(chi2) < chi2lim: 	
			arr_ai.append(float(ai))
			arr_roti.append(float(roti))
			arr_chi2.append(float(chi2))
			arr_age.append(float(age))
			arr_massp.append(float(massp))
			count = count + 1
	    		
	xyzfile.close()	

	if count > 0:
		#popt, pcov = curve_fit(func_sq, np.array(arr_massp), np.array(arr_age),sigma=np.array(arr_chi2))
		#a = popt[0]
		#b = popt[1]
		#c = popt[2]

		popt, pcov = curve_fit(func_lin, np.array(arr_massp), np.array(arr_age),sigma=np.array(arr_chi2))
		a = popt[0]
		b = popt[1]
		
		#linear interpolation
		time_mod = a*float(mp)+b
		
		#time_mod = a*float(mp)**2.0 + b*float(mp) + c
		
		
		
		residuals = (np.array(arr_age) - func_lin(np.array(arr_massp),*popt)) / np.array(arr_chi2)
		RMSE = (sum(residuals**2)/(residuals.size-3))**0.5

		meanage = np.mean(np.array(arr_age))
		residu_age = np.array(arr_age) - meanage
		std_age = np.std(arr_age)
		
		meanmp =  np.mean(func_lin(np.array(arr_massp),*popt))
		residu_mp = func_lin(np.array(arr_massp),*popt) - meanmp
		std_mp = np.std(func_lin(np.array(arr_massp),*popt))
		
		
		coef =  np.mean(residu_age*residu_mp)/(std_mp*std_age)

		
		#print "RMSE", stats.spearmanr(np.array(arr_age),func_lin(np.array(arr_massp),*popt))[0],coef, filename #, RMSE, nRMSE,nRMSE2,nRMSE3, r2
				
		
		sma_list[i] = float(sma)
		prot_list[i] = float(prot)
		age_list[i] = float(time_mod)
		massp_list[i] = float(mp)
		masss_list[i] = float(mstar)
	else:			
		sma_list[i] = float(sma)
		prot_list[i] = float(prot)
		age_list[i] = 0.000
		massp_list[i] = float(mp)
		masss_list[i] = float(mstar)
		
	return stats.spearmanr(np.array(arr_age),func_lin(np.array(arr_massp),*popt))[0]
	
	
#Given the information of Find_4, Find_age perform a 3D interpolation using the Griddata tool.
def Find_age(sma,prot,sma_list,prot_list,age_list,massp_list,masss_list):

	arr_xy = []


	for i in range(0,4):
		arr_xy.append([sma_list[i],prot_list[i]])

	if sma_list[0] > 0:
		smaobs = float(sma)
		protobs = float(prot)
		grid = griddata(arr_xy, age_list, (smaobs,protobs), method='cubic')
	else:
		grid = 0.0 
	
	if grid != grid:
		sys.exit("Problem with NaN in grid")
		
	return grid
		
arr_agemod_min = []
arr_agemod_max = []


arr_agemod_min_rand = []
arr_agemod_max_rand = []

#Find the four couples that encompass the observed couple
for index_mass in range(0,size_mass-1):
	if mstarobs >= massstar[index_mass]:
		massstarmin = massstar[index_mass]
		massstarmax = massstar[index_mass+1]
		
		
#For each requested systems, 100 loop to generate random SMA and Prot within their uncertainties
#It will be used to get the median and the standard deviation for the age estimation 
Nb = 0
Nbtest = 0
#for Nb in range(0,nstep):
while Nb < nstep:
	sma_list = [0.0,0.0,0.0,0.0]
	prot_list = [0.0,0.0,0.0,0.0] 
	age_list = [0.0,0.0,0.0,0.0] 
	massp_list = [0.0,0.0,0.0,0.0]  
	masss_list = [0.0,0.0,0.0,0.0] 	
	
	
	protrand = random.uniform(protobs-sigmarot,protobs+sigmarot)
	smarand = random.uniform(smaobs-sigmasma, smaobs+sigmasma)	
	
	for index_sma in range(0,size_sma-1):
		if smarand >= sma[index_sma]:
			smamin = sma[index_sma]
			smamax = sma[index_sma+1] 
			
			rand1 = random.uniform(0,1)
			rand2 = random.uniform(0,1)
			if rand1 >= 0.5 and index_sma>0:
				rand1 = 1
			else:
				rand1 = 0
			
			if rand2 >= 0.5 and index_sma<size_sma :
				rand2 = 1
			else:
				rand2 = 0	
						
			smaminrand = sma[index_sma-int(rand1)]
			smamaxrand = sma[index_sma+1+int(rand2)]	
	
	for index_prot in range(0,size_prot-1):
		if protrand >= prot[index_prot]:
			protmin = prot[index_prot]
			protmax = prot[index_prot+1]
			
			rand1 = random.uniform(0,1)
			rand2 = random.uniform(0,1)
			if rand1 >= 0.5 and index_prot>0 :
				rand1 = 1
			else:
				rand1 = 0
			
			if rand2 >= 0.5 and index_prot<size_prot:
				rand2 = 1
			else:
				rand2 = 0	
			protminrand = prot[index_prot-int(rand1)]
			protmaxrand = prot[index_prot+1+int(rand2)]
			
			
#	print smaminrand,smamaxrand, protminrand,protmaxrand
	

	sma_list=clean(sma_list)
	prot_list=clean(prot_list)
	age_list=clean(age_list)
	massp_list=clean(massp_list)
	masss_list=clean(masss_list)

	coef1_1 = Find_4(floatt(smamin),floatt2(protmin),mp,massstarmin,0,sma_list,prot_list,age_list,massp_list,masss_list)
	coef1_2 = Find_4(floatt(smamax),floatt2(protmin),mp,massstarmin,1,sma_list,prot_list,age_list,massp_list,masss_list)
	coef1_3 = Find_4(floatt(smamin),floatt2(protmax),mp,massstarmin,2,sma_list,prot_list,age_list,massp_list,masss_list)
	coef1_4 = Find_4(floatt(smamax),floatt2(protmax),mp,massstarmin,3,sma_list,prot_list,age_list,massp_list,masss_list)
	
	arr_agemod_min.append(Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)) #for massstarmin

	coef1 = (coef1_1 + coef1_2 + coef1_3 + coef1_4)/4.0

	sma_list=clean(sma_list)
	prot_list=clean(prot_list)
	age_list=clean(age_list)
	massp_list=clean(massp_list)
	masss_list=clean(masss_list)

	coef2_1 = Find_4(floatt(smamin),floatt2(protmin),mp,massstarmax,0,sma_list,prot_list,age_list,massp_list,masss_list)
	coef2_2 = Find_4(floatt(smamax),floatt2(protmin),mp,massstarmax,1,sma_list,prot_list,age_list,massp_list,masss_list)
	coef2_3 = Find_4(floatt(smamin),floatt2(protmax),mp,massstarmax,2,sma_list,prot_list,age_list,massp_list,masss_list)
	coef2_4 = Find_4(floatt(smamax),floatt2(protmax),mp,massstarmax,3,sma_list,prot_list,age_list,massp_list,masss_list)

	arr_agemod_max.append(Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)) #for massstarmax
	
	
	coef2 = (coef2_1 + coef2_2 + coef2_3 + coef2_4)/4.0
	
	Nbtest = Nbtest + 1
	if coef1 > 0.3 and coef2 > 0.3:
		Nb = Nb + 1
		#print coef1,coef2
		Nbtest = 0
	
	if Nbtest == Nbtest_limit:
		print "Limit of",Nbtest_limit,"iterations reached for", system,". No linear relation between the age and the mass of the planet found!"
		sys.exit()

	
################### Robustness ###################

	if robust == 1:
		sma_list=clean(sma_list)
		prot_list=clean(prot_list)
		age_list=clean(age_list)
		massp_list=clean(massp_list)
		masss_list=clean(masss_list)

		Find_4(floatt(smaminrand),floatt2(protminrand),mp,massstarmin,0,sma_list,prot_list,age_list,massp_list,masss_list)
		Find_4(floatt(smamaxrand),floatt2(protminrand),mp,massstarmin,1,sma_list,prot_list,age_list,massp_list,masss_list)
		Find_4(floatt(smaminrand),floatt2(protmaxrand),mp,massstarmin,2,sma_list,prot_list,age_list,massp_list,masss_list)
		Find_4(floatt(smamaxrand),floatt2(protmaxrand),mp,massstarmin,3,sma_list,prot_list,age_list,massp_list,masss_list)
	
	
		arr_agemod_min_rand.append(Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)) #for massstarmin

		sma_list=clean(sma_list)
		prot_list=clean(prot_list)
		age_list=clean(age_list)
		massp_list=clean(massp_list)
		masss_list=clean(masss_list)


		Find_4(floatt(smaminrand),floatt2(protminrand),mp,massstarmax,0,sma_list,prot_list,age_list,massp_list,masss_list)
		Find_4(floatt(smamaxrand),floatt2(protminrand),mp,massstarmax,1,sma_list,prot_list,age_list,massp_list,masss_list)
		Find_4(floatt(smaminrand),floatt2(protmaxrand),mp,massstarmax,2,sma_list,prot_list,age_list,massp_list,masss_list)
		Find_4(floatt(smamaxrand),floatt2(protmaxrand),mp,massstarmax,3,sma_list,prot_list,age_list,massp_list,masss_list)

		arr_agemod_max_rand.append(Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)) #for massstarmax	
	
###################               ###################


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


###################      ###################

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

	
