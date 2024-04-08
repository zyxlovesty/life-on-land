# app.py

import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output
from dash import callback

# External CSS
external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css',
    dbc.themes.MINTY
]

app = dash.Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets, external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/gsap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/ScrollTrigger.min.js'],
    suppress_callback_exceptions=True, prevent_initial_callbacks="initial_duplicate")

from pages import home
from pages import my_trails

server = app.server


app.layout = html.Div([
    dbc.Row([
        dbc.Col(
            html.Header([
                html.A('InSync', href='#', className='logo'),
                html.Ul([
                    html.Li(dcc.Link('Home', href='/home', className='active')),
                    html.Li(dcc.Link('My Trail', href='/my-trails')),
                    html.Li(dcc.Link('All Trails', href='/all-trails')),
                ], className='navigation'),
                html.Hr(),
                dash.page_container
            ])
        )
    ])
])


if __name__ == '__main__':
    app.run_server(debug=True)