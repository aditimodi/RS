#!/usr/bin/env python
#coding: utf-8

import numpy as np
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker
import matplotlib.colors as mcolors
import matplotlib.dates as dates
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import matplotlib as mpl
import xarray as xr
from cdo import *
cdo=Cdo()
import copy
import sys,os
mpl.rcParams.update({'font.size': 18})

fname = os.path.splitext(os.path.basename(__file__))[0]

MainPath="/home/cccr/aditi/red_sea_phenology/data/chl/"
ifile=MainPath+"CCI_ALL-v6.0-8DAY_1998-2023.nc4"
CHL_orig=cdo.seltimestep(30, input=ifile, returnXArray='chlor_a')
# print(CHL_orig)
CHL_remapcon=cdo.seltimestep(30, input=MainPath+"chl_v6.0_8day_1998-2023_0.25deg.nc4", returnXArray='chlor_a')
CHL_remapbil=cdo.seltimestep(30, input=MainPath+"chl_v6.0_8day_1998-2023_0.25deg_remapbil.nc4", returnXArray='chlor_a')

fig = plt.figure(figsize=(30,20))

ax1 = fig.add_subplot(1, 3, 1,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
cmap = plt.get_cmap('jet')
CHL1=ax1.pcolormesh(X,Y,CHL_orig[0,:,:],cmap=cmap,vmin=0.001,vmax=1,transform=ccrs.PlateCarree())
ax1.coastlines()
ax1.add_feature(cf.LAND,zorder=1, edgecolor='k',facecolor=cf.COLORS['land_alt1'])
plt.title('orig')

ax2 = fig.add_subplot(1, 3, 2,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_remapcon.lon,CHL_remapcon.lat)
cmap = plt.get_cmap('jet')
CHL2=ax2.pcolormesh(X,Y,CHL_remapcon[0,:,:],cmap=cmap,vmin=0.001,vmax=1,transform=ccrs.PlateCarree())
ax2.coastlines()
ax2.add_feature(cf.LAND,zorder=1, edgecolor='k',facecolor=cf.COLORS['land_alt1'])
plt.title('remapcon')

ax3 = fig.add_subplot(1, 3, 3, projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_remapbil.lon, CHL_remapbil.lat)
CHL3 = ax3.pcolormesh(X, Y, CHL_remapbil[0,:,:], cmap=cmap, vmin=0.001, vmax=1, transform=ccrs.PlateCarree())
ax3.coastlines()
ax3.add_feature(cf.LAND, zorder=1, edgecolor='k', facecolor=cf.COLORS['land_alt1'])
ax3.set_title('remapbil')

plt.subplots_adjust(wspace=0.15)
cbar_ax = fig.add_axes([0.18, 0.2, 0.6, 0.025])
fig.colorbar(CHL3, cax=cbar_ax, orientation="horizontal",extend='max')

plt.savefig(f'{fname}.png')