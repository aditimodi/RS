import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cf
import matplotlib.pyplot as plt
import matplotlib as mpl
import xarray as xr
import matplotlib.cm as cm
import cartopy.mpl.ticker as cticker
from cdo import *
cdo=Cdo()
import sys,os
mpl.rcParams.update({'font.size': 20})

fname = os.path.splitext(os.path.basename(__file__))[0]

def calc_miss_per(varname):
    dimsize = varname.shape
    per_miss = np.zeros(dimsize[1:]) - 999
    X = np.arange(dimsize[0])
    for i in range(dimsize[1]):
        for j in range(dimsize[2]):
            var1 = varname[:,i,j]
            xm = np.count_nonzero(np.isnan(var1))
            per_miss[i,j] = (xm / len(X)) * 100
    return per_miss

def get_axis_limits(ax, scalex=0.35, scaley=0.73):
    return ax.get_xlim()[1] * scalex, ax.get_ylim()[1] * scaley

def plot_subplot(ax, data, title, annotation, last_plot=False):
    nrows, ncols = data.shape
    lon_values = np.linspace(30,50, ncols)
    lat_values = np.linspace(10, 30, nrows)
    X, Y = np.meshgrid(lon_values, lat_values)
    cmap = plt.get_cmap('jet')
    cmap.set_under(color='white')
    cmap.set_over(color='black')
    p = ax.pcolormesh(X, Y, data, cmap=cmap, vmin=0.001, vmax=25, transform=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cf.LAND, zorder=1, edgecolor='k', facecolor=cf.COLORS['land_alt1'])
    ax.set_title(title)
    ax.set_xticks(np.arange(30, 55, 5), crs=ccrs.PlateCarree())
    ax.xaxis.set_major_formatter(cticker.LongitudeFormatter())
    ax.set_yticks(np.arange(10, 35, 5), crs=ccrs.PlateCarree())
    ax.yaxis.set_major_formatter(cticker.LatitudeFormatter())
    ax.annotate(annotation, xy=get_axis_limits(ax), fontsize=25)
    if last_plot:
        plt.colorbar(p, ax=ax, orientation='horizontal',extend='both', label="Missing satellite weeks (%)",cax=plt.gcf().add_axes([0.18, 0.05, 0.6, 0.025]))

MainPath="/home/cccr/aditi/red_sea_phenology/data/chl/"
ifile=MainPath+"chl_v6.0_8day_1998-2023_0.25deg.nc4"
lonlat = '30,50,10,30'

fig, axes = plt.subplots(3, 4, figsize=(30,20), subplot_kw={'projection': ccrs.PlateCarree()})
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
annotations = ['(a)', '(b)', '(c)', '(d)', '(e)', '(f)', '(g)', '(h)', '(i)', '(j)', '(k)', '(l)']

CHL3 = None
for i, ax_row in enumerate(axes):
    for j, ax in enumerate(ax_row):
        month_idx = i * 4 + j
        month_start = month_idx + 1
        CHL_month = cdo.sellonlatbox(f'{lonlat}', input=f"-selmon,{month_start} {ifile}", returnXArray='chlor_a')
        Per_data_miss_month = calc_miss_per(CHL_month.values)
        if i == 2 and j == 3:  # Last subplot
            CHL3 = Per_data_miss_month  # Store the last subplot data
            plot_subplot(ax, Per_data_miss_month, months[month_idx], annotations[month_idx],last_plot=True)
        else:
            plot_subplot(ax, Per_data_miss_month, months[month_idx], annotations[month_idx])

plt.subplots_adjust(wspace=0.18, hspace=0.2)
plt.savefig(f'../figures/{fname}.png', bbox_inches='tight')
