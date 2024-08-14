import numpy as np
import pandas as pd
import xarray as xr

data = np.array([1, 2, np.nan, 4, 5])
coords = {'time': range(5)}
ds = xr.DataArray(data, coords=coords, dims=['time'])

# Mask NaN values using xarray's .where() method
masked_ds = ds.where(~np.isnan(ds), np.nan)


mean_value = np.mean(masked_ds)
print("Mean value:", mean_value)

print("Masked DataArray:")
print(masked_ds)

print("\nOriginal DataArray:")
print(ds)






# # Example data and mask
# data = [1.2, 2.3, 3.4, 4.5, 5.6]
# coords = {
#     'time': pd.date_range('2024-01-01', periods=5)
# }

# # Create DataArray
# da = xr.DataArray(data, coords=coords, dims=['time'], name='example_data')
# # print(da)

# # Create a masked array
# # masked_array = np.ma.masked_where(mask, data)

# masked_array=da.where(da>4,np.nan)

# print(masked_array.values)

# mean_value = np.mean(masked_array)
# print("Mean value:", mean_value)
