from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest
from builtins import str

import pytest

import biggus
import netCDF4
import numpy as np

from odvc import get_formula_terms_variables, get_formula_terms, nc2biggus

data_path = os.path.join(os.path.dirname(__file__), 'data')


class UtilTests(unittest.TestCase):
    def setUp(self):
        roms = 'ocean_s_coordinate_g1_roms.nc'
        self.nc = netCDF4.Dataset(os.path.join(data_path, roms))
        self.formula_terms_variable = get_formula_terms_variables(self.nc)[0]
        self.formula_terms = get_formula_terms(self.formula_terms_variable)
        self.formula_terms_arrays = nc2biggus(self.nc, self.formula_terms)

    def tearDown(self):
        self.nc.close()
        unittest.TestCase.tearDown(self)

    def test_formula_terms_variables(self):
        formula_terms_variables = get_formula_terms_variables(self.nc)
        for var in formula_terms_variables:
            assert hasattr(var,  'formula_terms')

    def test_no_formula_terms_variables(self):
        no_formula_term = 'no_formula_terms.nc'
        with netCDF4.Dataset(os.path.join(data_path, no_formula_term)) as nc:
            with pytest.raises(ValueError):
                get_formula_terms_variables(nc)

    def test_get_formula_terms(self):
        assert isinstance(self.formula_terms, dict)

    def test_formula_terms_isstr(self):
        for k, v in self.formula_terms.items():
            assert isinstance(v,  str)

    def test_nc2biggus(self):
        for k, v in self.formula_terms_arrays.items():
            assert isinstance(v,  (biggus.ArrayContainer, np.ndarray))

if __name__ == '__main__':
    pytest.main()
