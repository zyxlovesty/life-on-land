# my_trails.py

import dash
from dash import dcc, html, Input, Output, State, ClientsideFunction, callback, clientside_callback
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import xml.etree.ElementTree as ET
from shapely.geometry import LineString, Point
import os
import pandas as pd
from geopy.distance import geodesic
import base64
from datetime import datetime

from database import *

dash.register_page(__name__)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='trigger_gsap_animation'),
    Output('mytrail-dummy-output', 'children'),
    [Input('mytrail-dummy-input', 'children')]
)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='scroll_to_map'),
    Output('mytrail-dummy-output-2', 'children'),  # Dummy output, we don't actually need to update anything in the layout
    [Input('mytrail-search-dropdown', 'value')]
)

session, connection = get_session()

df_uploads = pd.read_sql('SELECT * FROM uploads', con=connection)
df_trails = pd.read_sql('SELECT * FROM trails', con=connection)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:/Users/ojasv/OneDrive/Monash/Sem 4/FIT5120/life-on-land/iteration1/lifeonland-418914-00a1094d16b6.json'

def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    # content = base64.b64decode(path)
    image = vision.Image(content=path)
    response = client.label_detection(image=image)
    labels = response.label_annotations
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    return labels

def get_unique_species(df):
    unique_values = set()
    for row in df['trail_species']:
        items = row.split(', ')
        unique_values.update(item.strip() for item in items)
    unique_species = [x.lower() for x in list(unique_values)]
    return unique_species

def gpx_to_points(gpx_path):
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    namespaces = {'default': 'http://www.topografix.com/GPX/1/1'}
    route_points = [(float(pt.attrib['lat']), float(pt.attrib['lon'])) for pt in root.findall('.//default:trkpt', namespaces)]
    return LineString(route_points)
 
def load_trail_names():
    # df = pd.read_csv('data/50_trails.csv', encoding='utf-8')
    return [{'label': name, 'value': name} for name in df_trails['trail_name'].unique()]
 
def is_within_distance(point, trail_points, max_distance=500):
    return any(geodesic(point, trail_point).meters <= max_distance for trail_point in trail_points)
 
def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

def db_img(blob):
    return 'data:image/png;base64,' + base64.b64encode(blob).decode('utf-8')

layout = dbc.Container(fluid=True, children=[
    dbc.Row([
        dbc.Col(
            html.Header([
                html.A('InSync', href='#', className='logo'),
                html.Ul([
                    html.Li(dcc.Link('Home', href='/', className='active')),
                    html.Li(dcc.Link('My Trail', href='/my-trail')),
                    html.Li(dcc.Link('All Trails', href='/all-trails')),
                ], className='navigation')
            ])
        )
    ]),
    html.Div(id='location-div', style={'display': 'none'}),
    html.Section(className='parallax', children=[
        html.H2('Start your Trail', id='text2'),
        dcc.Dropdown(
                id='mytrail-search-dropdown',
                options=load_trail_names(),
                searchable=True,
                placeholder='Search for trails...',
                style={
                    'width': '55%',  # Adjusts the width to fit its container
                    'margin': '0 auto',  # Centers the dropdown if its container allows
                    'borderRadius': '20px',  # Matches the CSS for rounded corners
                    'fontFamily': '"Poppins", sans-serif',  # Ensure the font matches
                    'fontSize': '16px'  # Slightly larger font for readability
                }
            ),
        html.Img(src='/assets/monutain_01.png', id='m1'),
        html.Img(src='/assets/trees_02.png', id='t2', style={'top': '16px'}),
        html.Img(src='/assets/monutain_02.png', id='m2'),
        html.Img(src='/assets/trees_01.png', id='t1'),
        # html.Img(src='/assets/man.png', id='man'),
        html.Img(src='/assets/plants.png', id='plants')
    ]),
    html.Div(id='scroll-trigger', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-input', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-output', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-output-2', style={'display': 'none'}),
    dbc.Row([
        dbc.Col([
            dl.Map(
                id='mytrail-map',
                children=[dl.TileLayer(), dl.LayerGroup(id='mytrail-layer'), dl.LayerGroup(id='myimage-layer')],
                style={'width': '100%', 'height': '640px', 'margin-top':'40px', 'margin-bottom':'40px', 'margin-left':'20px'},
                center=(-37.8136, 144.9631),
                zoom=12
            )
        ], width=15, lg=7),  # Map takes up 6 columns on large screens, full width on smaller ones
        dbc.Col([
            dbc.Row(justify="center", className="h-100 align-items-center", children=[
                dbc.Col([
                    dbc.Button('Found something interesting? Upload your find!', id='find-btn', n_clicks=0,
                               color="primary", className="mb-3", style={'display': 'block', 'width': '100%','marginLeft': '100px',
                                                                         'backgroundColor':'#112434', 'color':'#fff',
                                                                         'border': 'none', 'borderRadius': '20px', 
                                                                         'cursor': 'pointer', 'transition': 'all 0.2s ease-in-out'}),
                    dcc.Upload(
                        id='upload-image',
                        children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
                        style={
                            'width': '100%', 'height': '60px', 'lineHeight': '60px',
                            'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                            'textAlign': 'center', 'margin': '0 auto', 'display': 'none','marginLeft': '100px'
                        },
                        accept='.png,.jpg,.jpeg,.heic',
                        multiple=True
                    )
                ], width=10)  # Adjust width as needed for aesthetic preferences
            ])
        ], width=9, lg=5, className="d-flex"),  # Make the column a flex container
    ]),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Action Required")),
        dbc.ModalBody("Please select a trail before uploading."),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0))
    ], id="modal", is_open=False),
    dbc.Modal([
        dbc.ModalHeader("Location Sharing Required"),
        dbc.ModalBody("You need to share your location before uploading an image."),
        dbc.ModalFooter(dbc.Button("OK", id="close-location-modal", className="ms-auto", n_clicks=0))
    ], id="location-error-modal", is_open=False),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Too Far From Trail")),
        dbc.ModalBody("You are too far from the selected trail to upload images."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-too-far-modal", className="ms-auto", n_clicks=0)
        )
    ], id="too-far-modal", is_open=False),
    html.Div(id='upload-status', style={'display': 'none'})
])

