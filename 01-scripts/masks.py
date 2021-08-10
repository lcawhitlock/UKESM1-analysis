# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 12:50:05 2021

@author: lcawh
"""

import xarray as xr
import numpy as np

from loaddata import load_data

def get_masks(scenario,startyear,endyear):
    '''function to derive masks of pf area for plotting maps for different
    CC scenarios
    Arguments:
    =========
    scenario (str) = identifier of ssp scenario
    startyear (int) = start year of time period (inclusive)
    endyear (int) = end year of time period (inclusive)'''
    
    #load data
    soil = load_data('tsl','L',scenario)
    air = load_data('tas','A',scenario)
    snow = load_data('snc','LI',scenario)
    
    #get the two-year mean for soil
    d = soil.sel(time=slice(f'{startyear}-01-01',f'{endyear}-12-16'))
    d1 = d['tsl']
    d2 = d1.sel(depth=2.0,method='nearest')
    d3 = d2-273.15
    d4 = d3.mean(dim='time')
    
    #mask for pf areas
    smask = d4
    smask = xr.where(smask>=0,np.nan,smask)
    smask = xr.where(smask<0,1,smask)
    
    #mask for ocean
    ocean = d4
    ocean = ocean.fillna(100)
    ocean = xr.where(ocean<100,np.nan,ocean)
    
    #get annual mean air
    a = air.sel(time=slice(f'{startyear}-01-01',f'{endyear}-12-16'))
    a1 = a['tas']
    a2 = a1-273.15
    a3 = a2.mean(dim='time')
    
    #mask for airtemp contours
    a0mask = a3
    a0mask = xr.where(a0mask>=0,np.nan,a0mask)
    a0mask = xr.where(a0mask<0,1,a0mask)
    
    a43mask = a3
    a43mask = xr.where(a43mask>=-4.3,np.nan,a43mask)
    a43mask = xr.where(a43mask<-4.3,1,a43mask)
    
    #get 10-yr mean snow coverage
    sn = snow.sel(time=slice(f'{startyear}-01-01',f'{endyear}-12-16'))
    sn1 = sn['snc']
    sn2 = sn1.mean(dim='time')
    
    #snow mask
    sncmask = sn2
    sncmask = xr.where(sncmask<95,np.nan,sncmask)
    sncmask = xr.where(sncmask>=95,1,sncmask)
    
    return smask,a0mask,a43mask,sncmask,ocean