# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:38:02 2021

@author: lcawh
"""
import numpy as np
import xarray as xr

from loaddata import load_data,load_mass

def tas_anomaly(info,months,startyear=1850,endyear=2100,latmin=-90,
             latmax=90):
    '''function to calculate seasonal surface air temp anomaly in deg
    C for speccified months adn tiemframe.
    Arguments:
    =========
    info = array of str, ccontaining variable[0], letter[1], scenario[2]#
    months (int) = list of int containing numbered months
    startyear (int) = first year of time slice
    endyear(int) = last year of time slice
    latmin (int) = minimum latitude of location slice
    latmax (int)  = maximum latitude of location slice'''
    
    #load data
    d = load_data(info)
    
    #define variables
    tas= d.tas
    lon= d.lon
    lat= d.lat
    
    #define weights (different cell areas!)
    tas_slice = tas.sel(lat=slice(latmin,latmax))

    weights = np.cos(np.deg2rad(tas_slice.lat))
    weights.name = "weights"

    tas_weighted = tas_slice.weighted(weights)
    tas_wmn = tas_weighted.mean(('lon','lat'))
        
    #get months only
    s = tas_wmn.sel(time=tas_wmn['time.month'].isin(months))
    
    #get climatology for each month compared to preindustrial levels
    bl = s.sel(time=slice('1850-01-01', '1900-12-16'))
    bl1 = bl.groupby('time.year').mean('time')
    bl2 = bl1.mean()
    
    s2 = s.sel(time=slice(f'{startyear}-01-01',f'{endyear}-12-16'))
    s3 = s2.groupby('time.year').mean('time')
    
    #final anomalies
    anom = s3 - bl2

    
    return anom

def c_anomaly(info,startyear,endyear,latmin,latmax):
    
    data = load_mass(info)
    
    #get baseline
    d = data.sel(time=slice('1850-01-01','1900-12-16'))
    d1 = d['mass']
    d2 = d1.mean(dim='time')
    d3 = d2.sel(lat=slice(latmin,latmax))
    bl = d3.sum(dim=('lat','lon'))
    
    #get total
    m = data.sel(time=slice(f'{startyear}-01-01',f'{endyear}-12-16'))
    m1 = m.groupby('time.year').mean('time')
    m2 = m1['mass']
    m3 = m2.sel(lat=slice(latmin,latmax))
    ttl = m3.sum(dim=('lat','lon'))
    
    anom = ttl-bl
    
    return anom