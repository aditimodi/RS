#!/bin/bash

infile="../data/chl_gap_filled_int_11pts.nc"
outfile="../data/chl_gap_filled_1998-2023_8day.nc"

cdo -O -P 8 -masklonlatbox,36,38,11,12.5 $infile out.nc
cdo -O -P 8 -masklonlatbox,31,34,22,24 out.nc $outfile