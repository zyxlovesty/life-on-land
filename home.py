# home.py

import dash
from dash import html, dcc
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ClientsideFunction

import pandas as pd
import os
import base64
import xml.etree.ElementTree as ET
from shapely.geometry import LineString

from database import *

# External CSS
external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css',
    dbc.themes.MINTY
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/gsap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/ScrollTrigger.min.js'],
    suppress_callback_exceptions=True)

session, connection = get_session()

df_trails = pd.read_sql('SELECT * FROM trails', con=connection)

all_trail_names = df_trails['trail_name'].tolist()

def gpx_to_points(gpx_path):
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    namespaces = {'default': 'http://www.topografix.com/GPX/1/1'}
    route_points = [(float(pt.attrib['lat']), float(pt.attrib['lon'])) for pt in root.findall('.//default:trkpt', namespaces)]
    return LineString(route_points)

app.layout = html.Div([
        dbc.Row([
        dbc.Col(
            html.Header([
                html.A('InSync', href='#', className='logo'),
                html.Ul([
                    html.Li(dcc.Link('Home', href='/home', className='active')),
                    html.Li(dcc.Link('My Trail', id='my-trail-link', href='/my-trail')),
                    html.Li(dcc.Link('All Trails', href='/all-trails')),
                ], className='navigation')
            ])
        )
    ]),
    dcc.Location(id='url', refresh=False),  # Add this line
    
    html.Section(className='parallax', children=[
        html.H2('Start Your Hiking Journey', id='text'),
        html.Img(src='/assets/monutain_01.png', id='m1'),
        html.Img(src='/assets/trees_02.png', id='t2'),
        html.Img(src='/assets/monutain_02.png', id='m2'),
        html.Img(src='/assets/trees_01.png', id='t1'),
        html.Img(src='/assets/man.png', id='man'),
        html.Img(src='/assets/plants.png', id='plants')
    ]),
    html.Div(id='dummy-input', style={'display': 'none'}),
    html.Div(id='dummy-output', style={'display': 'none'}),
    html.Section(className='sec', children=[
        # html.H2('Trail in Vic'),
        # html.P('Start your journey'),
        html.Br(), 
        dbc.Row([
            dbc.Col([
                html.H2('Trail Search'),

                dcc.Dropdown(
                    id='home-trail-dropdown',
                    options=[{'label': trail, 'value': trail} for trail in all_trail_names],
                    value=[],
                    multi=True,
                    placeholder="Select a trail.."
                ),

                html.Div([
                    dbc.Button(
                        'Search',
                        color="info",
                        id='home-search-button',
                        n_clicks=0,
                        className="me-1"
                    )
                ], style={
                    'width': '140px',
                    'margin': 'auto',
                    'borderRadius': '20px',
                    'text-align': 'center',
                    'fontSize': '20px',
                    'fontWeight': 'bold',
                    'padding': '7px 15px',
                    'border': 'none',
                    'cursor': 'pointer',
                    'transition': 'all 0.2s ease-in-out',
                    'backgroundColor':'#112434'
                }),

                html.H4('OR'),
                html.Br(),

                html.Div([
                    html.Label('Distance:', style={'color': 'white'}),
                    dcc.Slider(
                        id='distance-slider',
                        min=0,
                        max=120,
                        step=1,
                        value=5,
                        marks={i: f'{i} km' for i in range(0, 121, 10)},
                        tooltip={'always_visible': True, 'placement': 'bottom'}
                    ),
                ], style={'text-align': 'left', 'margin-top': '20px'}),

                html.Div([
                    html.Label('Elevation:', style={'color': 'white'}),
                    dcc.Slider(
                        id='elevation-slider',
                        min=0,
                        max=3900,
                        step=1,
                        value=5,
                        marks={i: f'{i}m' for i in range(0, 4000, 300)},
                        tooltip={'always_visible': True, 'placement': 'bottom'}
                    ),
                ], style={'text-align': 'left', 'margin-top': '20px'}),

                html.Div([
                    html.Label('Duration:', style={'color': 'white'}),
                    dcc.Slider(
                        id='duration-slider',
                        min=0,
                        max=30,
                        step=0.5,
                        value=1,
                        marks={i: f'{i}hr' for i in range(0, 31 , 3)},
                        tooltip={'always_visible': True, 'placement': 'bottom'}
                    ),
                ], style={'text-align': 'left', 'margin-top': '20px'}),

                html.Div([
                    html.Label('Loop:', style={'color': 'white'}),
                    dcc.RadioItems(
                        id='loop-radio',
                        options=[
                            {'label': 'Closed Loop', 'value': 'closed loop'},
                            {'label': 'One Way', 'value': 'one way'}
                        ],
                        value='closed',  # Default value
                        labelStyle={'color': 'white', 'display': 'block', 'margin-top': '5px'} # Style for the radio item labels
                    )
                ], style={'text-align': 'left', 'margin-top': '20px'}),

                html.Div([
                    dbc.Button(
                        'Search',
                        id='home-search-button2',
                        color="info",
                        n_clicks=0,
                        className='me-1'
                    )
                ], style={'width': '140px',
                    'margin': 'auto',
                    'borderRadius': '20px',
                    'text-align': 'center',
                    'fontSize': '20px',
                    'fontWeight': 'bold',
                    'padding': '7px 15px',
                    'border': 'none',
                    'cursor': 'pointer',
                    'transition': 'all 0.2s ease-in-out',
                    'backgroundColor':'#112434'}),

                html.Br(),
                html.Br(),

                html.Div(id='filtered-trails'),
                html.Br(),
                html.Br()

            ], width=6),

            dbc.Col([
                dl.Map(
                    id='home-trail-map',
                    children=[dl.TileLayer(), dl.LayerGroup(id='home-trail-layer')],
                    style={'width': '100%', 'height': '500px'},
                    center=(-37.8136, 144.9631),
                    zoom=12
                ),
                dcc.Location(id='url', refresh=False)
            ], width=6),
        ], style={'margin': '0 auto', 'width': '100%'}),
    ]),
])

