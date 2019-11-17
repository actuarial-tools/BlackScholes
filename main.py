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
from excelconnector import CreateDataFrame, OutputInExcel



controlPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
os.chdir(controlPath)

loadControlFile = CreateDataFrame(file_name='BlackScholes.xlsx')

dictionaryOfControlFile = loadControlFile.create_data_frame_from_excel()
controlFile1Y = dictionaryOfControlFile['Input 1Y']
controlFile3M = dictionaryOfControlFile['Input 3M']
controlFile3D = dictionaryOfControlFile['Input 3D']
controlFileScenarioGenerator = dictionaryOfControlFile['Input Scenario Generator']
controlFilePriceChange = dictionaryOfControlFile['Range For Equity Price Vol']['Price']
controlFileVolChange = dictionaryOfControlFile['Range For Equity Price Vol']['Volatility']


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

    o_black_scholes_3m = AnalyticBlackScholes(valuation_date=controlFile3M.loc[0, 'Value'],
                                              termination_date=controlFile3M.loc[1, 'Value'],
                                              schedule_freq=controlFile3M.loc[2, 'Value'],
                                              convention=controlFile3M.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                              calendar=qlConverter.mqlCalendar,
                                              business_convention=qlConverter.mqlBusinessConvention,
                                              termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                              date_generation=ql.DateGeneration.Forward,
                                              end_of_month=controlFile3M.loc[8, 'Value'],
                                              ##################################
                                              type_option=controlFile3M.loc[9, 'Value'],
                                              current_price=controlFile3M.loc[10, 'Value'],
                                              strike=controlFile3M.loc[11, 'Value'],
                                              ann_risk_free_rate=controlFile3M.loc[12, 'Value'],
                                              ann_volatility=controlFile3M.loc[13, 'Value'],
                                              ann_dividend=controlFile3M.loc[14, 'Value'])

    o_black_scholes_3d = AnalyticBlackScholes(valuation_date=controlFile3D.loc[0, 'Value'],
                                              termination_date=controlFile3D.loc[1, 'Value'],
                                              schedule_freq=controlFile3D.loc[2, 'Value'],
                                              convention=controlFile3D.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                              calendar=qlConverter.mqlCalendar,
                                              business_convention=qlConverter.mqlBusinessConvention,
                                              termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                              date_generation=ql.DateGeneration.Forward,
                                              end_of_month=controlFile3D.loc[8, 'Value'],
                                              ##################################
                                              type_option=controlFile3D.loc[9, 'Value'],
                                              current_price=controlFile3D.loc[10, 'Value'],
                                              strike=controlFile3D.loc[11, 'Value'],
                                              ann_risk_free_rate=controlFile3D.loc[12, 'Value'],
                                              ann_volatility=controlFile3D.loc[13, 'Value'],
                                              ann_dividend=controlFile3D.loc[14, 'Value'])

    prices_range = controlFilePriceChange.values
    vol_range = controlFileVolChange.values
    vol_range = vol_range[~np.isnan(vol_range)]


    option_price3d = [o_black_scholes_3d.black_scholes_price_fun() for o_black_scholes_3d._S0 in prices_range]
    change_vol3d = [o_black_scholes_3d.black_scholes_price_fun() for o_black_scholes_3d._sigma in vol_range]

    option_price1y = [o_black_scholes_1y.black_scholes_price_fun() for o_black_scholes_1y._S0 in prices_range]
    change_vol1y = [o_black_scholes_1y.black_scholes_price_fun() for o_black_scholes_1y._sigma in vol_range]

    option_price3m = [o_black_scholes_3m.black_scholes_price_fun() for o_black_scholes_3m._S0 in prices_range]
    change_vol3m = [o_black_scholes_3m.black_scholes_price_fun() for o_black_scholes_3m._sigma in vol_range]

    b_draw_plots = True
    if b_draw_plots == True:
        plt.plot(prices_range, option_price1y, label="1y to maturity")
        plt.plot(prices_range, option_price3m, label="3m to maturity")
        plt.plot(prices_range, option_price3d, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Option Price")
        plt.title("Relation price option to maturity")
        plt.legend()
        plt.savefig('OptionPrice.png')

    #############################################----GREEKS----#####################################################
    # GreeksParameters
    greeks_1y = GreeksParameters(valuation_date=controlFile1Y.loc[0, 'Value'],
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

    greeks_3m = GreeksParameters(valuation_date=controlFile1Y.loc[0, 'Value'],
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

    greeks_3d = GreeksParameters(valuation_date=controlFile1Y.loc[0, 'Value'],
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
    ##########Delta
    delta1y = [greeks_1y.delta() for greeks_1y._S0 in prices_range]
    delta3m = [greeks_3m.delta() for greeks_3m._S0 in prices_range]
    delta3d = [greeks_3d.delta() for greeks_3d._S0 in prices_range]

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

    b_theta_plots = False
    if b_theta_plots == True:
        plt.plot(prices_range, theta1y, label="1y to maturity")
        plt.plot(prices_range, theta3m, label="3m to maturity")
        plt.plot(prices_range, theta3d, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Theta")
        plt.title("Theta of Option")
        plt.legend()


    ########## Theta

    #############################################----SIMULATION----#####################################################

    o_black_scholes_scenarios = EquityModels(valuation_date=controlFileScenarioGenerator.loc[0, 'Value'],
                                             termination_date=controlFileScenarioGenerator.loc[1, 'Value'],
                                             schedule_freq=controlFileScenarioGenerator.loc[2, 'Value'],
                                             convention=controlFileScenarioGenerator.loc[3, 'Value'],
                                             # Daily,Monthly,Quarterly
                                             calendar=qlConverter.mqlCalendar,
                                             business_convention=qlConverter.mqlBusinessConvention,
                                             termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                             date_generation=ql.DateGeneration.Forward,
                                             end_of_month=controlFileScenarioGenerator.loc[8, 'Value'],
                                             ##################################
                                             type_option=controlFileScenarioGenerator.loc[9, 'Value'],
                                             current_price=controlFileScenarioGenerator.loc[10, 'Value'],
                                             strike=controlFileScenarioGenerator.loc[11, 'Value'],
                                             ann_risk_free_rate=controlFileScenarioGenerator.loc[12, 'Value'],
                                             ann_volatility=controlFileScenarioGenerator.loc[13, 'Value'],
                                             ann_dividend=controlFileScenarioGenerator.loc[14, 'Value'],
                                             runs=controlFileScenarioGenerator.loc[15, 'Value'])


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

    # o_black_scholes_scenarios.histogramOfSt()
    ####################################------OUTPUT in EXCEL------###############################################
    outputPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
    os.chdir(controlPath)
    ####################################------OUTPUT in EXCEL------###############################################
    excelPrepare = OutputInExcel(FileName='GBM realization.xlsx', SheetNames=['realizations'], Path=outputPath)

    # excelPrepare.createResultsToPresent(ldfToSave=o_black_scholes_scenarios.mdfprices)

    #############################################----SIMULATION----#####################################################

    print('the end')
