"""Functions to parse the formula terms and prepare arrays."""

from collections import OrderedDict

import netCDF4


def get_formula_terms(var):
    """
    Return a `formula_terms` dict mapping var_names to variables.

    The input can be a netCDF variable (`var`) holding the `formula_terms`
    attribute or the attribute itself.

    """
    formula_terms = OrderedDict()
    if isinstance(var, netCDF4.Variable):
        var = var.formula_terms
    terms = [x.strip(":") for x in var.split()]
    for k, v in zip(terms[::2], terms[1::2]):
        formula_terms.update({k: v})
    return formula_terms


def get_formula_terms_variables(nc):
    """Return a list with all variables that holds the formula_terms attribute."""

    def func(v):
        return v is not None

    var = nc.get_variables_by_attributes(formula_terms=func)
    if not var:
        msg = (
            "Could not find the attribute `formula_terms` in any of the "
            "{!r} variables."
        ).format
        raise ValueError(msg(nc))
    return var


def get_formula_terms_dims(nc, formula_terms):
    """Return an OrderedDict object `dims` holding the `formula_terms` dimensions."""
    dims = OrderedDict()
    for k, v in formula_terms.items():
        dims.update({k: nc[v].dimensions})
    return dims


def z_shape(nc, dims):
    """Return the vertical coordinate `shape` based on the formula_terms `dims`."""
    all_dims = (
        dims.get("eta"),
        dims.get("depth"),
        dims.get("sigma"),
        dims.get("s"),
    )
    all_dims = _filter_none(all_dims)
    all_dims = _flatten(all_dims)
    all_dims = _remove_duplicate(all_dims)
    if len(all_dims) > 1:
        z_dims = all_dims[:]
        z_dims.insert(1, z_dims.pop(-1))

    shape = []
    for dim in z_dims:
        try:
            shape.append(len(nc.dimensions.get(dim)))
        except TypeError:
            msg = "Could not get dimension size for dim {!r}".format
            raise ValueError(msg(dim))

    return tuple(shape)


def _reshape(arr, new_shape):
    """Reshape arrays according to the expected dimensions."""
    shape = arr.shape
    dims = [k for k in shape]
    slicer = slice(None, None, None)

    def select(dim):
        return slicer if dim in dims else None

    keys = tuple(select(k) for k in new_shape)

    return arr.__getitem__(keys)


def prepare_arrays(nc, formula_terms, new_shape):
    """Prepare arrays for formulas."""
    import dask.array as da

    arrays = {}
    for term, var in formula_terms.items():
        var = nc[var]
        if var.ndim == 0:
            arr = var[:]
        else:
            if var.ndim > 2:
                chunks = (1,) + var.shape[1:]
            else:
                chunks = var.shape
            if term == "sigma" and var.ndim == 2:
                chunks = var.shape
            if term == "eta" and var.ndim == 2:
                chunks = (1,) + var.shape[1:]
            arr = da.from_array(var, chunks=chunks)
            arr = _reshape(arr, new_shape)
        arrays.update({term: arr})
    return arrays


def _filter_none(seq):
    """Filter out None in a list."""
    return [x for x in seq if x is not None]


def _flatten(seq):
    """Flatten a list."""
    return [item for sublista in seq for item in sublista]


def _remove_duplicate(seq):
    """Drop duplicated from a list."""
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]
