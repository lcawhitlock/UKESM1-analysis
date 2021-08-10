# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 13:11:36 2021

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

#create map image for each year

startyear = 1850
endyear = 2099
years = range(startyear,endyear+1)
nyrs = range(1,len(years)+1)
len(nyrs)

#define cartopy projections
projection=ccrs.NorthPolarStereo()
transform = ccrs.PlateCarree()

#loop through each year
for y,i in zip(years,nyrs):
    tsl,sat0,sat43,sn,ocean = get_pf(tsl585,sat585,snc585,y)
    plt.ioff()
    
    #text for title
    text = AnchoredText(f'{y}',
                        loc=2,pad=1,frameon=False,
                        prop={'backgroundcolor': 'none','size': 16})
    
    #set up figure
    fig = plt.figure(figsize=(8,8))
    
    ax = plt.axes(projection=projection)
    ax.set_extent([-180,180,45,90],ccrs.PlateCarree())
    ax.gridlines(linewidth=0.5,linestyle='--')
    ax.coastlines()
    ax.add_feature(cartopy.feature.OCEAN,facecolor='aliceblue')
    ax.add_feature(cartopy.feature.LAND, facecolor='whitesmoke')
    ax.add_artist(text)
    ax.contourf(lon,lat,sat0,transform=transform,colors='thistle',alpha=0.5)
    ax.contourf(lon,lat,sat43,transform=transform,colors='plum',alpha=0.5)
    ax.contourf(lon,lat,tsl,transform=transform,colors='purple')
    ax.contourf(lon,lat,sn,transform=transform,colors='white')
    ax.contourf(lon,lat,ocean,transform=transform, colors='aliceblue')
    
    #legend
    ice = patches.Rectangle((0, 0), 1, 1, facecolor="white",edgecolor='purple')
    pfarea = patches.Rectangle((0, 0), 1, 1, facecolor="purple")
    satarea1 = patches.Rectangle((0, 0), 1, 1, facecolor="plum")
    satarea2 = patches.Rectangle((0, 0), 1, 1, facecolor="thistle")
    labels = ['Ice sheet',
              'Continuous permafrost (>90%)',
              'Discontinuous permafrost (>50%)',
              'Permafrost affected area (>1%)']
    plt.legend([ice,pfarea, satarea1,satarea2], labels,loc='lower left',frameon=True,
               fontsize=12,framealpha=1,facecolor='white',edgecolor='grey')
    plt.savefig(f'../03-output-graphics/gifs/ssp585/ssp585_{i:04d}.png',dpi=80,bbox_inches='tight')
    plt.close(fig)
    ax.clear()

#create gif direct in the command line using ImageMagick
magick convert -delay 12 frames/frame_*.png -delay 200 frames/fina/frame_0250.png 
-dispose background -loop 0 testdelay.gif