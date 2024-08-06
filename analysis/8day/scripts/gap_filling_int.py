import numpy as np
import xarray as xr
import os
import copy 
import typer
from cdo import Cdo

app = typer.Typer()
cdo = Cdo()
cdoOpts='--reduce_dim -f nc -P 8'

def fill_11ptavg(data):
    #data: 3d numpy array
    dimsize=data.shape
    
    outData = data.copy()

    for j in range(dimsize[1]):
        for i in range(dimsize[2]): 
            
            xm=np.isnan(data[:,j,i]).sum()
            upplim=0.7*dimsize[0]
            if xm>=upplim: 
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

                    outData[t,j,i] = round(val,3)
                    # print(outData[t,j,i])
 
    return outData

@app.command()       
def main(input,output):
    
    chl=cdo.sellonlatbox('30,50,10,30', input=input, \
        returnXArray='chlor_a')
    
    filledChl = fill_11ptavg(chl.values)
    filledChl_2ndIter = fill_11ptavg(filledChl)
    filledChl_3ndIter = fill_11ptavg(filledChl_2ndIter)
    print(type(filledChl_3ndIter))
    
    ds = xr.DataArray(filledChl_3ndIter, 
      coords={'time': chl.time, 'lat': chl.lat,'lon': chl.lon}, 
      dims=["time","lat","lon"],
      name="chlor_a")
    print(type(ds))
    ds.to_netcdf(path=output,mode='w',format="NETCDF4")
    
if __name__ == "__main__":
    app()             

#python gap_filling_int.py '/home/cccr/aditi/red_sea_phenology/data/chl/chl_v6.0_8day_1998-2023_0.25deg.nc4' '../data/chl_gap_filled_int_11pts.nc'

