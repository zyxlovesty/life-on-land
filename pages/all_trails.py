# all_trails.py

import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash.dependencies import Input, Output, State
import dash_leaflet as dl

import xml.etree.ElementTree as ET
from shapely.geometry import LineString
import pandas as pd
import base64
import os

from database import *

dash.register_page(__name__)

session, connection = get_session()

df = pd.read_sql('SELECT * FROM trails', con=connection)

def load_species_names():
    species_set = set()
    for species_list in df['trail_species'].str.split(','):
        species_set.update([species.strip() for species in species_list])
    return [{'label': species, 'value': species} for species in sorted(species_set)]

# App layout
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.H4('Customise your hiking experience by spotting rare species across Victoria', style={'color': '#fff',
                'margin-bottom': '10px', 'margin-top': '10px', 'margin-left': '40px', 'font-size': '2em', 'text-align': 'center'}),
        html.H4('Explore the diverse species of Victoria with our carefully curated selection. Click on a particular species to find out which hiking sites you can spot them on.',
                style={'font-size': '1em', 'color': '#fff', 'margin-left': '40px', 'text-align': 'center'}),
        html.P("    ")
    ], style={
        'background-color': '#112434',
        'border': '2px solid white',
        'padding': '60px',
        'margin': '40px',
        'margin-top': '100px',
        'border-radius': '15px',
        'color': 'white'
    }),
    # html.Div(id='trail-cards-row'),
    html.Div([
        dcc.Dropdown(
            id='species-search-dropdown',
            options=load_species_names(),
            searchable=True,
            placeholder='Search for species...',
            style={
                'width': '70%',  # Use 100% to make it responsive within the column
                'margin': '0 auto',  # Keep it centered
                'borderRadius': '20px',
                'fontFamily': '"Poppins", sans-serif',
                'fontSize': '16px',
                'margin-bottom': '30px'
            }
        ),
    ]),
    html.Div(id='dynamic-content', style={'padding': '20px'})
])

@callback(
    Output('url', 'pathname'),
    [Input('species-search-dropdown', 'value')],
    prevent_initial_call=True
)
def update_url(selected_species):
    if selected_species:
        # Convert the selected species to URL-friendly format if needed
        formatted_species_name = selected_species.replace(" ", "-")
        return f'/all-trails/{formatted_species_name}'
    # Fallback or default URL if no species is selected
    return '/all-trails'

# Update the dynamic content based on the URL pathname

def render_content(pathname):
    if pathname.startswith('/all-trails/'):
        species_name = pathname.split('/')[-1]
        return html.Div(f"Hello from {species_name}")
    else:
        return html.Div("Page not found")

@callback(
    Output('dynamic-content', 'children'),
    [Input('url', 'pathname')]
)

def update_dynamic_content(pathname):
    return render_content(pathname)