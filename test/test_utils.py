from __future__ import absolute_import, division, print_function

import os
import unittest

import dask.array as da

import netCDF4

import numpy as np

from odvc.utils import (
    get_formula_terms,
    get_formula_terms_dims,
    get_formula_terms_variables,
    prepare_arrays,
    z_shape,
)

import pytest

# py2/3 basestring compat.
try:
    basestring
except NameError:
    basestring = str


data_path = os.path.join(os.path.dirname(__file__), 'data')


class UtilTests(unittest.TestCase):
    def setUp(self):
        roms = 'ocean_s_coordinate_g1_roms.nc'
        self.nc = netCDF4.Dataset(os.path.join(data_path, roms))
        self.formula_terms_variables = get_formula_terms_variables(self.nc)
        self.formula_terms_variable = self.formula_terms_variables[0]
        self.formula_terms = get_formula_terms(self.formula_terms_variable)
        self.dims = get_formula_terms_dims(self.nc, self.formula_terms)
        self.new_shape = z_shape(self.nc, self.dims)
        self.arrays = prepare_arrays(self.nc, self.formula_terms, self.new_shape)

    def tearDown(self):
        self.nc.close()
        unittest.TestCase.tearDown(self)

    def test_no_formula_terms_variables(self):
        no_formula_term = 'no_formula_terms.nc'
        with netCDF4.Dataset(os.path.join(data_path, no_formula_term)) as nc:
            with pytest.raises(ValueError):
                get_formula_terms_variables(nc)

    def test_formula_terms_variables(self):
        assert len(self.formula_terms_variables) == 1
        assert hasattr(self.formula_terms_variable, 'formula_terms')
        assert self.formula_terms_variable.standard_name == 'ocean_s_coordinate_g1'

    def test_formula_terms_isstr(self):
        for k, v in self.formula_terms.items():
            assert isinstance(v,  basestring)

    def test_get_formula_terms(self):
        assert isinstance(self.formula_terms, dict)
        s = set(self.formula_terms.keys())
        assert s.issubset(['s', 'C', 'eta', 'depth', 'depth_c'])

    def test_get_formula_terms_dims(self):
        dims = {'s': 1, 'C': 1, 'eta': 3, 'depth': 2, 'depth_c': 0}
        for k, v in self.dims.items():
            assert dims[k] == len(v)

    def test_arrays(self):
        for k, v in self.arrays.items():
            if hasattr(v, 'compute'):
                assert isinstance(v,  da.Array)
                assert isinstance(v.compute(),  np.ndarray)
            else:
                assert isinstance(v,  np.ndarray)
