import numpy as np
import xarray as xr
import os
import copy 
import typer
from cdo import Cdo

app = typer.Typer()
cdo = Cdo()
cdoOpts='--reduce_dim -f nc -P 8'

def fill_clim_mean(data,data_clim,ntimestepsyr,nyears):
    dimsize=data.shape
    outData = data.copy()
    for j in range(dimsize[1]):
        for i in range(dimsize[2]): 
            if np.all(np.isnan(data[:,j,i])) or not np.any(np.isnan(data[:,j,i])):
                continue   
            if np.any(np.isnan(data_clim[:,j,i])):
                outData[:,j,i] = np.nan
                continue
            for t in range(dimsize[0]):
                if not np.isnan(data[t,j,i]):
                    continue
                ict = t%ntimestepsyr
                outData[t,j,i] = data_clim[ict,j,i]
    return outData

def fill_11ptavg(data):
    #data: 3d numpy array
    dimsize=data.shape
    outData = data.copy()
    for j in range(dimsize[1]):
        for i in range(dimsize[2]): 
            if np.all(np.isnan(data[:,j,i])) or not np.any(np.isnan(data[:,j,i])):
                continue 
            else:
                for t in range(dimsize[0]):
                    var1=data[t,j,i]
                    if not np.isnan(var1):
                        continue 
                    iStart = max(0,i-1)
                    iEnd = min(dimsize[2],i+2)
                    jStart = max(0,j-1)
                    jEnd = min(dimsize[1],j+2)
                    tStart =  max(0,t-1)
                    tEnd = min(dimsize[0],t+2)
                    neighbors = data[t,iStart:iEnd,jStart:jEnd].flatten()
                    neighbors = np.concatenate((neighbors,data[tStart:tEnd,j,i]))
                    if np.isnan(neighbors).all():
                        continue
                    val=np.nanmean(neighbors)
                    if np.isnan(val):
                        continue
                    outData[t,j,i] = round(val,2)
                    # print(outData[t,j,i])
    return outData

def mask_data(data, thresh):
    """
    Masks values in a 3D xarray.DataArray where the number of missing values 
    along the 'time' dimension exceeds a specified threshold.
    Parameters:
    - data (xr.DataArray): 3D xarray DataArray with 'time' dimension.
    - thresh (float): Threshold for the proportion of missing values.
    Returns:
    - xr.DataArray: Masked DataArray with values replaced by NaN where the condition is met.
    """
    dimsize =data.shape[0]
    nan_count = np.count_nonzero(np.isnan(data),0)
    x = nan_count < thresh * dimsize
    masked_data = data.copy() 
    for i in range(dimsize):
        masked_data[i,:,:] = np.where(x, data[i,:,:], np.nan)
    return masked_data

@app.command()       
def main(input:str,output:str):
    lonlat='30,50,10,30'
    chl=cdo.sellonlatbox(lonlat, input=input, returnXArray='chlor_a')   
    chl_clim=cdo.sellonlatbox(lonlat, input="-ydaymean "+input, returnXArray='chlor_a')
    timesteps_in_yr=chl_clim.shape[0]
    tyears = int(chl.shape[0] / timesteps_in_yr)
    print(tyears,timesteps_in_yr)
    maskedChl=mask_data(chl.values,thresh=0.4) 
    filledChl = maskedChl
    for i in range(3):
        print(i, "iter")
        filledChl = fill_11ptavg(filledChl)
    mask_chl_again = mask_data(filledChl,thresh=0.1)
    gapfilled_data=fill_clim_mean(mask_chl_again,chl_clim.values,timesteps_in_yr,tyears)
    print("gapfilled")
    ds = xr.DataArray(gapfilled_data, 
      coords={'time': chl.time, 'lat': chl.lat,'lon': chl.lon}, 
      dims=["time","lat","lon"],
      name="chlor_a")
    print(type(ds))
    ds.to_netcdf(path=output,mode='w',format="NETCDF4")
    
if __name__ == "__main__":
    app()             

#python gap_filling_int.py '/home/cccr/aditi/red_sea_phenology/data/chl/CCI_ALL-v6.0-8DAY_1998-2023_newtaxis.nc' '../data/chl_gap_filled_int_11pts.nc'

