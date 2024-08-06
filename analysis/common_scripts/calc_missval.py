import numpy as np

def calc_miss_per(varname):
    """
    Calculate the percentage of missing values (NaNs) for each grid cell.

    Parameters:
    varname (numpy.ndarray): 3D array of shape (time, lat, lon).

    Returns:
    numpy.ndarray: 2D array of shape (lat, lon) with percentage of missing values.
    """
    dimsize = varname.shape
    print(dimsize)
    print(type(varname))

    per_miss=np.zeros(dimsize[1:]) - 999
    X=np.arange(dimsize[0])

    for i in range(dimsize[1]):
        for j in range(dimsize[2]):
            var1=varname[:,i,j]
            xm=np.count_nonzero(np.isnan(var1))

            per_miss[i,j]=(xm/len(X))*100

    return per_miss