import dash
import dash_core_components as dcc
import dash_table as dt
import dash_html_components as html

from dash.dependencies import Output, Input
from dash.exceptions import PreventUpdate

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
                       dcc.Input(id='voltility', value='', type='number', placeholder='Volatility'),
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

    ]

)


if __name__ == '__main__':
    app.run_server(debug=True)
