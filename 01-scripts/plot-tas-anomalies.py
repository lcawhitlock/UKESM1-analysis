# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 12:34:05 2021

@author: lcawh
"""
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

from loaddata import load_data
from getanomalies import tas_anomaly

#set up figure
fig,axes = plt.subplots(nrows=2,ncols=2,figsize=(16,16))
fig.suptitle('Projected NHL temperature anomalies in UKESM1 output',fontsize=16)

#information for subplots
titles = ('Winter (DJF)','Spring (MAM)','Summer (JJA)','Autumn (SON)')
scen = ('ssp126','ssp245','ssp370','ssp585')
season = ((12,1,2),(3,4,5),(6,7,8),(9,10,11))
colours = ('#2CA02C','#FF7F0E','#9467BD','#D62728')
labels = ('SSP1-2.6','SSP2-4.5','SSP3-7.0','SSP5-8.5')

#plotting ranges historical/scenarios
x=range(2014,2101)
y=range(1850,2015)

#plot on subplot
for ax,m,t in zip(axes.flat,season,titles):
    ax.set_title(t)
    ax.set(ylabel='Anomaly \u00B0C')
    ax.set(xlabel='year')
    ax.set_ylim([-5,25])
    ax.plot(y,tas_anomaly(['tas','A','ssp126'],m,endyear=2014, latmin=60),color='#1F77B4',label='Historical')
    for s,c,la in zip(scen,colours,labels):      
        ax.plot(x,tas_anomaly(['tas','A',s],m,startyear=2014,latmin=60),color=c,label=la)
    ax.legend(loc='upper left',frameon=False)

#plt.savefig("../03-output-graphics/final-plots/temp-anom.jpg")
