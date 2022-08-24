#!/usr/bin/env python
# coding: utf-8

# # Velocity Vector Field on Surface

# In[33]:


#Import Packages

import xarray as xr
import matplotlib.pyplot as plt
import numpy as np 
import math
import matplotlib.font_manager
import cmocean as cmo
from tqdm import tqdm
import cartopy.crs as ccrs
import os
from matplotlib import colors
from matplotlib.animation import FuncAnimation 
import cartopy.crs as ccrs
import cartopy.feature as cfeature


#Ignore warnings for now
import warnings
warnings.filterwarnings('ignore')

os.chdir('/home/milon.miah/Documents/Scripts')
from worldmap import WorldMap
from calc import *
from util import *
os.chdir('/home/milon.miah/Documents')

#Plot parameters
plt.rcParams['font.size'] = 20.0


# In[20]:


#Load data from vortex directory - Meridonal velocity
vortex_path = '/vortex/clidex/data/NEMO/VIKING20X/hydrography_monthly_upper1000m/'
fname_prefix = '1_VIKING20X.L46-KFS003_1m_'
fname_suffix = '_45W_80W_30N_57N_upper1000m.nc'
ds_mev = xr.open_mfdataset(vortex_path + fname_prefix + '*_vomecrty' + fname_suffix)

#Load data from vortex directory - Zonal velocity
vortex_path = '/vortex/clidex/data/NEMO/VIKING20X/hydrography_monthly_upper1000m/'
fname_prefix = '1_VIKING20X.L46-KFS003_1m_'
fname_suffix = '_45W_80W_30N_57N_upper1000m.nc'
ds_zov = xr.open_mfdataset(vortex_path + fname_prefix + '*_vozocrtx' + fname_suffix)

#Load data from vortex directory - Temperature
vortex_path = '/vortex/clidex/data/NEMO/VIKING20X/hydrography_monthly_upper1000m/'
fname_prefix = '1_VIKING20X.L46-KFS003_1m_'
fname_suffix = '_45W_80W_30N_57N_upper1000m.nc'
ds_temp = xr.open_mfdataset(vortex_path + fname_prefix + '*_votemper' + fname_suffix)

#Load data from vortex directory - Salinity
vortex_path = '/vortex/clidex/data/NEMO/VIKING20X/hydrography_monthly_upper1000m/'
fname_prefix = '1_VIKING20X.L46-KFS003_1m_'
fname_suffix = '_45W_80W_30N_57N_upper1000m.nc'
ds_sal = xr.open_mfdataset(vortex_path + fname_prefix + '*_vosaline' + fname_suffix)

#Load data from vortex directory - SSH
vortex_path = '/vortex/clidex/data/NEMO/VIKING20X/SSH/'
fname_prefix = '1_VIKING20X.L46-KFS003_1d_'
fname_suffix = '_45W_80W_30N_57N.nc'
ds_ssh = xr.open_mfdataset(vortex_path + fname_prefix + '*_zeromean' + fname_suffix)


# In[21]:


# Only look at surface 
ds_mev = ds_mev.sel(depthv = ds_mev['vomecrty'][:,0].depthv.to_numpy())
ds_zov = ds_zov.sel(depthu = ds_zov['vozocrtx'][:,0].depthu.to_numpy())
ds_temp = ds_temp.sel(deptht = ds_temp['votemper'][:,0].deptht.to_numpy())
ds_sal = ds_sal.sel(deptht = ds_sal['vosaline'][:,0].deptht.to_numpy())

ds_ssh = list(ds_ssh.groupby('time_counter.day'))[15][1]

# Cut off land
ds_zov = ds_zov.where(ds_zov != 0.0)
ds_mev = ds_mev.where(ds_mev != 0.0)
ds_temp = ds_temp.where(ds_temp != 0.0)
ds_sal = ds_sal.where(ds_sal != 0.0)
ds_ssh = ds_ssh.where(ds_ssh != 0.0)


# In[4]:


#Create Animation for surface velocity and salinity field

#Creating the map object
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

#Adding features to the map
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
#ax.stock_img()
ax.set_extent([-85, -40, 30, 57])
ax.gridlines(draw_labels = True)

#Define observation period
time_begin = '16-01-1958'
time_end = '16-12-2019'

ds_zov_foc = ds_zov.sel(time_counter = slice(time_begin, time_end))
ds_mev_foc = ds_mev.sel(time_counter = slice(time_begin, time_end))
ds_sal_foc = ds_sal.sel(time_counter = slice(time_begin, time_end))

