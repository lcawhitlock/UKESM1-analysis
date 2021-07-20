# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 12:25:07 2021

@author: lcawh
"""
import xarray as xr
import numpy as np

def load_data(info):
    '''function to load and combine historical and scenario data for
    individual variables.
    Arguments:
    =========
    info = array of str, ccontaining variable[0], letter[1], scenario[2]'''
    
    #define paths
    path1 = f'../02-data/ukesm1-output/{info[0]}_{info[1]}mon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc'
    path2 = f'../02-data/ukesm1-output/{info[0]}_{info[1]}mon_UKESM1-0-LL_{info[2]}_r1i1p1f2_gn_*.nc'
    
    #combine data
    data1 = xr.open_mfdataset(paths=path1,combine='by_coords')
    data2 = xr.open_mfdataset(paths=path2,combine='by_coords')
    data3 = xr.concat([data1,data2],dim='time')
    
    return data3

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
    
    

