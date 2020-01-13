import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from tkinter import * 
from tkinter import ttk
from TATOO_forGUI import TATOO
import os
import time
from pathlib import Path
import webbrowser

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


master = Tk()
master.title("TATOO v1")

frame1 = Frame(master)
frame1.grid(row = 3, column = 4) 


frame2 = Frame(master)
frame2.grid(row = 4, column = 4) 

frame_result = Frame(master, bd=1)
frame_result.grid(row = 5, column = 1, columnspan = 4)

def alert():
    print("Ok")
    

def message(msg):
    download_message.configure(text=msg)
    download_message.grid(row=1)
    frame_result.update_idletasks()


download_message = Label(frame_result)
def download():
    global download_message 
    #download_message = Label(frame_result)
    file = Path("../Data/0.5Msol/")
    if file.exists():
        download_message = Label(frame_result,text="Directory already exists.")
        download_message.grid(row=1)
        frame_result.update_idletasks()
    else:    
        message("Downloading file, please wait.")
        mkdir = "mkdir ../Data/"
        os.system(mkdir)
        os.chdir("../Data/")    
        os.system("pwd")
        dl = "gdown --id 1VlQa1eEuAZOJp2OXijK8zh5RIvhjCRZO"
        os.system(dl)
        message("Data.tar.gz downloaded.Extraction of file.")
        extract = "tar zxvf Data.tar.gz"
        os.system(extract)
        remove = "rm Data.tar.gz"
        os.system(remove) 
        os.chdir("../GUI/") 
        message("Extraction done.")
        time.sleep(0.4)
        download_message.destroy()
        
def help_tatoo():
    print("© Florian Gallet 2019")
    print("Gallet 2020,A&A")
    webbrowser.open_new(r"https://github.com/GalletFlorian/TATOO/blob/master/README.rst")

menubar = Menu(master)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Dowload", command=download)
menu1.add_separator()
menu1.add_command(label="Quit", command=master.quit)
menubar.add_cascade(label="File", menu=menu1)

#Not included yet
#menu2 = Menu(menubar, tearoff=0)
#menu2.add_command(label="Tbc", command=alert)
#menu2.add_command(label="Tbc", command=alert)
#menu2.add_command(label="Tbc", command=alert)
#menubar.add_cascade(label="Edit", menu=menu2)

#menu3 = Menu(menubar, tearoff=0)
#menu3.add_command(label="About", command=help_tatoo)
#menubar.add_cascade(label="Help", menu=menu3)

master.config(menu=menubar)

Label(frame1,text="M_star =",width = 10,anchor='e').grid(row=0,column = 0, sticky = E)
Label(frame1,text="P_rot =",width = 10,anchor='e').grid(row=1,column = 0, sticky = E)
Label(frame1,text="Error_prot =",width = 10,anchor='e').grid(row=2,column = 0, sticky = E)
Label(frame1,text="Mp =",width = 10,anchor='e').grid(row=0,column = 2, sticky = E)
Label(frame1,text="Porb =",width = 10,anchor='e').grid(row=1,column = 2, sticky = E)
Label(frame1,text="Error_porb =",width = 10,anchor='e').grid(row=2,column = 2, sticky = E)


mstar = Entry(frame1, width = 8)
mstar.insert(0, 0.71)

prot = Entry(frame1, width = 8)
prot.insert(0, 15.6)

e_prot = Entry(frame1, width = 8)
e_prot.insert(0, 0.4)

mp = Entry(frame1, width = 8)
mp.insert(0, 2.052)

porb = Entry(frame1, width = 8)
porb.insert(0, 0.84)

e_porb = Entry(frame1, width = 8)
e_porb.insert(0, 1.0e-3)

mstar.grid(row=0, column=1, sticky = W)
prot.grid(row=1, column=1, sticky = W)
e_prot.grid(row=2, column=1, sticky = W)

mp.grid(row=0, column=3, sticky = W)
porb.grid(row=1, column=3, sticky = W)
e_porb.grid(row=2, column=3, sticky = W)

#frame1.pack()

#frame_result.pack()


