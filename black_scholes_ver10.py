import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql

sys.path.append('../CalendarAlgorithm')
from calendar_ql_supported import SetUpSchedule


class Check_Arguments(ValueError):
    pass


class AnalyticBlackScholes(SetUpSchedule):
    def __init__(self, valuation_date, termination_date, calendar, convention, schedule_freq, business_convention,
                 termination_business_convention,
                 date_generation, end_of_month, type_option, current_price, strike, ann_risk_free_rate, ann_volatility,
                 ann_dividend, lprices, lvolatilities
                 ):
        SetUpSchedule.__init__(self, valuation_date, termination_date, calendar, business_convention,
                               termination_business_convention,
                               date_generation, end_of_month, convention, schedule_freq)
        self._type_option = type_option  # call or put
        self._S0 = current_price
        self._K = strike
        self._r = ann_risk_free_rate
        self._sigma = ann_volatility
        self._divid = ann_dividend
        #############################################################################################################
        self._ml_prices = lprices
        self._n_volati = lvolatilities
        #############################################################################################################

        self.mfd1 = self.d1_fun()
        self.mfd2 = self.d2_fun()
        self.mblprice = self.black_scholes_price_fun()
        self.m_change_with_respect_to_price = self.price_change()
        self.m_change_with_respect_to_volatility = self.vol_change()



    def d1_fun(self):
        d1 = (np.log(self._S0 / self._K) + (
                self._r - self._divid + 0.5 * self._sigma ** 2) * self.ml_yf[0]) / (
                     np.sqrt(self.ml_yf) * self._sigma)
        return d1

    #
    def d2_fun(self):
        d2 = (np.log(self._S0 / self._K) + (
                self._r - self._divid - 0.5 * self._sigma ** 2) * self.ml_yf[0]) / (
                     np.sqrt(self.ml_yf) * self._sigma)
        return d2

    def black_scholes_price_fun(self):
        if (self._type_option == 'call'):
            price = self._S0 * np.exp(-self.ml_yf[0] * self._divid) * sc.stats.norm.cdf(
                self.d1_fun(), 0,
                1) - self._K * np.exp(
                -self.ml_yf[0] * self._r) * stats.norm.cdf(self.d2_fun(), 0, 1)
        else:
            price = self._K * np.exp(-self.ml_yf[0] * self._r) * stats.norm.cdf(-self.d2_fun(), 0,
                                                                                1) - self._S0 * np.exp(
                -self.ml_yf[0] * self._divid) * stats.norm.cdf(-self.d1_fun(), 0, 1)
        return price

    def price_change(self):
        return [self.black_scholes_price_fun() for self._S0 in self._ml_prices]

    def vol_change(self):
        return [self.black_scholes_price_fun() for self._sigma in self._n_volati]




if __name__ == '__main__':
    o_black_scholes_1y = AnalyticBlackScholes(valuation_date='2019-06-03',
                                                 termination_date='2020-06-03',
                                                 schedule_freq='Annual',
                                                 convention='ActualActual',  # Daily,Monthly,Quarterly
                                                 calendar=ql.Poland(),
                                                 business_convention=ql.Following, # TODO Find out what does it mean. It is int =0
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

    o_black_scholes_3m = AnalyticBlackScholes(valuation_date='2019-06-03',
                                               termination_date='2019-09-03',
                                               schedule_freq='Annual',
                                               convention='ActualActual',  # Daily,Monthly,Quarterly
                                               calendar=ql.Poland(),
                                               business_convention=ql.Following,
                                               # TODO Find out what does it mean. It is int =0
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

    o_black_scholes_3d = AnalyticBlackScholes(valuation_date='2019-06-03',
                                               termination_date='2019-06-04',
                                               schedule_freq='Annual',
                                               convention='ActualActual',  # Daily,Monthly,Quarterly
                                               calendar=ql.Poland(),
                                               business_convention=ql.Following,
                                               # TODO Find out what does it mean. It is int =0
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

    b_draw_plots = False
    if b_draw_plots == True:
        plt.plot(o_black_scholes_1y._ml_prices, o_black_scholes_1y.m_change_with_respect_to_price, label="1y to maturity")
        plt.plot(o_black_scholes_3m._ml_prices, o_black_scholes_3m.m_change_with_respect_to_price, label="3m to maturity")
        plt.plot(o_black_scholes_3d._ml_prices, o_black_scholes_3d.m_change_with_respect_to_price, '--', label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Option Price")
        plt.title("Relation price option to maturity")
        plt.legend()
        plt.show()

    print('the end')
