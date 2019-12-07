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


app.layout = html.Div([dcc.Textarea(value='Pricing Plain Vanilla Option',
                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                           'background-color': 'yellow', 'border-style': 'dashed',
                                           'text-align': 'center'}),
                       html.Label('Place provide the date for which you would like to price the contract'),
                       html.Br(),
                       dcc.DatePickerSingle(id='valuationDate', date=datetime.datetime(2019, 11, 25),
                                            display_format='YYYY-MM-DD'),
                       html.Label('Place provide the termination the contract.'),
                       html.Br(),
                       dcc.DatePickerSingle(id='endDate', date=datetime.datetime(2020, 2, 20),
                                            display_format='YYYY-MM-DD'),
                       html.Br(),
                       dcc.Input(id='schedule', placeholder='Define Schedule', value='Two Dates'),
                       html.Br(),
                       dcc.Dropdown(id='convention', placeholder='Chose Available Convention',
                                    options=[{'label': 'Actual Actual', 'value': 'ActualActual'},
                                             {'label': 'Actual360', 'value': 'Actual360'},
                                             {'label': 'Actual365', 'value': 'Actual365'},
                                             {'label': 'Thirty360', 'value': 'Thirty360'},
                                             {'label': 'Business252', 'value': 'Business252'}], value='ActualActual'),
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
                       dcc.Dropdown(id='optiontype', options=[{'label': 'Call Option', 'value': 'call'},
                                                              {'label': 'Put Option', 'value': 'put'}], value='call'),
                       html.Hr(),
                       dcc.Input(id='currentPrice', value=90, type='number', placeholder='Current Price'),
                       dcc.Input(id='strike', value=92, type='number', placeholder='Strike'),
                       dcc.Input(id='riskFree', value=0.1, type='number', placeholder='Risk Free Rate'),
                       dcc.Input(id='volatility', value=0.23, type='number', placeholder='Volatility'),
                       dcc.Input(id='dividend', value=0, type='number', placeholder='Dividend'),
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
        Input('optiontype', 'value'),
        Input('currentPrice', 'value'),
        Input('strike', 'value'),
        Input('riskFree', 'value'),
        Input('volatility', 'value'),
        Input('dividend', 'value'),

    ])
# def printInputs(valDate,endDate,schedule,convention,calendar,optionType,currentPrice,strike,riskFree,volatility,dividend):
#     print( valDate,\
#            endDate,\
#            schedule,\
#            convention,\
#            calendar,\
#            optionType,\
#            currentPrice,\
#            strike,\
#            riskFree,\
#            volatility,\
#            dividend)

def optionPrice(valDate, endDate, schedule, convention, calendar, optionType,
                currentPrice, strike, riskFree, volatility, dividend):
    o_black_scholes = AnalyticBlackScholes(valuation_date=valDate,
                                           termination_date=endDate,
                                           schedule_freq=schedule,
                                           convention=convention,
                                           calendar=QuantLibConverter(calendar=calendar).mqlCalendar,
                                           business_convention=QuantLibConverter(
                                               calendar=calendar).mqlBusinessConvention,
                                           termination_business_convention=QuantLibConverter(
                                               calendar=calendar).mqlTerminationBusinessConvention,
                                           date_generation=QuantLibConverter(calendar=calendar).mqlDateGeneration,
                                           end_of_month=False,
                                           ##################################
                                           type_option=optionType,
                                           current_price=currentPrice,
                                           strike=strike,
                                           ann_risk_free_rate=riskFree,
                                           ann_volatility=volatility,
                                           ann_dividend=dividend)
    price = round(o_black_scholes.black_scholes_price_fun()[0], 3)
    year_fraction = round(o_black_scholes.mf_yf_between_valu_date_and_maturity, 3)

    return html.Div([html.H4(f'Annuity for this contract  {year_fraction}'),
                     html.Hr(),
                     dcc.Textarea(value=f'Analytical price of option {price}',
                                  style={'width': '100%', 'color': 'red', 'fontSize': 18,
                                         'background-color': 'blue', 'border-style': 'dashed',
                                         'text-align': 'center'})

                     ])


if __name__ == '__main__':
    app.run_server(debug=True)
