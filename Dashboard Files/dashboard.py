import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import QuantLib as ql

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from black_scholes_ver10 import AnalyticBlackScholes
from utilities import QuantLibConverter

import plotly.graph_objs as go
import pandas as pd
import os
import datetime

external_stylesheets = ['https://codepen.io/chridyp/pen/bWLgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

qlConverter = QuantLibConverter(calendar='United Kingdom')

o_black_scholes = AnalyticBlackScholes(valuation_date=datetime.datetime(2019, 11, 25),
                                       termination_date=datetime.datetime(2020, 2, 20),
                                       schedule_freq='Two Dates',
                                       convention='ActualActual',  # Daily,Monthly,Quarterly
                                       calendar=qlConverter.mqlCalendar,  # qlConverter.mqlCalendar,
                                       business_convention=qlConverter.mqlBusinessConvention,
                                       # qlConverter.mqlBusinessConvention,
                                       termination_business_convention=qlConverter.mqlTerminationBusinessConvention,
                                       # qlConverter.mqlTerminationBusinessConvention,
                                       date_generation=ql.DateGeneration.Forward,  # ql.DateGeneration.Forward,
                                       end_of_month=False,  # controlFile3m.loc[8, 'Value'],
                                       ##################################
                                       type_option='call',  # controlFile3m.loc[9, 'Value'],
                                       current_price=90,  # controlFile3m.loc[10, 'Value'],
                                       strike=92,  # controlFile3m.loc[11, 'Value'],
                                       ann_risk_free_rate=0.1,  # controlFile3m.loc[12, 'Value'],
                                       ann_volatility=0.23,  # controlFile3m.loc[13, 'Value'],
                                       ann_dividend=0)  # controlFile3m.loc[14, 'Value'])

print('tests of object')

app.layout = html.Div([dcc.Textarea(value='Pricing Plain Vanilla Option',
                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                           'background-color': 'yellow', 'border-style': 'dashed',
                                           'text-align': 'center'}),
                       html.Label('Place provide parameters'),
                       html.Br(),
                       dcc.DatePickerSingle(id='valuationDate', date=datetime.datetime(2019, 11, 25)),
                       dcc.DatePickerSingle(id='endDate', date=datetime.datetime(2020, 2, 20)),
                       html.Br(),
                       dcc.Input(id='schedule', placeholder='Define Schedule'),
                       html.Br(),
                       dcc.Dropdown(id='convention', placeholder='Chose Available Convention',
                                    options=[{'label': 'Actual Actual', 'value': 'ActualActual'},
                                             {'label': 'Actual360', 'value': 'Actual360'},
                                             {'label': 'Actual365', 'value': 'Actual365'},
                                             {'label': 'Thirty360', 'value': 'Thirty360'},
                                             {'label': 'Business252', 'value': 'Business252'}]),
                       dcc.Dropdown(id='calendar', placeholder='Put the name of Country',
                                    options=[{'label': 'UK', 'value': 'United Kingdom'},
                                             {'label': 'United States', 'value': 'USA'},
                                             {'label': 'Switzerland', 'value': 'Switzerland'},
                                             {'label': 'Poland', 'value': 'Poland'}
                                             ], value='United Kingdom'),

                       dcc.Input(id='Business Convention', placeholder='Define Business Convention', value='Following'),
                       dcc.Input(id='Termination Business Convention',
                                 placeholder='Define Termination Business Convention', value='Following'),
                       dcc.Input(id='endOfMonth', value='False'),
                       dcc.Dropdown(id='optiontype', options=[{'label': 'Call Option', 'value': 'call'}]),
                       html.Hr(),
                       dcc.Input(id='currentPrice', value='90', type='number', placeholder='Current Price'),
                       dcc.Input(id='strike', value='92', type='number', placeholder='Strike'),
                       dcc.Input(id='riskFree', value='0.1', type='number', placeholder='Risk Free Rate'),
                       dcc.Input(id='volatility', value='0.23', type='number', placeholder='Volatility'),
                       dcc.Input(id='dividend', value='0', type='number', placeholder='Dividend'),
                       ###################################----RESULT----###############################################
                       html.Div(id='optionPrice', children='')
                       ###################################----RESULT----###############################################
                       ])


@app.callback(
    Output('optionPrice', 'children'),
    [
        Input('valuationDate', 'date'),
        Input('endDate', 'date'),
        Input('schedule', 'value'),
        Input('convention', 'value'),
        Input('calendar', 'value'),
        Input('Business Convention', 'value'),
        Input('Termination Business Convention', 'value'),
        Input('endOfMonth', 'value'),
        Input('optiontype', 'value'),
        Input('currentPrice', 'value'),
        Input('strike', 'value'),
        Input('riskFree', 'value'),
        Input('volatility', 'value'),
        Input('dividend', 'value'),

    ])
def presentParameters(valuationDate, endDate, schedule, convention, calendar, BusinessConvention,
                      TerminationBusinessConvention,
                      endOfMonth, optiontype, currentPrice, strike, riskFree, volatility, dividend):
    print(valuationDate,
          endDate,
          schedule,
          convention,
          calendar,
          BusinessConvention,
          TerminationBusinessConvention,
          endOfMonth,
          optiontype,
          currentPrice,
          strike,
          riskFree,
          volatility,
          dividend,
          QuantLibConverter(calendar=calendar).mqlCalendar,
          QuantLibConverter(calendar=calendar).mqlBusinessConvention,
          )


# def optionPrice(valDate, endDate, schedule, convention, calendar, bussConv, TerminationBussConv, endMonth, optionType,
#                 currentPrice, strike, riskFree, volatility, dividend):
#     o_black_scholes = AnalyticBlackScholes(valuation_date=valDate,
#                                            termination_date=endDate,
#                                            schedule_freq=schedule,
#                                            convention=convention,  # Daily,Monthly,Quarterly
#                                            calendar=calendar,  # qlConverter.mqlCalendar,
#                                            business_convention=bussConv,  # qlConverter.mqlBusinessConvention,
#                                            termination_business_convention=TerminationBussConv,
#                                            # qlConverter.mqlTerminationBusinessConvention,
#                                            date_generation=ql.DateGeneration.Forward,  # ql.DateGeneration.Forward,
#                                            end_of_month=endMonth,  # controlFile3m.loc[8, 'Value'],
#                                            ##################################
#                                            type_option=optionType,  # controlFile3m.loc[9, 'Value'],
#                                            current_price=currentPrice,  # controlFile3m.loc[10, 'Value'],
#                                            strike=strike,  # controlFile3m.loc[11, 'Value'],
#                                            ann_risk_free_rate=riskFree,  # controlFile3m.loc[12, 'Value'],
#                                            ann_volatility=volatility,  # controlFile3m.loc[13, 'Value'],
#                                            ann_dividend=dividend,  # controlFile3m.loc[14, 'Value'])
#
#                                            )
#     price = o_black_scholes.black_scholes_price_fun()
#
#     return html.Div([html.H4(f'price of option {price}')])


if __name__ == '__main__':
    app.run_server(debug=True)
