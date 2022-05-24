"""Ocean Dimensionless Vertical Coordinates formulas."""

import numpy as np


def ocean_double_sigma_coordinate(sigma, depth, z1, z2, a, href, k_c):
    """
    Create a dimensioned version of ocean double sigma.

    Definition:
      for k <= k_c
        z(k,j,i)= sigma(k)*f(j,i)
      for k > k_c
        z(k,j,i) = f(j,i) + (sigma(k)-1)*(depth(j,i)-f(j,i))
        f(j,i) = 0.5*(z1+ z2) + 0.5*(z1-z2)* tanh(2*a/(z1-z2)*(depth(j,i)-href))

    where z(k,j,i) is height, positive upwards, relative to ocean datum
    (e.g. mean sea level) at gridpoint (k,j,i) , sigma(k) is the dimensionless
    coordinate at vertical gridpoint (k) for k <= k_c , and depth(j,i) is the
    distance from ocean datum to sea floor (positive value) at horizontal
    gridpoint (j,i) . z1 , z2 , a , and href are constants.

    """
    raise NotImplementedError


def ocean_sigma_z_coordinate(sigma, eta, depth, depth_c, nsigma, zlev):
    """
    Create a dimensioned version of ocean sigma over z.

    Definition:
        for k <= nsigma
            z(n,k,j,i) = eta(n,j,i) + sigma(k)*(min(depth_c,depth(j,i))+eta(n,j,i))
        for k > nsigma
            z(n,k,j,i) = zlev(k)

        where z(n,k,j,i) is height, positive upwards, relative to ocean datum
        (e.g. mean sea level) at gridpoint (n,k,j,i) , eta(n,j,i) is the height
        of the ocean surface, positive upwards, relative to ocean datum at
        gridpoint (n,j,i) , sigma(k) is the dimensionless coordinate at
        vertical gridpoint (k) for k <= nsigma , and depth(j,i) is the distance
        from ocean datum to sea floor (positive value) at horizontal
        gridpoint (j,i) . Above depth depth_c there are nsigma layers.

    """
    raise NotImplementedError


def ocean_sigma_coordinate(sigma, eta, depth):
    """
    Create a dimensioned version of ocean sigma coordinate.

    z(n, k, j, i) = eta(n, j, i) + sigma(k) *
                    (depth(j, i) + eta(n, j, i))

    """
    return eta + sigma * (depth + eta)


def ocean_s_coordinate(s, eta, depth, a, b, depth_c):
    """
    Create a dimensioned version of ocean s-coordinate.

    z(n,k,j,i) = eta(n,j,i)*(1+s(k)) + depth_c*s(k) +
                    (depth(j,i)-depth_c)*C(k)

    where:
        C(k) = (1-b) * sinh(a*s(k)) / sinh(a) +
                b * [tanh(a * (s(k) + 0.5)) / (2 * tanh(0.5*a)) - 0.5]

    """
    c = (1 - b) * np.sinh(a * s) / np.sinh(a) + b * (
        np.tanh(a * (s + 0.5)) / (2 * np.tanh(0.5 * a)) - 0.5
    )
    return eta * (1 + s) + depth_c * s + (depth - depth_c) * c


def ocean_s_coordinate_g1(s, c, eta, depth, depth_c):
    """
    Create a dimensioned version of ocean s-coordinate generic form 1.

    z(n,k,j,i) = S(k,j,i) + eta(n,j,i) * (1 + S(k,j,i) / depth(j,i))

    where:
        S(k,j,i) = depth_c * s(k) + (depth(j,i) - depth_c) * C(k)

    """
    S = (depth_c * s) + ((depth - depth_c) * c)
    return eta * (S / depth + 1) + S


def ocean_s_coordinate_g2(s, eta, depth, depth_c, c):
    """
    Create a dimensioned version of s-coordinate generic form 2.

    z(n,k,j,i) = eta(n,j,i) + (eta(n,j,i) + depth(j,i)) * S(k,j,i)

    where:
        S(k,j,i) = (depth_c * s(k) + depth(j,i) * C(k)) /
                    (depth_c + depth(j,i))

    """
    S = (depth_c * s + depth * c) / (depth_c + depth)
    return eta + (eta + depth) * S
