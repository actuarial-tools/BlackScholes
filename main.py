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


if __name__ == '__main__':
    o_black_scholes_1y = AnalyticBlackScholes(valuation_date='2019-06-03',
                                              termination_date='2020-06-03',
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
                                              )

    o_black_scholes_3d = AnalyticBlackScholes(valuation_date='2019-06-03',
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

    b_draw_plots = False
    if b_draw_plots == True:
        plt.plot(prices_range,option_price1y, label="1y to maturity")
        plt.plot(prices_range,option_price3m,  label="3m to maturity")
        plt.plot(prices_range,option_price3d, label="3d to maturity")
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

    delta1y=[greeks_1y.delta_fun() for greeks_1y._S0 in  prices_range]
    delta3m=[greeks_3m.delta_fun() for greeks_3m._S0 in  prices_range]
    delta3d=[greeks_3d.delta_fun() for greeks_3d._S0 in  prices_range]




    b_delta_plots = False
    if b_delta_plots == True:
        plt.plot(prices_range, delta1y, label="1y to maturity")
        plt.plot(prices_range, delta3m, label="3m to maturity")
        plt.plot(prices_range, delta3d, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Delta")
        plt.title("Delta of Option")
        plt.legend()
        plt.show()

    #############################################----SIMULATION----#####################################################

    o_black_scholes_scenarios = EquityModels(valuation_date='2019-06-20',
                                        termination_date='2019-08-20',
                                        schedule_freq='Daily',
                                        convention='ActualActual',  # Daily,Monthly,Quarterly
                                        calendar=ql.Poland(),
                                        business_convention=ql.Following,
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

    gbmRealizations=o_black_scholes_scenarios.m_ar_equity_price

    set_index=list(map(lambda x: str(x),o_black_scholes_scenarios.ml_dates))




    df_scenarios = pd.DataFrame(gbmRealizations, index=set_index)

    for k in range(15):
        plt.plot(df_scenarios[k])
    plt.grid(True)
    plt.xlabel('time')
    plt.ylabel('prices')
    plt.xticks([set_index[0],set_index[-1]])
    plt.show()

    ##


    #############################################----SIMULATION----#####################################################

    print('the end')
