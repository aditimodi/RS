#!/usr/bin/env python
#coding: utf-8

import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import xarray as xr
from cdo import *
import matplotlib as mpl
import sys
cdo=Cdo()
plt.style.use('/home/cccr/aditi/AM_DataViz/style_sheets/styleSheetDoublecolumn.mplstyle')

MainPath="/home/cccr/aditi/red_sea_phenology/data/chl/"
ifile=MainPath+"CCI_ALL-v6.0-8DAY_1998-2023.nc4"
lonlat='30,50,10,30'
CHL_orig=cdo.timmean(input=f'-sellonlatbox,{lonlat} {ifile}', returnXArray='chlor_a')
print(CHL_orig)

ifile2="../data/chl_gap_filled_int_11pts.nc"
CHL_step1=cdo.timmean(input=f'-sellonlatbox,{lonlat} {ifile2}', returnXArray='chlor_a')
print(CHL_step1)

fig = plt.figure()
levels=np.arange(0,1,0.05)

ax1 = fig.add_subplot(1, 2, 1,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
cmap = plt.get_cmap('viridis')
CHL1=ax1.contourf(X,Y,CHL_orig[0,:,:],cmap=cmap,levels=levels,extend='max',transform=ccrs.PlateCarree())
# ax1.coastlines(color=None)
# ax1.add_feature(cf.LAND,zorder=1, edgecolor='grey',facecolor=cf.COLORS['land_alt1'])
ax1.text(0.02, 0.95, '(a)', transform=ax1.transAxes, fontsize=14, 
         fontweight='bold', va='top', ha='left')
# gl1 = ax1.gridlines(draw_labels=True)
# gl1.top_labels = False
# gl1.right_labels = False
plt.title('mean chl-a: before gap-filling')

ax2 = fig.add_subplot(1, 2, 2,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
cmap = plt.get_cmap('viridis')
CHL2=ax2.contourf(X,Y,CHL_step1[0,:,:],cmap=cmap,levels=levels,extend='max',transform=ccrs.PlateCarree())
# ax2.coastlines(color=None)
# ax2.add_feature(cf.LAND,zorder=1, edgecolor='grey',facecolor=cf.COLORS['land_alt1'])
ax2.text(0.02, 0.95, '(b)', transform=ax2.transAxes, fontsize=14,
         fontweight='bold', va='top', ha='left')
# gl2 = ax2.gridlines(draw_labels=True)
# gl2.top_labels = False
# gl2.right_labels = False
plt.title('mean chl-a: after gap-filling')

plt.subplots_adjust(wspace=0.2)

cbar_ax = fig.add_axes([0.18, 0.2, 0.6, 0.025])
fig.colorbar(CHL2, cax=cbar_ax, orientation="horizontal",label="chlorophyll conc. (mg/m$^3$)")

plt.savefig('../figures/chl_clim_after_int.png')