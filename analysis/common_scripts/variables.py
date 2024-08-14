import calendar
import os
import sys

from pathlib import Path

import cartopy.mpl.ticker as cticker
from netCDF4 import Dataset, num2date, date2num
import numpy as np
import xarray as xr
import matplotlib
matplotlib.use('AGG')# or PDF, SVG or PS
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.colors import ListedColormap
import matplotlib.ticker as tick
from matplotlib import colors
import matplotlib.colors as mcolors
import cartopy.crs as ccrs
import cartopy.feature as cf
import iris
import iris.plot as iplt
from cdo import Cdo
import cftime
from datetime import datetime
import matplotlib as mpl
from matplotlib.colors import BoundaryNorm
import seaborn as sns
import colorcet as cc

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial','DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']
})
a4size = (8.27,11.69)
cdo = Cdo()
cdoOpts='--reduce_dim -f nc -P 8'

region={
  'Western Arabian Sea':'56,59,17,22',
  'Somalia': '52,56,7,14',
  'Central Arabian Sea': '61,67,8,12',
  'South Tropical Indian Ocean': '52,90,-19,-8',
  'Sri Lankan Dome':'74,78,8,14',
  'Central Bay of Bengal': '87,90,9,12',
  'South Bay of Bengal': '84,89,4,8',
  'North Equatorial Indian Ocean': '63,74,1,6',
  'North Arabian Sea':'62,66,17,23',
  'Equatorial Indian Ocean': '65,90,-5,0',
  'Western Bay of Bengal': '81,86,10,14',
  'Eastern Equatorial Indian Ocean': '93,98,-1,4',
}


week_boundaries = {
    0: ["01 Jan - 08 Jan"],
    1: ["09 Jan - 16 Jan"],
    2: ["17 Jan - 24 Jan"],
    3: ["25 Jan - 01 Feb"],
    4: ["02 Feb - 09 Feb"],
    5: ["10 Feb - 17 Feb"],
    6: ["18 Feb - 25 Feb"],
    7: ["26 Feb - 05 Mar"],
    8: ["06 Mar - 13 Mar"],
    9: ["14 Mar - 21 Mar"],
    10: ["22 Mar - 29 Mar"],
    11: ["30 Mar - 06 Apr"],
    12: ["07 Apr - 14 Apr"],
    13: ["15 Apr - 22 Apr"],
    14: ["23 Apr - 30 Apr"],
    15: ["01 May - 08 May"],
    16: ["09 May - 16 May"],
    17: ["17 May - 24 May"],
    18: ["25 May - 01 Jun"],
    19: ["02 Jun - 09 Jun"],
    20: ["10 Jun - 17 Jun"],
    21: ["18 Jun - 25 Jun"],
    22: ["26 Jun - 03 Jul"],
    23: ["04 Jul - 11 Jul"],
    24: ["12 Jul - 19 Jul"],
    25: ["20 Jul - 27 Jul"],
    26: ["28 Jul - 04 Aug"],
    27: ["05 Aug - 12 Aug"],
    28: ["13 Aug - 20 Aug"],
    29: ["21 Aug - 28 Aug"],
    30: ["29 Aug - 05 Sep"],
    31: ["06 Sep - 13 Sep"],
    32: ["14 Sep - 21 Sep"],
    33: ["22 Sep - 29 Sep"],
    34: ["30 Sep - 07 Oct"],
    35: ["08 Oct - 15 Oct"],
    36: ["16 Oct - 23 Oct"],
    37: ["24 Oct - 31 Oct"],
    38: ["01 Nov - 08 Nov"],
    39: ["09 Nov - 16 Nov"],
    40: ["17 Nov - 24 Nov"],
    41: ["25 Nov - 02 Dec"],
    42: ["03 Dec - 10 Dec"],
    43: ["11 Dec - 18 Dec"],
    44: ["19 Dec - 26 Dec"],
    45: ["27 Dec - 03 Jan"]
}
