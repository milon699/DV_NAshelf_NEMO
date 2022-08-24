# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 14:35:27 2022

Class with basic calculation tools

@author: milon
"""

import xarray as xr
import numpy as np

def mean_weighted(self, dim=None, weights=None):
    
    if weights is None:
        mean = self.mean(dim, skipna = True)
        std = self.std(dim, skipna = True)
        return mean, std
    else:
        mean = (self * weights).sum(dim, skipna = True) / weights.sum(dim, skipna = True)
        len_weights = np.isfinite(weights).sum(dim = dim, skipna = True)
        std = xr.ufuncs.sqrt(((self - mean)**2 * weights).sum(dim, skipna = True) / ((len_weights-1)/len_weights*weights.sum(dim, skipna = True)))
        return mean, std
