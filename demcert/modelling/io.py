#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 10:02:02 2020

@author: lukas
"""

import os
import rasterio


def readRaster(rasterFile, bandNum=1):
    """
    reads gridded data from a raster file for a specific band and returns the
    data as numpy array alongside with the georeference information.

    :param rasterFile: file-path to the gridded dataset to be read
    :param bandNum: number of the band to read; Default: 1
    :return: a dict containing the data and the actual dataset (for georeferencation, etc.)
    """
    # check inputs
    assert os.path.isfile(rasterFile)
    assert bandNum >= 1

    # open the dataset
    ds = rasterio.open(rasterFile)
    data = {}
    data['ds'] = ds
    # read the specified band
    data['data'] = ds.read(bandNum)

    return data


def writeRaster(src, fname, array):
    """
    writes a numpy array as georeferenced gridded dataset using a source dataset
    for providing the georeference information

    :param src: dict returned from readRaster function with the spatial info
    :param fname: file-path of the output dataset to be created
    :param array: numpy array with data to be written to a new gridded dataset
    """
    # use Env(ironment) to handle all the georeferencation stuff
    with rasterio.Env():

        # use the same profile specifications as for the input dataset
        profile = src['ds'].profile
    
        with rasterio.open(fname, 'w', **profile) as dst:
            dst.write(array.astype(rasterio.float32), 1)
