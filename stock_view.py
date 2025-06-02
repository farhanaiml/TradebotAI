import dash
from dash import dash_table, dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd
from flask import Flask, request
from datetime import  datetime, timedelta, date
#import dash_bootstrap_components as dbc
from apps.app import app, application
import numpy as np
from collections.abc import Iterable
import plotly.graph_objects as go
import plotly.io as pio
import pytz
import yfinance as yf
import plotly.express as px

#  = pytz.timezone('Asia/Kolkata')

def flatten(lis):
    for item in lis:
        if isinstance(item, Iterable) and not isinstance(item, str):
            for x in flatten(item):
                yield x
        else:
            yield item

body_CONTENT_STYLE = {'height':'5rem','fontSize': 15,'textAlign': 'center','color':'black',
                      'width':'100rem',"position": "Flex", 'opacity': '0.9'}

manager_login = 'user'


df_user =pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

df1 = pd.DataFrame(columns=['Date','Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

"/* HTML Layout starts */"

layout = html.Div(
    [

       #symbol
        html.Br(), html.Br(),  html.Br(), html.Br(), html.Br(), html.Br(), html.Br(), html.Br(),
        html.Div(id='symbol-info', children=[
            html.Div([
                html.Span(["Symbol"],
                          style={"margin-left": "-50%", 'fontSize': 18, 'textAlign': 'left',
                                 'color': 'white',}),
                dcc.Input(type='text', id='symbol-id', value='', minLength=2, maxLength=500,
                          style={"margin-left": "5%", 'color': 'black',  'fontSize': 16,}, ),
            ],className = "row"),
        ]),html.Br(), html.Br(),   html.Br(),

        html.Div(id='mark-info', children=[
            html.Div([
                html.Span(["Market"],
                          style={"margin-left": "-50%", 'fontSize': 18, 'textAlign': 'left',
                                 'color': 'white', }),
                dcc.Input(type='text', id='mark-id', value=None, minLength=2, maxLength=500,
                          style={"margin-left": "5%", 'color': 'black', 'fontSize': 16, }, ),
            ], className="row"),
        ]), html.Br(), html.Br(), html.Br(),


        # html.Div(id='market-info', children=[
        #     html.Div([
        #         html.Span(["market"],
        #                   style={'margin-left':'-65%','fontSize': 18, 'textAlign': 'left',"margin-top":"200px",
        #                          'color': 'white'}),
        #         dcc.Dropdown(id='activity-dropdown',
        #                      options=[
        #                          {'label': 'NSE', 'value': 'NSE'},
        #                          {'label': 'BSE', 'value': 'BSE'},
        #                      ],
        #                      value='NSE',
        #                      style={'margin-left':'18.5%','width':'30%', 'color': 'black', 'fontSize': 16, }
        #                      ),
        #     ], className="row"),
        # ]),
        # date range
        html.Div([
                html.Div([
                    html.Span(["Start Date"], style={"margin-left": "-54%",'text-align':'center', 'color': 'white','align-items':'left'}),

                    dcc.DatePickerSingle(id='sum-from-date-id', with_portal = True,
                            max_date_allowed=datetime.now(),
                            min_date_allowed=(datetime.now() - timedelta(days=730)),
                            initial_visible_month = datetime.now(),
                         date=(datetime.now() - timedelta(days=90)),day_size=43, display_format='M-D-Y',placeholder="Select a date",style={"margin-left": "5%",'align-items':'left'}),

                    html.Br(), html.Br(),html.Br(),

                    html.Span(["To Date"], style={"margin-left": "-54%",'color': 'white','text-align': 'center', 'align-items': 'left'}),

                    dcc.DatePickerSingle(id='sum-to-date-id', with_portal=True,
                                     max_date_allowed=datetime.now(),
                                     min_date_allowed=(datetime.now() - timedelta(days=730)),
                                     initial_visible_month=datetime.now(),
                                     date=datetime.now(), day_size=43, display_format='M-D-Y', placeholder="Select a date",
                                     style={"margin-left": "6%", 'align-items': 'left'}),
                    html.Br(), html.Br(), html.Br(), html.Br(),

                    html.Span([
        html.Button('Search', id='sum-go-btn-id', n_clicks=0,
                    style={'background-color':'#000000',"margin-left": "-55%",'color':'#FFFFFF'})]),
                        ],style={"margin-left": "0%", 'align-items': 'right'}),
                ], className = "row",),

        html.Br(),

        html.Div([
            html.Div(children=[html.Div([dash.html.H2(["Stock Price History"],style={'color': 'white','text-align': 'left', }),

                dash_table.DataTable(
                id='sum-main-table',
                columns=[{"name": i, "id": i} for i in df1.columns],
                style_cell={'fontFamily': 'Open Sans', 'textAlign': 'start', 'height': '20px'},
                style_header_conditional=[
                    {
                        "backgroundColor": "#000000",
                        "fontWeight": 700,
                        "color": "white",
                    }],
                export_format='xlsx',
                export_headers='display',
                data=df1.to_dict('records'))],style={ 'margin-left':'20%'} )]), html.Br(), html.Br()],id ='sum-table-container',
            className="row pretty_container table",
            style={'display': 'none', 'margin-left':'15%'}
            ),
        #graph
        html.Br(),html.Br(),
        dcc.Loading(
            type="default",
            fullscreen=True,
            children=
            html.Div(id='graph-container-id',children = [], style={ 'margin-left':'15%'})),
        # html.Div(id='graph-container-id',children = [], style={ 'margin-left':'15%'}),
        html.Br(),html.Br(),
        html.Div(id='line-chart-id',children = [],style={ 'margin-left':'15%'}),
        html.Br(),html.Br(),
    ], style = {"margin-left": "-12%", 'top':'25%', 'bottom':'-50%',})



@app.callback([Output('sum-main-table', 'columns'), Output('sum-main-table', 'data'),
               Output('sum-table-container', 'style'),Output('graph-container-id', 'children'),Output('line-chart-id', 'children')],
              [Input('sum-go-btn-id', 'n_clicks')],
              [State('sum-from-date-id','date'),State('sum-to-date-id','date'),State('symbol-id','value'),
               ]
              )
def use_df_callback(go_click,from_date, to_date, symbol):
    container_style = {'fontSize': 15, 'textAlign': 'center',
             'color': 'black', 'max-height': '1000px', 'overflow': 'scroll',
             'opacity': '0.9', 'display': 'block'}
    if go_click:
        symbol = symbol + ".ns"
        print(from_date, to_date)
        from_date = from_date.split('T')[0]
        to_date = to_date.split('T')[0]
        print(from_date, to_date)
        df1 = yf.download(symbol, from_date, to_date)
        df = df1.reset_index()
        df['symbol'] = symbol
        hovertext = []
        for i in range(len(df['Open'])):
            hovertext.append('Open: ' + str(df['Open'][i]) + '<br>Close: ' + str(df['Close'][i]))
        pio.templates.default = "plotly_dark"
        fig = go.Figure(data=go.Candlestick(x=df['Date'],
                                     open=df['Open'],
                                     high=df['High'],
                                     low=df['Low'],
                                     close=df['Close'],text=hovertext,
                hoverinfo='text'))
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text="Stock history")
        graph = html.Div(children=[ dcc.Graph(figure=fig)], style={'background-color':'black'})
        ticker = yf.Ticker(symbol)

        df_pie = ticker.dividends.reset_index()
        df_pie["Dividends"] = df_pie["Dividends"].round(2)
        pie_chart= px.line(df_pie, x='Date', y="Dividends", text = "Dividends")
        pie_chart.update_traces(textposition='top center',text = df_pie["Dividends"])
        pie_chart.update_layout(title_text="Dividend history")
        line_chart = html.Div(children=[ dcc.Graph(figure=pie_chart)], style={'background-color':'black'})


        return ([{"name": i, "id": i} for i in df.columns], df.to_dict('records'),
                container_style,graph, line_chart)
    else:
        raise dash.exceptions.PreventUpdate

