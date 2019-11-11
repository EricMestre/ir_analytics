# -*- coding: utf-8 -*-
"""
@author: Eric
"""

import pytest
from ir_analytics.models.bachelier import Bachelier
from math import sqrt, pi

ERROR_MAX = 1e-12

### WRONG INPUTS ###

def test_negative_expiry():
	with pytest.raises(ValueError):
		Bachelier(K=0.02, F=0.03, T=-1, vol=0.005, is_call=True)

def test_negative_vol():
	with pytest.raises(ValueError):
		Bachelier(K=0.02, F=0.03, T=1, vol=-0.005, is_call=True)


### CALL PUT PARITY ###

def test_call_put_parity():
	strike = 0.02 ; fwd = 0.03 ; expiry = 2 ; vol = 0.005
	call = Bachelier(K=strike, F=fwd, T=expiry, vol=vol, is_call=True)
	put = Bachelier(K=strike, F=fwd, T=expiry, vol=vol, is_call=False)
	assert (call.price()-put.price(), call.delta()-put.delta(), call.vega()-put.vega()) == pytest.approx(
		    (fwd-strike, 1, 0), abs=ERROR_MAX)


### ATM ###

def test_atm_call():
	fwd = 0.02 ; expiry = 2 ; vol = 0.005
	call = Bachelier(K=fwd, F=fwd, T=expiry, vol=vol, is_call=True)
	assert (call.price(), call.delta(), call.vega()) == pytest.approx(
		   (vol * sqrt(expiry/2/pi), 0.5, sqrt(expiry/2/pi)), abs=ERROR_MAX)

def test_atm_put():
	fwd = 0.02 ; expiry = 2 ; vol = 0.005
	put = Bachelier(K=fwd, F=fwd, T=expiry, vol=vol, is_call=False)
	assert (put.price(), put.delta(), put.vega()) == pytest.approx(
		   (vol * sqrt(expiry/2/pi), -0.5, sqrt(expiry/2/pi)), abs=ERROR_MAX)


### ASYMPTOTIC BEHAVIOR ###

def test_deep_itm_call():
	strike = 0 ; fwd = 0.1 ; expiry = 0.5 ; vol = 0.005
	call = Bachelier(K=strike, F=fwd, T=expiry, vol=vol, is_call=True)
	assert (call.price(), call.delta(), call.vega()) == pytest.approx(
		   (fwd-strike, 1, 0), abs=ERROR_MAX)

def test_deep_otm_call():
	strike = 0 ; fwd = -0.1 ; expiry = 0.5 ; vol = 0.005
	call = Bachelier(K=strike, F=fwd, T=expiry, vol=vol, is_call=True)
	assert (call.price(), call.delta(), call.vega()) == pytest.approx(
		   (0, 0, 0), abs=ERROR_MAX)

def test_deep_itm_put():
	strike = 0 ; fwd = -0.1 ; expiry = 0.5 ; vol = 0.005
	put = Bachelier(K=strike, F=fwd, T=expiry, vol=vol, is_call=False)
	assert (put.price(), put.delta(), put.vega()) == pytest.approx(
		   (strike-fwd, -1, 0), abs=ERROR_MAX)

def test_deep_otm_put():
	strike = 0 ; fwd = 0.1 ; expiry = 0.5 ; vol = 0.005
	put = Bachelier(K=strike, F=fwd, T=expiry, vol=vol, is_call=False)
	assert (put.price(), put.delta(), put.vega()) == pytest.approx(
		   (0, 0, 0), abs=ERROR_MAX)


### EXPIRY DAY ###

def test_expired_itm_call():
	call = Bachelier(K=0.02, F=0.03, T=0, vol=0.005, is_call=True)
	assert (call.price(), call.delta(), call.vega()) == pytest.approx(
		   (0.01, 1, 0), abs=ERROR_MAX)

def test_expired_otm_call():
	call = Bachelier(K=0.04, F=0.03, T=0, vol=0.005, is_call=True)
	assert (call.price(), call.delta(), call.vega()) == pytest.approx(
		   (0, 0, 0), abs=ERROR_MAX)

def test_expired_itm_put():
	put = Bachelier(K=0.04, F=0.03, T=0, vol=0.005, is_call=False)
	assert (put.price(), put.delta(), put.vega()) == pytest.approx(
		   (0.01, -1, 0), abs=ERROR_MAX)

def test_expired_otm_put():
	put = Bachelier(K=0.02, F=0.03, T=0, vol=0.005, is_call=False)
	assert (put.price(), put.delta(), put.vega()) == pytest.approx(
		   (0, 0, 0), abs=ERROR_MAX)


### NO VOL ###

def test_no_vol_itm_call():
	call = Bachelier(K=0.02, F=0.03, T=1, vol=0, is_call=True)
	assert (call.price(), call.delta(), call.vega()) == pytest.approx(
		   (0.01, 1, 0), abs=ERROR_MAX)

def test_no_vol_otm_call():
	call = Bachelier(K=0.04, F=0.03, T=1, vol=0, is_call=True)
	assert (call.price(), call.delta(), call.vega()) == pytest.approx(
		   (0, 0, 0), abs=ERROR_MAX)

def test_no_vol_itm_put():
	put = Bachelier(K=0.04, F=0.03, T=1, vol=0, is_call=False)
	assert (put.price(), put.delta(), put.vega()) == pytest.approx(
		   (0.01, -1, 0), abs=ERROR_MAX)

def test_no_vol_otm_put():
	put = Bachelier(K=0.02, F=0.03, T=1, vol=0, is_call=False)
	assert (put.price(), put.delta(), put.vega()) == pytest.approx(
		   (0, 0, 0), abs=ERROR_MAX)