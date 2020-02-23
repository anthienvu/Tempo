#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 20:44:06 2020

@author: trungminh

https://dash.plot.ly/sharing-data-between-callbacks

Storing Data in the Browser with a Hidden Div
"""


import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table
import tempo
import pandas as pd


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.layout = html.Div([
                 html.H1(children = 'Tempo Demo'),
                 html.Div(dcc.Input(id = 'input_box', type = 'text')),
                 html.Button('Start', id = 'button'),
                 html.Div(id = 'output_start_button', children = 'Enter your name and press start.'),
                 html.Div(id = 'time_report'),
                 html.Div(id = 'detail_report'),
#                 html.Div(id = 'note_display'),

                 # Hidden div inside the app that stores the intermediate value
                 html.Div(id='time_report_value', style={'display': 'none'}),
                 html.Div(id='detail_report_value', style={'display': 'none'})

#                 html.Div(id = 'image_display'),
                 ], style = {'textAlign': 'center'})


@app.callback(Output('output_start_button', 'children'),
              [Input('button', 'n_clicks')],
              [State('input_box', 'value')])

def update_output(n_clicks, value):
#    return 'The input value was "{}" and the button has been clicked {} times'.format(value,n_clicks)
    if value is None or len(value) == 0:
        return 'Enter your name and press start.'
        
    if n_clicks is not None and n_clicks % 2 != 0:
        return 'Hi {}. Tempo has started.'.format(value)
    else:
        return 'Goodbye {}. Tempo has stopped.'.format(value)


@app.callback([Output('time_report_value', 'children'), Output('detail_report_value', 'children')],
              [Input('button', 'n_clicks')],
              [State('input_box', 'value')])

def run_tempo(n_clicks, value):
    if value is None or len(value) == 0:
        return None, None
        
    if n_clicks is not None and n_clicks % 2 != 0: 
        time_report_df, detail_report_df = tempo.check_workingtime()
        # more generally, this line would be
        # json.dumps(cleaned_df)
        return time_report_df.to_json(date_format='iso', orient='split'), \
               detail_report_df.to_json(date_format='iso', orient='split')
    else:
        return None, None
        
        
#@app.callback(Output('time_report','children'),
#              [Input('button', 'n_clicks'), Input('time_report_value', 'children')],
#              [State('input_box', 'value')])
#
#def update_time_report(n_clicks, time_report_value, value):
#    if (value is None) or len(value) == 0 or (time_report_value is None):
#        return None
#        
#    time_report_df = pd.read_json(time_report_value, orient='split')
#    if n_clicks is not None and n_clicks % 2 != 0:
#        return html.Div([
#                   html.H2(children='Report'),
#                   dash_table.DataTable(id = 'time_table',
#                       columns=[{'name': i, 'id': i} for i in time_report_df.columns],
#                       data = time_report_df.to_dict('records'))
#                   ], style={'display': 'inline-block'})
##               html.Div([
##                   html.H2(children='Detail'),
##                   dcc.Dropdown(id = 'detail_dropdown',
##                       options = [{'label': i, 'value': i} for i in detail_report_df['Time']],
##                       value = detail_report_df['Time'][0])
##                   ])
##                   dcc.Dropdown(id = 'detail_image',
##                       options = [{'label': i, 'value': i} for i in detail_report_df['Time']],
##                       value = detail_report_df['Time'][0])
#    else:
#        return None

        
@app.callback([Output('time_report','children'), Output('detail_report','children')],
               [Input('button', 'n_clicks'), Input('time_report_value', 'children'), Input('detail_report_value', 'children')],
               [State('input_box', 'value')])

def update_report(n_clicks, time_report_value, detail_report_value, value):
    if (value is None) or len(value) == 0 or (time_report_value is None) or (detail_report_value is None):
        return None, None
        
    time_report_df = pd.read_json(time_report_value, orient='split')    
    detail_report_df = pd.read_json(detail_report_value, orient='split')
    
    if n_clicks is not None and n_clicks % 2 != 0:
        if len(detail_report_df) == 0:
            return html.Div([
                       html.H2(children='Report'),
                       dash_table.DataTable(id = 'time_table',
                           columns=[{'name': i, 'id': i} for i in time_report_df.columns],
                           data = time_report_df.to_dict('records'))
                       ], style={'display': 'inline-block'}), None
        
        else:
            return html.Div([
                       html.H2(children='Report'),
                       dash_table.DataTable(id = 'time_table',
                           columns=[{'name': i, 'id': i} for i in time_report_df.columns],
                           data = time_report_df.to_dict('records'))
                       ], style={'display': 'inline-block'}), \
                   html.Div([
                       html.H2(children='Detail'),
                       dcc.Dropdown(id = 'detail_dropdown',
                           options = [{'label': i, 'value': i} for i in detail_report_df['Time']],
                           value = detail_report_df['Time'][0])
                       ])
                   
    else:
        return None, None        

#
#@app.callback(Output('note_display', 'children'),
#              [Input('detail_report', 'children')])
#def update_note(value):
#    note_text = detail_report_df.loc[detail_report_df['Time'] == value, 'Note'].values[0]
#    return note_text

                 
if __name__ == '__main__':
    app.run_server(debug=True)
#    app.run_server(host = '127.0.0.1', port = '5000',debug=True)