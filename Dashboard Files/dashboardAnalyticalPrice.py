import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import QuantLib as ql

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from black_scholes_ver10 import AnalyticBlackScholes
from scenario_generator import EquityModels
from greeks import GreeksParameters
from utilities import QuantLibConverter

import plotly.graph_objs as go
import pandas as pd
import os
import datetime

external_stylesheets = ['https://codepen.io/chridyp/pen/bWLgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([dcc.Textarea(value='Black Scholes World',
                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                           'background-color': 'yellow', 'border-style': 'dashed',
                                           'text-align': 'center'}),
                       dcc.Tabs(children=[
                           # tab 1
                           dcc.Tab(label='Analytical Price', style={'background-color': 'blue'},
                                   children=[html.Label(
                                       'Place provide the date for which you would like to price the contract'),
                                       html.Br(),
                                       dcc.DatePickerSingle(id='valuationDateAnalitical',
                                                            date=datetime.datetime(2019, 11, 25),
                                                            display_format='YYYY-MM-DD'),
                                       html.Hr(),
                                       html.Label('Place provide the termination the contract.'),
                                       html.Hr(),
                                       dcc.DatePickerSingle(id='endDateAnalitical',
                                                            date=datetime.datetime(2020, 2, 20),
                                                            display_format='YYYY-MM-DD'),
                                       html.Br(),
                                       dcc.Input(id='scheduleAnalitical', placeholder='Define Schedule',
                                                 value='Two Dates'),
                                       html.Hr(),
                                       dcc.Dropdown(id='conventionAnalitical',
                                                    placeholder='Chose Available Convention',
                                                    options=[{'label': 'Actual Actual', 'value': 'ActualActual'},
                                                             {'label': 'Actual360', 'value': 'Actual360'},
                                                             {'label': 'Actual365', 'value': 'Actual365'},
                                                             {'label': 'Thirty360', 'value': 'Thirty360'},
                                                             {'label': 'Business252', 'value': 'Business252'}],
                                                    value='ActualActual'),
                                       dcc.Dropdown(id='calendarAnalitical',
                                                    placeholder='Put the name of Country',
                                                    options=[{'label': 'UK', 'value': 'United Kingdom'},
                                                             {'label': 'United States', 'value': 'USA'},
                                                             {'label': 'Switzerland', 'value': 'Switzerland'},
                                                             {'label': 'Poland', 'value': 'Poland'}
                                                             ], value='United Kingdom'),

                                       dcc.Input(id='BusinessConventionAnalitical',
                                                 placeholder='Define Business Convention', value='Following'),
                                       dcc.Input(id='Termination Business ConventionAnalitical',
                                                 placeholder='Define Termination Business Convention',
                                                 value='Following'),
                                       dcc.Input(id='endOfMonthAnalitical', value='False'),
                                       dcc.Dropdown(id='optiontypeAnalitical',
                                                    options=[{'label': 'Call Option', 'value': 'call'},
                                                             {'label': 'Put Option', 'value': 'put'}],
                                                    value='call'),
                                       html.Hr(),
                                       dcc.Input(id='currentPriceAnalitical', value=90, type='number',
                                                 placeholder='Current Price'),
                                       dcc.Input(id='strikeAnalitical', value=92, type='number',
                                                 placeholder='Strike'),
                                       dcc.Input(id='riskFreeAnalitical', value=0.1, type='number',
                                                 placeholder='Risk Free Rate'),
                                       dcc.Input(id='volatilityAnalitical', value=0.23, type='number',
                                                 placeholder='Volatility'),
                                       dcc.Input(id='dividendAnalitical', value=0, type='number',
                                                 placeholder='Dividend'),
                                       html.Hr(),
                                       html.Button('Press to get year fraction', id='yearFractionButton',
                                                   style={'background-color': 'orange', 'fontSize': 20}),
                                       html.Hr(),
                                       ###################################----RESULT YEAR FRACTION----###############################################
                                       html.Div(id='yearFraction'),
                                       ###################################----RESULT YEAR FRACTION----###############################################
                                       html.Button('Press to get analytical price', id='AnalyticalPrice',
                                                   style={'background-color': 'red', 'fontSize': 20}),
                                       ###################################----RESULT OPTION PRICE----###############################################
                                       html.Div(id='optionPriceAnalitical', children=''),
                                       ###################################----RESULT OPTION PRICE----###############################################

                                       ###################################----DYNAMIC OPTION PRICE----###############################################
                                       html.Hr(),
                                       dcc.Textarea(value='PRICE BEHAVIOUR',
                                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                                           'background-color': 'brown', 'border-style': 'dashed',
                                                           'text-align': 'center'}),
                                       html.Hr(),
                                       html.Label('Slider for underlying price'),
                                       dcc.RangeSlider(id='priceSliderAnalytical', min=50, max=130),
                                       html.Button('Press to check dynamic with respect to UNDERLYING PRICE.',
                                                   id='AnalyticalUnderlyingPriceButton',
                                                   style={'background-color': 'red', 'fontSize': 20}),
                                       html.Div(id='optionDynamicWRTPrice'),
                                       html.Hr(),
                                       html.Label('Slider for Strike'),
                                       dcc.RangeSlider(id='strikeSliderAnalytical', min=50, max=130),
                                       html.Button('Press to check dynamic with respect to STRIKE.',
                                                   id='AnalyticalStrikeButton',
                                                   style={'background-color': 'red', 'fontSize': 20}),
                                       html.Div(id='optionDynamicWRTStrike'),

                                       html.Hr(),
                                       html.Label('Slider for Volatility'),
                                       dcc.RangeSlider(id='sliderVolatilityAnalytic', min=0, max=1, step=0.05,
                                                       value=[0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                                                              0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95],
                                                       marks={i: f'{i}' for i in
                                                              [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
                                                               0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1]}),

                                       html.Hr(),
                                       html.Div(id='optionDynamicWRTSigma'),

                                   ]

                                   ),
                           ###################################----DYNAMIC OPTION PRICE----###############################################
                           # tab 2
                           dcc.Tab(label='Monte Carlo Price', style={'background-color': 'green'},
                                   children=[html.Div([
                                       html.Br(),
                                       dcc.DatePickerSingle(id='valuationDateMc', date=datetime.datetime(2019, 11, 25),
                                                            display_format='YYYY-MM-DD'),
                                       html.Br(),
                                       html.Label('Place provide the end of modeling.'),
                                       html.Br(),
                                       dcc.DatePickerSingle(id='endDateMc', date=datetime.datetime(2020, 2, 20),
                                                            display_format='YYYY-MM-DD'),
                                       html.Br(),
                                       dcc.Dropdown(id='scheduleMc', style={'background-color': 'orange'},
                                                    placeholder='Define Schedule',
                                                    value='Daily',
                                                    options=[{'label': 'Two Dates', 'value': 'Two Dates'},
                                                             {'label': 'Daily', 'value': 'Daily'},
                                                             {'label': 'Weekly', 'value': 'Weekly'},
                                                             {'label': 'Monthly', 'value': 'Monthly'},
                                                             {'label': 'Quarterly', 'value': 'Quarterly'},
                                                             {'label': 'Semiannual', 'value': 'Semiannual'},
                                                             {'label': 'Annual', 'value': 'Annual'},

                                                             ]),
                                       html.Br(),
                                       dcc.Dropdown(id='conventionMc', style={'background-color': 'purple'},
                                                    placeholder='Chose Available Convention',
                                                    options=[{'label': 'Actual Actual', 'value': 'ActualActual'},
                                                             {'label': 'Actual360', 'value': 'Actual360'},
                                                             {'label': 'Actual365', 'value': 'Actual365'},
                                                             {'label': 'Thirty360', 'value': 'Thirty360'},
                                                             {'label': 'Business252', 'value': 'Business252'}],
                                                    value='ActualActual'),
                                       dcc.Dropdown(id='calendarMc', placeholder='Put the name of Country',
                                                    options=[{'label': 'UK', 'value': 'United Kingdom'},
                                                             {'label': 'United States', 'value': 'USA'},
                                                             {'label': 'Switzerland', 'value': 'Switzerland'},
                                                             {'label': 'Poland', 'value': 'Poland'}
                                                             ], value='United Kingdom'),

                                       dcc.Input(id='Business ConventionMc', placeholder='Define Business Convention',
                                                 value='Following'),
                                       dcc.Input(id='Termination Business ConventionMc',
                                                 placeholder='Define Termination Business Convention',
                                                 value='Following'),
                                       dcc.Input(id='endOfMonthMc', value='False'),
                                       html.Br(),
                                       html.Label('Place provide the parameters for option'),
                                       dcc.Dropdown(id='optiontypeMc',
                                                    options=[{'label': 'Call Option', 'value': 'call'},
                                                             {'label': 'Put Option', 'value': 'put'}],
                                                    value='call'),
                                       html.Hr(),
                                       dcc.Input(id='currentPriceMc', value=90, type='number',
                                                 placeholder='Current Price'),
                                       dcc.Input(id='strikeMc', value=92, type='number', placeholder='Strike'),
                                       dcc.Input(id='riskFreeMc', value=0.1, type='number',
                                                 placeholder='Risk Free Rate'),
                                       dcc.Input(id='volatilityMc', value=0.23, type='number',
                                                 placeholder='Volatility'),
                                       dcc.Input(id='dividendMc', value=0, type='number', placeholder='Dividend'),
                                       html.Hr(),
                                       html.Label('Place provide the parameters for running simulation'),
                                       html.Br(),
                                       dcc.RadioItems(id='sampleMc',
                                                      options=[{'label': '1000', 'value': 1000},
                                                               {'label': '10000', 'value': 10000},
                                                               {'label': '100000', 'value': 100000}], value=1000),
                                       dcc.RadioItems(id='numberOfPathToDisplayMc',
                                                      options=[{'label': '10', 'value': 10},
                                                               {'label': '15', 'value': 15},
                                                               {'label': '25', 'value': 25},
                                                               {'label': '50', 'value': 50}],
                                                      value=15),
                                       # html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                       # style={'text-align': 'center'}),
                                       html.Button('Press to get monte carlo price.', id='monteCarloButton',
                                                   style={'background-color': 'orange', 'fontSize': 20}),
                                       html.Hr(),
                                       ###################################----RESULT----###############################################
                                       html.Div(id='MonteCarloPriceMc', children=''),
                                       html.Button('Press to display paths.', id='DisplayPathButton',
                                                   style={'background-color': 'orange', 'fontSize': 20}),
                                       html.Div(id='graph')

                                   ]
                                   )]),
                           # tab 3
                           dcc.Tab(label='Sensitivity Analysis', style={'background-color': 'pink'},
                                   # short
                                   children=[html.Div([
                                       html.Label('Short Term Contract',
                                                  style={'color': 'red', 'text-align': 'center'}),
                                       html.Br(),
                                       dcc.DatePickerSingle(id='valuationDateShort',
                                                            date=datetime.datetime(2019, 11, 25),
                                                            display_format='YYYY-MM-DD'),
                                       html.Br(),
                                       html.Label('Place provide the end of modeling.'),
                                       html.Br(),
                                       dcc.DatePickerSingle(id='endDateShort', date=datetime.datetime(2019, 12, 5),
                                                            display_format='YYYY-MM-DD'),
                                       html.Br(),
                                       dcc.Dropdown(id='scheduleShort', style={'background-color': 'orange'},
                                                    placeholder='Define Schedule',
                                                    value='Two Dates',
                                                    options=[{'label': 'Two Dates', 'value': 'Two Dates'},
                                                             {'label': 'Daily', 'value': 'Daily'},
                                                             {'label': 'Weekly', 'value': 'Weekly'},
                                                             {'label': 'Monthly', 'value': 'Monthly'},
                                                             {'label': 'Quarterly', 'value': 'Quarterly'},
                                                             {'label': 'Semiannual', 'value': 'Semiannual'},
                                                             {'label': 'Annual', 'value': 'Annual'},

                                                             ]),
                                       html.Br(),
                                       dcc.Dropdown(id='conventionShort', style={'background-color': 'purple'},
                                                    placeholder='Chose Available Convention',
                                                    options=[{'label': 'Actual Actual', 'value': 'ActualActual'},
                                                             {'label': 'Actual360', 'value': 'Actual360'},
                                                             {'label': 'Actual365', 'value': 'Actual365'},
                                                             {'label': 'Thirty360', 'value': 'Thirty360'},
                                                             {'label': 'Business252', 'value': 'Business252'}],
                                                    value='ActualActual'),
                                       dcc.Dropdown(id='calendarShort', placeholder='Put the name of Country',
                                                    options=[{'label': 'UK', 'value': 'United Kingdom'},
                                                             {'label': 'United States', 'value': 'USA'},
                                                             {'label': 'Switzerland', 'value': 'Switzerland'},
                                                             {'label': 'Poland', 'value': 'Poland'}
                                                             ], value='United Kingdom'),

                                       dcc.Input(id='Business ConventionShort',
                                                 placeholder='Define Business Convention',
                                                 value='Following'),
                                       dcc.Input(id='Termination Business ConventionShort',
                                                 placeholder='Define Termination Business Convention',
                                                 value='Following'),
                                       dcc.Input(id='endOfMonthShort', value='False'),
                                       html.Br(),
                                       html.Label('Place provide the parameters for option'),
                                       dcc.Dropdown(id='optionTypeShort',
                                                    options=[{'label': 'Call Option', 'value': 'call'},
                                                             {'label': 'Put Option', 'value': 'put'}],
                                                    value='call'),
                                       html.Hr(),
                                       dcc.Input(id='currentPriceShort', value=90, type='number',
                                                 placeholder='Current Price'),
                                       dcc.Input(id='strikeShort', value=92, type='number', placeholder='Strike'),
                                       dcc.Input(id='riskFreeShort', value=0.1, type='number',
                                                 placeholder='Risk Free Rate'),
                                       dcc.Input(id='volatilityShort', value=0.23, type='number',
                                                 placeholder='Volatility'),
                                       dcc.Input(id='dividendShort', value=0, type='number', placeholder='Dividend'),
                                       html.Div(id='shortGreeks'),

                                       # html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                       # style={'text-align': 'center'}),

                                       html.Hr(),

                                   ]),
                                       # medium
                                       html.Div([
                                           html.Label('Medium Term Contract',
                                                      style={'color': 'red', 'text-align': 'center'}),
                                           html.Br(),
                                           dcc.DatePickerSingle(id='valuationDateMedium',
                                                                date=datetime.datetime(2019, 11, 25),
                                                                display_format='YYYY-MM-DD'),
                                           html.Br(),
                                           html.Label('Place provide the end of modeling.'),
                                           html.Br(),
                                           dcc.DatePickerSingle(id='endDateMedium',
                                                                date=datetime.datetime(2020, 2, 20),
                                                                display_format='YYYY-MM-DD'),
                                           html.Br(),
                                           dcc.Dropdown(id='scheduleMedium', style={'background-color': 'orange'},
                                                        placeholder='Define Schedule',
                                                        value='Two Dates',
                                                        options=[{'label': 'Two Dates', 'value': 'Two Dates'},
                                                                 {'label': 'Daily', 'value': 'Daily'},
                                                                 {'label': 'Weekly', 'value': 'Weekly'},
                                                                 {'label': 'Monthly', 'value': 'Monthly'},
                                                                 {'label': 'Quarterly', 'value': 'Quarterly'},
                                                                 {'label': 'Semiannual', 'value': 'Semiannual'},
                                                                 {'label': 'Annual', 'value': 'Annual'},

                                                                 ]),
                                           html.Br(),
                                           dcc.Dropdown(id='conventionMedium',
                                                        style={'background-color': 'purple'},
                                                        placeholder='Chose Available Convention',
                                                        options=[{'label': 'Actual Actual', 'value': 'ActualActual'},
                                                                 {'label': 'Actual360', 'value': 'Actual360'},
                                                                 {'label': 'Actual365', 'value': 'Actual365'},
                                                                 {'label': 'Thirty360', 'value': 'Thirty360'},
                                                                 {'label': 'Business252', 'value': 'Business252'}],
                                                        value='ActualActual'),
                                           dcc.Dropdown(id='calendarMedium', placeholder='Put the name of Country',
                                                        options=[{'label': 'UK', 'value': 'United Kingdom'},
                                                                 {'label': 'United States', 'value': 'USA'},
                                                                 {'label': 'Switzerland', 'value': 'Switzerland'},
                                                                 {'label': 'Poland', 'value': 'Poland'}
                                                                 ], value='United Kingdom'),

                                           dcc.Input(id='Business ConventionMedium',
                                                     placeholder='Define Business Convention',
                                                     value='Following'),
                                           dcc.Input(id='Termination Business ConventionMedium',
                                                     placeholder='Define Termination Business Convention',
                                                     value='Following'),
                                           dcc.Input(id='endOfMonthMedium', value='False'),
                                           html.Br(),
                                           html.Label('Place provide the parameters for option'),
                                           dcc.Dropdown(id='optionTypeMedium',
                                                        options=[{'label': 'Call Option', 'value': 'call'},
                                                                 {'label': 'Put Option', 'value': 'put'}],
                                                        value='call'),
                                           html.Hr(),
                                           dcc.Input(id='currentPriceMedium', value=90, type='number',
                                                     placeholder='Current Price'),
                                           dcc.Input(id='strikeMedium', value=92, type='number', placeholder='Strike'),
                                           dcc.Input(id='riskFreeMedium', value=0.1, type='number',
                                                     placeholder='Risk Free Rate'),
                                           dcc.Input(id='volatilityMedium', value=0.23, type='number',
                                                     placeholder='Volatility'),
                                           dcc.Input(id='dividendMedium', value=0, type='number',
                                                     placeholder='Dividend'),
                                           html.Div(id='deltaMedium'),

                                           # html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                           # style={'text-align': 'center'}),

                                           html.Hr(),

                                       ]),
                                       # LONG
                                       html.Div([
                                           html.Label('Long Term Contract',
                                                      style={'color': 'red', 'text-align': 'center'}),
                                           html.Br(),
                                           dcc.DatePickerSingle(id='valuationDateLong',
                                                                date=datetime.datetime(2019, 11, 25),
                                                                display_format='YYYY-MM-DD'),
                                           html.Br(),
                                           html.Label('Place provide the end of modeling.'),
                                           html.Br(),
                                           dcc.DatePickerSingle(id='endDateShortLong',
                                                                date=datetime.datetime(2020, 11, 25),
                                                                display_format='YYYY-MM-DD'),
                                           html.Br(),
                                           dcc.Dropdown(id='scheduletLong', style={'background-color': 'orange'},
                                                        placeholder='Define Schedule',
                                                        value='Two Dates',
                                                        options=[{'label': 'Two Dates', 'value': 'Two Dates'},
                                                                 {'label': 'Daily', 'value': 'Daily'},
                                                                 {'label': 'Weekly', 'value': 'Weekly'},
                                                                 {'label': 'Monthly', 'value': 'Monthly'},
                                                                 {'label': 'Quarterly', 'value': 'Quarterly'},
                                                                 {'label': 'Semiannual', 'value': 'Semiannual'},
                                                                 {'label': 'Annual', 'value': 'Annual'},

                                                                 ]),
                                           html.Br(),
                                           dcc.Dropdown(id='conventionLong',
                                                        style={'background-color': 'purple'},
                                                        placeholder='Chose Available Convention',
                                                        options=[{'label': 'Actual Actual', 'value': 'ActualActual'},
                                                                 {'label': 'Actual360', 'value': 'Actual360'},
                                                                 {'label': 'Actual365', 'value': 'Actual365'},
                                                                 {'label': 'Thirty360', 'value': 'Thirty360'},
                                                                 {'label': 'Business252', 'value': 'Business252'}],
                                                        value='ActualActual'),
                                           dcc.Dropdown(id='calendarShortLong', placeholder='Put the name of Country',
                                                        options=[{'label': 'UK', 'value': 'United Kingdom'},
                                                                 {'label': 'United States', 'value': 'USA'},
                                                                 {'label': 'Switzerland', 'value': 'Switzerland'},
                                                                 {'label': 'Poland', 'value': 'Poland'}
                                                                 ], value='United Kingdom'),

                                           dcc.Input(id='Business ConventionLong',
                                                     placeholder='Define Business Convention',
                                                     value='Following'),
                                           dcc.Input(id='Termination Business ConventionLong',
                                                     placeholder='Define Termination Business Convention',
                                                     value='Following'),
                                           dcc.Input(id='endOfMonthLong', value='False'),
                                           html.Br(),
                                           html.Label('Place provide the parameters for option'),
                                           dcc.Dropdown(id='optionTypeLong',
                                                        options=[{'label': 'Call Option', 'value': 'call'},
                                                                 {'label': 'Put Option', 'value': 'put'}],
                                                        value='call'),
                                           html.Hr(),
                                           dcc.Input(id='currentPriceLong', value=90, type='number',
                                                     placeholder='Current Price'),
                                           dcc.Input(id='strikeLong', value=92, type='number', placeholder='Strike'),
                                           dcc.Input(id='riskFreelong', value=0.1, type='number',
                                                     placeholder='Risk Free Rate'),
                                           dcc.Input(id='volatilityLong', value=0.23, type='number',
                                                     placeholder='Volatility'),
                                           dcc.Input(id='dividendLong', value=0, type='number',
                                                     placeholder='Dividend'),
                                           html.Div(id='deltaLong'),

                                           # html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),
                                           # style={'text-align': 'center'}),

                                           html.Hr(),

                                       ]),
                                       dcc.Textarea(value='GREEKS',
                                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                                           'background-color': 'yellow', 'border-style': 'dashed',
                                                           'text-align': 'center'}),
                                       ###################################----RESULT Dynamic Slider----###############################################
                                       dcc.RangeSlider(id='sliderPriceGreeks', min=50, max=130),
                                       html.Hr(),

                                       html.Hr(),
                                       html.Button('Press to get delta and gamma', id='shortDeltaGammaButton',
                                                   style={'background-color': 'brown', 'fontSize': 20}),
                                       html.Div(id='shortDeltaGamma'),
                                       html.Button('Press to get vega', id='shortVegaButton',
                                                   style={'background-color': 'brown', 'fontSize': 20}),

                                       ###################################----GREEK PARAMETERS----###############################################
                                       html.Div(id='shortVega', children='')
                                       ###################################----GREEK PARAMETERS----###############################################

                                   ],

                                   )

                       ])

                       ]

                      )


