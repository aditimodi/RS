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
sys.path.append('/home/cccr/aditi/red_sea_phenology/analysis/common_scripts')
from calc_missval import calc_miss_per
mpl.rcParams.update({'font.size': 18})

fname = os.path.splitext(os.path.basename(__file__))[0]

MainPath="/home/cccr/aditi/red_sea_phenology/data/chl/"
ifile=MainPath+"chl_v6.0_8day_1998-2023_0.25deg.nc4"
CHL_orig=cdo.sellonlatbox(30,50,10,30, input=ifile, returnXArray='chlor_a')
print(type(CHL_orig))

CHL_step1=xr.open_dataset("../data/chl_gap_filled_int_11pts.nc",decode_cf=True)['chlor_a']
print(type(CHL_step1))

Per_data_miss_orig=calc_miss_per(CHL_orig.values)
Per_data_miss_step1=calc_miss_per(CHL_step1.values)

fig = plt.figure(figsize=(30,20))

ax1 = fig.add_subplot(1, 2, 1,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
cmap = plt.get_cmap('jet')
cmap.set_under(color='white')
cmap.set_over(color='black')
CHL1=ax1.pcolormesh(X,Y,Per_data_miss_orig[:,:],cmap=cmap,vmin=0.001,vmax=20,transform=ccrs.PlateCarree())
ax1.coastlines()
ax1.add_feature(cf.LAND,zorder=1, edgecolor='k',facecolor=cf.COLORS['land_alt1'])
plt.title('Step 0: Before gap-filling')

ax2 = fig.add_subplot(1, 2, 2,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
cmap = plt.get_cmap('jet')
cmap.set_under(color='white')
cmap.set_over(color='black')
CHL2=ax2.pcolormesh(X,Y,Per_data_miss_step1,cmap=cmap,vmin=0.001,vmax=20,transform=ccrs.PlateCarree())
ax2.coastlines()
ax2.add_feature(cf.LAND,zorder=1, edgecolor='k',facecolor=cf.COLORS['land_alt1'])
plt.title('Step I: After gap-filling')
plt.subplots_adjust(wspace=0.15)
cbar_ax = fig.add_axes([0.18, 0.2, 0.6, 0.025])
fig.colorbar(CHL2, cax=cbar_ax, orientation="horizontal",extend='both',label="Percentage gaps in data (%)")

plt.savefig(f'../figures/{fname}.png')