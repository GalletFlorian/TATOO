import numpy as np
import random
import sys
from Function import Find_4
from Function import clean
from Function import Control_file
from Function import Find_age
import argparse

np.seterr(divide='ignore', invalid='ignore')


def floatt3(number) :
    return "%.3f"%number
    
def floatt2(number) :
    return "%.2f"%number
    
def floatt1(number) :
	return "%.1f"%number
	
#List of pre-compiled age estimate couples 
massstar = np.array([0.5,0.6,0.7,0.8,0.9,1.0])
prot = np.array([2,4,6,8,10,11,12,13,14,15,16,17,18,19,20,22,24,26,28,30])
sma = np.array([0.008,0.009,0.010,0.011,0.012,0.013,0.014,0.015,0.02,0.025,0.03,0.035,0.04,0.045,0.05,0.055,0.06,0.065,0.07,0.075,0.08,0.085,0.09,0.095])

size_mass = len(massstar)
size_prot = len(prot)
size_sma = len(sma)

#Input parameter: 
# 1) Planetary orbital period (Porb) in days 
# 2) Stellar rotation period (Prot) in days
# 3) Mass of the planet in Mjup
# 4) Mass of the star in Msun
# Optional
# 5) Name of the system
# 6) Error_Prot in days
# 7) Error_Porb in days

if len(sys.argv) < 4:
	print("Not enouth information")
	print("TATOO needs: Porb_obs |  Prot_obs | M_planet | M_star  (| Name of the system | Error_Prot | Error_Porb)")
	sys.exit()
	

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs=4)
parser.add_argument('system',nargs='?')
parser.add_argument('error_prot',nargs='?')
parser.add_argument('error_porb',nargs='?')

args = parser.parse_args()

porbobs = float(args.input[0])
protobs = float(args.input[1])
mp = float(args.input[2])
mstarobs = float(args.input[3])

G = 6.6742367e-11
Mjup = 1.8986112e27    
Msun = 1.98892e30 
pi = 3.14159265359

smaobs =  ( (porbobs * 24.*3600. / (2*pi))**2.0 * G * (mstarobs*Msun+mp*Mjup))**(1./3.) / 1.49598e11


if (args.system == None):
	system = "Unknown_system"
else:	
	system = args.system


if (args.error_prot == None):
	print("Standard Error_Prot = 0.4 days")
	sigmarot = 0.4	
else:
	sigmarot = float(args.error_prot)

if (args.error_porb == None):
	print("Standard Error_Porb = 1e-3 days")
	sigmasma = 0.002	
else:
	sigmaporb = float(args.error_porb)	
	sigmasma =  ( (sigmaporb * 24.*3600. / (2*pi))**2.0 * G * (mstarobs*Msun+mp*Mjup))**(1./3.) / 1.49598e11	
		

#Number of age estimations for a given system. 
nstep = 100

#Nbtest_limit indicate the maximum number of iterations without finding any good enough age. 
Nbtest_limit = 100

#Assess the robustness of the age estimation? When robust = 1, TATOO will randomly explore the vicinity of the 4
#corner points. 
robust = 0

#If you want to display the gyrochronological age based on the calibration of Angus et al. (2019), AJ, 158, 173
gyro = 1


#The minimum value of the spearmanr coefficient.
coeflim = 0.7