#####################################################----ANALYTICAL PRICE CALLBACK----###########################################
#
@app.callback(
    Output('yearFraction', 'children'),
    [
        Input('valuationDateAnalitical', 'date'),
        Input('endDateAnalitical', 'date'),
        Input('scheduleAnalitical', 'value'),
        Input('conventionAnalitical', 'value'),
        Input('calendarAnalitical', 'value'),
        Input('optiontypeAnalitical', 'value'),
        Input('currentPriceAnalitical', 'value'),
        Input('strikeAnalitical', 'value'),
        Input('riskFreeAnalitical', 'value'),
        Input('volatilityAnalitical', 'value'),
        Input('dividendAnalitical', 'value'),
        Input('yearFractionButton', 'n_clicks')

    ])
def dashYearFraction(valDate, endDate, schedule, convention, calendar, optionType,
                     currentPrice, strike, riskFree, volatility, dividend, click):
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

    year_fraction = round(o_black_scholes.mf_yf_between_valu_date_and_maturity, 3)

    if click is None:
        raise PreventUpdate
    else:

        return html.Div([html.H4(f'Annuity for this contract  {year_fraction}'),
                         html.Hr(),

                         ])


@app.callback(
    Output('optionPriceAnalitical', 'children'),
    [
        Input('valuationDateAnalitical', 'date'),
        Input('endDateAnalitical', 'date'),
        Input('scheduleAnalitical', 'value'),
        Input('conventionAnalitical', 'value'),
        Input('calendarAnalitical', 'value'),
        Input('optiontypeAnalitical', 'value'),
        Input('currentPriceAnalitical', 'value'),
        Input('strikeAnalitical', 'value'),
        Input('riskFreeAnalitical', 'value'),
        Input('volatilityAnalitical', 'value'),
        Input('dividendAnalitical', 'value'),
        Input('AnalyticalPrice', 'n_clicks'),

    ])
