#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 20:44:06 2020

@author: trungminh
"""


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
import tempo


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
                       html.H1(children='Tempo Demo'),
                       html.Div(dcc.Input(id='input-box', type='text')),
                       html.Button('Start', id='button'),
                       html.Div(id='output-start-button', children='Enter your name and press start.'),
                       html.Div(id='workingtime_table')],
                       style={'textAlign': 'center'})


@app.callback(Output('output-start-button', 'children'),
            [Input('button', 'n_clicks')],
            [State('input-box', 'value')])
def update_output(n_clicks, value):
#    return 'The input value was "{}" and the button has been clicked {} times'.format(value,n_clicks)
    if value is None:
        return 'Enter your name and press start.'
    if n_clicks is not None and n_clicks % 2 != 0:
        return 'Hi {}. Tempo has started.'.format(value)
    else:
        return 'Goodbye {}. Tempo has stopped.'.format(value)

            
@app.callback(Output('workingtime_table','children'),
            [Input('button', 'n_clicks')],
            [State('input-box', 'value')])

def output_report(n_clicks, value):
    if value is None:
        return []
        
    if n_clicks is not None and n_clicks % 2 != 0:
        time_report, detail_report = tempo.check_workingtime()

        return html.Div([
                         html.H2(children='Report'),
                         dash_table.DataTable(
                         id='table',
                         columns=[{"name": i, "id": i} for i in time_report.columns],
                         data = time_report.to_dict('records'))
                        ], style={'display': 'inline-block'})
      

if __name__ == '__main__':
#    app.run_server(debug=True)
    app.run_server(host = '127.0.0.1', port = '5000',debug=True)