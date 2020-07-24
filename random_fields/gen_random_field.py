#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 10:06:15 2020

@author: Lukas Graf
"""

import numpy as np


class random_field(object):
    """
    class for generating random fields (2-d) using numpy.random.normal

    :param rows: Rows (y-dim) of the field to be generated
    :param cols: Columns (x-dim) of the field to be generated
    """
    def __init__(self, rows, cols):
        """class constructor"""
        self.rows = rows
        self.cols = cols


    def gaussian(self, mean, std, minval=None, maxval=None):
        """
        returns a Gaussian random field based on mean and standard deviation.
        If specified, a truncated Gaussian random field is generated

        :param mean: mean value of the Gaussian distribution (mu)
        :param std: standard deviation of the Gaussian distribution (sigma)
        :param minval: min value to truncate the Gaussian distribution (opt.)
        :param maxval: max value to truncate the Gaussian distribution (opt.)
        :return: array with Gaussian random field
        """
        # check inputs
        if minval is None and maxval is not None:
            raise ValueError('if minval is None also maxval must be None')
        if minval is not None and maxval is  None:
            raise ValueError('if maxval is None also minval must be None')

        rfield = None
        # Gaussian distribution without truncation
        if minval is None and maxval is None:
            rfield = np.random.normal(mean, std, (self.rows, self.cols))
        # with truncation
        else:
            n_samples = self.rows * self.cols
            # fill a 1-d array first and convert to 2-d afterwards
            # solution found on Stackoverflow
            # (https://stackoverflow.com/questions/47933019/how-to-properly-sample-truncated-distributions)
            # on 7th July 2020
            samples = np.zeros((0,))
            while samples.shape[0] < n_samples: 
                s = np.random.normal(0, 1, size=(n_samples,))
                accepted = s[(s >= minval) & (s <= maxval)]
                samples = np.concatenate((samples, accepted), axis=0)
            # take the first n_samples since probably more samples are returned
            # than required
            samples = samples[:n_samples]
            # reshape to 2-d
            rfield = np.reshape(samples, (self.rows, self.cols))

        return rfield


    def multiple_gaussian(self, n_realizations, **kwargs):
        """
        generates a set of (truncated) Gaussian random field realizations
        and returns a list of random fields

        :param n_realizations: number of realizations to be generated
        :kwargs: key arguments to pass to random_field.gaussian
        :return: list of arrays with Gaussian random fields
        """
        assert n_realizations > 0

        # list comprehension to get set of random fields
        fields = [self.gaussian(**kwargs) for x in range(n_realizations)]
        return fields


if __name__ == '__main__':

    # usage example
    # set properties of the Gaussian function to draw samples from to
    # generate the random field
    rows = cols = 100
    mean = 0.
    std = 1.
    minval = -1
    maxval = 1.
    n_realizations = 5

    # create a instance of the random_field class
    rand = random_field(rows=rows, cols=cols)
    # generate a single Gaussian random field (without truncation)
    rfield = rand.gaussian(mean=mean, std=std)
    # generate a single truncated Gaussian field
    rfield_trunc = rand.gaussian(mean=mean, std=std, minval=minval,
                                 maxval=maxval)
    # generate a set of Gaussian random fields
    rfields = rand.multiple_gaussian(n_realizations=n_realizations, mean=mean,
                                     std=std)
    # generate a set of truncated Gaussian random fields
    rfields_trunc = rand.multiple_gaussian(n_realizations=n_realizations,
                                           mean=mean, std=std,
                                           minval=minval, maxval=maxval)