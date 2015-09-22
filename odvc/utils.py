# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import OrderedDict
import netCDF4
from biggus import NumpyArrayAdapter


__all__ = ['get_formula_terms',
           'get_formula_terms_variables',
           'get_formula_terms_dims',
           'nc2biggus']


def get_formula_terms(var):
    """
    Return a `formula_terms` dict mapping var_names to variables.
    The input can be a netCDF variable (`var`) holding the `formula_terms`
    attribute or the attribute itself.

    """
    formula_terms = OrderedDict()
    if isinstance(var, netCDF4.Variable):
        var = var.formula_terms
    terms = [x.strip(':') for x in var.split()]
    for k, v in zip(terms[::2], terms[1::2]):
        formula_terms.update({k: v})
    return formula_terms


def get_formula_terms_variables(nc):
    """
    Return a list with all variables from the `nc` object that holds the
    `formula_terms` attribute.

    """
    def func(v):
        return v is not None
    var = nc.get_variables_by_attributes(formula_terms=func)
    if not var:
        msg = ("Could not find the attribute `formula_terms` in any of the "
               "{!r} variables.").format
        raise ValueError(msg(nc))
    return var


def get_formula_terms_dims(nc, formula_terms):
    """
    Returns an OrderedDict object `dims` holding the `formula_terms` dimensions
    listed in the netCDF4-python object `nc`

    """
    dims = OrderedDict()
    for k, v in formula_terms.items():
        dims.update({k: nc[v].dimensions})
    return dims


def get_z_dims(dims):
    """
    Returns the vertical coordinate final dimensions (`final_dims`) based on
    the combined dimensions of the formula_terms `dims`.

    """
    all_dims = (dims.get('eta'), dims.get('depth'),
                dims.get('sigma'), dims.get('s'))
    all_dims = _filter_none(all_dims)
    all_dims = _flatten(all_dims)
    all_dims = _remove_duplicate(all_dims)
    if len(all_dims) > 1:
        final_dims = all_dims[:]
        final_dims.insert(1, final_dims.pop(-1))
    return final_dims


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


def _filter_none(seq):
    return [x for x in seq if x is not None]


def _flatten(seq):
    return [item for sublista in seq for item in sublista]


def _remove_duplicate(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
