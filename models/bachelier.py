# -*- coding: utf-8 -*-
"""
@author: Eric
"""

from math import sqrt
from scipy.stats import norm

class Bachelier:

    def __init__(self, K, F, T, vol, is_call):
        try:
            self.K = float(K)
            self.F = float(F)
            self.T = float(T)
            self.vol = float(vol)
            self.is_call = bool(is_call)
        except Exception as e:
            raise TypeError

        if self.T < 0:
            raise ValueError("Time to expiry should be positive.")

        if self.vol < 0:
            raise ValueError("Volatility should be positive.")

        self.money = self.F - self.K
        self.stddev = self.vol * sqrt(self.T)
        self._theta = 1 if self.is_call else -1 # _theta == 1 for calls, -1 for puts


    def price(self):
        if self.stddev == 0:
            return max(self._theta * self.money, 0)
        else:
            d = self.money / self.stddev
            return self._theta * self.money * norm.cdf(self._theta * d) + self.stddev * norm.pdf(d)

    def delta(self):
        if self.stddev == 0:
            return self._theta if self._theta * self.money > 0 else 0
        else:
        	d = self.money / self.stddev
        	return self._theta * norm.cdf(self._theta * d)

    def vega(self):
        # vega is assumed to be null when vol is zero
        if self.stddev == 0:
            return 0
        else:
        	d = self.money / self.stddev
        	return sqrt(self.T)	* norm.pdf(d)