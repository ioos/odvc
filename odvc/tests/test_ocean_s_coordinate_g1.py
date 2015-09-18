from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import pytest
import unittest

import netCDF4


from odvc import get_formula_terms_variables, get_formula_terms, nc2biggus
from odvc import ocean_s_coordinate_g1

data_path = os.path.join(os.path.dirname(__file__), 'data')


class OceanSCoordinateG1(unittest.TestCase):
    def setUp(self):
        roms = 'ocean_s_coordinate_g1_roms.nc'
        self.nc = netCDF4.Dataset(os.path.join(data_path, roms))
        formula_terms_variable = get_formula_terms_variables(self.nc)[0]
        formula_terms = get_formula_terms(formula_terms_variable)
        formula_terms_arrays = nc2biggus(self.nc, formula_terms)

        self.s = formula_terms_arrays['s']
        self.c = formula_terms_arrays['C']
        self.eta = formula_terms_arrays['eta']
        self.depth = formula_terms_arrays['depth']
        self.depth_c = formula_terms_arrays['depth_c']

    def tearDown(self):
        self.nc.close()
        unittest.TestCase.tearDown(self)

    def test_ocean_s_coordinate_g1(self):
        z = ocean_s_coordinate_g1(self.s, self.c, self.eta,
                                  self.depth, self.depth_c)
        assert z.ndim == 4

if __name__ == '__main__':
    pytest.main()
