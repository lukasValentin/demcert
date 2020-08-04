#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 10:22:09 2020

@author: lukas
"""

import os
import logging
import numpy as np
from demcert.modelling.io import readRaster, writeRaster
from demcert.convolution.convolutions import convolutions
from demcert.random_fields.gen_random_field import random_field


class model(object):
    """
    base class to apply uncertainty models using Gaussian random fields and
    statistical convolutional filters to gridded data. A set of scenarios based
    on different realization of Gaussian random fields is generated (Monte-
    Carlo approach) and used to model uncertainty ranges of the gridded data.

    :param dataset: file-path to the gridded dataset for which uncertainty shall be determined
    :param savepath: directory where to save the scenarios
    :param operator: operator to be used for convolution
    :param shift_elements: number of elements to shift the kernel in x and y direction
    :param kernel_size_x: size of the kernel in grid cells in x direction
    :param kernel_size_y: size of the kernel in grid cells in y direction
    """

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

    def __init__(self, dataset, savepath, operator, shift_elements,
                 kernel_size_x, kernel_size_y):
        """class constructor"""
        # define class-specific variables and check inputs
        assert os.path.isfile(dataset)
        self.dataset = dataset

        assert os.path.isdir(savepath)
        self.savepath = savepath

        self.operator = operator
        self.shift_elements = shift_elements
        self.kernel_size_x = kernel_size_x
        self.kernel_size_y = kernel_size_y

        # read the gridded data into memory
        self.orig_data = readRaster(self.dataset)
        logging.info('Read dataset {} into memory'.format(dataset))

        # get row and column number to call the random field class
        self.rows, self.cols = self.orig_data['data'].shape
        logging.info('Dataset rows = {0} | cols = {1}'.format(self.rows,
                     self.cols))
        # get the nodata value of the raster
        self.nodata_value = self.orig_data['ds'].nodatavals[0]


    def model_uncertainty(self, n_realizations, **kwargs):
        """
        apply the actual uncertainty model to the original gridded dataset

        :param n_realizations: number of realizations (scenarios) to generate
        :kwargs: key args to pass to the random field generator
        """
        assert n_realizations > 0

        # create a random field object
        rand_field = random_field(rows=self.rows, cols=self.cols)
        # determine how many random fields to be generated
        if n_realizations == 1:
            self.rand_fields = rand_field.gaussian(n_realizations=n_realizations,
                                                   **kwargs)
        else:
            self.rand_fields = rand_field.multiple_gaussian(n_realizations=n_realizations,
                                                            **kwargs)
    
        logging.info('Created {} random Gaussian fields - start convolution'.format(
                len(self.rand_fields)))
        
        # determine offset since the convolution is not defined at the
        # raster border
        offset_x = int(np.floor(self.kernel_size_x / 2)) - 1 # -1 because array indices start at 0
        offset_y = int(np.floor(self.kernel_size_y / 2)) - 1 # -1 because array indices start at 0

        # iterate over the random fields (i.e., single scenarios) and perform
        # the convolution; save the outputs to a new list
        self.scenarios = []
        counter = 1
        for rfield in self.rand_fields:
            # create a convolution operator
            convolution_op = convolutions(inp_raster=rfield,
                                          step=self.shift_elements,
                                          size_x=self.kernel_size_x,
                                          size_y=self.kernel_size_y,
                                          nodata_value=self.nodata_value,
                                          operator=self.operator)
            # perform the convolution
            logging.info('Perform convolution on random field {}/{}'.format(
                    counter, len(self.rand_fields)))
            counter += 1
            convolution_op.convolve()
            # add the convolution result to the original dataset and save the
            # output
            scenario = self.orig_data['data'][offset_x:offset_x+convolution_op.out_raster.shape[0],
                                      offset_y:offset_y+convolution_op.out_raster.shape[1]] + \
                        convolution_op.out_raster                                           
            logging.info('Adding convolution to origina dataset')
            self.scenarios.append(scenario)


    def saveScenarios(self):
        """save the scenarios to the selected save path as gridded datasets"""
        # determine file names
        basename = os.path.basename(self.dataset)
        fileBasename, fileExtension = os.path.splitext(basename)
        outNames = [self.savepath + os.sep + fileBasename + '_scenario_' + \
                    str(i+1) + fileExtension for i in range(len(self.scenarios))]
        # write the scenarios to files using the same format as for the input
        for ii in range(len(outNames)):
            logging.info('Saving scenario to file ({})'.format(outNames[ii]))
            writeRaster(self.orig_data, outNames[ii], self.scenarios[ii])