@callback(
    Output('modal', 'is_open'),
    [Input('find-btn', 'n_clicks'), Input('close-modal', 'n_clicks')],
    [State('mytrail-search-dropdown', 'value'), State('modal', 'is_open')],
    prevent_initial_call=True
)
def toggle_trail_modal(find_clicks, close_clicks, selected_trail, is_open):
    ctx = dash.callback_context
    if not ctx.triggered or selected_trail is not None:
        # If no button was clicked or a trail is selected, don't open the modal
        return False
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "find-btn" and not selected_trail:
            # If the find button was clicked without a trail selected, open the modal
            return True
        elif button_id == "close-modal":
            # If the close button on the modal was clicked, close the modal
            return False
    return is_open

@callback(
    Output('location-div', 'children'),
    [Input('find-btn', 'n_clicks')],
    [State('mytrail-search-dropdown', 'value')]
)
def display_geolocation(n, selected_trail):
    if n > 0 and selected_trail:
        return dcc.Geolocation(id='geo')
    return []

@callback(
    Output('location-error-modal', 'is_open'),
    [Input('close-location-modal', 'n_clicks'), Input('geo', 'position_error')],
    [State('location-error-modal', 'is_open')],
    prevent_initial_call=True
)
def toggle_location_error_modal(close_clicks, position_error, is_open):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
   
    if triggered_id == 'close-location-modal':
        return False
    elif triggered_id == 'geo' and position_error:
        return True
    return is_open

@callback(
    Output('too-far-modal', 'is_open'),
    [Input('close-too-far-modal', 'n_clicks'),
     Input('geo', 'position')],
    [State('mytrail-search-dropdown', 'value'),
     State('too-far-modal', 'is_open')],
    prevent_initial_call=True
)
def handle_too_far_modal(close_clicks, position, selected_trail, is_open):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'close-too-far-modal':
        return False
    elif triggered_id == 'geo':
        if not position or not selected_trail:
            return False
        gpx_path = os.path.join('data/trails', f'{selected_trail}.gpx')
        trail_points = gpx_to_points(gpx_path).coords
        user_position = (position['lat'], position['lon'])
        if is_within_distance(user_position, trail_points):
            return False
        else:
            return True
    return is_open

