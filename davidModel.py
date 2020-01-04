# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 10:21:02 2016

@author: Luke Griffiths
"""
import numpy as np

class DavidModel:
    def __init__(self, stress, E0 = 1e3, mu = 0.7, Y = 1, alpha = 1e-3, strainInit = 0): 
        # Data properties
        self.mu = mu
        self.sigmax = np.max(stress)
        self.imax = np.argmax(stress)
        self.stress = stress
        self.Y = Y
        self.alpha = alpha
        self.E0 = E0
        self.sigmax_n = self.sigmax*2 / (self.E0*self.alpha) # maximum normalised stress
        self.strainInit = strainInit # Initial strain
        self.calculateStrain() # Calculate strain
        
    def Bc(self, x): # Angle from main stress above which which cracks can close
        return np.arcsin(np.sqrt(1./x)) 
        
    def Bs(self, x): # Angle from main stress below which cracks can slide
        return (np.arccos(self.mu*(1-2./x)/np.sqrt(1+self.mu**2))+np.arctan(1/self.mu))/2.

    def Brs(self, x): # Angle from main stress below which cracks do some crazy reverse sliding
        return 0.5*(np.arccos((self.mu*(self.sigmax_n+x)-4*self.mu)/np.sqrt((self.sigmax_n-x)**2+self.mu**2 * (self.sigmax_n+x)**2)) + 
            np.arctan((self.sigmax_n-x)/(self.mu*(self.sigmax_n+x))))

    def Copen(self, x): # Compliance due to open cracks
        return 2*(np.arcsin(np.sqrt(1./x))-(1./x)*np.sqrt(x-1))
        
    def Cslide(self, x): # Compliance due to sliding crack  
        return ((0.5*(self.Bs(x)-np.sin(4*self.Bs(x))/4.)-self.mu*(np.sin(self.Bs(x))**4)-self.mu*np.cos(2*self.Bs(x))/x)-(0.5*(self.Bc(x)-np.sin(4*self.Bc(x))/4.)-self.mu*(np.sin(self.Bc(x))**4)-self.mu*np.cos(2*self.Bc(x))/x))
        
    def Creverse(self, x): # Compliance due to reverse sliding
        return (((self.Brs(x)-np.sin(4*self.Brs(x))/4.)*(self.sigmax_n/x-1)/2.-self.mu*(self.sigmax_n/x + 1)*(np.sin(self.Brs(x))**4)-2*self.mu*np.cos(2*self.Brs(x))/x) - 
            ((self.Bc(x)-np.sin(4*self.Bc(x))/4.)*(self.sigmax_n/x-1)/2.-self.mu*(self.sigmax_n/x + 1)*(np.sin(self.Bc(x))**4)-2*self.mu*np.cos(2*self.Bc(x))/x))

    def calculateStrain(self):
        # Calculation of 1/E^ i.e. de^/dsig^ for forward sliding
        stress_n = self.stress*2/(self.E0*self.alpha) # Normalise the values of stress
        Einv_n = np.zeros(len(stress_n)) # 1/E^ inversed normalised Young's modulus

        for i in range(self.imax): # Loading curve up until peak
            if stress_n[i] < 1: # i.e. regime where all cracks are still open
                Einv_n[i] = 1 + self.Y*np.pi
            else:
                Einv_n[i] = 1+self.Y*self.Copen(stress_n[i])+self.Y*self.Cslide(stress_n[i])

        for i in range(self.imax, len(stress_n)): # Reverse sliding
            if stress_n[i] > 1: # Regime of reverse sliding
                Einv_n[i] = 1 + self.Y*self.Copen(stress_n[i]) + self.Y*self.Creverse(stress_n[i])
            else: # regime where all cracks are open
                Einv_n[i] = 1 + self.Y*np.pi

        # Numerical intergation of 1/E^ to find e^(sig^)
        eps_n = np.zeros(len(Einv_n)) # Normalised strain as a function of normalised stress
        eps_n[0] = self.strainInit # Initial strain
        for i in range(len(Einv_n)-1):
            eps_n[i+1] = eps_n[i] + (stress_n[i+1]-stress_n[i])*Einv_n[i] # strain = stress/E

        eps=eps_n*(self.alpha/2) # Conversion from normalised to real stress/strain
        
        self.E = self.E0/Einv_n # Scale Young's modulus
        self.strain = np.real(eps);# Take only real values
        
class DavidModel45: # David model but with fixed crack angle of 45°
    def __init__(self, stress, E0 = 1e3, mu = 0.7, Y = 1, alpha = 1e-3, strainInit = 0): 
        # Data properties
        self.mu = mu
        self.sigmax = np.max(stress)
        self.imax = np.argmax(stress)
        self.stress = stress
        self.Y = Y
        self.alpha = alpha
        self.E0 = E0
        self.sigmax_n = self.sigmax*2 / (self.E0*self.alpha) # maximum normalised stress
        self.strainInit = strainInit # Initial strain
        self.calculateStrain() # Calculate strain
        
    def Bc(self, x): # Angle from main stress above which which cracks can close
        return np.arcsin(np.sqrt(1./x)) 
        
    def Bs(self, x): # Angle from main stress below which cracks can slide
        return (np.arccos(self.mu*(1-2./x)/np.sqrt(1+self.mu**2))+np.arctan(1/self.mu))/2.

    def Brs(self, x): # Angle from main stress below which cracks do some crazy reverse sliding
        return 0.5*(np.arccos((self.mu*(self.sigmax_n+x)-4*self.mu)/np.sqrt((self.sigmax_n-x)**2+self.mu**2 * (self.sigmax_n+x)**2)) + 
            np.arctan((self.sigmax_n-x)/(self.mu*(self.sigmax_n+x))))

    def Copen(self, x): # Compliance due to open cracks
        return 2*(np.arcsin(np.sqrt(1./x))-(1./x)*np.sqrt(x-1))
        
    def Cslide(self, x): # Compliance due to sliding crack  
        return ((0.5*(self.Bs(x)-np.sin(4*self.Bs(x))/4.)-self.mu*(np.sin(self.Bs(x))**4)-self.mu*np.cos(2*self.Bs(x))/x)-(0.5*(self.Bc(x)-np.sin(4*self.Bc(x))/4.)-self.mu*(np.sin(self.Bc(x))**4)-self.mu*np.cos(2*self.Bc(x))/x))
        
    def Creverse(self, x): # Compliance due to reverse sliding
        return (((self.Brs(x)-np.sin(4*self.Brs(x))/4.)*(self.sigmax_n/x-1)/2.-self.mu*(self.sigmax_n/x + 1)*(np.sin(self.Brs(x))**4)-2*self.mu*np.cos(2*self.Brs(x))/x) - 
            ((self.Bc(x)-np.sin(4*self.Bc(x))/4.)*(self.sigmax_n/x-1)/2.-self.mu*(self.sigmax_n/x + 1)*(np.sin(self.Bc(x))**4)-2*self.mu*np.cos(2*self.Bc(x))/x))

    def calculateStrain(self):
        # Calculation of 1/E^ i.e. de^/dsig^ for forward sliding
        stress_n = self.stress*2/(self.E0*self.alpha) # Normalise the values of stress
        Einv_n = np.zeros(len(stress_n)) # 1/E^ inversed normalised Young's modulus

        for i in range(self.imax): # Loading curve up until peak
            if stress_n[i] < 1: # i.e. regime where all cracks are still open
                Einv_n[i] = 1 + self.Y*np.pi
            else:
                Einv_n[i] = 1+self.Y*self.Copen(stress_n[i])+self.Y*self.Cslide(stress_n[i])

        for i in range(self.imax, len(stress_n)): # Reverse sliding
            if stress_n[i] > 1: # Regime of reverse sliding
                Einv_n[i] = 1 + self.Y*self.Copen(stress_n[i]) + self.Y*self.Creverse(stress_n[i])
            else: # regime where all cracks are open
                Einv_n[i] = 1 + self.Y*np.pi

        # Numerical intergation of 1/E^ to find e^(sig^)
        eps_n = np.zeros(len(Einv_n)) # Normalised strain as a function of normalised stress
        eps_n[0] = self.strainInit # Initial strain
        for i in range(len(Einv_n)-1):
            eps_n[i+1] = eps_n[i] + (stress_n[i+1]-stress_n[i])*Einv_n[i] # strain = stress/E

        eps=eps_n*(self.alpha/2) # Conversion from normalised to real stress/strain
        
        self.E = self.E0/Einv_n # Scale Young's modulus
        self.strain = np.real(eps);# Take only real values

