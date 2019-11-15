import sys


import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql
import seaborn as sns
import os
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append('../CalendarAlgorithm')
from calendar_ql_supported import SetUpSchedule

controlPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
os.chdir(controlPath)
controlFile = pd.read_excel('BlackScholes.xlsx', sheet_name='Input')


class QuantLibConverter:
    def __init__(self, calendar):
        self._calendar = calendar
        self.mqlCalendar = self.setCalendar()
        self.mqlBusinessConvention = self.setBusinessConvention()
        self.mqlTerminationBusinessConvention = self.setTerminationBusinessConvention()

    def setCalendar(self):
        if self._calendar == 'USA':
            return ql.UnitedStates()
        if self._calendar == 'United Kingdom':
            return ql.UnitedKingdom()
        if self._calendar == 'Switzerland':
            return ql.Switzerland()
        if self._calendar == 'Poland':
            return ql.Poland()

    def setBusinessConvention(self):
        return ql.Following

    def setTerminationBusinessConvention(self):
        return ql.Following


qlConverter = QuantLibConverter(calendar=controlFile.loc[4, 'Value'])


class EquityModels(SetUpSchedule):

    def __init__(self, valuation_date, termination_date, calendar, convention, schedule_freq, business_convention,
                 termination_business_convention,
                 date_generation, end_of_month, type_option: str, current_price: float, strike: float,
                 ann_risk_free_rate: float,
                 ann_volatility: float, ann_dividend: float, runs: int):
        SetUpSchedule.__init__(self, valuation_date, termination_date, calendar, business_convention,
                               termination_business_convention,
                               date_generation, end_of_month, convention, schedule_freq)
        self._type_option = type_option  # call or put
        self._S0 = current_price
        self._K = strike
        self._drift = ann_risk_free_rate
        self._sigma = ann_volatility
        self._divid = ann_dividend
        self._runs = runs
        self.m_ar_equity_price = self.geometric_brownian_motion_scenario_fun()
        self.mlt_payoffandST = self.calculate_payoffs()  # lt list of tuples ST and tuples and payoff sorted
        self.mf_monte_carlo_price = self.monte_carlo_price()
        self.mListOfDates=self.m_schedule

    def geometric_brownian_motion_scenario_fun(self):
        dt = self.ml_yf
        gbm_model = np.zeros((self._runs, len(
            self.ml_dates)))  # create empty array #TODO to nie moze byc do scenario calendar tylko zalezec od obiektu o_gbmscenarios
        gbm_model[:, 0] = self._S0  # current price
        for t in range(1, len(gbm_model[0])):
            z = np.random.standard_normal(self._runs)  # draw number from normal distribution N(0,sqrt(t*sigma))
            gbm_model[:, t] = gbm_model[:, t - 1] * np.exp(
                (self._drift - 0.5 * self._sigma ** 2) * dt[t - 1] +
                self._sigma * np.sqrt(dt[t - 1]) * z)
        return np.transpose(gbm_model)

    def calculate_payoffs(self):  # delivery_data random or given
        ST = self.m_ar_equity_price[-1]

        vpayoff = np.zeros(len(ST))
        for i in range(len(ST)):#
            if (self._type_option == 'call'):
                vpayoff[i] = max(ST[i] - self._K, 0)
            else:
                vpayoff[i] = max(self._K - ST[i], 0)
        zipped = list((zip(ST, vpayoff)))
        sorted_zip = sorted(zipped, key=lambda x: x[0])  # without sorting there is a problem with ploting
        return sorted_zip

    def monte_carlo_price(self) -> float:
        take_payoff = lambda x: x[1] #get second coordinates from tuple
        payoff = list(map(take_payoff, self.mlt_payoffandST))
        return np.mean(payoff)*np.exp(-self._drift*self.mf_yf_between_valu_date_and_maturity)

    # histogram corresponding to the final values of paths
    def histogramOfSt(self):
        ST = self.m_ar_equity_price[-1]
        hist = sns.distplot(ST, hist=True, rug=True)
        plt.axvline(self._S0, color='red')
        plt.xlim((0, max(ST) + 5))
        plt.xlabel("Spot Price")
        plt.show()




if __name__ == '__main__':
    o_black_scholes_scenarios = EquityModels(valuation_date=controlFile.loc[0, 'Value'],
                                             termination_date=controlFile.loc[1, 'Value'],
                                             schedule_freq=controlFile.loc[2, 'Value'],
                                             convention=controlFile.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                             calendar=qlConverter.mqlCalendar,
                                             business_convention=ql.Following,
                                             termination_business_convention=ql.Following,
                                             date_generation=ql.DateGeneration.Forward,
                                             end_of_month=controlFile.loc[8, 'Value'],
                                             ##################################
                                             type_option=controlFile.loc[9, 'Value'],
                                             current_price=controlFile.loc[10, 'Value'],
                                             strike=controlFile.loc[11, 'Value'],
                                             ann_risk_free_rate=controlFile.loc[12, 'Value'],
                                             ann_volatility=controlFile.loc[13, 'Value'],
                                             ann_dividend=controlFile.loc[14, 'Value'],
                                             runs=controlFile.loc[15, 'Value'])

    gbmRealizations = o_black_scholes_scenarios.m_ar_equity_price
    o_black_scholes_scenarios.histogramOfSt()

    print('the end')
