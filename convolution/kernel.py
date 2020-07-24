#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 17:11:07 2020

@author: lukas
"""
import numpy as np


class kernel(object):
    """
    a class defining a convolutional kernel to filter the random field and
    apply the depicted spatial uncertainty model to the original data

    :param size_x: x size of the kernel in array elements
    :param size_y: y size of the kernel in array elements
    :param nodata_value: no data value to set to nan when calculating statistics
    """
    def __init__(self, size_x, size_y, nodata_value):
        """class constructor"""
        self.size_x = size_x
        self.size_y = size_y
        self.nodata_value = nodata_value
        self.values = np.zeros(shape=(self.size_x, self.size_y))
        self.conv_val = np.nan


    def set_values(self, values):
        """
        populate the kernel with values to be passed to the convolution operator.
        No-data values are replaced with np.nan

        :param values: array with same x and y dimensions as the kernel
        """
        # filter nodata values and set them to nan
        values[values==self.nodata_value] = np.nan
        self.values = values


    def applyConvolution(self, operator='mean'):
        """
        once the values are loaded, the convolution is performed using a user-
        selected operator. The default is 'mean' but also 'median' and 'min' as
        well as 'max' or 'majority' are possible

        :param operator: convolution operation to be performed. Default: mean.
            Other possible values include:
                - median
                - min
                - max
                - majority
        """
        if operator == 'mean':
            self.conv_val = np.nanmean(self.values)
        elif operator == 'median':
            self.conv_val = np.nanmedian(self.values)
        elif operator == 'min':
            self.conv_val = np.nanmin(self.values)
        elif operator == 'max':
            self.conv_val = np.nanmax(self.values)
        elif operator == 'majority':
            (vals, counts) = np.unique(self.values,return_counts=True)
            most_frequent = np.argmax(counts)
            self.conv_val = vals[most_frequent]
        else:
            raise ValueError('The specified operator does not exist!')
