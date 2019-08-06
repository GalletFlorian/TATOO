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

#chi2 threshold
chi2lim = 100.0




		
arr_agemod_min = []
arr_agemod_max = []


arr_agemod_min_rand = []
arr_agemod_max_rand = []

#Useful functions
def floatt(number) :
    return "%.3f"%number
    
def floatt2(number) :
    return "%.2f"%number
    
def floatt3(number) :
	return "%.1f"%number

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


def Is_empty(mstar,sma,prot):

	arr_ai = []
	arr_roti = []
	arr_chi2 = []
	arr_massp = []
	arr_age = []
	filename = "./%sMsol/Explo_100_%s_%s_sort.dat" %(mstar,floatt(sma),floatt2(prot))
	flag = 0
	inputfile = open(filename)
	next(inputfile)
	for line in inputfile:
		age,ai,roti,chi2,massp = line.split()
		if float(chi2) < chi2lim: 	
			arr_ai.append(float(ai))
			arr_roti.append(float(roti))
			arr_chi2.append(float(chi2))
			arr_age.append(float(age))
			arr_massp.append(float(massp))
			flag = flag + 1
	    		
	inputfile.close()	
	
	return flag
	
def Control_file(protin,smain,iprot,isma,mstar,smamin,protmin,smamax,protmax):

	
	prot = protin 
	sma = smain
	index_ref_prot = iprot
	index_ref_sma = isma

	size_prot = len(prot)
	size_sma = len(sma)
	
	
	#Control on the containt of the files
	#Re-ajust the 4 corner points if needed
	
	#smamax
	flag = Is_empty(mstar,smamax,protmin)
	flag_full = 0
	index = 1
	while flag == 0:
		if flag_full == 0:
			flag = Is_empty(mstar,smamax,protmin)	
			protmin = prot[index_ref_prot-index]
			index = index + 1
			if index_ref_prot-index == 0:
				flag_full = 1
				index = 1
		else:
			protmin = prot[index_ref_prot]
			flag = Is_empty(mstar,smamax,protmin)	
			smamax = sma[index_ref_sma+index]
			index = index + 1	
	
	flag = Is_empty(mstar,smamax,protmax)	
	flag_full = 0
	index = 1 
	while flag == 0:
		if flag_full == 0:
			flag = Is_empty(mstar,smamax,protmax)	
			protmax = prot[index_ref_prot+index]
			index = index + 1
			if index_ref_prot+index == size_prot:
				flag_full = 1
				index = 1
		else:
			protmax = prot[index_ref_prot+1]
			flag = Is_empty(mstar,smamax,protmax)	
			smamax = sma[index_ref_sma+index]
			index = index + 1	
	
	
	#smamin
	flag = Is_empty(mstar,smamin,protmin)
	flag_full = 0
	index = 1
	while flag == 0:
		if flag_full == 0:
			flag = Is_empty(mstar,smamin,protmin)	
			protmin = prot[index_ref_prot-index]
			index = index + 1
			if index_ref_prot-index == 0:
				flag_full = 1
				index = 1
		else:
			protmin = prot[index_ref_prot]
			flag = Is_empty(mstar,smamin,protmin)	
			print sma[index_ref_sma-index]
			smamin = sma[index_ref_sma-index]
			index = index + 1		
		
	flag = Is_empty(mstar,smamin,protmax)	
	flag_full = 0
	index = 1 
	while flag == 0:
		if flag_full == 0:
			flag = Is_empty(mstar,smamin,protmax)	
			protmax = prot[index_ref_prot+index]
			index = index + 1
			if index_ref_prot+index == size_prot:
				flag_full = 1
				index = 1
		else:
			protmax = prot[index_ref_prot+1]
			flag = Is_empty(mstar,smamin,protmax)	
			smamin = sma[index_ref_sma-index]
			index = index + 1
			
	return smamin,protmin,smamax,protmax		
		

#Function used to get the age estimation, at the selected planetary mass, of the 4 couples that surround the observed couple.
def Find_4(sma,prot,mp,mstar,i,sma_list,prot_list,age_list,massp_list,masss_list):

	
	filename = "./%sMsol/Explo_100_%s_%s_sort.dat" %(mstar,sma,prot)
	arr_ai = []
	arr_roti = []
	arr_chi2 = []
	arr_massp = []
	arr_age = []
	count = 0
	inputfile = open(filename)
	next(inputfile)
	for line in inputfile:
		age,ai,roti,chi2,massp = line.split()
		if float(chi2) < chi2lim: 	
			arr_ai.append(float(ai))
			arr_roti.append(float(roti))
			arr_chi2.append(float(chi2))
			arr_age.append(float(age))
			arr_massp.append(float(massp))
			count = count + 1
	    		
	inputfile.close()	

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
		
		
		
		#residuals = (np.array(arr_age) - func_lin(np.array(arr_massp),*popt)) / np.array(arr_chi2)
		#RMSE = (sum(residuals**2)/(residuals.size-3))**0.5

		#meanage = np.mean(np.array(arr_age))
		#residu_age = np.array(arr_age) - meanage
		#std_age = np.std(arr_age)
		
		#meanmp =  np.mean(func_lin(np.array(arr_massp),*popt))
		#residu_mp = func_lin(np.array(arr_massp),*popt) - meanmp
		#std_mp = np.std(func_lin(np.array(arr_massp),*popt))
		
		#if std_mp != 0.0 and std_age != 0.0:
		#	coef =  np.mean(residu_age*residu_mp)/(std_mp*std_age)
		#else:
		#	coef = 0.0	

			
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
		popt = [0.0, 0.0]
	
	#print np.array(arr_age),func_lin(np.array(arr_massp),*popt)
	coef  = stats.spearmanr(np.array(arr_age),func_lin(np.array(arr_massp),*popt))[0]	
	#coef = 1
		
	if coef != coef:
		#print coef,np.array(arr_age),func_lin(np.array(arr_massp),*popt)
		coef = 0.0	
	
	return coef
	
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
		#sys.exit("Problem with NaN in grid")
		grid = -1.0
		
	return grid
