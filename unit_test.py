# IMPORTS
import numpy as np
import random as rd
from classes import *

try:
    # TEST COORDINATE CHANGE

    minimal_error_cartesian=CartesianCoordinate(0.1, 0.1, 0.1)
    minimal_error_spherical=SphericalCoordinate(0.1, 0.1, 0.1)

    for i in range(50):
        x=rd.randint(1,100)
        y=rd.randint(1,100)
        z=rd.randint(1,100)
        coordinate_cartesian=CartesianCoordinate(x, y, z)
        coordinate_spherical=coordinate_cartesian.ToSpherical()
        coordinate_cart_test=coordinate_spherical.ToCartesian()
        coordinate_sphe_test=coordinate_cart_test.ToSpherical()
        error_cartesian=coordinate_cart_test-coordinate_cartesian
        error_spherical=coordinate_sphe_test-coordinate_spherical
        if error_cartesian.first>minimal_error_cartesian.first:
            raise Exception('bad cartesian coordinate at the '+str(i)+' test')
        if error_cartesian.second>minimal_error_cartesian.second:
            raise Exception('bad cartesian coordinate at the '+str(i)+' test')
        if error_cartesian.third>minimal_error_cartesian.third:
            raise Exception('bad cartesian coordinate at the '+str(i)+' test')
        if error_spherical.first>minimal_error_spherical.first:
            raise Exception('bad spherical coordinate at the '+str(i)+' test')
        if error_spherical.second>minimal_error_spherical.second:
            raise Exception('bad spherical coordinate at the '+str(i)+' test')
        if error_spherical.third>minimal_error_spherical.third:
            raise Exception('bad spherical coordinate at the '+str(i)+' test')

    # END
    print('success')

except Exception as err:
    print('Error during unit testing '+str(err))