def saisie():
    print("\nControl on initial parameters")
    print("M_star: %s Msun\nP_rot: %s days\nError_prot: %s days\nMp: %s Mjup\nPorb: %s days\nError_porb: %s days" %(mstar.get(), prot.get(), e_prot.get(),mp.get(), porb.get(), e_porb.get() ))              
    global coeflim 
    coeflim_var = coeflim.get()
    if is_number(coeflim_var) == False :
        coeflim_var = 0.7
    else:
        coeflim_var = float(coeflim_var)
        
    print("Coef. lim=",coeflim_var)
    
    print("Gyro =",gyro_var.get())
    print("Robust =",robust_var.get())

def run():
    
    #run TATOO here => return age of system
    #Then display age of system
    file = Path("../Data/0.5Msol/")
    if file.exists():
        G = 6.6742367e-11
        Mjup = 1.8986112e27    
        Msun = 1.98892e30
        pi = 3.14159265359
    
        age, e_age, age_gyro = 0.0, 0.0, 0.0
    
        global coeflim 
        coeflim_var = coeflim.get()
        if is_number(coeflim_var) == False :
            coeflim_var = 0.7
        else:
            coeflim_var = float(coeflim_var)
        
        global nbstep 
        nbstep_var = nbstep.get()
        if is_number(nbstep_var) == False :
            nbstep_var = 10
        else:
            nbstep_var = float(nbstep_var)
                 
        _gyro_var = gyro_var.get()
        _robust_var = robust_var.get()
    
        _mstar = float(mstar.get())
        _prot = float(prot.get())
        _e_prot = float(e_prot.get())
        _mp = float(mp.get())
        _porb = float(porb.get())
        _sma =  ( (_porb * 24.*3600. / (2*pi))**2.0 * G * (_mstar*Msun+_mp*Mjup))**(1./3.) / 1.49598e11
        _e_porb = float(e_porb.get())
        _e_sma =  ( (_e_porb * 24.*3600. / (2*pi))**2.0 * G * (_mstar*Msun+_mp*Mjup))**(1./3.) / 1.49598e11
        age, e_age, age_gyro = TATOO(frame_result,_mstar,_prot,_e_prot,_mp,_sma,_e_sma, " ", _gyro_var, _robust_var, coeflim_var,nbstep_var)    
        global labelage_gyro
        global labelage_tidal
        if (_gyro_var == 1):
            if (age > 0.0):
                charage = "Age of the system = "+str(round(age,2))+" +- "+str(round(e_age,2))+" Myr"
                charage_gyro = "Age_gyro = "+str(round(age_gyro,2))+" Myr"
                labelage_tidal = Label(frame_result,text=charage)
                labelage_tidal.grid(row=0)
                
                labelage_gyro = Label(frame_result,text=charage_gyro)
                labelage_gyro.grid(row=1)
            else:
                labelage_tidal.destroy()
                labelage_gyro.destroy()
                download_message.destroy()
                frame_result.update_idletasks()
        else:   
            if (age > 0.0):
                charage = "Age of the system = "+str(round(age,2))+" +- "+str(round(e_age,2))+" Myr"
                labelage_tidal = Label(frame_result,text=charage)
                labelage_tidal.grid(row=0)
                
                labelage_gyro.destroy()
                download_message.destroy()

    else:
        message("Download data first")
 

gyro_var = IntVar(value=1)
Checkbutton(frame1, text="Gyro", variable=gyro_var).grid(row=4,column=0,sticky = W)

robust_var = IntVar()
Checkbutton(frame1, text="Robust", variable=robust_var).grid(row=4,column=1,sticky = W)

coeflim = Entry(frame1, width = 8)
coeflim.insert(0, "Coef limit")
coeflim.grid(row=4, column=2, sticky = W+E)   

nbstep = Entry(frame1,width = 8)
nbstep.insert(0, "Nb_step")
nbstep.grid(row=4, column=3, sticky = W+E)   

Button(frame2,text='Run',command=run).grid(row=0,column=3, sticky = W)
Button(frame2,text='Control',command=saisie).grid(row=0,column=4,sticky = W)
Button(frame2,text='Quit',command=master.quit).grid(row=0,column=5,sticky = W)

master.mainloop()


master.destroy()

