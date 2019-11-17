import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql
import os
import pandas as pd

sys.path.append('../CalendarAlgorithm')
from calendar_ql_supported import SetUpSchedule

from black_scholes_ver10 import AnalyticBlackScholes
from greeks import GreeksParameters
from scenario_generator import EquityModels
from utilities import QuantLibConverter

controlPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
os.chdir(controlPath)
controlFile1Y = pd.read_excel('BlackScholes.xlsx', sheet_name='Input 1Y')



if __name__ == '__main__':
    qlConverter = QuantLibConverter(calendar=controlFile1Y.loc[4, 'Value'])

    o_black_scholes_1y = AnalyticBlackScholes(valuation_date=controlFile1Y.loc[0, 'Value'],
                                              termination_date=controlFile1Y.loc[1, 'Value'],
                                              schedule_freq=controlFile1Y.loc[2, 'Value'],
                                              convention=controlFile1Y.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                              calendar=qlConverter.mqlCalendar,
                                              business_convention=qlConverter.mqlBusinessConvention,
                                              termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                              date_generation=ql.DateGeneration.Forward,
                                              end_of_month=controlFile1Y.loc[8, 'Value'],
                                              ##################################
                                              type_option=controlFile1Y.loc[9, 'Value'],
                                              current_price=controlFile1Y.loc[10, 'Value'],
                                              strike=controlFile1Y.loc[11, 'Value'],
                                              ann_risk_free_rate=controlFile1Y.loc[12, 'Value'],
                                              ann_volatility=controlFile1Y.loc[13, 'Value'],
                                              ann_dividend=controlFile1Y.loc[14, 'Value'])

    o_black_scholes_3m = AnalyticBlackScholes(valuation_date=controlFile1Y.loc[0, 'Value'],
                                              termination_date=controlFile1Y.loc[1, 'Value'],
                                              schedule_freq=controlFile1Y.loc[2, 'Value'],
                                              convention=controlFile1Y.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                              calendar=qlConverter.mqlCalendar,
                                              business_convention=qlConverter.mqlBusinessConvention,
                                              termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                              date_generation=ql.DateGeneration.Forward,
                                              end_of_month=controlFile1Y.loc[8, 'Value'],
                                              ##################################
                                              type_option=controlFile1Y.loc[9, 'Value'],
                                              current_price=controlFile1Y.loc[10, 'Value'],
                                              strike=controlFile1Y.loc[11, 'Value'],
                                              ann_risk_free_rate=controlFile1Y.loc[12, 'Value'],
                                              ann_volatility=controlFile1Y.loc[13, 'Value'],
                                              ann_dividend=controlFile1Y.loc[14, 'Value'])


    o_black_scholes_3d = AnalyticBlackScholes(valuation_date='2019-06-03',
                                              termination_date='2019-06-06',
                                              schedule_freq='Annual',  # tu powinno byc two dates czemu to dziala ?:D
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
                                              )

    prices_range = np.arange(60, 100)
    vol_range = np.arange(0.1, 0.5, 0.05)

    option_price1y = [o_black_scholes_1y.black_scholes_price_fun() for o_black_scholes_1y._S0 in prices_range]
    change_vol1y = [o_black_scholes_1y.black_scholes_price_fun() for o_black_scholes_1y._sigma in vol_range]

    option_price3m = [o_black_scholes_3m.black_scholes_price_fun() for o_black_scholes_3m._S0 in prices_range]
    change_vol3m = [o_black_scholes_3m.black_scholes_price_fun() for o_black_scholes_3m._sigma in vol_range]

    option_price3d = [o_black_scholes_3d.black_scholes_price_fun() for o_black_scholes_3d._S0 in prices_range]
    change_vol3d = [o_black_scholes_3d.black_scholes_price_fun() for o_black_scholes_3d._sigma in vol_range]

    b_draw_plots = True
    if b_draw_plots == True:
        plt.plot(prices_range, option_price1y, label="1y to maturity")
        plt.plot(prices_range, option_price3m, label="3m to maturity")
        plt.plot(prices_range, option_price3d, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Option Price")
        plt.title("Relation price option to maturity")
        plt.legend()
        plt.show()

    #############################################----GREEKS----#####################################################

    greeks_1y = GreeksParameters(valuation_date='2019-06-03',
                                 termination_date='2020-06-03',
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
                                 ann_dividend=0)

    greeks_3m = GreeksParameters(valuation_date='2019-06-03',
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
                                 )

    greeks_3d = GreeksParameters(valuation_date='2019-06-03',
                                 termination_date='2019-06-06',
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
                                 ann_dividend=0)
    ##########Delta
    delta1y = [greeks_1y.delta() for greeks_1y._S0 in prices_range]
    delta3m = [greeks_3m.delta() for greeks_3m._S0 in prices_range]
    delta3d = [greeks_3d.delta() for greeks_3d._S0 in prices_range]

    b_delta_plots = True
    if b_delta_plots == True:
        plt.plot(prices_range, delta1y, label="1y to maturity")
        plt.plot(prices_range, delta3m, label="3m to maturity")
        plt.plot(prices_range, delta3d, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Delta")
        plt.title("Delta of Option")
        plt.legend()
        plt.show()
    ##########Delta

    ##########Gamma

    gamma1y = [greeks_1y.gamma() for greeks_1y._S0 in prices_range]
    gamma3m = [greeks_3m.gamma() for greeks_3m._S0 in prices_range]
    gamma3d = [greeks_3d.gamma() for greeks_3d._S0 in prices_range]

    b_gamma_plots = False
    if b_gamma_plots == True:
        plt.plot(prices_range, gamma1y, label="1y to maturity")
        plt.plot(prices_range, gamma3m, label="3m to maturity")
        plt.plot(prices_range, gamma3d, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Gamma")
        plt.title("Gamma of Option")
        plt.legend()
        plt.show()
    ##########Gamma

    ########## Theta

    theta1y = [greeks_1y.theta() for greeks_1y._S0 in prices_range]
    theta3m = [greeks_3m.theta() for greeks_3m._S0 in prices_range]
    theta3d = [greeks_3d.theta() for greeks_3d._S0 in prices_range]

    b_theta_plots = True
    if b_theta_plots == True:
        plt.plot(prices_range, theta1y, label="1y to maturity")
        plt.plot(prices_range, theta3m, label="3m to maturity")
        plt.plot(prices_range, theta3d, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Theta")
        plt.title("Theta of Option")
        plt.legend()
        plt.show()

    ########## Theta

    #############################################----SIMULATION----#####################################################

    o_black_scholes_scenarios = EquityModels(valuation_date='2019-06-20',
                                             termination_date='2019-08-20',
                                             schedule_freq='Daily',
                                             convention='ActualActual',  # Daily,Monthly,Quarterly
                                             calendar=ql.Poland(),
                                             business_convention=ql.Following,
                                             # TODO Find out what does it mean. It is int =0
                                             # TODO Find out what does it mean. It is int =0
                                             termination_business_convention=ql.Following,
                                             date_generation=ql.DateGeneration.Forward,
                                             end_of_month=False,
                                             ##################################
                                             type_option='call',
                                             current_price=90,
                                             strike=91,
                                             ann_risk_free_rate=0.03,
                                             ann_volatility=0.25,
                                             ann_dividend=0,
                                             runs=100000)

    gbmRealizations = o_black_scholes_scenarios.m_ar_equity_price

    set_index = list(map(lambda x: str(x), o_black_scholes_scenarios.ml_dates))

    df_scenarios = pd.DataFrame(gbmRealizations, index=set_index)

    b_scenario_plots = False
    if b_scenario_plots == True:
        for k in range(18):
            plt.plot(df_scenarios[k])
        plt.grid(True)
        plt.xlabel('time')
        plt.ylabel('prices')
        plt.xticks([set_index[0], set_index[-1]])
        plt.show()

    #############################################----SIMULATION----#####################################################

    print('the end')
