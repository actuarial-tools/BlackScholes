import numpy as np
import pandas as pd
import datetime as dt
import QuantLib as ql

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
                 ann_dividend, lprices, lvolatilities
                 ):

        AnalyticBlackScholes.__init__(self, valuation_date, termination_date, calendar, convention, schedule_freq,
                                      business_convention,
                                      termination_business_convention,
                                      date_generation, end_of_month, type_option, current_price, strike,
                                      ann_risk_free_rate,
                                      ann_volatility,
                                      ann_dividend, lprices, lvolatilities
                                      )

        self.m_delta = self.delta_fun()
        self.m_gamma = self.gamma_fun()
        self.m_vega=self.vega_fun()

    def delta_fun(self):#for call and put is identical
        vdelta = []
        ld1 = [self.d1_fun() for self._S0 in self._ml_prices]
        for i in range(len(ld1)):

            if (self._type_option == 'call'):
                delta = stats.norm.cdf(ld1[i], 0, 1)
                vdelta.append(delta)
            else:
                delta = -stats.norm.cdf(-ld1[i], 0, 1)
                vdelta.append(delta)
        return vdelta

    def gamma_fun(self): #for call and put is identical
        vgamma = []
        ld1 = [self.d1_fun() for self._S0 in self._ml_prices]
        for i in range(len(ld1)):
            gamma = stats.norm.pdf(ld1[i], 0, 1) / (
                        self._ml_prices[i] * self._sigma * np.sqrt(self.mf_yf_between_valu_date_and_maturity))
            vgamma.append((gamma))
        return vgamma

    def vega_fun(self):
        vvega = []
        ld1 = [self.d1_fun() for self._sigma in self._n_volati]
        for i in range(len(self._n_volati)):
            d1 = (np.log(self._S0 / self._K) + (
                        self._r - self._divid + 0.5 * self._n_volati[i] ** 2) * self.mf_yf_between_valu_date_and_maturity) / (
                         np.sqrt(self.mf_yf_between_valu_date_and_maturity) * self._n_volati[i])
            vega = self._S0 * np.sqrt(self.mf_yf_between_valu_date_and_maturity) * stats.norm.pdf(d1, 0, 1)
            vvega.append(vega)
        return vvega


if __name__ == '__main__':
    #############################################----GREEKS----#####################################################

    o_black_scholes_3m = GreeksParameters(valuation_date='2019-06-03',
                                          termination_date='2019-09-03',
                                          schedule_freq='Annual',
                                          convention='ActualActual',  # Daily,Monthly,Quarterly
                                          calendar=ql.Poland(),
                                          business_convention=ql.Following,
                                          termination_business_convention=ql.Following,
                                          date_generation=ql.DateGeneration.Forward,
                                          end_of_month=False,
                                          ##################################
                                          type_option='call',
                                          current_price=90,  # change for 90
                                          strike=91,
                                          ann_risk_free_rate=0.03,
                                          ann_volatility=0.25,
                                          ann_dividend=0,
                                          lprices=np.arange(60, 100),
                                          lvolatilities=np.arange(0.1, 0.5, 0.05))

    print('the end')

    #                              S0=41,
    #                              K=40,
    #                              r=0.08,
    #                              t=0,
    #                              volatility=0.25,
    #                              today=dt.date(2018, 9, 8),
    #                              maturity_date=dt.date(2018, 12, 8),
    #                              day_convention='Actual/365',
    #                              dr=0.02,  # domestic rate
    #                              fr=0.018,
    #                              divid=0)  # foreing rate
    #
    # greeks_7d = GreeksParameters_kb(type_option='call',
    #                                 S0=41,
    #                                 K=40,
    #                                 r=0.08,
    #                                 t=0,
    #                                 volatility=0.25,
    #                                 today=dt.date(2018, 12, 1),
    #                                 maturity_date=dt.date(2018, 12, 8),
    #                                 day_convention='Actual/365',
    #                                 dr=0.02,  # domestic rate
    #                                 fr=0.018,
    #                                 divid=0)  # fore
    #
    # delta_v_6m = greeks_6m.delta_fun(scope=np.arange(30, 56))
    # delta_v_3m=greeks_3m.delta_fun(scope=np.arange(30, 56))
    # delta_v_7d = greeks_7d.delta_fun(scope=np.arange(30, 56))
    # plt.plot(np.arange(30, 56), delta_v_6m,label="6 months")
    # plt.plot(np.arange(30, 56), delta_v_3m,label="3 months")
    # plt.plot(np.arange(30, 56), delta_v_7d,label="7 days")
    # plt.xlabel("Spot Price")
    # plt.ylabel("Delta")
    # plt.title("Delta of Call Options")
    # plt.legend()
    # plt.show()
    #
    # delta_v_6m = greeks_6m.gamma_fun(scope=np.arange(30, 56))
    # delta_v_3m = greeks_3m.gamma_fun(scope=np.arange(30, 56))
    # delta_v_7d = greeks_7d.gamma_fun(scope=np.arange(30, 56))
    # plt.plot(np.arange(30, 56), delta_v_6m, label="6 months")
    # plt.plot(np.arange(30, 56), delta_v_3m, label="3 months")
    # plt.plot(np.arange(30, 56), delta_v_7d, label="7 days")
    # plt.xlabel("Spot Price")
    # plt.ylabel("Delta")
    # plt.title("Delta of Call Options")
    # plt.legend()
    # plt.show()
