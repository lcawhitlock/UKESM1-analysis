# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:02:46 2021

@author: lcawh
"""

import xarray as xr
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches


import cartopy
import cartopy.crs as ccrs
import scipy

from masks import get_masks

areacell = xr.open_dataset('../02-data/ukesm1-output/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc')
#set lat and lon
lat = areacell['lat']
lon = areacell['lon']

#define cartopy projections
projection = ccrs.NorthPolarStereo()
transform = ccrs.PlateCarree()

#set up figure
#sublot_kw hack from cartopy/mpl formum
fig,axes = plt.subplots(nrows=3,ncols=2,figsize=(16,24),
                        subplot_kw=dict(projection=projection))
fig.suptitle('Projected permafrost extent in UKESM1 output',fontsize=16)
titles = ('Historical baseline 1850-1990','Baseline 1961-1990','SSP 1-2.6','SSP 2-4.5',
          'SSP 3-7.0','SSP 5-8.5')
masks = (get_masks('ssp126',1850,1900),get_masks('ssp126',1961,1990),
         get_masks('ssp126',2090,2099),get_masks('ssp245',2090,2099),
         get_masks('ssp370',2090,2099),get_masks('ssp585',2090,2099))
startyear = (1850,1961,2090,2090,2090,2090)
endyear = (1900,1991,2099,2099,2099,2099)

#plot on subplot
for ax,m,t in zip(axes.flat,masks,titles):
    ax.set_title(t)
    ax.set_extent([-180,180,50,90],ccrs.PlateCarree())
    ax.gridlines(linewidth=0.5,linestyle='--')
    ax.coastlines()
    ax.add_feature(cartopy.feature.OCEAN,facecolor='aliceblue')
    ax.add_feature(cartopy.feature.LAND, facecolor='whitesmoke')
    im = ax.contourf(lon,lat,m[1],transform=transform,colors='thistle',alpha=0.5)
    im = ax.contourf(lon,lat,m[2],transform=transform,colors='plum',alpha=0.5)
    im = ax.contourf(lon,lat,m[0],transform=transform,colors='purple')
    im = ax.contourf(lon,lat,m[3],transform=transform, colors='white')
    im = ax.contourf(lon,lat,m[4],transform=transform, colors='aliceblue')

ice = patches.Rectangle((0, 0), 1, 1, facecolor="white",edgecolor='purple')
pfarea = patches.Rectangle((0, 0), 1, 1, facecolor="purple")
satarea1 = patches.Rectangle((0, 0), 1, 1, facecolor="plum")
satarea2 = patches.Rectangle((0, 0), 1, 1, facecolor="thistle")
labels = ['Ice sheet',
          'Mean soil temperature at 2 m depth < 0\u00B0C',
          'Mean annual surface air temperature < - 4.3\u00B0C',
          'Mean annual surface air temperature < 0\u00B0C']
plt.legend([ice, pfarea, satarea1,satarea2], labels,loc='lower center', 
           bbox_to_anchor=(-1.2, -0.2, 1., .2),mode="expand", borderaxespad=0.,frameon=False)