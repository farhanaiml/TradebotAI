import dash
from dash import Dash, dcc, html, callback, Input, Output,State, ClientsideFunction
#import dash_bootstrap_components as dbc
from flask import Flask, request
from apps.app import app, application

colors = {'background': '#111111', 'text': '#7FDBFF'}

SIDEBAR_STYLE = {"top": 0,"left": 0,"bottom": 0,"width": "15%",
                 "background-color": '#00022e','text': '#FFFFFF','z-index': 9999}

user_logo_style = {'position': 'relative',
                    'width': '50px',  'height': '50px',  'border-radius': '50%', 'align-items': 'right',}

CONTENT_STYLE = {"margin-left": "0.1rem","margin-right": "2rem",'color':'#FFFFFF',}

text_CONTENT_STYLE = {'height':'5rem','fontSize': 18,'textAlign': 'center',"margin-left": "1rem", 'background-image':'https://media.zenfs.com/en/the_motley_fool_261/0c578c94f293f2aa443d12b24d530f90'}
# body_CONTENT_STYLE = {'height':'5rem','fontSize': 15,'textAlign': 'center',"margin-left": "15.5%",'color':'black',
#                       'width':'100rem'}
PLOTLY_LOGO = "https://previews.123rf.com/images/sondem/sondem1701/sondem170100021/68790687-vintage-old-pocket-watch.jpg"
user_logo = ""

navbar = html.Div([

    html.Div(children = [
        html.Div(
            [
                html.Div(html.A("HOME", href="/stockview", id="page-1-link",style={'height':'5rem','fontSize': 18,
                                                                                           'textAlign': 'center',"margin-left": "5%",
                                                                                           'color':'#FFFFFF'}),
                         ),
                html.Div(html.A("CONTACT US", href="/stockview",id="page-2-link", style={'height':'5rem','fontSize': 18,
                                                                                           'textAlign': 'center',"margin-left": "10%",
                                                                                           'color':'#FFFFFF'}),
                         ),
                html.Div(html.A("TRADING", href="/stockview", id="page-3-link", style={'height':'5rem','fontSize': 18,
                                                                                           'textAlign': 'center',"margin-left": "15%",
                                                                                           'color':'#FFFFFF'}),
                         ),

                html.Div(html.A("MORE", href="/stockview", id="page-5-link", style={'height':'5rem','fontSize': 18,
                                                                                           'textAlign': 'center',"margin-left": "20%",
                                                                                           'color':'#FFFFFF'}),
                        ),

            ],

         className='row'),
                                 ])], className='navbar')

content = html.Div(id="page-contents", style=CONTENT_STYLE)
