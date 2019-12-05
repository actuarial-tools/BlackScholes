import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import QuantLib as ql

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from black_scholes_ver10 import AnalyticBlackScholes

import plotly.graph_objs as go
import pandas as pd
import os
import datetime

external_stylesheets = ['https://codepen.io/chridyp/pen/bWLgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([dcc.Textarea(value='Pricing Plain Vanilla Option',
                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                           'background-color': 'yellow', 'border-style': 'dashed',
                                           'text-align': 'center'}),
                       html.Label('Place provide parametrs'),
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
                       dcc.Input(id='calendar', placeholder='Put the name of Coiuntry'),
                       dcc.Input(id='Business Convention', placeholder='Define Business Convention', value='Following'),
                       dcc.Input(id=' Termination Business Convention',
                                 placeholder='Define Termination Business Convention', value='Following'),
                       dcc.Input(id='endOfMonth, value=False'),
                       dcc.Dropdown(id='optiontype', options=[{'label': 'Call Option', 'value': 'call'}]),
                       html.Hr(),
                       dcc.Input(id='currentPrice', value='', type='number', placeholder='Current Price'),
                       dcc.Input(id='strike', value='', type='number', placeholder='Strike'),
                       dcc.Input(id='riskFree', value='', type='number', placeholder='Risk Free Rate'),
                       dcc.Input(id='volatility', value='', type='number', placeholder='Volatility'),
                       dcc.Input(id='dividend', value='', type='number', placeholder='Dividend'),
                       ])


@app.callback(
    Output('optionPrice', 'children')
    [
        Input('valuationDate', 'value'),
        Input('endDate', 'value'),
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
def optionPrice(valDate, endDate, schedule, convention, calendar, bussConv, TerminationBussConv, endMonth, optionType,
                currentPrice, strike, riskFree, volatility, dividend):
    qlDate1 = ql.Date(valDate.day, valDate.month, valDate.year)
    qlDate2 = ql.Date(endDate.day, endDate.month, endDate.year)

    o_black_scholes_3m = AnalyticBlackScholes(valuation_date=valDate,
                                              termination_date=endDate,
                                              schedule_freq=schedule,
                                              convention=convention,  # Daily,Monthly,Quarterly
                                              calendar=calendar,  # qlConverter.mqlCalendar,
                                              business_convention=bussConv,  # qlConverter.mqlBusinessConvention,
                                              termination_business_convention=bussConv,
                                              # qlConverter.mqlTerminationBusinessConvention,
                                              date_generation=TerminationBussConv,  # ql.DateGeneration.Forward,
                                              end_of_month=endMonth,  # controlFile3m.loc[8, 'Value'],
                                              ##################################
                                              type_option=optionType,  # controlFile3m.loc[9, 'Value'],
                                              current_price=currentPrice,  # controlFile3m.loc[10, 'Value'],
                                              strike=strike,  # controlFile3m.loc[11, 'Value'],
                                              ann_risk_free_rate=riskFree,  # controlFile3m.loc[12, 'Value'],
                                              ann_volatility=volatility,  # controlFile3m.loc[13, 'Value'],
                                              ann_dividend=dividend,  # controlFile3m.loc[14, 'Value'])

                                              )


if __name__ == '__main__':
    app.run_server(debug=True)
