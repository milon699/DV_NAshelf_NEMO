#!/usr/bin/env python
# coding: utf-8

# # Quick Programm zu summarize stored data into one xarray.Dataset per Mask

# In[22]:


import xarray as xr
from tqdm import tqdm


# In[3]:


#String list of masks 
masks = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Southern MAB', 'Northern MAB',
         'Georges Bank', 'Western GoM', 'Eastern GoM', 'Western SS', 
         'Eastern SS', 'Southern GSL', 'Northern GSL', 
         'NFL Shelf', 'Northern NFL Shelf', 'Labrador Shelf1', 'Labrador Shelf2']


# In[28]:


#Read temperature and salinity masks data from created files
ds_temp_masks = {}
ds_sal_masks = {}
ds_mev_masks = {}
ds_zov_masks = {}

ds = {}

for i in tqdm(range(len(masks))):
    
    ds_temp_masks[masks[i]] = xr.open_dataset('/mnt/data/Temp_Masks/temp_' + masks[i] + '.nc')
    ds_sal_masks[masks[i]] = xr.open_dataset('/mnt/data/Sal_Masks/sal_' + masks[i] + '.nc')
    ds_mev_masks[masks[i]] = xr.open_dataset('/mnt/data/MeVelo_Masks/mev_' + masks[i] + '.nc')
    ds_zov_masks[masks[i]] = xr.open_dataset('/mnt/data/ZoVelo_Masks/zov_' + masks[i] + '.nc')    
    ds[masks[i]] = xr.Dataset(data_vars = dict(votemper = (['time_counter', 'deptht', 'y', 'x'], ds_temp_masks[masks[i]].votemper.data),
                                              vosaline = (['time_counter', 'deptht', 'y', 'x'], ds_sal_masks[masks[i]].vosaline.data),
                                              vomecrty = (['time_counter', 'deptht', 'y', 'x'], ds_mev_masks[masks[i]].vomecrty.data),
                                              vozocrtx = (['time_counter', 'deptht', 'y', 'x'], ds_zov_masks[masks[i]].vozocrtx.data)),
                             coords = ds_temp_masks[masks[i]].coords)
    
    ds[masks[i]].to_netcdf('/mnt/data/Masks/NEMO_VIKING20X_mask_' + masks[i] + '.nc')