def dashOptionPrice(valDate, endDate, schedule, convention, calendar, optionType,
                    currentPrice, strike, riskFree, volatility, dividend, click):
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

    if click is None:
        raise PreventUpdate
    else:

        return html.Div([

            dcc.Textarea(value=f'Analytical price of option {price}',
                         style={'width': '100%', 'color': 'red', 'fontSize': 18,
                                'background-color': 'blue', 'border-style': 'dashed',
                                'text-align': 'center'})

        ]
        )


@app.callback(
    Output('optionDynamicWRTPrice', 'children'),
    [
        Input('valuationDateAnalitical', 'date'),
        Input('endDateAnalitical', 'date'),
        Input('scheduleAnalitical', 'value'),
        Input('conventionAnalitical', 'value'),
        Input('calendarAnalitical', 'value'),
        Input('optiontypeAnalitical', 'value'),
        Input('currentPriceAnalitical', 'value'),
        Input('strikeAnalitical', 'value'),
        Input('riskFreeAnalitical', 'value'),
        Input('volatilityAnalitical', 'value'),
        Input('dividendAnalitical', 'value'),
        Input('AnalyticalUnderlyingPriceButton', 'n_clicks'),

        Input('priceSliderAnalytical', 'value'),

    ])
def dashOptionPrice(valDate, endDate, schedule, convention, calendar, optionType,
                    currentPrice, strike, riskFree, volatility, dividend, click, priceDynamic):
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

    optionPrices = [o_black_scholes.black_scholes_price_fun() for o_black_scholes._S0 in priceDynamic]

    if click is None:
        raise PreventUpdate
    else:

        return html.Div([

            dcc.Textarea(value=f'{optionPrices}',
                         style={'width': '100%', 'color': 'red', 'fontSize': 18,
                                'background-color': 'pink', 'border-style': 'dashed',
                                'text-align': 'center'})

        ]
        )


