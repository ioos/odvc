# -*- coding: utf-8 -*-

__version__ = '0.0.1'


from formulas import (ocean_sigma_coordinate, ocean_double_sigma_coordinate,
                      ocean_sigma_z_coordinate, ocean_s_coordinate,
                      ocean_s_coordinate_g1, ocean_s_coordinate_g2)


odvcs = {'ocean_sigma_coordinate': ocean_sigma_coordinate,
         'ocean_double_sigma_coordinate': ocean_double_sigma_coordinate,
         'ocean_sigma_z_coordinate': ocean_sigma_z_coordinate,
         'ocean_s_coordinate': ocean_s_coordinate,
         'ocean_s_coordinate_g1': ocean_s_coordinate_g1,
         'ocean_s_coordinate_g2': ocean_s_coordinate_g2}
