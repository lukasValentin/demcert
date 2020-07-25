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
    :param operator: convolution operation to be performed. Default: mean.
            Other possible values include:
                - median
                - min
                - max
                - majority
    """
    def __init__(self, size_x, size_y, nodata_value, operator='mean'):
        """class constructor"""
        self.size_x = size_x
        self.size_y = size_y
        self.nodata_value = nodata_value
        self.operator = operator


    def setOperator(self, operator):
        """
        set a different statistical operator to the kernel
        :param operator: convolution operation to be performed. Default: mean.
            Other possible values include:
                - median
                - min
                - max
                - majority
        """
        self.operator = operator


    def applyConvolution(self, values):
        """
        once the values are loaded, the convolution is performed using a user-
        selected operator. The default is 'mean' but also 'median' and 'min' as
        well as 'max' or 'majority' are possible

        :param values: values to be passed to the convolution operator
        :return: result of the statistical operator
        """
        conv_val = np.nan
        # apply the selected statistical operator to the data in the kernel
        if self.operator == 'mean':
            conv_val = np.nanmean(values)
        elif self.operator == 'median':
            conv_val = np.nanmedian(values)
        elif self.operator == 'min':
            conv_val = np.nanmin(values)
        elif self.operator == 'max':
            conv_val = np.nanmax(values)
        elif self.operator == 'majority':
            (vals, counts) = np.unique(values,return_counts=True)
            most_frequent = np.argmax(counts)
            conv_val = vals[most_frequent]
        else:
            raise ValueError('The specified operator does not exist!')
        return conv_val
