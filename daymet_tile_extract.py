# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 14:49:29 2021

@author: Jason.Roth
@title: Environmental Engineer
@affiliation: USDA-NRCS WNTSC
@email:jason.roth@usda.gov

"""

import os
import sys
import datetime

# code for daymet_timeseries function taken from daymetpy on 03/14/2018
# https://github.com/khufkens/daymetpy

if sys.version_info[0] == 3:
    from urllib.request import urlretrieve
else:
    from urllib import urlretrieve
	

def read_input(infile):

    with open(infile,'r') as f:
        lines = f.readlines()
        
        for l in lines:
            if l.strip()[0] != "#":
                param = l.split(":")[0].strip()
                vals = l.strip().split(":")[1].split(",")
                if param == "period":
                    per = [int(vals[0].strip()), int(vals[1].strip())]
                elif param == "location":
                    loc = [float(vals[0].strip()), float(vals[1].strip())]
    return per, loc
            
            
def daymet_timeseries(lat=36.0133, lon=-84.2625, 
                      start_year=2012, end_year=2014,
                      verbose=False):
    '''Download a Daymet timeseries for a single location as either a local 
    csv or pandas dataframe
    Keyword arguments:
    lat -- geographic latitude of location for timeseries,  must be within 
            Daymet extent
    long -- geographic longitude of location for timeseries,  must be 
            within Daymet extent
    start_yr -- timeseris will begin on January 1st of this year ( >= 1980)
    end_yr -- timeseris will end on December 31st of this year ( < Current year)
    as_dataframe -- if True return a pandas data frame of the timesereis
                    if False return a local path to the CSV downloaded
    download_dname -- The local directory to save the downloaded csv into
                    if none specified saves the file into the temp workspace
                    returned by tempfile.gettempdir()
    https://github.com/khufkens/daymetpy
    '''
    max_year = datetime.datetime.now().year - 1
    MIN_YEAR = 1980  # The begining of the Daymet time series

    if start_year < MIN_YEAR:
        start_year = MIN_YEAR
    if end_year > max_year:
        end_year = max_year

    year_range = ",".join([str(i) for i in range(start_year, end_year+1)])

    # create download string / url
    TIMESERIES_URL = ("https://daymet.ornl.gov/data/send/saveData?lat={lat}&" +
                     "lon={lon}&measuredParams=tmax,tmin,dayl,prcp,srad,swe," +
                     "vp&year={year_range}")
    timeseries_url = TIMESERIES_URL.format(lat=lat, lon=lon,
                                           year_range=year_range)

    if verbose:
        print("Daymet webservice URL:\n{}".format(timeseries_url))

    # create filename for the output file
    daymet_file = "Daymet_{}_{}_{}_{}.csv".format(lat, lon,
                                                  start_year, end_year)

    if verbose:
        print("File downloaded to:\n{}".format(daymet_file))

    # download the daymet data (if available)
    urlretrieve(timeseries_url, daymet_file)

    if os.path.getsize(daymet_file) == 0:
        os.remove(daymet_file)
        raise NameError("You requested data is outside DAYMET coverage," +
                        "the file is empty --> check coordinates!")

    return "operation complete"
	

cwd = os.getcwd()

infile = os.path.join(cwd, "extract_input.txt")
p, l = read_input(infile)

r = daymet_timeseries(lat=l[0], lon=l[1], 
                      start_year=p[0], end_year=p[1],
                      verbose=False)