#Decrease arrow resolution
skip = 10
to_skip = (slice(None, None, skip), slice(None, None, skip))
nav_lon = ds_zov_foc.nav_lon[to_skip]
nav_lat = ds_zov_foc.nav_lat[to_skip]
nav_lon_sal = ds_sal_foc.nav_lon[to_skip]
nav_lat_sal = ds_sal_foc.nav_lat[to_skip]
zov = ds_zov_foc['vozocrtx'][0][to_skip]
mev = ds_mev_foc['vomecrty'][0][to_skip]
sal = ds_sal_foc['vosaline'][0][to_skip]

#Add colormesh of salerature plot
vmin = 0
vmax = 30
cmesh = ax.pcolormesh(nav_lon_sal, nav_lat_sal, sal, 
                      transform = ccrs.PlateCarree(), vmin = 30, vmax = 37)
cbar = fig.colorbar(cmesh, ax = ax, cmap = 'cmo.haline', location = 'right', label = 'Salinity in g/kg', pad = 0.1)

#Start plotting vector field for time begin
quiv = ax.quiver(nav_lon, nav_lat, zov, mev)

def animate(i):
    
    plt.title(np.datetime_as_string(ds_zov_foc['time_counter'][i].to_numpy(), unit = 'M'))
    cmesh.set_array(ds_sal_foc['vosaline'][i][to_skip])
    quiv.set_UVC(ds_zov_foc['vozocrtx'][i][to_skip], ds_mev_foc['vomecrty'][i][to_skip])
    ax.coastlines()

    
# # # anim = FuncAnimation(fig_sctt2, animate, init_func = init, frames = 200, interval = 20, blit = True)
anim = FuncAnimation(fig, animate, frames = len(ds_zov_foc.time_counter.to_numpy()), interval = 5, blit = False)
anim.save('/home/milon.miah/Documents/Plots/surface_sal_vel.gif', writer='imagemagick', fps=5)


# In[ ]:


#Create Animation for surface velocity and ssh field

#Creating the map object
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

#Adding features to the map
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
#ax.stock_img()
ax.set_extent([-85, -40, 30, 57])
ax.gridlines(draw_labels = True)

#Define observation period
time_begin = '16-01-1958'
time_end = '16-12-2019'

ds_zov_foc = ds_zov.sel(time_counter = slice(time_begin, time_end))
ds_mev_foc = ds_mev.sel(time_counter = slice(time_begin, time_end))
ds_ssh_foc = ds_ssh.sel(time_counter = slice(time_begin, time_end))

#Decrease arrow resolution
skip = 10
to_skip = (slice(None, None, skip), slice(None, None, skip))
nav_lon = ds_zov_foc.nav_lon[to_skip]
nav_lat = ds_zov_foc.nav_lat[to_skip]
nav_lon_ssh = ds_ssh_foc.nav_lon[0][to_skip]
nav_lat_ssh = ds_ssh_foc.nav_lat[0][to_skip]
zov = ds_zov_foc['vozocrtx'][0][to_skip]
mev = ds_mev_foc['vomecrty'][0][to_skip]
ssh = ds_ssh_foc['sossheig'][0][to_skip]

#Add colormesh of ssherature plot
vmin = 0
vmax = 30
cmesh = ax.pcolormesh(nav_lon_ssh, nav_lat_ssh, ssh, 
                      transform = ccrs.PlateCarree(), cmap = 'cmo.balance', norm = colors.CenteredNorm())
cbar = fig.colorbar(cmesh, ax = ax, location = 'right', label = 'Sea Surface Height (Zero mean) in m', pad = 0.1)

#Start plotting vector field for time begin
quiv = ax.quiver(nav_lon, nav_lat, zov, mev)

def animate(i):
    
    plt.title(np.datetime_as_string(ds_zov_foc['time_counter'][i].to_numpy(), unit = 'M'))
    cmesh.set_array(ds_ssh_foc['sossheig'][i][to_skip])
    quiv.set_UVC(ds_zov_foc['vozocrtx'][i][to_skip], ds_mev_foc['vomecrty'][i][to_skip])
    ax.coastlines()

    
# # # anim = FuncAnimation(fig_sctt2, animate, init_func = init, frames = 200, interval = 20, blit = True)
anim = FuncAnimation(fig, animate, frames = len(ds_zov_foc.time_counter.to_numpy()), interval = 5, blit = False)
anim.save('/home/milon.miah/Documents/Plots/surface_ssh_vel.gif', writer='imagemagick', fps=5)

