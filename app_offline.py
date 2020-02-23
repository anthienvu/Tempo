#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Feb 20 20:44:06 2020

@author: trungminh

Computing Aggregations Upfront

Sending the computed data over the network can be expensive if the data is large.
In some cases, serializing this data and JSON can also be expensive.
'''


import dash
import dash_daq as daq
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import dash_table as dt
import tempo
import pandas as pd
import json


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.layout = html.Div([
                 html.H1(children = 'Tempo Demo'),
                 html.Div(dcc.Input(id = 'input_name', type = 'text')),
                 html.Div(id = 'text_name', children = 'Enter your name and time to test in seconds.', style = {'padding': 10}),
                 
                 html.Div([
                     html.Div(children='Time Step', style={'width': 100, 'display': 'inline-block'}),
                     html.Div(dcc.Input(id = 'input_timestep', type = 'number'), style={'display': 'inline-block'}),
                     html.Div(children='Total Time', style={'width': 100, 'display': 'inline-block'}),
                     html.Div(dcc.Input(id = 'input_totaltime', type = 'number'), style={'display': 'inline-block'}),
                     ], style = {'margin-bottom': 10}),
                           
                 daq.BooleanSwitch(id = 'bswitch_start', on = False, color =' #8ed62f', disabled = True,
                                   label = ['OFF', 'ON'], style = {'width': '50px', 'margin': 'auto'}),
                 html.H2(children='Report'),
                 html.Div(
                     dt.DataTable(id = 'dtable_time',
                         columns = [{'name': i, 'id': i} for i in ['Working Time', 'Free Time']]),
                         style = {'display': 'inline-block'}),
                 html.H2(children = 'Detail'),
                 dcc.Dropdown(id = 'ddown_detail', style = {'width': '500px', 'display': 'inline-block'}),
                 html.Div(id = 'text_note', style = {'padding': 10}),
                 html.Div([
                     html.Div(style={'width': '30%', 'display': 'inline-block'}),
                     html.Div([
                         html.H3(children = 'Before'),
                         html.Img(id='image_before', style={'height':'90%', 'width':'90%', 'border': '2px black solid'})
                              ], style={'width': '20%', 'display': 'inline-block'}),
                     html.Div([
                         html.H3(children = 'After'),
                         html.Img(id='image_after', style={'height':'90%', 'width':'90%', 'border': '2px black solid'})
                              ], style={'width': '20%', 'display': 'inline-block'}),
                     html.Div(style={'width': '30%', 'display': 'inline-block'}),
                     ]),
         
                 # Hidden div inside the app that stores the intermediate value
                 html.Div(id = 'json_report', style = {'display': 'none'}),
                                      
                      ], style = {'textAlign': 'center'})

                     
@app.callback(Output('bswitch_start', 'disabled'),
              [Input('input_name', 'value')])
def update_start(value):
    if value is None or len(value) == 0:
        return True
    else:
        return False
                     

@app.callback([Output('text_name', 'children'), Output('input_name', 'disabled')],
              [Input('bswitch_start', 'on')],
              [State('input_name', 'value')])
def update_name(on, value):
    if value is None or len(value) == 0:
        return 'Enter your name and time to test in seconds.', False
    else:
        if on is True:
            return 'Hi {}. Tempo is ON.'.format(value), True
        else:
            return 'Goodbye {}. Tempo is OFF.'.format(value), False


@app.callback(Output('json_report', 'children'),
              [Input('bswitch_start', 'on')],
              [State('input_name', 'value'), State('input_timestep', 'value'), State('input_totaltime', 'value')])
def run_tempo(on, value_name, value_timestep, value_totaltime):
    report_dict = {}

    if on is True and (value_name is not None and len(value_name) > 0):
        if value_totaltime is not None and value_timestep is not None:
            if value_totaltime >= value_timestep:
                time_report_df, detail_report_df = tempo.check_workingtime(value_totaltime, value_timestep)
                report_dict = {
                    'time_report_df': time_report_df.to_json(orient = 'split', date_format = 'iso'),
                    'detail_report_df': detail_report_df.to_json(orient = 'split', date_format = 'iso'),
                      }
                      
    return json.dumps(report_dict)
        

@app.callback(Output('dtable_time', 'data'),
              [Input('json_report', 'children')])
def update_time(children):
    time_report_df = pd.DataFrame()
    report_dict = json.loads(children)
    
    if len(report_dict) > 0:
        time_report_df = pd.read_json(report_dict['time_report_df'], orient = 'split')
    
    return time_report_df.to_dict('records')

    
@app.callback([Output('ddown_detail', 'options'), Output('ddown_detail', 'value')],
              [Input('json_report', 'children')])
def update_dropdown(children):
    options = []
    value = None
    report_dict = json.loads(children)
    
    if len(report_dict) > 0:
        time_report_df = pd.read_json(report_dict['time_report_df'], orient = 'split')
        if time_report_df.loc[0,'Free Time'] != '0:00:00':
            detail_report_df = pd.read_json(report_dict['detail_report_df'], orient = 'split')
            options = [{'label': i, 'value': i} for i in detail_report_df['Time']]
            value = detail_report_df['Time'].values[0]
    
    return options, value


@app.callback(Output('text_note', 'children'),
              [Input('json_report', 'children'), Input('ddown_detail', 'value')])
def update_note(children, value):
    note = None
    report_dict = json.loads(children)
    
    if len(report_dict) > 0:
        detail_report_df = pd.read_json(report_dict['detail_report_df'], orient = 'split')
        if value is not None:
            note = detail_report_df.loc[detail_report_df['Time'] == value, 'Note'].values[0]

    return note   
    
        
@app.callback([Output('image_before', 'src'), Output('image_after', 'src')],
              [Input('json_report', 'children'), Input('ddown_detail', 'value')])
def update_image_src(children, value):
    image_before_b64 = None
    image_after_b64 = None
    report_dict = json.loads(children)
    
    if len(report_dict) > 0:
        detail_report_df = pd.read_json(report_dict['detail_report_df'], orient = 'split')
        if value is not None:
            image_before_b64 = detail_report_df.loc[detail_report_df['Time'] == value, 'Image_Before'].values[0]
            image_after_b64 = detail_report_df.loc[detail_report_df['Time'] == value, 'Image_After'].values[0]

    return 'data:image/png;base64,{}'.format(image_before_b64), 'data:image/png;base64,{}'.format(image_after_b64)
        
        
        
if __name__ == '__main__':
    app.run_server(debug=True)
#    app.run_server(host = '127.0.0.1', port = '5000',debug=True)