# -*- coding: utf-8 -*-
"""
@author: Eric
"""

from math import sqrt, sin, cos, pi
import numpy as np

def cube_root(x): return x**(1/3) if 0<=x else -(-x)**(1/3)

class Cubic:
    '''
    The Cubic class defines a cubic polynomial based on a sequence of 4 real numbers
    representing the coefficients in descending order.
    Eg. Cubic([1,2,-3,4]) corresponds to the polynomial x**3 + 2x**2 -3x + 4.
    --------------------------------------------------------------------------------
    Cubic.coef      coefficients of the cubic polynomial
    Cubic.delta     delta of the cubic polynomial.
                    Indicates the number of real roots:
                      - delta > 0 : one real root
                      - delta = 0 : three repeated real roots (one root is either double or triple)
                      - delta < 0 : three distinct real roots
    Cubic(val)      computes the value of the cubic polynomial at x = val.
    Cubic.roots()   returns the roots of the cubic polynomial sorted in ascending order.
    --------------------------------------------------------------------------------
    '''

    def __init__(self, coef):
    	'''Raises TypeError when inputs are invalid:
    	    - number of coefficients is different from 4;
    	    - coefficients cannot be converted to float;
    	    - leading coefficient is null.
    	'''

    	if len(coef) != 4:
    		raise TypeError("Please enter a sequence of 4 real numbers.")

    	try:
    		self.coef = (float(coef[0]), float(coef[1]),
    			         float(coef[2]), float(coef[3]))
    	except Exception as e:
    		raise TypeError("Please enter a sequence of 4 real numbers.")

    	try:
    		self._a = self.coef[1] / self.coef[0]
    		self._b = self.coef[2] / self.coef[0]
    		self._c = self.coef[3] / self.coef[0]
    	except ZeroDivisionError as e:
    		raise TypeError("Please enter a leading coeficient that is not zero.")

    	self._p = self._b - self._a**2 / 3
    	self._q = 2 * self._a**3 / 27 - self._a*self._b/3 + self._c

    	# deltas in the range [-tol; +tol] are rounded to 0
    	# to account for floating point numerical errors
    	tol = 1e-15
    	delta = (self._q/2)**2 + (self._p/3)**3
    	self.delta = 0 if abs(delta)<tol else delta

    def __call__(self, val):
    	return ((self.coef[0] * val + self.coef[1]) * val + self.coef[2]) * val + self.coef[3]

    def roots(self):
    	inflection = - self._a/3
    	if self.delta == 0:
    		temp = cube_root(self._q/2)
    		root1 = -2*temp + inflection
    		root2 = temp + inflection
    		return sorted([root1, root2, root2])
    	elif self.delta > 0:
    		return [cube_root(-self._q/2 + sqrt(self.delta)) + cube_root(-self._q/2 - sqrt(self.delta)) + inflection]
    	else:
    		r = sqrt(-self._p/3)
    		theta = np.arcsin(self._q/2/r**3)
    		root1 = 2 * r * sin(theta/3) + inflection
    		root2 = -2 * r * sin(theta/3 + pi/3) + inflection
    		root3 = 2 * r * cos(theta/3 + pi/6) + inflection
    		return sorted([root1, root2, root3])