#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Import Packages

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np 
import math
import matplotlib.font_manager
import cmocean as cmo
from tqdm import tqdm
import cartopy.crs as ccrs
import dask
import os

os.chdir('/home/milon.miah/Documents/Scripts')
from worldmap import WorldMap
from calc import *
os.chdir('/home/milon.miah/Documents')


# In[4]:


#Split large chunks (from obtained warning)
dask.config.set({"array.slicing.split_large_chunks": True})


# In[7]:


#Load data from vortex directory
vortex_path = '/vortex/clidex/data/NEMO/VIKING20X/hydrography_monthly_upper1000m/'
fname_prefix = '1_VIKING20X.L46-KFS003_1m_'
fname_suffix = '_45W_80W_30N_57N_upper1000m.nc'
ds = xr.open_mfdataset(vortex_path + fname_prefix + '*_vomecrty' + fname_suffix)


# In[8]:


#Load spatial data of defined boxes
ds_masks = xr.open_dataset('/vortex/clidex/data/NEMO/VIKING20X/ecomasks_viking.nc')

#String list of masks 
masks = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Eastern GoM', 'Eastern SS', 'Georges Bank', 'Labrador Shelf1',
         'Labrador Shelf2', 'Labrador Shelf3', 'NFL Shelf', 'Northern GSL', 'Northern MAB', 'Northern NFL Shelf',
         'Southern GSL', 'Southern MAB', 'Western GoM', 'Western SS']

#Convert to float32 array to save memory
for i in range(len(masks)):
    ds_masks[masks[i]] = xr.DataArray(data = np.float32(ds_masks[masks[i]]), dims = ['y', 'x'])


# In[ ]:


#Cut off data for each mask
ds_mev_masks = {}
for i in range(len(masks)):
    ds_mev_masks[masks[i]] = ds['vomecrty'].where(np.isnan(ds_masks[masks[i]]) != True, drop = True)
    ds_mev_masks[masks[i]].name = 'vomecrty'

    ds_mev_masks[masks[i]] = ds_mev_masks[masks[i]].where(ds_mev_masks[masks[i]] != 0)
    #Form merged Dataset
    #if i == 0:
    #    ds_mev_tot = ds_mev_masks[masks[i]]
    #else:
    #    ds_mev_tot = xr.merge([ds_mev_tot, ds_mev_masks[masks[i]]])
    
#Save temperature data of every mask in separate netCDF file for later use
for i in tqdm(range(len(masks))):
    ds_mev_masks[masks[i]].to_netcdf('/mnt/data/MeVelo_Masks/mev_' + masks[i] + '.nc')

