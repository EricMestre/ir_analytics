# -*- coding: utf-8 -*-
"""
@author: Eric
"""

import pytest
from ir_analytics.math.cubic import Cubic
import numpy as np

ERROR_MAX = 1e-12

def test_single_root():
    cubic = Cubic([1,1,1,-3])
    assert cubic.roots() == pytest.approx([1], abs=ERROR_MAX)

def test_double_root():
    cubic = Cubic([1,-5,8,-4])
    assert cubic.roots() == pytest.approx([1,2,2], abs=ERROR_MAX)

def test_triple_root():
    cubic = Cubic([1,-3,3,-1])
    assert cubic.roots() == pytest.approx([1,1,1], abs=ERROR_MAX)

def test_distinct_roots():
    cubic = Cubic([1,-6,11,-6])
    assert cubic.roots() == pytest.approx([1,2,3], abs=ERROR_MAX)

def test_scattered_roots():
    cubic = Cubic([1,-103,302,-200])
    assert cubic.roots() == pytest.approx([1,2,100], abs=ERROR_MAX)

def test_negative_roots():
    cubic = Cubic([1,-4,-55,-50])
    assert cubic.roots() == pytest.approx([-5,-1,10], abs=ERROR_MAX)

def test_scaling_roots_invariance():
    coef = np.array([1,-6,11,-6])
    cubic1 = Cubic(coef)
    cubic2 = Cubic(2*coef)
    assert cubic1.roots() == cubic2.roots()

def test_tuple_list():
    coef_tuple = (1,-6,11,-6)
    coef_list = [1,-6,11,-6]
    cubic_tuple = Cubic(coef_tuple)
    cubic_list = Cubic(coef_list)
    assert cubic_tuple.roots() == cubic_list.roots()

def test_list_ndarray():
    coef_list = [1,-6,11,-6]
    coef_ndarray = np.array(coef_list)
    cubic_list = Cubic(coef_list)
    cubic_ndarray = Cubic(coef_ndarray)
    assert cubic_list.roots() == cubic_ndarray.roots()

def test_too_few_inputs():
    with pytest.raises(TypeError):
        Cubic([1,2.2,-6])

def test_too_many_inputs():
    with pytest.raises(TypeError):
        Cubic([1,2.2,-6,1,-4])

def test_numeric_string_input():
    assert Cubic([1,2.2,-3.5,'4']).coef == Cubic([1,2.2,-3.5,4]).coef

def test_non_numeric_inputs():
    with pytest.raises(TypeError):
        Cubic([1,2.2,-3.5,'abc'])

def test_cubic_not_quadratic():
    with pytest.raises(TypeError):
        Cubic((0, -2, 4, -2.3))