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
from mpl_toolkits.axes_grid1 import make_axes_locatable
import inspect
from matplotlib import rcParams
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import cartopy.mpl.ticker as cticker
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cdo import *
cdo=Cdo()
import copy
import sys,os
mpl.rcParams.update({'font.size': 11})
sys.path.append('/home/cccr/aditi/red_sea_phenology/analysis/common_scripts')
from calc_missval import calc_miss_per
fname = os.path.splitext(os.path.basename(__file__))[0]

MainPath="/home/cccr/aditi/red_sea_phenology/data/chl/"
ifile=MainPath+"CCI_ALL-v6.0-8DAY_1998-2023.nc4"
# ifile=MainPath+"chl_v6.0_8day_1998-2023_0.25deg.nc4"
lonlat = '30,60,10,30'
xaxistick=np.arange(30,60,5)
yaxistick=np.arange(10,30,5)
CHL_orig=cdo.sellonlatbox(f'{lonlat}', input=ifile, returnXArray='chlor_a')
CHL_sum=cdo.sellonlatbox(f'{lonlat}', input="-selmon,6/9 "+ifile, returnXArray='chlor_a')
CHL_win=cdo.sellonlatbox(f'{lonlat}', input="-selmon,12,1,2 "+ifile, returnXArray='chlor_a')
# print(CHL_orig)

Per_data_miss_orig=calc_miss_per(CHL_orig.values)
Per_data_miss_step1=calc_miss_per(CHL_sum.values)
Per_data_miss_final=calc_miss_per(CHL_win.values)

fig = plt.figure(figsize=(30,20))
xaxis_ticks=xaxistick
yaxis_ticks=yaxistick

ax1 = fig.add_subplot(1, 3, 1,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
cmap = plt.get_cmap('jet')
cmap.set_under(color='white')
cmap.set_over(color='black')
CHL1=ax1.pcolormesh(X,Y,Per_data_miss_orig[:,:],cmap=cmap,vmin=0.001,vmax=25,transform=ccrs.PlateCarree())
# CHL1=ax1.contourf(X,Y,Per_data_miss_orig,cmap=plt.cm.jet,levels=np.arange(0.001,30,3),extend='both',transform=ccrs.PlateCarree())
ax1.coastlines()
ax1.add_feature(cf.LAND,zorder=1, edgecolor='k',facecolor=cf.COLORS['land_alt1'])
# plt.colorbar(CHL1,ax=ax1,shrink=0.40,extend='both')
plt.title('Jan-Dec')

ax2 = fig.add_subplot(1, 3, 2,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
cmap = plt.get_cmap('jet')
cmap.set_under(color='white')
cmap.set_over(color='black')
CHL2=ax2.pcolormesh(X,Y,Per_data_miss_step1,cmap=cmap,vmin=0.001,vmax=25,transform=ccrs.PlateCarree())
ax2.coastlines()
ax2.add_feature(cf.LAND,zorder=1, edgecolor='k',facecolor=cf.COLORS['land_alt1'])
# plt.colorbar(CHL2,ax=ax2,shrink=0.40,extend='both')
plt.title('June-Sept')

ax3 = fig.add_subplot(1, 3, 3,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
# cmap = plt.cm.jet
# cmap.set_under(color='white')
# cmap.set_over(color='black')
CHL3=ax3.pcolormesh(X,Y,Per_data_miss_final,cmap=cmap,vmin=0.001,vmax=25,transform=ccrs.PlateCarree())
ax3.coastlines()
ax3.add_feature(cf.LAND,zorder=1, edgecolor='k',facecolor=cf.COLORS['land_alt1'])
plt.title('Dec-Feb')
plt.subplots_adjust(wspace=0.15)
cbar_ax = fig.add_axes([0.18, 0.25, 0.6, 0.025])
fig.colorbar(CHL3, cax=cbar_ax, orientation="horizontal",extend='both',label="Missing satellite weeks (%)")

ax1.set_xticks(xaxis_ticks, crs=ccrs.PlateCarree())
lon_formatter = cticker.LongitudeFormatter()
ax1.xaxis.set_major_formatter(lon_formatter)
ax1.set_yticks(yaxis_ticks, crs=ccrs.PlateCarree())
lat_formatter = cticker.LatitudeFormatter()
ax1.yaxis.set_major_formatter(lat_formatter)

ax2.set_xticks(xaxis_ticks, crs=ccrs.PlateCarree())
ax2.xaxis.set_major_formatter(lon_formatter)
ax2.set_yticks(yaxis_ticks, crs=ccrs.PlateCarree())
ax2.yaxis.set_major_formatter(lat_formatter)

ax3.set_xticks(xaxis_ticks, crs=ccrs.PlateCarree())
ax3.xaxis.set_major_formatter(lon_formatter)
ax3.set_yticks(yaxis_ticks, crs=ccrs.PlateCarree())
ax3.yaxis.set_major_formatter(lat_formatter)

def get_axis_limits(ax, scalex=0.35,scaley=0.73):
    return ax.get_xlim()[1]*scalex, ax.get_ylim()[1]*scaley

# ax1.annotate('a', xy=get_axis_limits(ax1),fontsize=35,weight='bold')
# ax2.annotate('b', xy=get_axis_limits(ax2),fontsize=35,weight='bold')
# ax3.annotate('c', xy=get_axis_limits(ax3),fontsize=35,weight='bold')

plt.savefig(f'../figures/{fname}.png',bbox_inches='tight')