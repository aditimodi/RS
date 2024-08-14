#!/bin/bash
set -xe

CDO="cdo -O -P 8"

 for year in {1998..2023}
 do
    $CDO -settaxis,${year}-01-01T,00:00:00,8day -setcalendar,365_day -selyear,$year CCI_ALL-v6.0-8DAY_1998-2023.nc4 ${year}_newtaxis.nc
done

cdo -mergetime *newtaxis.nc CCI_ALL-v6.0-8DAY_1998-2023_newtaxis.nc
