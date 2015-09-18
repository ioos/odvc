# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np

__all__ = ['ocean_double_sigma_coordinate',
           'ocean_sigma_z_coordinate',
           'ocean_sigma_coordinate',
           'ocean_s_coordinate',
           'ocean_s_coordinate_g1',
           'ocean_s_coordinate_g2']


def ocean_double_sigma_coordinate(sigma, depth, z1, z2, a, href, k_c):
    """
    Creates a dimensioned version of ocean double sigma.

    """
    raise NotImplemented


def ocean_sigma_z_coordinate():
    """
    Creates a dimensioned version of ocean sigma over z.

    """
    raise NotImplemented


def ocean_sigma_coordinate(sigma, eta, depth):
    """
    Creates a dimensioned version of ocean sigma coordinate.

    z(n, k, j, i) = eta(n, j, i) + sigma(k) *
                    (depth(j, i) + eta(n, j, i))

    """
    return eta + sigma * (depth + eta)


def ocean_s_coordinate(s, eta, depth, a, b, depth_c):
    """
    Creates a dimensioned version of ocean s-coordinate.

    z(n,k,j,i) = eta(n,j,i)*(1+s(k)) + depth_c*s(k) +
                    (depth(j,i)-depth_c)*C(k)

    where:
        C(k) = (1-b) * sinh(a*s(k)) / sinh(a) +
                b * [tanh(a * (s(k) + 0.5)) / (2 * tanh(0.5*a)) - 0.5]

    """
    c = ((1 - b) * np.sinh(a * s) / np.sinh(a) + b *
         (np.tanh(a * (s + 0.5)) / (2 * np.tanh(0.5 * a)) - 0.5))
    return eta * (1 + s) + depth_c * s + (depth - depth_c) * c


def ocean_s_coordinate_g1(s, c, eta, depth, depth_c):
    """
    Creates a dimensioned version of ocean s-coordinate generic form 1.

    z(n,k,j,i) = S(k,j,i) + eta(n,j,i) * (1 + S(k,j,i) / depth(j,i))

    where:
        S(k,j,i) = depth_c * s(k) + (depth(j,i) - depth_c) * C(k)

    """
    S = (depth_c * s) + ((depth - depth_c) * c)
    return eta * (S / depth + 1) + S


def ocean_s_coordinate_g2(s, eta, depth, depth_c, c):
    """
    Creates a dimensioned version of s-coordinate generic form 2.

    z(n,k,j,i) = eta(n,j,i) + (eta(n,j,i) + depth(j,i)) * S(k,j,i)

    where:
        S(k,j,i) = (depth_c * s(k) + depth(j,i) * C(k)) /
                    (depth_c + depth(j,i))

    """
    S = (depth_c * s + depth * c) / (depth_c + depth)
    return eta + (eta + depth) * S
