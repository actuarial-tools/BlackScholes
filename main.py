import sys

import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import stats
import operator
import QuantLib as ql
import os
import pandas as pd
import xlsxwriter

sys.path.append('../CalendarAlgorithm')
from calendar_ql_supported import SetUpSchedule


from black_scholes_ver10 import AnalyticBlackScholes
from greeks import GreeksParameters
from scenario_generator import EquityModels
from utilities import QuantLibConverter
from excelconnector import CreateDataFrame, OutputInExcel



controlPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
os.chdir(controlPath)

loadControlFile = CreateDataFrame(file_name='OptionPrice.xlsx')

dictionaryOfControlFile = loadControlFile.create_data_frame_from_excel()
controlFile3m = dictionaryOfControlFile['Input 3M']
controlFile6m = dictionaryOfControlFile['Input 6M']
controlFile10d = dictionaryOfControlFile['Input 10D']
controlFileDynamic = dictionaryOfControlFile['Dynamic For Report']
controlFileScenarioGenerator = dictionaryOfControlFile['Scenario Generator']
controlFilePriceChange = dictionaryOfControlFile['Range']['Price']
controlFileVolChange = dictionaryOfControlFile['Range']['Volatility']




if __name__ == '__main__':
    qlConverter = QuantLibConverter(calendar=controlFile3m.loc[4, 'Value'])

    o_black_scholes_3m = AnalyticBlackScholes(valuation_date=controlFile3m.loc[0, 'Value'],
                                              termination_date=controlFile3m.loc[1, 'Value'],
                                              schedule_freq=controlFile3m.loc[2, 'Value'],
                                              convention=controlFile3m.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                              calendar=qlConverter.mqlCalendar,
                                              business_convention=qlConverter.mqlBusinessConvention,
                                              termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                              date_generation=ql.DateGeneration.Forward,
                                              end_of_month=controlFile3m.loc[8, 'Value'],
                                              ##################################
                                              type_option=controlFile3m.loc[9, 'Value'],
                                              current_price=controlFile3m.loc[10, 'Value'],
                                              strike=controlFile3m.loc[11, 'Value'],
                                              ann_risk_free_rate=controlFile3m.loc[12, 'Value'],
                                              ann_volatility=controlFile3m.loc[13, 'Value'],
                                              ann_dividend=controlFile3m.loc[14, 'Value'])

    o_black_scholes_6m = AnalyticBlackScholes(valuation_date=controlFile6m.loc[0, 'Value'],
                                              termination_date=controlFile6m.loc[1, 'Value'],
                                              schedule_freq=controlFile6m.loc[2, 'Value'],
                                              convention=controlFile6m.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                              calendar=qlConverter.mqlCalendar,
                                              business_convention=qlConverter.mqlBusinessConvention,
                                              termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                              date_generation=ql.DateGeneration.Forward,
                                              end_of_month=controlFile6m.loc[8, 'Value'],
                                              ##################################
                                              type_option=controlFile6m.loc[9, 'Value'],
                                              current_price=controlFile6m.loc[10, 'Value'],
                                              strike=controlFile6m.loc[11, 'Value'],
                                              ann_risk_free_rate=controlFile6m.loc[12, 'Value'],
                                              ann_volatility=controlFile6m.loc[13, 'Value'],
                                              ann_dividend=controlFile6m.loc[14, 'Value'])

    o_black_scholes_10d = AnalyticBlackScholes(valuation_date=controlFile10d.loc[0, 'Value'],
                                               termination_date=controlFile10d.loc[1, 'Value'],
                                               schedule_freq=controlFile10d.loc[2, 'Value'],
                                               convention=controlFile10d.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                               calendar=qlConverter.mqlCalendar,
                                               business_convention=qlConverter.mqlBusinessConvention,
                                               termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                               date_generation=ql.DateGeneration.Forward,
                                               end_of_month=controlFile10d.loc[8, 'Value'],
                                               ##################################
                                               type_option=controlFile10d.loc[9, 'Value'],
                                               current_price=controlFile10d.loc[10, 'Value'],
                                               strike=controlFile10d.loc[11, 'Value'],
                                               ann_risk_free_rate=controlFile10d.loc[12, 'Value'],
                                               ann_volatility=controlFile10d.loc[13, 'Value'],
                                               ann_dividend=controlFile10d.loc[14, 'Value'])

    o_black_scholes_Dynamic = AnalyticBlackScholes(valuation_date=controlFileDynamic.loc[0, 'Value'],
                                                   termination_date=controlFileDynamic.loc[1, 'Value'],
                                                   schedule_freq=controlFileDynamic.loc[2, 'Value'],
                                                   convention=controlFileDynamic.loc[3, 'Value'],
                                                   # Daily,Monthly,Quarterly
                                                   calendar=qlConverter.mqlCalendar,
                                                   business_convention=qlConverter.mqlBusinessConvention,
                                                   termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                                   date_generation=ql.DateGeneration.Forward,
                                                   end_of_month=controlFileDynamic.loc[8, 'Value'],
                                                   ##################################
                                                   type_option=controlFileDynamic.loc[9, 'Value'],
                                                   current_price=controlFileDynamic.loc[10, 'Value'],
                                                   strike=controlFileDynamic.loc[11, 'Value'],
                                                   ann_risk_free_rate=controlFileDynamic.loc[12, 'Value'],
                                                   ann_volatility=controlFileDynamic.loc[13, 'Value'],
                                                   ann_dividend=controlFileDynamic.loc[14, 'Value'])



    prices_range = controlFilePriceChange.values
    vol_range = controlFileVolChange.values
    vol_range = vol_range[~np.isnan(vol_range)]

    option_price10d = [o_black_scholes_10d.black_scholes_price_fun() for o_black_scholes_10d._S0 in prices_range]
    change_vol10d = [o_black_scholes_10d.black_scholes_price_fun() for o_black_scholes_10d._sigma in vol_range]

    option_price6m = [o_black_scholes_6m.black_scholes_price_fun() for o_black_scholes_6m._S0 in prices_range]
    change_vol6m = [o_black_scholes_6m.black_scholes_price_fun() for o_black_scholes_6m._sigma in vol_range]

    option_price3m = [o_black_scholes_3m.black_scholes_price_fun() for o_black_scholes_3m._S0 in prices_range]
    change_vol3m = [o_black_scholes_3m.black_scholes_price_fun() for o_black_scholes_3m._sigma in vol_range]

    optionPriceDynamic = [o_black_scholes_Dynamic.black_scholes_price_fun() for o_black_scholes_Dynamic._S0 in
                          prices_range]


    # Create Data Frame that represents price change
    transposePricesRange = np.transpose(prices_range)
    columns = ['Underlying price', 'Option Price 10D maturity', 'Option Price 3M maturity', 'Option Price 6Y maturity']
    dfPriceChange = pd.DataFrame([prices_range, option_price10d, option_price3m, option_price6m])
    dfPriceChange = dfPriceChange.transpose()
    # dfPriceChange = pd.DataFrame([dfPriceChange.values], columns=columns)

    # https://towardsdatascience.com/writing-to-excel-with-python-micropython-42cf9541c101
    b_draw_plots = False
    if b_draw_plots == True:
        plt.plot(prices_range, option_price6m, label="6m to maturity")
        plt.plot(prices_range, option_price3m, label="3m to maturity")
        plt.plot(prices_range, option_price10d, label="10d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Option Price")
        plt.title("Relation price option to maturity")
        plt.legend()
        plt.savefig('OptionPrice.png')

    #############################################----GREEKS----#####################################################
    # GreeksParameters
    greeks_3m = GreeksParameters(valuation_date=controlFile3m.loc[0, 'Value'],
                                 termination_date=controlFile3m.loc[1, 'Value'],
                                 schedule_freq=controlFile3m.loc[2, 'Value'],
                                 convention=controlFile3m.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                 calendar=qlConverter.mqlCalendar,
                                 business_convention=qlConverter.mqlBusinessConvention,
                                 termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                 date_generation=ql.DateGeneration.Forward,
                                 end_of_month=controlFile3m.loc[8, 'Value'],
                                 ##################################
                                 type_option=controlFile3m.loc[9, 'Value'],
                                 current_price=controlFile3m.loc[10, 'Value'],
                                 strike=controlFile3m.loc[11, 'Value'],
                                 ann_risk_free_rate=controlFile3m.loc[12, 'Value'],
                                 ann_volatility=controlFile3m.loc[13, 'Value'],
                                 ann_dividend=controlFile3m.loc[14, 'Value'])

    greeks_6m = GreeksParameters(valuation_date=controlFile6m.loc[0, 'Value'],
                                 termination_date=controlFile6m.loc[1, 'Value'],
                                 schedule_freq=controlFile6m.loc[2, 'Value'],
                                 convention=controlFile6m.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                 calendar=qlConverter.mqlCalendar,
                                 business_convention=qlConverter.mqlBusinessConvention,
                                 termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                 date_generation=ql.DateGeneration.Forward,
                                 end_of_month=controlFile6m.loc[8, 'Value'],
                                 ##################################
                                 type_option=controlFile6m.loc[9, 'Value'],
                                 current_price=controlFile6m.loc[10, 'Value'],
                                 strike=controlFile6m.loc[11, 'Value'],
                                 ann_risk_free_rate=controlFile6m.loc[12, 'Value'],
                                 ann_volatility=controlFile6m.loc[13, 'Value'],
                                 ann_dividend=controlFile6m.loc[14, 'Value'])

    greeks_10d = GreeksParameters(valuation_date=controlFile10d.loc[0, 'Value'],
                                  termination_date=controlFile10d.loc[1, 'Value'],
                                  schedule_freq=controlFile10d.loc[2, 'Value'],
                                  convention=controlFile10d.loc[3, 'Value'],  # Daily,Monthly,Quarterly
                                  calendar=qlConverter.mqlCalendar,
                                  business_convention=qlConverter.mqlBusinessConvention,
                                  termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                  date_generation=ql.DateGeneration.Forward,
                                  end_of_month=controlFile10d.loc[8, 'Value'],
                                  ##################################
                                  type_option=controlFile10d.loc[9, 'Value'],
                                  current_price=controlFile10d.loc[10, 'Value'],
                                  strike=controlFile10d.loc[11, 'Value'],
                                  ann_risk_free_rate=controlFile10d.loc[12, 'Value'],
                                  ann_volatility=controlFile10d.loc[13, 'Value'],
                                  ann_dividend=controlFile10d.loc[14, 'Value'])
    ##########Delta
    delta6m = [greeks_6m.delta() for greeks_6m._S0 in prices_range]
    delta3m = [greeks_3m.delta() for greeks_3m._S0 in prices_range]
    delta10 = [greeks_10d.delta() for greeks_10d._S0 in prices_range]

    b_delta_plots = False
    if b_delta_plots == True:
        plt.plot(prices_range, delta6m, label="6m to maturity")
        plt.plot(prices_range, delta3m, label="3m to maturity")
        plt.plot(prices_range, delta10, label="10d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Delta")
        plt.title("Delta of Option")
        plt.legend()
        plt.savefig('Delta.png')
    ##########Delta

    ##########Gamma

    gamma6m = [greeks_3m.gamma() for greeks_3m._S0 in prices_range]
    gamma3m = [greeks_6m.gamma() for greeks_6m._S0 in prices_range]
    gamma10D = [greeks_10d.gamma() for greeks_10d._S0 in prices_range]

    b_gamma_plots = False
    if b_gamma_plots == True:
        plt.plot(prices_range, gamma6m, label="1y to maturity")
        plt.plot(prices_range, gamma3m, label="3m to maturity")
        plt.plot(prices_range, gamma10D, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Gamma")
        plt.title("Gamma of Option")
        plt.legend()
        plt.savefig('Gamma.png')
    ##########Gamma

    ########## Theta

    theta6m = [greeks_6m.theta() for greeks_6m._S0 in prices_range]
    theta3m = [greeks_3m.theta() for greeks_3m._S0 in prices_range]
    theta10D = [greeks_10d.theta() for greeks_10d._S0 in prices_range]

    b_theta_plots = False
    if b_theta_plots == True:
        plt.plot(prices_range, theta6m, label="1y to maturity")
        plt.plot(prices_range, theta3m, label="3m to maturity")
        plt.plot(prices_range, theta10D, label="3d to maturity")
        plt.xlabel("Spot Price")
        plt.ylabel("Theta")
        plt.title("Theta of Option")
        plt.legend()
        plt.savefig('Theta.png')


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
        plt.savefig('Equity Paths.png')

    # o_black_scholes_scenarios.histogramOfSt()
    # ####################################------OUTPUT in EXCEL------###############################################
    # outputPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
    # os.chdir(controlPath)
    def presentBlackScholesReport():
        controlPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
        os.chdir(controlPath)
        workbook = xlsxwriter.Workbook('BlackScholesReport1.xlsx')
        worksheet = workbook.add_worksheet('Option Info')
        worksheet.write('A1', 'Price of ' + o_black_scholes_Dynamic._type_option + ' Option')
        worksheet.write('A2', o_black_scholes_Dynamic.mblprice[0])
        worksheetPrice = workbook.add_worksheet('')

        workbook.close()


    presentBlackScholesReport()
    ####################################------OUTPUT in EXCEL------###############################################

    #excelPrepare.loadWorkbook(cellLocation='D2',value=o_black_scholes_1y.mblprice[0])

    # excelPrepare.createResultsToPresent(ldfToSave=o_black_scholes_scenarios.mdfprices)

    #############################################----SIMULATION----#####################################################

    print('the end')
