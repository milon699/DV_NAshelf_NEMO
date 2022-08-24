# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 14:35:27 2022

Script with util plot functionss

@author: milon
"""

import seawater as sw
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

def ts_append(levels,axh=None):
    """
    ts_append(levels,axh=None)
    
    function to append TS plots with density contours and axis labels
    
    INPUT:
    levels:    array of density levels that should be plotted, e.g. np.arange(20,29,0.5)
    axh:       axis handle if desired
    
    """
    
    # get axis limits of current plot
    if axh:
        tlim = np.ceil(axh.get_ylim())
        slim = np.ceil(axh.get_xlim())
    else: 
        axh = plt.gca()
        tlim = np.ceil(axh.get_ylim())
        slim = np.ceil(axh.get_xlim())
        
    # create meshgrid and derive  potential density
    sm,tm = np.meshgrid(np.arange(slim[0]-7,slim[1]+7),np.arange(tlim[0]-7,tlim[1]+7))
    densm = sw.pden(sm,tm,0,0)
    
    # plot contours
    cc=axh.contour(sm,tm,densm-1000,colors='k',alpha=0.3,zorder=0,levels=levels,linestyle='dashed')
    
    # set axis limits to original
    axh.set_ylim(tlim)
    axh.set_xlim(slim)
    
    plt.clabel(cc,fmt='%2.1f',fontsize=8)

    axh.set_xlabel('Salinity in g/kg')
    axh.set_ylabel('Temperature [°C]')
    axh.grid(False)

def vertical_append(levels, sec, axh = None):
    
    """
    Function to append for vertical sections contours 
    INPUT:
    levels:    array of density levels that should be plotted, e.g. np.arange(20,29,0.5)
    axh:       axis handle if desired
    sec:      Dataset of a vertical cut-off section in format of NEMO output 
    
    """

    #Create meshgrid and calculate pressure out of depth information
    latm, depthm = np.meshgrid(sec.lat, sec.z)
    pres = sw.pres(depthm, latm)
    
    #Calculate density out of temperature, salinity and pressure data
    dens = sw.pden(sec.vosaline, sec.votemper, pres)
    
    #Plot contours
    cc = axh.contour(sec.c/1e3, sec.z, dens - 1000, colors = 'black', alpha = 1, levels = levels)

    plt.clabel(cc, fmt = '%2.1f', fontsize = 12)
    axh.grid(False)

def butterworth_lowpass_filter(data, order = 2, cutoff_freq = 1.0/10.0, axis = 0):
    """Filter input data corresponding to a lowpass filter

    For unfiltered data, use `cutoff_freq=1`.

    Frequencies in unit 1/month 

    Currently, this returns a numpy array.
    """

    B, A = signal.butter(order, cutoff_freq, output="ba")
    
    return signal.filtfilt(B, A, data, axis=0)
