import numpy as np
import pandas as pd
import datetime as dt
import QuantLib as ql
import math as mth

from black_scholes_ver10 import AnalyticBlackScholes
import scipy as sc
from scipy import stats
import matplotlib.pyplot as plt


class GreeksParameters(AnalyticBlackScholes):
    def __init__(self, valuation_date, termination_date, calendar, convention, schedule_freq,
                 business_convention,
                 termination_business_convention,
                 date_generation, end_of_month, type_option, current_price, strike,
                 ann_risk_free_rate,
                 ann_volatility,
                 ann_dividend
                 ):

        AnalyticBlackScholes.__init__(self, valuation_date, termination_date, calendar, convention, schedule_freq,
                                      business_convention,
                                      termination_business_convention,
                                      date_generation, end_of_month, type_option, current_price, strike,
                                      ann_risk_free_rate,
                                      ann_volatility,
                                      ann_dividend,
                                      )

        self.m_delta = self.delta_fun()
        self.m_gamma = self.gamma_fun()
        self.m_vega = self.vega_fun()

    def delta_fun(self):

        if (self._type_option == 'call'):
            delta = stats.norm.cdf(self.d1_fun(), 0, 1)

        else:
            delta = -stats.norm.cdf(-self.d1_fun(), 0, 1)

        return delta

    def gamma_fun(self):  # for call and put is identical
        gamma = stats.norm.pdf(self.d1_fun(), 0, 1) * np.exp(
            -self._divid * self.mf_yf_between_valu_date_and_maturity) / (
                        self.black_scholes_price_fun() * self._sigma * np.sqrt(
                    self.mf_yf_between_valu_date_and_maturity))

        return gamma

    def vega_fun(self):
        vega = self._S0 * np.sqrt(-self._divid * self.mf_yf_between_valu_date_and_maturity) * np.sqrt(
            self.mf_yf_between_valu_date_and_maturity) * stats.norm.pdf(self.d1_fun(), 0, 1)

        return vega

    def theta(self):
        if (self._type_option == 'call'):
            fTheta = -self._S0 * stats.norm.pdf(self.d1_fun(), 0, 1) * self._sigma * np.exp(
                -self._divid * self.mf_yf_between_valu_date_and_maturity) / 2 * np.sqrt(-self._divid *
                                                                                        self.mf_yf_between_valu_date_and_maturity) + self._divid * self._S0 * np.sqrt(
                -self._divid *
                self.mf_yf_between_valu_date_and_maturity) * stats.norm.pdf(self.d1_fun(), 0,
                                                                            1) - self._r * self._K * np.sqrt(-self._r *
                                                                                                             self.mf_yf_between_valu_date_and_maturity) * stats.norm.pdf(
                self.d2_fun(), 0, 1)
        if (self._type_option == 'call'):
            fTheta = -self._S0 * stats.norm.pdf(self.d1_fun(), 0, 1) * self._sigma * np.exp(
                -self._divid * self.mf_yf_between_valu_date_and_maturity) / 2 * np.sqrt(-self._divid *
                                                                                        self.mf_yf_between_valu_date_and_maturity) - self._divid * self._S0 * np.sqrt(
                -self._divid *
                self.mf_yf_between_valu_date_and_maturity) * stats.norm.pdf(-self.d1_fun(), 0,
                                                                            1) + self._r * self._K * np.sqrt(-self._r *
                                                                                                             self.mf_yf_between_valu_date_and_maturity) * stats.norm.pdf(
                -self.d2_fun(), 0, 1)
        return fTheta


if __name__ == '__main__':
    pass
