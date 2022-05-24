"""Test ocean_s_coordinate_g1."""

from pathlib import Path

import dask.array as da
import numpy as np
import pytest
from netCDF4 import Dataset

from odvc import ocean_s_coordinate_g1
from odvc.parse_formula_terms import (
    get_formula_terms,
    get_formula_terms_dims,
    get_formula_terms_variables,
    prepare_arrays,
    z_shape,
)

data_path = Path(__file__).parent.resolve().joinpath("data")


@pytest.fixture
def setup():
    """Set all the formula terms objects up for the tests."""
    roms = "ocean_s_coordinate_g1_roms.nc"
    with Dataset(data_path.joinpath(roms)) as nc:
        formula_terms_variable = get_formula_terms_variables(nc)[0]
        formula_terms = get_formula_terms(formula_terms_variable)
        dims = get_formula_terms_dims(nc, formula_terms)
        new_shape = z_shape(nc, dims)
        arrays = prepare_arrays(nc, formula_terms, new_shape)

        s = arrays["s"]
        c = arrays["C"]
        eta = arrays["eta"]
        depth = arrays["depth"]
        depth_c = arrays["depth_c"]

        z = ocean_s_coordinate_g1(s, c, eta, depth, depth_c)
        sliced = z[0, :, 30, 80]
        yield {"z": z, "sliced": sliced}


def test_shape(setup):
    """Assert that the calculated shape is correct."""
    expected = (1, 36, 82, 130)
    assert setup["z"].shape == expected


def test_slice(setup):
    """Assert that the slice is a dask array."""
    assert isinstance(setup["sliced"], da.Array)


def test_slice_ndarray(setup):
    """Assert that theslice is a numpy array."""
    assert isinstance(setup["sliced"].compute(), np.ndarray)


def test_z_values(setup):
    """Assert that the calculated z values are correct."""
    z_comp = np.array(
        [
            -2531.46656205,
            -2337.58793694,
            -2167.67949235,
            -2018.28088531,
            -1886.27977235,
            -1768.84270488,
            -1663.35273478,
            -1567.35533466,
            -1478.516278,
            -1394.59779732,
            -1313.46227081,
            -1233.11474357,
            -1151.79449631,
            -1068.11831429,
            -981.26114252,
            -891.13435155,
            -798.4970414,
            -704.92970128,
            -612.62956129,
            -524.05182095,
            -441.49011516,
            -366.71960543,
            -300.79609284,
            -244.03541034,
            -196.13254143,
            -156.34993361,
            -123.71062861,
            -97.1566744,
            -75.65879794,
            -58.28034096,
            -44.20608553,
            -32.74776123,
            -23.33605136,
            -15.50607592,
            -8.88076055,
            -3.15458049,
        ],
    )
    np.testing.assert_allclose(setup["sliced"].compute(), z_comp)
