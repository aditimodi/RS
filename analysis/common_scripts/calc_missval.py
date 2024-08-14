import numpy as np
import xarray as xr
def calc_miss_per(varname):
    """
    Calculate the percentage of missing values (NaNs) for each grid cell.
    Parameters:
    varname (xarray) 3D array of shape (time, lat, lon).
    Returns:
    numpy.ndarray: 2D array of shape (lat, lon) with percentage of missing values.
    """
    dimsize = varname.shape
    print(dimsize)
    print(type(varname))
    per_miss=np.zeros(dimsize[1:]) - np.nan
    X = dimsize[0]
    print(X)
    for i in range(dimsize[1]):
        for j in range(dimsize[2]):
            var1=varname[:,i,j]
            if np.all(np.isnan(var1)):
                continue
            xm=np.count_nonzero(np.isnan(var1))
            per_miss[i,j]=(xm/X)*100
    return per_miss

# def calc_miss_per(varname):
#     dimsize = varname.shape
#     X = dimsize[0]
#     nan_count = varname.isnull().sum(dim='time')
#     all_nan = varname.isnull().all(dim='time')
#     per_miss = xr.full_like(nan_count, np.nan)
#     per_miss = xr.where(~all_nan, (nan_count / X) * 100, per_miss)
#     return per_miss.values.astype(float)
