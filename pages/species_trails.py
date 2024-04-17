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


def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

# Create species card


def format_species_name_for_url(species_name):
    placeholder = "____"  # Using an unlikely placeholder
    formatted_name = species_name.replace("-", placeholder)
    formatted_name = formatted_name.replace(" ", "-")
    formatted_name = formatted_name.replace(placeholder, "--")
    return formatted_name


def get_species_name_from_url(formatted_name):
    placeholder = "____"  # Using an unlikely placeholder
    original_name = formatted_name.replace("--", placeholder)
    original_name = original_name.replace("-", " ")
    original_name = original_name.replace(placeholder, "-")
    return original_name


def create_species_card(species_name):
    image_filename = species_name.replace(" ", "_") + '.jpg'
    image_path = os.path.join('data/species/', image_filename)
    url_path = f'species-trails/{format_species_name_for_url(species_name)}'
    return dbc.Card(
        [
            html.A(dbc.CardImg(src=b64_image(image_path), top=True, alt=f"Image of {species_name}", style={
                'width': '100%', 'height': '200px', 'object-fit': 'cover', 'margin-top': '10px'}),
                href=url_path, style={"text-decoration": "none", "color": "inherit"}),
            html.A(dbc.CardBody([
                html.H5(species_name, className="card-title", style={'text-align': 'center'}),
                # dcc.Link('View Trails', href=f'/species/{species_name.replace(" ", "-")}', style={'color': '#140c1f'})
            ]), href=url_path, style={"text-decoration": "none", "color": "inherit"}),
        ],
        style={"width": "18rem", "margin": "10px", "background-color": "#fff"}
    )


@callback(
    Output('dynamic-content', 'children'),
    [Input('url', 'pathname'),
     Input('species-search-dropdown', 'value')]
)
def update_dynamic_content(pathname, selected_species):
    ctx = dash.callback_context

    if not ctx.triggered or pathname == '/' or pathname == '/all-species':
        if selected_species:
            species_to_display = [{'label': selected_species, 'value': selected_species}]
        else:
            species_to_display = load_species_names()

        species_cards = [create_species_card(species['value']) for species in species_to_display]
        # return species_cards
        return dbc.Row(species_cards, className="row-cols-1 row-cols-md-3 justify-content-center g-4")

    elif pathname.startswith('species-trails/'):
        species_name = get_species_name_from_url(pathname.split('/')[-1])
        filtered_trails = df[df['trail_species'].str.contains(species_name, case=False)]

        trails_content = []

        for _, trail in filtered_trails.iterrows():
            trail_name = trail['trail_name']
            description = trail['trail_desc']
            duration = trail['trail_duration']
            elevation_gain = trail['trail_ele_gain']
            distance = trail['trail_distance']
            dist_mel = trail['trail_dist_mel']
            time_mel = trail['trail_time_mel']
            loop = trail['trail_loop']

            trail_card = dbc.Row([
                dbc.Col(html.Img(src=b64_image(f"data/trail_img/{trail_name}.jpg"),
                                 style={'max-width': '100%', 'height': 'auto', 'max-height': '1000px', 'display': 'block'}), width=3),
                dbc.Col([
                    html.P(description, style={'margin-left': '30px', 'text-align': 'justify'}),
                    html.Div([
                        dbc.Row([
                             dbc.Col([
                                 html.I(
                                     className="fas fa-clock", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '20px', 'margin-left': '30px'}),
                                 html.Span(f"Duration: {duration}hours", style={'color': '#808080'}),
                                 html.Div(""),
                                 # Mountain icon
                                 html.I(
                                     className="fas fa-mountain", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '30px', 'margin-top': '15px'}),
                                 html.Span(f"Elevation Gain: {elevation_gain}m", style={'color': '#808080'}),
                                 html.Div(""),
                                 # Route icon
                                 html.I(
                                     className="fas fa-route", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '30px', 'margin-top': '15px'}),
                                 html.Span(f" Distance: {distance}km", style={'color': '#808080'}),
                             ], width=4),
                             dbc.Col([
                                 html.I(className="fas fa-solid fa-car",
                                        style={'color': '#808080', 'margin-right': '5px', 'margin-top': '20px', 'margin-left': '200px'}),
                                 html.Span(f"Drive from Melbourne: {time_mel}hours", style={'color': '#808080'}),
                                 html.Div(""),
                                 html.I(
                                     className="fas fa-map-pin", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '15px', 'margin-left': '200px'}),
                                 html.Span(f"Distance from Melbourne: {dist_mel}km", style={'color': '#808080'}),
                                 html.Div(""),
                                 html.I(
                                     className="fas fa-redo", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '15px', 'margin-left': '200px'}),
                                 html.Span(f"Trail route: {loop}", style={'color': '#808080'}),
                             ], width=8),
                             ], style={'display': 'flex'}),
                    ])], width=9)
            ], style={'margin': '0 30px', 'display': 'flex', 'padding': '40px', 'border': '1px solid', 'border-color': 'rgba(0, 0, 0, 0.2)', 'border-radius': '50px', 'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                      'margin-top': '20px', 'margin-bottom': '20px'})

            trails_content.append(trail_card)

        # return dbc.Row(trails_content, className="row-cols-1 row-cols-md-3 g-4 justify-content-around")
        return trails_content

    return "Select a species to see the trails."


@callback(
    Output('url', 'pathname'),
    [Input('species-search-dropdown', 'value')],
    prevent_initial_call=True
)
def update_url_from_dropdown(selected_species):
    if selected_species:
        # Convert the selected species to URL-friendly format
        species_url_part = format_species_name_for_url(selected_species)
        return f'species-trails/{species_url_part}'
    # Fallback or default URL if no species is selected
    return '/'


# App layout
layout = html.Div([
    dcc.Location(id='url', refresh=False),
    # dbc.Row([
    #     dbc.Col(
    #         html.Header([
    #             html.A('InSync', href='#', className='logo'),
    #             html.Ul([
    #                 html.Li(dcc.Link('Home', href='/')),
    #                 html.Li(dcc.Link('My Trail', href='/my-trail')),
    #                 html.Li(dcc.Link('All Trails', href='/all-trails', className='active')),
    #             ], className='navigation')
    #         ])
    #     )
    # ]),
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
