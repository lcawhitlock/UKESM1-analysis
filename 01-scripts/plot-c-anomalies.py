# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:42:10 2021

@author: lcawh
"""

import matplotlib.pyplot as plt
import xarray as xr
import numpy as np

from loaddata import load_mass
from getanomalies import c_anomaly

#set up figure

fig,axes = plt.subplots(nrows=2,ncols=2,figsize=(16,16))
fig.suptitle('Projected terrestrial carbon anomalies in UKESM1 output',fontsize=16)
titles = ('Global soil carbon anomaly','NHL soil carbon anomaly','Global vegetation carbon anomaly',
          'NHL vegetation carbon anomaly')
var = ('cSoil','cVeg','cSoil','cVeg')
n = ('E','L','E','L')
scen = ('ssp126','ssp245','ssp370','ssp585')
latmin = (-90,60,-90,60)
colours = ('#2CA02C','#FF7F0E','#9467BD','#D62728')
labels = ('SSP1-2.6','SSP2-4.5','SSP3-7.0','SSP5-8.5')

x=range(2014,2101)
y=range(1850,2015)

#plot on subplot
for ax,v,n,l,t in zip(axes.flat,var,n,latmin,titles):
    ax.set_title(t)
    ax.set(ylabel='PgC')
    ax.set(xlabel='year')
    ax.plot(y,c_anomaly([v,n,'ssp126'],1850,2014,l,90),color='#1F77B4',label='Historical')
    for s,c,la in zip(scen,colours,labels):      
        ax.plot(x,c_anomaly([v,n,s],2014,2100,l,90),color=c,label=la)
    ax.legend(loc='best',frameon=False)

#plt.savefig("../03-output-graphics/final-plots/c-anom.jpg")