@app.callback(
    [Output('filtered-trails', 'children'), Output('home-trail-layer', 'children'), Output('home-trail-map', 'center')],
    [Input('home-search-button', 'n_clicks'), Input('home-search-button2', 'n_clicks')],
    [State('home-trail-dropdown', 'value'),
     State('distance-slider', 'value'),
     State('elevation-slider', 'value'),
     State('duration-slider', 'value'),
     State('loop-radio', 'value')]
)
def update_filtered_trails(n_clicks1, n_clicks2, selected_trails, distance, elevation, duration, loop):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'home-search-button':
        n_clicks = n_clicks1
        trails_to_display = selected_trails
        print("debug1 trails:", trails_to_display)
    elif button_id == 'home-search-button2':
        n_clicks = n_clicks2
        trails_to_display = df_trails[
            (df_trails['trail_distance'] >= distance - 5) &
            (df_trails['trail_distance'] <= distance + 5) &
            (df_trails['trail_ele_gain'] >= elevation - 300) &
            (df_trails['trail_ele_gain'] <= elevation + 300) &
            (df_trails['trail_duration'] >= duration - 0.5) &
            (df_trails['trail_duration'] <= duration + 0.5) &
            (df_trails['trail_loop'] == loop)
        ]
        trails_to_display = trails_to_display['trail_name'].tolist()
        print("debug2 trails:", trails_to_display)

    else:
        n_clicks = 0

    if n_clicks == 0:
        return dash.no_update, dash.no_update, dash.no_update
    
    # Display filtered trails under "Search" button 2
    if trails_to_display==[]:
        filtered_trails_output = html.P("No trails match the selected criteria.", style={'color': 'white'})
    else:
        filtered_trails_output = html.Ul([
            html.Li(trail_name, style={'color': 'white'}) for trail_name in trails_to_display
        ])
    
    # Display filtered trails on the map
    features = []
    centroids = []
    colors = ['blue', 'red', 'green', 'yellow', 'purple']
    
    for i, trail_name in enumerate(trails_to_display):
        gpx_path = os.path.join('data/trails', f'{trail_name}.gpx')
        line_string = gpx_to_points(gpx_path)
        centroid = line_string.centroid.coords[0]
        centroids.append(centroid)  
        color = colors[i % len(colors)]
        feature = dl.Polyline(positions=list(line_string.coords), color=color)
        feature.children = dl.Tooltip(trail_name)
        features.append(feature)
    
    # Calculate center based on centroids of filtered trails
    if centroids:
        center_latitude = sum([centroid[0] for centroid in centroids]) / len(centroids)
        center_longitude = sum([centroid[1] for centroid in centroids]) / len(centroids)
        center = (center_latitude, center_longitude)
    else:
        # Default center if no trails are found
        center = (-37.8136, 144.9631)
    
    return filtered_trails_output, features, center

@app.callback(
    Output('home-trail-dropdown', 'options'),
    [Input('home-trail-dropdown', 'search_value')]
)
def update_trail_list(search_term):
    if search_term:
        # Filter trail names based on the input
        search_term_lower = search_term.lower()
        filtered_trails = df_trails[df_trails['trail_name'].str.lower().str.startswith(search_term_lower)]
        if not filtered_trails.empty:
            # Extract just the 'name' column from the filtered DataFrame
            trail_names = filtered_trails['trail_name']
            # Create a list of options for dropdown
            options = [{'label': name, 'value': name} for name in trail_names]
            return options
    # If no search term provided or no matching trails found, return all trail options
    return [{'label': trail, 'value': trail} for trail in all_trail_names]

# app.layout = app.layout + gdc.Import(src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js") + gdc.Import(src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js")


app.clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='trigger_gsap_animation'),
    Output('dummy-output', 'children'),
    [Input('dummy-input', 'children')]
)


if __name__ == '__main__':
    app.run_server(debug=True)