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
from matplotlib.colors import ListedColormap, BoundaryNorm
import xarray as xr
from cdo import *
cdo=Cdo()
import copy
import sys,os
sys.path.append('/home/cccr/aditi/red_sea_phenology/analysis/common_scripts')
from calc_missval import calc_miss_per
mpl.rcParams.update({'font.size': 18})
import sszpalette
colorsmaps = sszpalette.register()

fname = os.path.splitext(os.path.basename(__file__))[0]
# cmap=plt.get_cmap('sequential9ocker')
# num_colors = cmap.N
# colors = cmap(np.linspace(0, 1, num_colors))
# for i, color in enumerate(colors):
#     hex_color = mcolors.to_hex(color)
#     print(f"Color {i}: RGB={color}, HEX={hex_color}")

MainPath="/home/cccr/aditi/red_sea_phenology/data/chl/"
# ifile=MainPath+"chl_v6.0_8day_1998-2023_0.25deg.nc4"
ifile=MainPath+"CCI_ALL-v6.0-8DAY_1998-2023.nc4"

lonlat='30,50,10,30'
CHL_orig=cdo.sellonlatbox(lonlat, input=ifile, returnXArray='chlor_a')
CHL_step1=cdo.sellonlatbox(lonlat, input="../data/chl_gap_filled_int_11pts.nc", returnXArray='chlor_a')

Per_data_miss_orig=calc_miss_per(CHL_orig.values)
Per_data_miss_step1=calc_miss_per(CHL_step1.values)

fig = plt.figure(figsize=(30,20))

# colormap_percentage = ['#fee391', '#fec44f', '#fe992a', '#ec7015', '#cc4c01','#993404','#672506','deeppink']
colormap_percentage =hex_colors = [
    "deeppink",
    "#df9114",
    "#9d6100",
    "#452b00",
    "#1a1000"
]

cmap = ListedColormap(colormap_percentage)
cmap.set_under(color='white')
boundaries = [0.01, 10, 20, 30,40,90]  # Intervals as specified
norm = BoundaryNorm(boundaries, cmap.N)

ax1 = fig.add_subplot(1, 2, 1,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)

CHL1=ax1.pcolormesh(X,Y,Per_data_miss_orig[:,:],cmap=cmap,norm=norm,transform=ccrs.PlateCarree())
# ax1.coastlines(color=None)
# ax1.add_feature(cf.LAND,zorder=1, edgecolor='#dddddd',facecolor='#dddddd')
gl2 = ax1.gridlines(draw_labels=True)
gl2.top_labels = False
gl2.right_labels = False
plt.title('Step 0: Before gap-filling')

ax2 = fig.add_subplot(1, 2, 2,projection=ccrs.PlateCarree())
X, Y = np.meshgrid(CHL_orig.lon,CHL_orig.lat)
CHL2=ax2.pcolormesh(X,Y,Per_data_miss_step1,cmap=cmap,norm=norm,transform=ccrs.PlateCarree())
# ax2.coastlines(color=None)
# ax2.add_feature(cf.LAND,zorder=1, edgecolor='#dddddd',facecolor='#dddddd')
gl2 = ax2.gridlines(draw_labels=True)
gl2.top_labels = False
gl2.right_labels = False
plt.title('Step I: After gap-filling')
plt.subplots_adjust(wspace=0.15)
cbar_ax = fig.add_axes([0.25, 0.15, 0.35, 0.025])
cb=plt.colorbar(CHL2, cax=cbar_ax, orientation="horizontal",label="Percentage gaps in data (%)",drawedges=True)
cb.set_ticks(boundaries)
cb.outline.set_color('white')
cb.outline.set_linewidth(2)
cb.dividers.set_color('white')
cb.dividers.set_linewidth(4)
plt.savefig(f'../figures/{fname}.png')