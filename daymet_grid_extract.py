# -*- coding: utf-8 -*-
"""
Created on Thu Jan 15 12:10:20 2015

@author: Jay
"""

# -*- coding: utf-8 -*-

import os
import urllib 

def read_input(infile):
    with open(infile,'r') as f:
        lines = f.readlines()
        for l in lines:
            if l.strip()[0] != "#":
                param = l.split(":")[0].strip()
                vals = l.strip().split(":")[1].split(",")
                if param == "period":
                    yrs = [int(vals[0].strip()), int(vals[1].strip())]
                elif param == "location":
                    loc = [float(v.strip()) for v in vals]
                elif param == "params":
                    par = [v.strip() for v in vals]
    return yrs, loc, par

def getDayMet(out_dir, parameters, years, loc):
    """
    Created on Wed Dec 17 17:01:37 2014
    
    @author: jroth
    
    
    """
    urlpth = "http://thredds.daac.ornl.gov/thredds/ncss/grid/ornldaac/1840/"+\
                "daymet_v4_daily_na_{0}_{1}.nc?var=lat&var=lon&var={0}&"+\
                "north={3}&west={4}&east={5}&south={6}&horizStride=1&"+\
                "time_start={1}-01-01T12:00:00Z&time_end={2}-12-{7}T12:00:00Z&"+\
                "timeStride=1&accept=netcdf" 
                
    file_name = "daymet_v4_daily_$na_${0}_${1}.nc"

    for p in parameters:
        for y in range(years[0], years[1]+1):
            if y%4 == 0:
                d = 30
            else:
                d = 31
                
            r = urlpth.format(p, y, y+1, loc[0], loc[1], loc[2], loc[3], d)

            file_name = "{0}_{1}_{2}N_{3}W_{4}E_{5}S.nc".format(p, y, 
                                                              int(loc[0]), 
                                                              int(loc[1]), 
                                                              int(loc[2]), 
                                                              int(loc[3]))
            out_file = os.path.join(out_dir, file_name)
            try:
                x = os.stat(out_file)
                
            except:
                x = False
                print("downloading " + file_name)
                resp = urllib.request.urlretrieve(r, out_file)
                print("\t"+file_name+" download complete")
            if x :
                print(file_name + " already exists")
                
cwd = os.getcwd()    

infile = os.path.join(cwd, "daymet_download_input.txt")

yrs, loc, par  = read_input(infile)

getDayMet(cwd, par, yrs, loc)