@callback(
    [Output('find-btn', 'style'), Output('upload-image', 'style')],
    [Input('geo', 'local_date'), Input('geo', 'position_error'), Input('close-too-far-modal', 'n_clicks')],
    prevent_initial_call=True
)
def update_button_visibility(local_date, position_error, close_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
 
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'geo' and local_date and not position_error:
        return {'display': 'none'}, {
                                    'width': '100%', 'height': '60px', 'lineHeight': '60px',
                                    'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                                    'textAlign': 'center', 'margin': '0 auto', 'display': 'block','marginLeft': '100px'
                                    }
    if triggered_id in ('close-too-far-modal', 'geo') and (position_error or close_clicks > 0):
        return {'display': 'block', 'width': '100%','marginLeft': '100px',
                'backgroundColor':'#112434', 'color':'#fff',
                'border': 'none', 'borderRadius': '20px', 
                'cursor': 'pointer', 'transition': 'all 0.2s ease-in-out'}, {'display': 'none'}
    return {'display': 'block', 'width': '100%','marginLeft': '100px',
                'backgroundColor':'#112434', 'color':'#fff',
                'border': 'none', 'borderRadius': '20px', 
                'cursor': 'pointer', 'transition': 'all 0.2s ease-in-out'}, {'display': 'none'}

@callback(
    Output('upload-status', 'children'),  # An Output to indicate the upload status
    [Input('upload-image', 'contents'),  # Contents from the upload component
     Input('geo', 'local_date')],  # Date from the geolocation component
    [State('geo', 'position'),  # Position state from geolocation
     State('geo', 'position_error')],  # Position error state from geolocation
    prevent_initial_call=True
)
def handle_upload(contents, local_date, position, position_error):
    if contents is None:
        # If no image is uploaded, do nothing
        return "No image uploaded."
    if position_error:
        # Handle case where geolocation failed
        return "Failed to get geolocation data."
    content_type, content_string = contents[0].split(',')  # Taking the first uploaded file
    image_bytes = content_string  # base64 encoded string of the first image
    latitude = position['lat']
    longitude = position['lon']
    decoded = base64.b64decode(content_string)
    detected_labels = detect_labels(decoded)
    labels = [l.description.lower() for l in detected_labels]
    if len(set(labels).intersection(set(get_unique_species(df_trails)))):
        species = list(labels.intersection(get_unique_species(df_trails)))[0].capitalize()
    else:
        species = detected_labels[0].description
    # last_row = session.query(Uploads).order_by(Uploads.id.desc()).first()
    # last_row_id = last_row.id
    new_upload = Uploads(
        upload_id = len(df_uploads)+1,
        upload_lat = latitude,
        upload_long = longitude, 
        upload_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        upload_img = decoded,
        upload_species = species
    )
    session.add(new_upload)
    session.commit()
    return "Image uploaded successfully!"

@callback(
    [Output('myimage-layer', 'children')],
    [Input('upload-image', 'contents'),
     Input('mytrail-search-dropdown', 'value')],
    [State('mytrail-map', 'zoom')]  # Include map zoom as state
)
def display_image_marker(contents, trail, zoom):
    markers = []
    if not trail:
        return [dash.no_update]
    gpx_path = os.path.join('data/trails', f'{trail}.gpx')
    trail_points = gpx_to_points(gpx_path).coords
    # Start and finish markers with a custom className for targeting
    start_marker = dl.Marker(
        position=trail_points[0],
        children=[dl.Tooltip("Start")],
        icon={
            "iconUrl": 'assets/start.png',
            "iconSize": [zoom * 10, zoom * 10],  # Dynamically adjust based on zoom
            "className": "dynamic-icon3"
        }
    )
    finish_marker = dl.Marker(
        position=trail_points[-1],
        children=[dl.Tooltip("Finish")],
        icon={
            "iconUrl": 'assets/finish.png',
            "iconSize": [zoom * 10, zoom * 10],  # Dynamically adjust based on zoom
            "className": "dynamic-icon3"
        }
    )
    markers.extend([start_marker, finish_marker])
    # Image markers
    if not df_uploads.empty:
        filtered_df = df_uploads[df_uploads.apply(lambda row: is_within_distance((row['upload_lat'], row['upload_long']), trail_points), axis=1)]
        for _, row in filtered_df.iterrows():
            image_url = db_img(row['upload_img'])
            image_element = html.Img(src=image_url, style={'width': '100px', 'height': 'auto'})
            image_marker = dl.Marker(
                position=[row['upload_lat'], row['upload_long']],
                children=[dl.Tooltip(children=[image_element])],
                icon={
                    "iconUrl": 'assets/species.png',
                    "iconSize": [zoom * 5, zoom * 7],  
                    # "className": "dynamic-icon"  # Use this class to adjust the icon size via JS if needed
                }
            )
            markers.append(image_marker)
    return [markers]

@callback(
    [Output('mytrail-layer', 'children'), Output('mytrail-map', 'center')],
    [Input('mytrail-search-dropdown', 'value')]
)
def update_map(trail_name):
    if not trail_name:
        return [], dash.no_update
    gpx_path = os.path.join('data/trails', f'{trail_name}.gpx')
    line_string = gpx_to_points(gpx_path)
    centroid = line_string.centroid.coords[0]
    positions = list(line_string.coords)
    features = [dl.Polyline(positions=positions, color='blue')]
    return features, centroid

@callback(
    Output('url', 'pathname'),
    [Input('my-trail-link', 'n_clicks')],
)
def update_url(n_clicks):
    if n_clicks:
        return '/my-trail'
