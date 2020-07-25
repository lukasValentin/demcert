#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 17:44:05 2020

@author: lukas
"""

import numpy as np
from demcert.convolution.kernel import kernel


class convolutions(object):
    """
    a class to perform convolution(s) on the random fields to model uncertainty
    of gridded spatial data. If a mask shall be used, masking must be done in
    advance.
    Please note that the convolution is 'valid', i.e., only those array with
    full (spatial) context are used for convolution. Thus, the output is always
    smaller than the input.

    :param inp_raster: array with values (i.e., random field) on which convolution should be carried out
    :param step: number of array elements (x and y direction) to move the kernel on
    :kwargs: key-word arguments to pass to the kernel constructor
    :return: array with output of the convolution with same dimensions as input
    """
    def __init__(self, inp_raster, step, **kwargs):
        """class constructor"""
        self.inp_raster = inp_raster
        self.step = step
        # create a convolution kernel
        self.kernel = kernel(**kwargs)
        self.out_raster = None


    def _get_windows(self):
        """
        method to obtain the single filter kernels (2d array slices).
        Found on Stackoverflow on 25th July 2020:
            https://stackoverflow.com/questions/8174467/vectorized-moving-window-on-2d-array-in-numpy

        :return: 4-d tensor of shape (n_kernels_x, n_kernels_y, kernel_size_x, kernel_size_y)
        """
        s = (self.inp_raster.shape[0] - self.kernel.size_x + 1,) + \
            (self.inp_raster.shape[1] - self.kernel.size_y + 1,) + \
            (self.kernel.size_x, self.kernel.size_y)
        strides = self.inp_raster.strides + self.inp_raster.strides
        strided = np.lib.stride_tricks.as_strided(self.inp_raster,
                                                  shape=s, strides=strides)
        return strided


    def convolve(self):
        """method to carry out the actual convolution on the gridded data"""
        # get the kernel windows
        stridded = self._get_windows()
        # set the output raster dimensions
        self.out_raster = np.empty(shape=(stridded.shape[0],
                                   stridded.shape[1]))
        # iterate over the available kernels and perform the actual convolution
        # using the selected statistical operator
        for ii in range(stridded.shape[0]):
            for jj in range(stridded.shape[1]):
                self.out_raster[ii, jj] = self.kernel.applyConvolution(
                        values=stridded[ii,jj,:,:])
        