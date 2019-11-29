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

controlFileDynamic = dictionaryOfControlFile['Dynamic For Report']
controlFileScenarioGenerator = dictionaryOfControlFile['Scenario Generator']
controlFilePriceChange = dictionaryOfControlFile['Range']['Price']
controlFileVolChange = dictionaryOfControlFile['Range']['Volatility']

if __name__ == '__main__':
    qlConverter = QuantLibConverter(calendar=controlFileDynamic.loc[4, 'Value'])

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

    greekObjects = GreeksParameters(valuation_date=controlFileDynamic.loc[0, 'Value'],
                                    termination_date=controlFileDynamic.loc[1, 'Value'],
                                    schedule_freq=controlFileDynamic.loc[2, 'Value'],
                                    convention=controlFileDynamic.loc[3, 'Value'],  # Daily,Monthly,Quarterly
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
    optionPriceDynamic = [o_black_scholes_Dynamic.black_scholes_price_fun() for o_black_scholes_Dynamic._S0 in
                          prices_range]
    plt.figure(0)
    plt.plot(prices_range, optionPriceDynamic, label="6m to maturity")
    plt.scatter(controlFileDynamic.loc[10, 'Value'], o_black_scholes_Dynamic.mblprice[0], c='red')
    plt.xlabel("Spot Price")
    plt.ylabel("Option Price")
    plt.title("Relation price option to maturity")
    plt.legend()
    plt.savefig('OptionPrice.png')

    delta = [greekObjects.delta()[0] for greekObjects._S0 in prices_range]
    gamma = [greekObjects.gamma()[0] for greekObjects._S0 in prices_range]
    # theta = [greekObjects.theta() for greekObjects._S0 in prices_range]

    transposePricesRange = np.transpose(prices_range)

    greeks = pd.DataFrame([prices_range, delta, gamma])
    greeks = greeks.transpose()
    greeks = pd.DataFrame(greeks.values, columns=['Underlying Price', 'Delta', 'Gamma'])

    plt.figure(1)
    plt.plot(prices_range, delta, label="Delta")
    plt.xlabel("Spot Price")
    plt.ylabel("Delta")
    plt.title("Delta of Option")
    plt.legend()
    plt.savefig('Delta.png')


    ##########Delta

    def presentBlackScholesReport():
        controlPath = '/Users/krzysiekbienias/Downloads/ControlFiles'
        os.chdir(controlPath)
        writer = pd.ExcelWriter('BlackScholesReport5.xlsx', engine='xlsxwriter')
        workbook = writer.book
        worksheet = workbook.add_worksheet('Option Info')
        #####################################################
        cell_format = workbook.add_format()
        cell_format.set_bg_color('green')
        cell_format.set_bold()
        #####################################################
        worksheet.write('A1', 'Price of ' + o_black_scholes_Dynamic._type_option + ' Option', cell_format)

        worksheet.write('A2', o_black_scholes_Dynamic.mblprice[0])
        worksheet.insert_image('C5', 'OptionPrice.png')
        greeks.to_excel(writer, sheet_name='greeks')
        worksheet2 = writer.sheets['greeks']
        worksheet2.insert_image('G5', 'Delta.png')
        workbook.close()


    presentBlackScholesReport()
