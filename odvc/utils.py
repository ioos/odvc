# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)

import netCDF4
from biggus import NumpyArrayAdapter


__all__ = ['get_formula_terms_variables',
           'get_formula_terms',
           'nc2biggus']


def get_formula_terms_variables(nc):
    """
    Return a list with all variables from the `nc` object that holds the
    `formula_terms` attribute.

    """
    func = lambda v: v is not None
    return nc.get_variables_by_attributes(formula_terms=func)


def get_formula_terms(var):
    """
    Return a `formula_terms` dict mapping var_names to variables.
    The input can be a netCDF variable (`var`) holding the `formula_terms`
    attribute or the attribute itself.

    """
    if isinstance(var, netCDF4.Variable):
        var = var.formula_terms
    terms = [x.strip(':') for x in var.split()]
    return {k: v for k, v in zip(terms[::2], terms[1::2])}


def nc2biggus(nc, formula_terms):
    """
    Create `biggus.NumpyArrayAdapter` arrays for the variables
    listed in `formula_terms`.

    CAVEAT: There are a few assumptions here that might not hold everywhere.
    1) `eta` is the only 3D variable time x 2D space.
    2) 2D variables (e.g.: depth) are defined in a 2D space.
    3) 1D variables are defined in 1D vertical space.
    4) 0D variables are just parameters.
    5) There are no >4D variables.

    """
    arrays = dict()
    for term, var in formula_terms.items():
        var = nc[var]
        if var.ndim == 0:
            var = var[:]
        elif var.ndim == 1:
            var = NumpyArrayAdapter(var)[None, :, None, None]
        elif var.ndim == 2:
            var = NumpyArrayAdapter(var)[None, None, ...]
        elif var.ndim == 3:
            var = NumpyArrayAdapter(var)[:, None, ...]
        else:
            raise ValueError('Cannot deal with {} dimensions'.format(var.ndim))
        arrays.update({term: var})
    return arrays
