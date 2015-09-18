from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os
import unittest

import pytest

import biggus
import netCDF4
import numpy as np

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

        s = formula_terms_arrays['s']
        c = formula_terms_arrays['C']
        eta = formula_terms_arrays['eta']
        depth = formula_terms_arrays['depth']
        depth_c = formula_terms_arrays['depth_c']

        self.z = ocean_s_coordinate_g1(s, c, eta, depth, depth_c)
        self.sliced = self.z[0, :, 30, 80]

    def tearDown(self):
        self.nc.close()
        unittest.TestCase.tearDown(self)

    def test_shape(self):
        assert self.z.shape == (1, 36, 82, 130)

    def test_slice_biggus(self):
        assert isinstance(self.sliced, biggus._Elementwise)

    def test_slice_ndarray(self):
        assert isinstance(self.sliced.ndarray(), np.ndarray)

    def test_z_values(self):
        z_comp = np.array([-2531.46656205, -2337.58793694, -2167.67949235,
                           -2018.28088531, -1886.27977235, -1768.84270488,
                           -1663.35273478, -1567.35533466, -1478.516278,
                           -1394.59779732, -1313.46227081, -1233.11474357,
                           -1151.79449631, -1068.11831429, -981.26114252,
                           -891.13435155, -798.4970414, -704.92970128,
                           -612.62956129, -524.05182095, -441.49011516,
                           -366.71960543, -300.79609284, -244.03541034,
                           -196.13254143, -156.34993361, -123.71062861,
                           -97.1566744, -75.65879794, -58.28034096,
                           -44.20608553, -32.74776123, -23.33605136,
                           -15.50607592, -8.88076055, -3.15458049])
        z = self.sliced.ndarray()
        np.testing.assert_allclose(z, z_comp)

if __name__ == '__main__':
    pytest.main()
