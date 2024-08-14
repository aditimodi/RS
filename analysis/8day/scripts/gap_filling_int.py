import numpy as np
import xarray as xr
import os
import copy 
import typer
from cdo import Cdo

app = typer.Typer()
cdo = Cdo()
cdoOpts='--reduce_dim -f nc -P 8'

# def fill_clim_mean(data,ntimestepsyr):
#     dimsize=data.shape
#     outData = data.copy()
#     nyears=int(dimsize[0]/ntimestepsyr)
    
#     for j in range(dimsize[1]):
#         for i in range(dimsize[2]): 
#             xm=np.isnan(data[:,j,i]).sum()
#             upplim=0.3*dimsize[0]
#             if xm>=upplim or not np.any(np.isnan(data[:,j,i])):
#                 continue        
#             reshaped_data = data[:,j,i].reshape((nyears, ntimestepsyr))
#             clim_var = np.nanmean(reshaped_data, axis=0)
#             for t in range(nyears):
#                 tstart=t*ntimestepsyr
#                 tend=(t+1)*ntimestepsyr
#                 var=data[tstart:tend,j,i]
#                 nanIdx=np.argwhere(np.isnan(var)).flatten() 
#                 if not np.any(nanIdx):
#                     # print("no nan value in this yr",tstart,tend)
#                     continue      
#                 var[nanIdx] = clim_var[nanIdx]
#                 outData[tstart:tend,j,i] = var
#     return outData

def fill_clim_mean(data,data_clim,ntimestepsyr,nyears):
    dimsize=data.shape
    for j in range(dimsize[1]):
        for i in range(dimsize[2]): 
            xm=np.isnan(data[:,j,i]).sum()
            upplim=int(0.4*dimsize[0])
            if not np.any(np.isnan(data[:,j,i])):
                continue   
            elif xm>=upplim:
                data[:,j,i] = np.nan
                print(data[:,j,i],data[:,j,i].shape)
                continue     
            clim_var = data_clim[:,j,i]
            for t in range(nyears):
                tstart=t*ntimestepsyr
                tend=(t+1)*ntimestepsyr
                var=data[tstart:tend,j,i]
                data[tstart:tend,j,i] = fill_year(var,clim_var)
    return data

def fill_year(var,clim_var):
    nanIdx=np.argwhere(np.isnan(var)).flatten() 
    if not np.any(nanIdx):
        return var
    if nanIdx.size == 1:
        idx=nanIdx[0]
        var[idx] = clim_var[idx]
    else:
        var[nanIdx] = clim_var[nanIdx]

    return var

def fill_11ptavg(data,thresh):
    #data: 3d numpy array
    dimsize=data.shape
    outData = data.copy()
    for j in range(dimsize[1]):
        for i in range(dimsize[2]): 
            xm=np.isnan(data[:,j,i]).sum()
            upplim=thresh*dimsize[0]
            if xm>=upplim or not np.any(np.isnan(data[:,j,i])):
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

def mask_data(data: xr.DataArray, thresh: float) -> xr.DataArray:
    """
    Masks values in a 3D xarray.DataArray where the number of missing values 
    along the 'time' dimension exceeds a specified threshold.
    Parameters:
    - data (xr.DataArray): 3D xarray DataArray with 'time' dimension.
    - thresh (float): Threshold for the proportion of missing values.
    Returns:
    - xr.DataArray: Masked DataArray with values replaced by NaN where the condition is met.
    """
    dimsize = data.sizes['time']
    nan_count = data.isnull().sum(dim='time')
    mask = nan_count > thresh * dimsize
    masked_data = data.where(~mask, np.nan)
    return masked_data

@app.command()       
def main(input:str,output:str):
    chl=cdo.sellonlatbox('30,50,10,30', input=input, \
        returnXArray='chlor_a')   
    chl_clim=cdo.sellonlatbox('30,50,10,30', input="-ydaymean "+input, \
        returnXArray='chlor_a')
    timesteps_in_yr=chl_clim.shape[0]
    tyears = int(chl.shape[0] / timesteps_in_yr)
    print(tyears,timesteps_in_yr)
    thresh=0.4
    maskedChl=mask_data(chl,thresh) 
    filledChl = fill_11ptavg(maskedChl.values,thresh)
    filledChl_2ndIter = fill_11ptavg(filledChl,thresh)
    filledChl_3rdIter = fill_11ptavg(filledChl_2ndIter,thresh)
    # print(type(filledChl_3rdIter))
    gapfilled_data=fill_clim_mean(filledChl_3rdIter,chl_clim.values,timesteps_in_yr,tyears)
    ds = xr.DataArray(gapfilled_data, 
      coords={'time': chl.time, 'lat': chl.lat,'lon': chl.lon}, 
      dims=["time","lat","lon"],
      name="chlor_a")
    print(type(ds))
    masked_ds = ds.where(~np.isnan(ds), np.nan)
    ds.to_netcdf(path=output,mode='w',format="NETCDF4")
    
if __name__ == "__main__":
    app()             

#python gap_filling_int.py '/home/cccr/aditi/red_sea_phenology/data/chl/CCI_ALL-v6.0-8DAY_1998-2023_newtaxis.nc' '../data/chl_gap_filled_int_11pts.nc'

