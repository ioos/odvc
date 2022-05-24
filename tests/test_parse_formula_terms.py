"""Test parse formula terms."""

from pathlib import Path

import dask.array as da
import numpy as np
import pytest
from netCDF4 import Dataset

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
    """Set all the formula terms and arrays objects up for the tests."""
    roms = "ocean_s_coordinate_g1_roms.nc"
    with Dataset(data_path.joinpath(roms)) as nc:
        formula_terms_variable = get_formula_terms_variables(nc)[0]
        formula_terms = get_formula_terms(formula_terms_variable)
        dims = get_formula_terms_dims(nc, formula_terms)
        new_shape = z_shape(nc, dims)
        arrays = prepare_arrays(nc, formula_terms, new_shape)
        yield {
            "formula_terms_variable": formula_terms_variable,
            "formula_terms": formula_terms,
            "dims": dims,
            "new_shape": new_shape,
            "arrays": arrays,
        }


def test_formula_terms_variables(setup):
    """Assert that the formula_terms_variables are correctly identified."""
    assert hasattr(setup["formula_terms_variable"], "formula_terms")
    assert setup["formula_terms_variable"].standard_name == "ocean_s_coordinate_g1"
    for k, v in setup["formula_terms"].items():
        assert isinstance(v, str)


def test_get_formula_terms_and_dims(setup):
    """Assert that the formula_terms are correctly identified."""
    assert isinstance(setup["formula_terms"], dict)
    s = set(setup["formula_terms"].keys())
    assert s.issubset(["s", "C", "eta", "depth", "depth_c"])

    dims = {"s": 1, "C": 1, "eta": 3, "depth": 2, "depth_c": 0}
    for k, v in setup["dims"].items():
        assert dims[k] == len(v)


def test_arrays(setup):
    """Assert that the arrays are the right obj instance."""
    for k, v in setup["arrays"].items():
        if hasattr(v, "compute"):
            assert isinstance(v, da.Array)
            assert isinstance(v.compute(), np.ndarray)
        else:
            assert isinstance(v, np.ndarray)


def test_no_formula_terms_variables():
    """Test if it will fail as expected when formula terms are missing."""
    no_formula_term = "no_formula_terms.nc"
    with Dataset(data_path.joinpath(no_formula_term)) as nc:
        with pytest.raises(ValueError):
            get_formula_terms_variables(nc)
