#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 17:21:42 2020

@author: Lukas Graf
"""

from demcert.operational import model

# specify DTM (or other gridded dataset) with a single band on which uncertainty shall be determined
# (of course, replace the path and file with your own)
dataset = './example/malldem_5m_esFangar.tif'

# specify the directory where to save the scenarios (same file format and projection as input)
savepath = './example'

# define parameters to run uncertainty model
shift_elements = 5	# number of grid cells to move the kernel over the dataset
kernel_size_x = 9	# size of the kernel in x-direction in grid cells (odd number)
kernel_size_y = 9	# size of the kernel in y-direction in grid cells (odd number)

# call the model class and get a new instance
operator = 'median' # use a median operator for convolution
m = model(dataset, savepath, operator, shift_elements, kernel_size_x, kernel_size_y)

# use the model_uncertainty method to perform the actual uncertainty modelling using
# Gaussian random fields and convolution
# determine properties of the Gaussian random field (see keyword arguments below)
# if minval and maxval are given, the Gaussian distribution will be truncated
# NOTE: depending on the number of scenarios and the size of your raster this might take a while!
m.model_uncertainty(n_realizations=10, mean=0., std=1.,minval=-2.,maxval=2.)

# once this step is done, you can access the resulting scenarios which are available as a list
# of numpy arrays
scenarios = m.scenarios
assert type(scenarios)	== list	# will be 'list'

# you can use the numpy arrays in this list to do some statistical analysis or further workflows
# to automatically analyze the uncertainty

# OR - you save the results as gridded, georeferenced datasets and use them for further analysis
# in any GIS software of your choice
# this is very simple:
m.saveScenarios()