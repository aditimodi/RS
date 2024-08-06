#!/bin/bash
set -xe

NCKS="ncks -3 -F -O -t 16"
NCRCAT="ncrcat -F -O -t 16"
NCRA="ncra -F -O"
CDO="cdo -O -P 8"

dPath="/home/cccr/aditi/red_sea_phenology/data/chl"

# $CDO -selyear,1998/2023 $dPath/CCI_ALL-v6.0-8DAY.nc4 $dPath/CCI_ALL-v6.0-8DAY_1998-2023.nc4
# $CDO -selyear,1998/2023 $dPath/CCI_ALL-v6.0-5DAY.nc4 $dPath/CCI_ALL-v6.0-5DAY_1998-2023.nc4

# # Perform conservative remapping
$CDO -remapcon,gridspec.txt $dPath/CCI_ALL-v6.0-8DAY_1998-2023.nc4 $dPath/chl_v6.0_8day_1998-2023_0.25deg.nc4
$CDO -remapcon,gridspec.txt $dPath/CCI_ALL-v6.0-5DAY_1998-2023.nc4 $dPath/chl_v6.0_5day_1998-2023_0.25deg.nc4
