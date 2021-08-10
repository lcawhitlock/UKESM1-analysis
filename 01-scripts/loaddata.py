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
    info = array of str, containing variable[0], letter[1], scenario[2]'''
    
    #define paths
    path1 = f'../02-data/ukesm1-output/{info[0]}_{info[1]}mon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc'
    path2 = f'../02-data/ukesm1-output/{info[0]}_{info[1]}mon_UKESM1-0-LL_{info[2]}_r1i1p1f2_gn_*.nc'
    
    #combine data
    data1 = xr.open_mfdataset(paths=path1,combine='by_coords')
    data2 = xr.open_mfdataset(paths=path2,combine='by_coords')
    data3 = xr.concat([data1,data2],dim='time')
    
    return data3

def load_mass(info):
    '''function to load carbon anomaly data and assign mass variable for each cell
    (C mass in kg)
    
    Arguments:
    =========
    info = array of str, containing variable[0], letter[1], scenario[2]'''
    
    #get land area
    areacell = xr.open_dataset('../02-data/ukesm1-output/areacella_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc')
    lndfrac = xr.open_dataset('../02-data/ukesm1-output/sftlf_fx_UKESM1-0-LL_piControl_r1i1p1f2_gn.nc')
    acl = areacell['areacella'].values
    lfr = lndfrac['sftlf'].values
    lp = lfr/100
    lndarea = np.multiply(acl,lp)
    
    #define paths
    path1 = f'../02-data/ukesm1-output/{info[0]}_{info[1]}mon_UKESM1-0-LL_historical_r1i1p1f2_gn_*.nc'
    path2 = f'../02-data/ukesm1-output/{info[0]}_{info[1]}mon_UKESM1-0-LL_{info[2]}_r1i1p1f2_gn_*.nc'
    data1 = xr.open_mfdataset(paths=path1,combine='by_coords')
    data2 = xr.open_mfdataset(paths=path2,combine='by_coords')
    data3 = xr.concat([data1,data2],dim='time')
    
    data4 = data3.assign(mass = data3[info[0]]*lndarea)
    return data4


    
    

