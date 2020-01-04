# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:52:06 2016

@author: Luke Griffiths
"""
import numpy as np
import pylab as plt
import matplotlib
from matplotlib.widgets import Slider, Button
#from experiment import ShenckExperiment
from davidModel import DavidModel
import pandas as pd
plt.close('all')

#%% Set parameters
rcParams = matplotlib.rcParams
rcParams['svg.fonttype'] = 'none'
rcParams['font.sans-serif'] = ['Arial']
rcParams['font.family'] = 'sans-serif'
rcParams['font.size'] = '14'
rcParams['legend.numpoints'] = 1

#%% Input parameters (CAN BE CHANGED)

# data filepath
filepath = './data/data_template.xlsx'

# range of possible aspect ratio values for the model (x10-4)
alpha_max = 10
alpha_min = 0.1
alpha_step = 0.1

# range of possible crack densities
Y_max = 7
Y_min = 0.1
Y_step = 0.1

#%% Load data
data = pd.read_excel(filepath)
data_stress = data['sigV'] # axial stress data
model_stress = data['sigV'] # axial stress for model (same as data)
data_strain = data['defAx'] # axial strain data

def std(model, data): # Calculate standard deviation beteen model and data
    if len(data) == len(model):
        return np.sqrt(np.sum(np.square(data - model))/len(data) )
    else: 
        return -1

alpha = np.arange(alpha_min, alpha_max, alpha_step)
Y = np.arange(Y_min, Y_max, Y_step)

#%% Draw interactive plot window
fig = plt.figure(figsize = (25/2.54, 15/2.54 ))
plt.ax = plt.subplot(111)
plt.subplots_adjust(left=0.1, bottom=0.45) # Leave blank space
initStrain0 = 0; mu0 = 0.7; E0 = 65; alpha0 = 4; Y0 = 2.7 # Initial parameter values
mod = DavidModel(model_stress, 1e3*E0 , mu0 , Y0 , 1e-4*alpha0, initStrain0)  
 
# plot data stress-strain curve
lData, = plt.plot(data_strain, data_stress, lw=2, color='blue') 
 # plot modelled stress-strain curve
l, = plt.plot(mod.strain, model_stress, lw=2, color='red')

plt.ax.set_xlabel('Strain')
plt.ax.set_ylabel('Stress [MPa]')
plt.title('David et al. (2012) compressibility model', size=14)

# Slider axes
axcolor = 'lightgoldenrodyellow'
axInitStrain = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
axE = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axAlpha  = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
axY = plt.axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
axMu  = plt.axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)

# Create the sliders for each parameter
sE = Slider(axE, "Intact Young's modulus [GPa]", 0, 200, valinit=E0)
sAlpha = Slider(axAlpha, 'Aspect ratio (x10-4)', 0, 10, valinit=alpha0)
sY = Slider(axY, 'Crack density', 0, 10, valinit=Y0)
sMu = Slider(axMu, 'Friction coefficient', 0.3, 1.2, valinit=mu0)
sInitStrain = Slider(axInitStrain, 'Initial strain', -10, 10, valinit=initStrain0)

def update(val): # Update figure with new model
    E0 = sE.val
    alpha = sAlpha.val  
    Y = sY.val
    mu = sMu.val  
    initStrain = sInitStrain.val
    mod = DavidModel(model_stress, 1e3*E0, mu, Y, 1e-4*alpha, initStrain)    
    l.set_xdata(mod.strain)
    l.set_ydata(model_stress)
    plt.draw()
    print('Standard deviation: ' + str(100 * std(mod.strain, data_strain)))
sE.on_changed(update)
sAlpha.on_changed(update)
sY.on_changed(update)
sMu.on_changed(update)
sInitStrain.on_changed(update)

plt.resetax = plt.axes([0.8, 0.025, 0.1, 0.04]) # Reset button coordinates
plt.button = Button(plt.resetax, 'Reset', color=axcolor, hovercolor='0.975')
def reset(event): # Reset values and model
    sE.reset()
    sAlpha.reset()
    sY.reset()
    sMu.reset()
    sInitStrain.reset()
plt.button.on_clicked(reset)

#plt.tight_layout()
plt.show()

