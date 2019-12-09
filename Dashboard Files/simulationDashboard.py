import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html
import QuantLib as ql

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate
from scenario_generator import EquityModels
from utilities import QuantLibConverter

import plotly.graph_objs as go
import pandas as pd
import os
import datetime


def generate_table(dataframe, max_rows=26):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +
        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chridyp/pen/bWLgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([dcc.Textarea(value='Simulate Equity Price',
                                    style={'width': '100%', 'color': 'green', 'fontSize': 18,
                                           'background-color': 'yellow', 'border-style': 'dashed',
                                           'text-align': 'center'}),
                       html.Label('Place provide the date when you want to start modeling'),
                       html.Br(),
                       dcc.DatePickerSingle(id='valuationDate', date=datetime.datetime(2019, 11, 25),
                                            display_format='YYYY-MM-DD'),
                       html.Br(),
                       html.Label('Place provide the end of modeling.'),
                       html.Br(),
                       dcc.DatePickerSingle(id='endDate', date=datetime.datetime(2020, 2, 20),
                                            display_format='YYYY-MM-DD'),
                       html.Br(),
                       dcc.Dropdown(id='schedule', style={'background-color': 'orange'}, placeholder='Define Schedule',
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
                       dcc.Dropdown(id='convention', style={'background-color': 'purple'},
                                    placeholder='Chose Available Convention',
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
                       html.Br(),
                       html.Label('Place provide the parameters for option'),
                       dcc.Dropdown(id='optiontype', options=[{'label': 'Call Option', 'value': 'call'},
                                                              {'label': 'Put Option', 'value': 'put'}], value='call'),
                       html.Hr(),
                       dcc.Input(id='currentPrice', value=90, type='number', placeholder='Current Price'),
                       dcc.Input(id='strike', value=92, type='number', placeholder='Strike'),
                       dcc.Input(id='riskFree', value=0.1, type='number', placeholder='Risk Free Rate'),
                       dcc.Input(id='volatility', value=0.23, type='number', placeholder='Volatility'),
                       dcc.Input(id='dividend', value=0, type='number', placeholder='Dividend'),
                       dcc.RadioItems(id='sample',
                                      options=[{'label': '1000', 'value': 1000}, {'label': '10000', 'value': 10000},
                                               {'label': '100000', 'value': 100000}], value=1000),
                       dcc.RadioItems(id='numberOfPathToDisplay',
                                      options=[{'label': '10', 'value': 10}, {'label': '15', 'value': 15},
                                               {'label': '25', 'value': 25}, {'label': '50', 'value': 50}], value=15),
                       ###################################----RESULT----###############################################
                       html.Div(id='MonteCarloPrice', children=''),
                       dcc.Graph(id='paths')

                       ###################################----RESULT----###############################################
                       ])


@app.callback(

    Output('MonteCarloPrice', 'children'),

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
        Input('sample', 'value'),
        Input('numberOfPathToDisplay', 'value')

    ])
def optionPrice(valDate, endDate, schedule, convention, calendar, optionType,
                currentPrice, strike, riskFree, volatility, dividend, runs, display):
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
                  style={'height': 300},
                  id='my-graph'
                  ),

        dcc.Textarea(value=f'Monte Carlo Price price of option {price}',
                     style={'width': '100%', 'color': 'red', 'fontSize': 18,
                            'background-color': 'blue', 'border-style': 'dashed',
                            'text-align': 'center'})

    ])


if __name__ == '__main__':
    app.run_server(debug=True)
