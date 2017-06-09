# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from . import utils
from ._version import get_versions
from .formulas import (
    ocean_double_sigma_coordinate,
    ocean_s_coordinate,
    ocean_s_coordinate_g1,
    ocean_s_coordinate_g2,
    ocean_sigma_coordinate,
    ocean_sigma_z_coordinate,
)


__version__ = get_versions()['version']
del get_versions

__all__ = [
    utils,
    ocean_double_sigma_coordinate,
    ocean_sigma_z_coordinate,
    ocean_sigma_coordinate,
    ocean_s_coordinate,
    ocean_s_coordinate_g1,
    ocean_s_coordinate_g2
]