@app.callback(
    Output('optionDynamicWRTStrike', 'children'),
    [
        Input('valuationDateAnalitical', 'date'),
        Input('endDateAnalitical', 'date'),
        Input('scheduleAnalitical', 'value'),
        Input('conventionAnalitical', 'value'),
        Input('calendarAnalitical', 'value'),
        Input('optiontypeAnalitical', 'value'),
        Input('currentPriceAnalitical', 'value'),
        Input('strikeAnalitical', 'value'),
        Input('riskFreeAnalitical', 'value'),
        Input('volatilityAnalitical', 'value'),
        Input('dividendAnalitical', 'value'),
        Input('AnalyticalStrikeButton', 'n_clicks'),
        Input('strikeSliderAnalytical', 'value'),

    ])
def dashOptionPricestrike(valDate, endDate, schedule, convention, calendar, optionType,
                          currentPrice, strike, riskFree, volatility, dividend, click2, strikechange):
    o_black_scholes2 = AnalyticBlackScholes(valuation_date=valDate,
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

    optionPrices = [o_black_scholes2.black_scholes_price_fun() for o_black_scholes2._K in [85, 76, 70]]

    if click2 is None:
        raise PreventUpdate
    else:

        return html.Div([

            dcc.Textarea(value=f'{optionPrices}',
                         style={'width': '100%', 'color': 'red', 'fontSize': 18,
                                'background-color': 'pink', 'border-style': 'dashed',
                                'text-align': 'center'})

        ]
        )

#####################################################----ANALYTICAL PRICE CALLBACK----###########################################

@app.callback(Output('optionDynamicWRTSigma', 'children'),
              Input[
                  Input('valuationDateAnalitical', 'date'),
                  Input('endDateAnalitical', 'date'),
                  Input('scheduleAnalitical', 'value'),
                  Input('conventionAnalitical', 'value'),
                  Input('calendarAnalitical', 'value'),
                  Input('optiontypeAnalitical', 'value'),
                  Input('currentPriceAnalitical', 'value'),
                  Input('strikeAnalitical', 'value'),
                  Input('riskFreeAnalitical', 'value'),
                  Input('volatilityAnalitical', 'value'),
                  Input('dividendAnalitical', 'value'),
                  Input('AnalyticalStrikeButton', 'n_clicks'),
                  Input('strikeSliderAnalytical', 'value'),
              ]
              )
#####################################################----MONTE CARLO CALL BACK----###########################################

@app.callback(

    Output('MonteCarloPriceMc', 'children'),

    [
        Input('valuationDateMc', 'date'),
        Input('endDateMc', 'date'),
        Input('scheduleMc', 'value'),
        Input('conventionMc', 'value'),
        Input('calendarMc', 'value'),
        Input('optiontypeMc', 'value'),
        Input('currentPriceMc', 'value'),
        Input('strikeMc', 'value'),
        Input('riskFreeMc', 'value'),
        Input('volatilityMc', 'value'),
        Input('dividendMc', 'value'),
        Input('sampleMc', 'value'),
        Input('monteCarloButton', 'n_clicks'),
        Input('numberOfPathToDisplayMc', 'value'),
        # Input('monteCarloButton','n_clicks'),

    ])
def optionPrice(valDate, endDate, schedule, convention, calendar, optionType,
                currentPrice, strike, riskFree, volatility, dividend, runs, click, click2):
    equitySimulation = EquityModels(valuation_date=valDate,
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
                                    ann_dividend=dividend,
                                    runs=runs)

    price = round(equitySimulation.mf_monte_carlo_price, 3)
    paths = equitySimulation.m_ar_equity_price
    lqlDates = list(equitySimulation.mListOfDates)
    ldtDates = [d.to_date() for d in lqlDates]

    if click is None:
        raise PreventUpdate
    else:

        return html.Div([
            dcc.Textarea(value=f'Monte Carlo Price price of option {price}',
                         style={'width': '100%', 'color': 'red', 'fontSize': 18,
                                'background-color': 'blue', 'border-style': 'dashed',
                                'text-align': 'center'})

        ])


@app.callback(

    Output('graph', 'children'),

    [
        Input('valuationDateMc', 'date'),
        Input('endDateMc', 'date'),
        Input('scheduleMc', 'value'),
        Input('conventionMc', 'value'),
        Input('calendarMc', 'value'),
        Input('optiontypeMc', 'value'),
        Input('currentPriceMc', 'value'),
        Input('strikeMc', 'value'),
        Input('riskFreeMc', 'value'),
        Input('volatilityMc', 'value'),
        Input('dividendMc', 'value'),
        Input('sampleMc', 'value'),
        # Input('monteCarloButton','n_clicks'),

        Input('DisplayPathButton', 'n_clicks'),
        Input('numberOfPathToDisplayMc', 'value'),

    ])
def optionPrice(valDate, endDate, schedule, convention, calendar, optionType,
                currentPrice, strike, riskFree, volatility, dividend, runs, click, display):
    equitySimulation = EquityModels(valuation_date=valDate,
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
                                    ann_dividend=dividend,
                                    runs=runs)

    paths = equitySimulation.m_ar_equity_price
    lqlDates = list(equitySimulation.mListOfDates)
    ldtDates = [d.to_date() for d in lqlDates]

    if click is None:
        raise PreventUpdate
    else:

        return html.Div([
            dcc.Graph(figure=dict(data=
                                  [dict(x=ldtDates,
                                        y=paths[:, i],
                                        name=f'Path{i}',
                                        marker=dict(color='')) for i in range(display)],
                                  layout=dict(
                                      xaxis={'title': 'Dates'},
                                      yaxis={'title': 'Equity Price'},
                                      title='Equity simulation modeled by geometric brownian motion',
                                      showlegend=True,
                                      legend=dict(x=0,
                                                  y=1.0),
                                      margin=dict(l=40, r=0, t=40, b=30),
                                  )

                                  ),
                      style={'height': 300}

                      ),

        ])


#####################################################----MONTE CARLO CALL BACK----###########################################

#####################################################----GREEKS CALL BACK----###########################################

#####################################----Price Slider Analytical----#######################################
@app.callback(
    Output('priceSliderAnalytical', 'value'),
    [
        Input('currentPriceAnalitical', 'value')
    ]
)
def defineDashboard(starpoint):
    values = [i for i in range(starpoint - 10, starpoint + 11)]
    return values


@app.callback(
    Output('priceSliderAnalytical', 'marks'),
    [
        Input('currentPriceAnalitical', 'value')
    ]
)
def defineDashboard(starpoint):
    marks = {i: f'{i}' for i in range(starpoint - 40, starpoint + 41)}
    return marks


#####################################----Price Slider Analytical----#######################################

#####################################----Strike Slider Analytical----#######################################
@app.callback(
    Output('strikeSliderAnalytical', 'value'),
    [
        Input('strikeAnalitical', 'value')
    ]
)
def defineslider(starpoint):
    values = [i for i in range(starpoint - 2, starpoint + 2)]
    return values


@app.callback(
    Output('strikeSliderAnalytical', 'marks'),
    [
        Input('strikeAnalitical', 'value')
    ]
)
def defineslider(starpoint):
    marks = {i: f'{i}' for i in range(starpoint - 40, starpoint + 41)}
    return marks


#####################################----Strike Slider Analytical----#######################################


#####################################----Price Slider Greeks----#######################################
@app.callback(
    Output('sliderPriceGreeks', 'value'),
    [
        Input('currentPriceAnalitical', 'value')
    ]
)
def defineDashboard(starpoint):
    values = [i for i in range(starpoint - 10, starpoint + 11)]
    return values


@app.callback(
    Output('sliderPriceGreeks', 'marks'),
    [
        Input('currentPriceAnalitical', 'value')
    ]
)
def defineDashboard(starpoint):
    marks = {i: f'{i}' for i in range(starpoint - 40, starpoint + 41)}
    return marks


#####################################----Price Slider Greeks----#######################################


@app.callback(
    Output('shortGreeks', 'children'),
    [
        Input('valuationDateShort', 'date'),
        Input('endDateShort', 'date'),
        Input('scheduleShort', 'value'),
        Input('conventionShort', 'value'),
        Input('calendarShort', 'value'),
        Input('optionTypeShort', 'value'),
        Input('currentPriceShort', 'value'),
        Input('strikeShort', 'value'),
        Input('riskFreeShort', 'value'),
        Input('volatilityShort', 'value'),
        Input('dividendShort', 'value'),
        Input('shortDeltaGammaButton', 'n_clicks'),
        Input('sliderPriceGreeks', 'value'),

    ])
def getGreeks(valDate, endDate, schedule, convention, calendar, optionType,
              currentPrice, strike, riskFree, volatility, dividend, click, sliderRange):
    greeks = GreeksParameters(valuation_date=valDate,
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

    deltaShort = [greeks.delta() for greeks._S0 in sliderRange]
    gammaShort = [greeks.gamma() for greeks._S0 in sliderRange]
    vegaShort = [greeks.vega() for greeks._S0 in sliderRange]

    if click is None:
        raise PreventUpdate
    else:

        return html.Div([html.H4(f'Delta {deltaShort}'),
                         html.Hr(),
                         html.H4(f'Gamma {gammaShort}'),
                         html.Hr(),
                         html.H4(f'Vega {vegaShort}'),
                         ])


#####################################################----GREEKS CALL BACK----###########################################

if __name__ == '__main__':
    app.run_server(debug=True)
