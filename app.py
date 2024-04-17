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
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    dbc.themes.MINTY
]

app = dash.Dash(__name__, use_pages=True, external_stylesheets=external_stylesheets, external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/gsap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/ScrollTrigger.min.js'],
    suppress_callback_exceptions=True, prevent_initial_callbacks="initial_duplicate")

from pages import home
from pages import my_trails
from pages import species_trails

server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Add dcc.Location component
    dbc.Row([
        dbc.Col(
            html.Header([
                html.A('WildStep', href='#', className='logo'),
                html.Ul([
                    html.Li(dcc.Link('Home', href='/', id='home-link', className='navigation-link')),
                    html.Li(dcc.Link('My Trail', href='/my-trails', id='my-trails-link', className='navigation-link')),
                    html.Li(dcc.Link('Species Trails', href='/species-trails', id='species-trails-link', className='navigation-link')),
                ], className='navigation'),

            ])
        )
    ]),
    html.Hr(),
    dash.page_container,
html.Footer(
    
        dbc.Row(
            dbc.Col(
                html.P("2024 INSynC, LLC All Rights Reserved", className="footer-text", style={'text-align': 'center', 'color': 'white'}),
                width={'size': 12, 'offset': 3}
            )
        ),
        style={'background-color': '#112434', 'padding': '20px', 'width': '100%'}  # Add background color and padding
    )

])

# Callback to update the active link based on the current pathname
@app.callback(
    [Output('home-link', 'className'),
     Output('my-trails-link', 'className'),
     Output('species-trails-link', 'className')],
    [Input('url', 'pathname')]
)
def update_active_link(pathname):
    home_class = 'active' if pathname == '/' else ''
    my_trails_class = 'active' if pathname == '/my-trails' else ''
    all_trails_class = 'active' if pathname == '/species-trails' else ''
    return home_class, my_trails_class, all_trails_class

if __name__ == '__main__':
    #app.run_server(debug=False, host="0.0.0.0", port=8080)
    app.run_server(debug=True)