#Number of try before crash
Nbtest_step_try = 5

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
	
	protrand = -100
	smarand = -100
	fail = 0 
	#random exploration on P_rot and SMA given Error_Prot and Error_SMA
	while(protrand <= prot[0] or protrand >= prot[-1]): 
		protrand = random.uniform(protobs-sigmarot,protobs+sigmarot)
		fail += 1 
		if(fail > 5):
			exit()
	while(smarand <= sma[0] or smarand >= sma[-1]): 	
		smarand = random.uniform(smaobs-sigmasma, smaobs+sigmasma)
		fail += 1 	
		if(fail > 5):
			exit()
	
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
	coef_min[0] = Find_4(floatt3(smamin),floatt2(protmin),mp,massstarmin,0,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_min[1] = Find_4(floatt3(smamax),floatt2(protmin),mp,massstarmin,1,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_min[2] = Find_4(floatt3(smamin),floatt2(protmax),mp,massstarmin,2,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_min[3] = Find_4(floatt3(smamax),floatt2(protmax),mp,massstarmin,3,sma_list,prot_list,age_list,massp_list,masss_list)
	
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
	coef_max[0] = Find_4(floatt3(smamin),floatt2(protmin),mp,massstarmax,0,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_max[1] = Find_4(floatt3(smamax),floatt2(protmin),mp,massstarmax,1,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_max[2] = Find_4(floatt3(smamin),floatt2(protmax),mp,massstarmax,2,sma_list,prot_list,age_list,massp_list,masss_list)
	coef_max[3] = Find_4(floatt3(smamax),floatt2(protmax),mp,massstarmax,3,sma_list,prot_list,age_list,massp_list,masss_list)
	
	age_max = Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)
	
	
	if age_max >= 0.0:
		flag_max = 1
		arr_agemod_max.append(age_max) #for massstarmax
	
	coef_max_f = np.mean(coef_max)
		
	#Control on the Pearson averaged correlation coefficient. It is used to ensure a good enough linear relation between the estimated age and the 
	#mass of the planet?
	Nbtest = Nbtest + 1
	if (abs(coef_min_f) > coeflim and abs(coef_max_f) > coeflim) and flag_max*flag_min == 1:
		#print (Nb,arr_agemod_min[Nb],arr_agemod_max[Nb],coef_min_f,coef_max_f)
		Nb = Nb + 1
		Nbtest = 0

	
	if Nbtest == Nbtest_limit:
		Nbtest_step = Nbtest_step + 1
		if Nbtest_step > Nbtest_step_try:
			print ("Number of crashes reached, stop.")
			sys.exit()
		print("Limit of {} iterations reached for {} and coeflim = {}. No linear relation between the age and the mass of the planet found!".format(Nbtest_limit,system,coeflim))
		#print "Limit of",Nbtest_limit,"iterations reached for", system,"and coeflim =",coeflim, ". No linear relation between the age and the mass of the planet found!"
		print ("Try with reduced coeflim of {}".format(coeflim*0.8))
		Nbtest = 0
		coeflim = coeflim * 0.8
		

	
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

		coef_min[0] = Find_4(floatt3(smaminrand),floatt2(protminrand),mp,massstarmin,0,sma_list,prot_list,age_list,massp_list,masss_list)
		coef_min[1] = Find_4(floatt3(smamaxrand),floatt2(protminrand),mp,massstarmin,1,sma_list,prot_list,age_list,massp_list,masss_list)
		coef_min[2] = Find_4(floatt3(smaminrand),floatt2(protmaxrand),mp,massstarmin,2,sma_list,prot_list,age_list,massp_list,masss_list)
		coef_min[3] = Find_4(floatt3(smamaxrand),floatt2(protmaxrand),mp,massstarmin,3,sma_list,prot_list,age_list,massp_list,masss_list)

		age_min = Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)
	
		if age_min >= 0.0:
			flag_min = 1
			arr_agemod_min_rand.append(age_min) #for massstarmin

		coef_min_f = np.mean(coef_min)
	

		sma_list=clean(sma_list)
		prot_list=clean(prot_list)
		age_list=clean(age_list)
		massp_list=clean(massp_list)
		masss_list=clean(masss_list)


		coef_max[0] = Find_4(floatt3(smaminrand),floatt2(protminrand),mp,massstarmax,0,sma_list,prot_list,age_list,massp_list,masss_list)
		coef_max[1] = Find_4(floatt3(smamaxrand),floatt2(protminrand),mp,massstarmax,1,sma_list,prot_list,age_list,massp_list,masss_list)
		coef_max[2] = Find_4(floatt3(smaminrand),floatt2(protmaxrand),mp,massstarmax,2,sma_list,prot_list,age_list,massp_list,masss_list)
		coef_max[3] = Find_4(floatt3(smamaxrand),floatt2(protmaxrand),mp,massstarmax,3,sma_list,prot_list,age_list,massp_list,masss_list)

		age_max = Find_age(smarand,protrand,sma_list,prot_list,age_list,massp_list,masss_list)

		if age_max >= 0.0:
			flag_max = 1
			arr_agemod_max_rand.append(age_max) #for massstarmax
	
		coef_max_f = np.mean(coef_max)
		
		
		
	
##################################################

age_med_min = np.median(arr_agemod_min, 0)
std_age_min = np.std(arr_agemod_min)

age_med_max = np.median(arr_agemod_max, 0)
std_age_max = np.std(arr_agemod_max,0)

arr_avgage = []

for i in range(0,Nb):
	arr_age = [arr_agemod_min[i],arr_agemod_max[i]]
	arr_masss = [massstarmin,massstarmax]
	popt = np.polyfit(np.array(arr_masss), np.array(arr_age),1)
	a = popt[0]
	b = popt[1]
	arr_avgage.append(a*mstarobs + b)
	
age_med_avg = np.median(arr_avgage, 0)
std_age_avg = np.std(arr_avgage)

print ("Estimated averaged age for {} = {} +- {} Myr with a spearman coefficient of {}.".format(system,age_med_avg,std_age_avg,coeflim))


##################################################

if robust == 1:
	arr_avgage = []

	for i in range(0,Nb):
		arr_age = [arr_agemod_min_rand[i],arr_agemod_max_rand[i]]
		arr_masss = [massstarmin,massstarmax]
		popt = np.polyfit(np.array(arr_masss), np.array(arr_age),1)
		a = popt[0]
		b = popt[1]
		arr_avgage.append(a*mstarobs + b)
	
	age_med_avg = np.median(arr_avgage, 0)
	std_age_avg = np.std(arr_avgage)

	print ("Robustness: estimated averaged age for {} = {} +- {} Myr.".format(system,age_med_avg,std_age_avg))
	
	
##################################################

if gyro == 1:	
	
	arr_age_gyro = []
	for nb_gyro in range(0,nstep):
		
		protrand = random.uniform(protobs-sigmarot,protobs+sigmarot)
		#Based on the calibration from Angus et al. 2015
		BV_ = np.array([1.6033,1.5906,1.5640,1.5176,1.4476,1.2513,1.0070,0.8289,0.6900,0.5906,0.5077,0.4418,0.3368,0.2474])
		flag_gyro = 0   
		for i in range(0,len(BV_)): 
			if float(mstarobs) <= 0.1*(i+2) and flag_gyro==0:
				a = (BV_[i]-BV_[i-1])/(0.1*(i+2) - (0.1*(i+1)))
				b = BV_[i]-a*0.1*(i+2)
				BV = a*mstarobs+b
				flag_gyro = 1
	
		age_gyro =(float(protrand) / (0.4*(BV-0.45)**0.31) )**(1.0/0.55)
		arr_age_gyro.append(age_gyro)
	
		#Based on the calibration from Delorme et al. (2011) MNRAS, 413, 2218
		#JK_ = np.array([0.8654,0.8529,0.8419,0.8268,0.8023,0.7439,0.5936,0.4751,0.3670,0.3116,0.2622,0.2119,0.1673,0.1392])
	
		#flag_gyro = 0   
		#for i in range(0,len(JK_)): 
		#	if float(mstarobs) <= 0.1*(i+2) and flag_gyro==0:
		#		a = (JK_[i]-JK_[i-1])/(0.1*(i+2) - (0.1*(i+1)))
		#		b = JK_[i]-a*0.1*(i+2)
		#		JK = a*mstarobs+b
		#		flag_gyro = 1
		
		#pow=1./0.56

		#avper=10.603
		#avcol=0.570
		#dxdy=12.314
		#age_clus=625.0

		#disp=0.45
		#per_c=avper+dxdy*(JK-avcol)
		#age_gyro=age_clus*(float(protobs)/per_c)**pow
	
	age_gyro_med_avg = np.median(arr_age_gyro, 0)
	std_age_gyro_avg = np.std(arr_age_gyro)
	
	print ("Age gyro for {} = {} +- {} Myr.".format(system,age_gyro_med_avg,std_age_gyro_avg))
