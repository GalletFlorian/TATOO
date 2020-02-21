import numpy as np
from scipy.interpolate import griddata
from scipy import stats
from scipy.optimize import curve_fit

#chi2 threshold used in Find_4 and in Is_empty
chi2lim = 9.0

	
arr_agemod_min = []
arr_agemod_max = []


arr_agemod_min_rand = []
arr_agemod_max_rand = []

#Useful functions

def floatt3(number) : 
#return a float with 3 digit precision
    return "%.3f"%number
    
def floatt2(number) : 
#return a float with 2 digit precision
    return "%.2f"%number
    
def floatt1(number) : 
#return a float with 1 digit precision
	return "%.1f"%number

def func_sq(x,a,b,c): 
#return a power law function value
	return a*x**2.0+ b*x + c
	
def func_lin(x,a,b): 
#return a linear function value
	return a*x + b

	
def clean(array): 
#function that "clean" a given array of size 4
	array = [0.0,0.0,0.0,0.0]
	return array
	
		
def Is_empty(mstar,sma,prot): 
#Function used to check the content of a given pre-compiled age exploration files
#If empty return flag = 0 else flag > 0
	arr_ai = []
	arr_roti = []
	arr_chi2 = []
	arr_massp = []
	arr_age = []
	filename = "../Data/%sMsol/Explo_100_%s_%s_sort.dat" %(mstar,floatt3(sma),floatt2(prot))
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
#Function used to control on the containt of the pre-compiled exploration files using 
#the function Is_empty above.
#Re-ajust the 4 corner points if needed
	
	prot = protin 
	sma = smain
	index_ref_prot = iprot
	index_ref_sma = isma

	size_prot = len(prot)
	size_sma = len(sma)
	
	#smamax
	flag = Is_empty(mstar,smamax,protmin)
	flag_full = 0
	index = 1
	while flag == 0:
		if flag_full == 0:
			flag = Is_empty(mstar,smamax,protmin)	
			protmin = prot[index_ref_prot-index]
			index = index + 1
			if index_ref_prot-index <= 0:
				flag_full = 1
				index = 1
		else:
			if index_ref_sma+1+index >= size_sma:
				print("No non empty pre-compiled file found. Stop")
				exit()
				
			protmin = prot[index_ref_prot]
			flag = Is_empty(mstar,smamax,protmin)	
			smamax = sma[index_ref_sma+1+index]
			index = index + 1
				
	flag = Is_empty(mstar,smamax,protmax)	
	flag_full = 0
	index = 1 
	while flag == 0:
		if flag_full == 0:
			flag = Is_empty(mstar,smamax,protmax)	
			protmax = prot[index_ref_prot+1+index]
			index = index + 1
			if index_ref_prot+1+index >= size_prot:
				flag_full = 1
				index = 1
		else:
			if index_ref_sma+1+index >= size_sma:
				print("No non empty pre-compiled file found. Stop")
				exit()
			protmax = prot[index_ref_prot+1]
			flag = Is_empty(mstar,smamax,protmax)	
			smamax = sma[index_ref_sma+1+index]
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
			if index_ref_prot-index <= 0:
				flag_full = 1
				index = 1
		else:
			if index_ref_sma-index <= size_sma:
				print("No non empty pre-compiled file found. Stop")
				exit()
			protmin = prot[index_ref_prot]
			flag = Is_empty(mstar,smamin,protmin)	
			smamin = sma[index_ref_sma-index]
			index = index + 1		
		
	flag = Is_empty(mstar,smamin,protmax)	
	flag_full = 0
	index = 1 
	while flag == 0:
		if flag_full == 0:
			flag = Is_empty(mstar,smamin,protmax)	
			protmax = prot[index_ref_prot+1+index]
			index = index + 1
			if index_ref_prot+1+index >= size_prot:
				flag_full = 1
				index = 1
		else:
			if index_ref_sma-index <= size_sma:
				print("No non empty pre-compiled file found. Stop")
				exit()
			protmax = prot[index_ref_prot+1]
			flag = Is_empty(mstar,smamin,protmax)	
			smamin = sma[index_ref_sma-index]
			index = index + 1
			
	return smamin,protmin,smamax,protmax		
		


def Find_4(sma,prot,mp,mstar,i,sma_list,prot_list,age_list,massp_list,masss_list):
#Function used to get the age estimation, at the selected planetary mass, 
#of the 4 couples that surround the observed couple.
#Return the Pearson correlation coefficient of M_p vs. Age of the file "filename"
	
	filename = "../Data/%sMsol/Explo_100_%s_%s_sort.dat" %(mstar,sma,prot)

	arr_ai = []
	arr_roti = []
	arr_chi2 = []
	arr_massp = []
	arr_age = []
	
	arr_ai_all = []
	arr_roti_all = []
	arr_chi2_all = []
	arr_massp_all = []
	arr_age_all = []
	arr_weight_all = []
	
	for k in range(0,7): 
		arr_ai_all.append([])
		arr_roti_all.append([])
		arr_chi2_all.append([])
		arr_massp_all.append([])
		arr_age_all.append([])
		arr_weight_all.append([])
	
	arr_mean_age_coef = []
	arr_massp_coef = []
	
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
				
			k = int(2*float(massp)-1)
					
			arr_ai_all[k].append(float(ai))
			arr_roti_all[k].append(float(roti))
			arr_chi2_all[k].append(float(chi2))
			arr_weight_all[k].append(1.0/float(chi2))
			arr_age_all[k].append(float(age))
			arr_massp_all[k].append(float(massp))
					
			count = count + 1
	    				    		 		
	inputfile.close()	

	count_mp = 0
	 
	for k in range(0,7):
		if arr_weight_all[k]:

			arr_mean_age_coef.append(np.average(np.array(arr_age_all[k]), axis=None, weights=np.array(arr_weight_all[k])))
			arr_massp_coef.append(arr_massp_all[k][0])
			count_mp = count_mp + 1
			
	if count > 0 and count_mp > 1:
		
		popt, pcov = curve_fit(func_lin, np.array(arr_massp_coef), np.array(arr_mean_age_coef))
		a = popt[0]
		b = popt[1]
		time_mod = a*float(mp)+b
					
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
		
	coef_pear  = stats.pearsonr(np.array(arr_mean_age_coef),func_lin(np.array(arr_massp_coef),*popt))[0]	
	
	coef = coef_pear
	
	if coef != coef:
		coef = 0.0	
	
	return coef
	
def Find_age(sma,prot,sma_list,prot_list,age_list,massp_list,masss_list):
#Given the information of Find_4, Find_age perform a 3D interpolation using the Griddata tool.
#Return the estimated 3D age 
	
	arr_xy = [[sma_list[i],prot_list[i]] for i in range(len(sma_list))]

	
	age = 0.0
	
	if sma_list[0] > 0:
		smaobs = float(sma)
		protobs = float(prot)
		age = griddata(arr_xy, age_list, (smaobs,protobs), method='cubic')
	else:
		age = 0.0 
	
	if age != age:
		age = -1.0

	return age
	
	