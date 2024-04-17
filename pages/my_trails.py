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
from sqlalchemy.exc import SQLAlchemyError

from database import *

dash.register_page(__name__)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='trigger_gsap_animation'),
    Output('mytrail-dummy-output', 'children'),
    [Input('mytrail-dummy-input', 'children')]
)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='scroll_to_map'),
    # Dummy output, we don't actually need to update anything in the layout
    Output('mytrail-dummy-output-2', 'children'),
    [Input('mytrail-search-dropdown', 'value')]
)

session, connection = get_session()

external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    dbc.themes.MINTY
]

# df_uploads = pd.read_sql('SELECT * FROM uploads', con=connection)
df_trails = pd.read_sql('SELECT * FROM trails', con=connection)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'assets/lifeonland-418914-00a1094d16b6.json'


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
    route_points = [(float(pt.attrib['lat']), float(pt.attrib['lon']))
                    for pt in root.findall('.//default:trkpt', namespaces)]
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

    dcc.Geolocation(id='geo'),
    html.Section(className='parallax', children=[
        dbc.Row([
            dbc.Col([
                    html.H2('Get real time updates on your trail', id='text2',
                            style={'margin-right': '400%', 'margin-top': '20%', 'text-align': 'center'}),
                    dcc.Dropdown(
                        id='mytrail-search-dropdown',
                        options=load_trail_names(),
                        searchable=True,
                        placeholder="Tell us the trail you're on...",
                        style={
                            'width': '70%',  # Use 100% to make it responsive within the column
                            'margin': '0 auto',  # Keep it centered
                            'borderRadius': '20px',
                            'fontFamily': '"Poppins", sans-serif',
                            'fontSize': '16px',
                            'margin-top': '270px',
                            'borderWidth': '2px',
                            'borderColor': '#D9D9D9'
                        }
                    ),
                    ], width=6),
                dbc.Col([
                    html.Div([
                        html.H2('Explore your trail', style={'font-size': '3em', 'color': '#fff',
                                                             'margin-bottom': '10px', 'margin-top': '10px'}),
                        html.P("Embark on a journey through the heart of Victoria's trails, where every step you take reveals the delicate balance of life teeming with unique and endangered species that are struggling to survive.", style={
                            'font-size': '1em', 'color': '#fff'}),
                        html.P('Explore the diverse trails of Victoria with our carefully curated selection.',
                               style={'font-size': '1em', 'color': '#fff'}),
                        html.P("    "),
                        html.H4('Happy Hiking!', style={'margin-top': '20px', 'margin-bottom': '10px', 'color': '#fff'})
                    ], style={
                        'background-color': '#112434',
                        'border': '2px solid white',
                        'padding': '40px',
                        'border-radius': '15px',
                    })
                ], width=5)
                ]),
        html.Img(src='/assets/monutain_01.png', id='m1', style={'z-index': '-1', 'height': '50%'}),
        html.Img(src='/assets/trees_02.png', id='t2', style={'z-index': '-1', 'top': '357px', 'height': '60%'}),
        html.Img(src='/assets/monutain_02.png', id='m2', style={'z-index': '-1', 'height': '50%'}),
        html.Img(src='/assets/trees_01.png', id='t1', style={'z-index': '-1'}),
        # html.Img(src='/assets/man.png', id='man'),
        html.Img(src='/assets/plants.png', id='plants', style={'z-index': '-1'})
    ]),
    html.Div(id='scroll-trigger', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-input', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-output', style={'display': 'none'}),
    html.Div(id='mytrail-dummy-output-2', style={'display': 'none'}),
    html.Div(
        dbc.Row([
                dbc.Col([
                    # dl.Map(
                    #     id='mytrail-map',
                    #     children=[dl.TileLayer(), dl.LayerGroup(id='mytrail-layer'), dl.LayerGroup(id='myimage-layer')],
                    #     style={'width': '100%', 'height': '640px', 'margin-top': '40px',
                    #            'margin-bottom': '40px', 'margin-left': '20px'},
                    #     center=(-37.8136, 144.9631),
                    #     zoom=12
                    # )
                    dl.Map(
                        id='mytrail-map',
                        children=[
                            dl.TileLayer(),
                            dl.LayerGroup(id='mytrail-layer'),
                            dcc.Loading(  # Wrap the layer or component being updated with the loading indicator
                                id="loading-layer",
                                type="default",
                                children=dl.LayerGroup(id='myimage-layer')
                            )
                        ],
                        style={'width': '100%', 'height': '640px', 'margin-top': '40px',
                               'margin-bottom': '40px', 'margin-left': '20px'},
                        center=(-37.8136, 144.9631),
                        zoom=12
                    ),
                ], width=15, lg=7),  # Map takes up 6 columns on large screens, full width on smaller ones
                dbc.Col([
                    dbc.Row(justify="center", className="h-100 align-items-center", children=[
                        dbc.Col([
                            html.H4("See what other hikers have found on your trail",
                                    style={'color': '#fff', 'text-align': 'center'}),
                            html.P("   "),
                            html.P("Hover over each icon on the map to find the hike start and end points.",
                                   style={'color': '#fff', 'text-align': 'center'}),
                            html.P("   "),
                            html.P("Please share your location before seeing real-time updates",
                                   style={'color': '#fff', 'text-align': 'center'}),
                            dcc.Loading(
                                id="loading-upload",
                                type="default",  # Or any other type you prefer
                                children=[
                                    dcc.Upload(
                                        id='upload-image',
                                        children=html.Div([html.I(className="fas fa-solid fa-upload"),
                                                           '  Drag and Drop or Select Files'], style={'margin-top': '10px'}),
                                        style={'display': 'block', 'width': '100%', 'height': '50px',
                                               'color': '#112434', 'backgroundColor': '#fff', 'lineHeight': '50px',
                                               'border': 'none', 'borderRadius': '20px', 'textAlign': 'center',
                                               'cursor': 'pointer', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'},  # Initial style (disabled)
                                        accept='.png,.jpg,.jpeg,.heic',
                                        multiple=True
                                    ),
                                ]),
                            dbc.Tooltip("Please share your location & choose your trail to enable uploads.",
                                        target="upload-image",  # Match the id of dcc.Upload
                                        id="tooltip-upload",
                                        is_open=False,
                                        style={'display': 'block'}),
                            html.Div(id='upload-status', style={'margin-top': '30px', 'textAlign': 'center'})
                            # ])
                        ], width=10)  # Adjust width as needed for aesthetic preferences
                    ])
                ], width=9, lg=5, className="d-flex"),  # Make the column a flex container
                ], style={'backgroundColor': '#112434'})
    ),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Action Required")),
        dbc.ModalBody("Please select a trail before uploading."),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal", className="ms-auto", n_clicks=0))
    ], id="modal", is_open=False),
    dbc.Modal([
        dbc.ModalHeader("Location Sharing Required"),
        dbc.ModalBody("You need to share your location before getting real-time updates."),
        dbc.ModalFooter(dbc.Button("OK", id="close-location-modal", className="ms-auto", n_clicks=0))
    ], id="location-error-modal", is_open=False),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Too Far From Trail")),
        dbc.ModalBody("You are too far from the selected trail to upload images."),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-too-far-modal", className="ms-auto", n_clicks=0)
        )
    ], id="too-far-modal", is_open=False),
    dcc.Interval(
        id='interval-component',
        interval=2*1000,  # in milliseconds, e.g., 5*1000 for 5 seconds
        n_intervals=0
    )
])


@callback(
    [Output('upload-image', 'style'),
     Output('tooltip-upload', 'is_open'),
     Output('tooltip-upload', 'style')],
    [Input('geo', 'position'),
     Input('mytrail-search-dropdown', 'value')],
    [State('upload-image', 'style')]
)
def update_upload_style_and_tooltip(position, trail_value, style):
    # Check if both the location is shared (position is not None) and a trail is selected (trail_value is not None)
    if position and trail_value:
        return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#112434', 'backgroundColor': '#fff', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'auto',
                'cursor': 'pointer', 'transition': 'all 0.2s ease-in-out', 'opacity': '1'}, False, {'display': 'none'}
    elif position and not trail_value:
        return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#112434', 'backgroundColor': '#fff', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'none',
                'cursor': 'not-allowed', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'}, False, {'display': 'block'}
    elif trail_value and not position:
        return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#112434', 'backgroundColor': '#fff', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'none',
                'cursor': 'not-allowed', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'}, False, {'display': 'block'}
    else:
        return {'display': 'block', 'width': '100%', 'height': '50px',
                'color': '#112434', 'backgroundColor': '#fff', 'lineHeight': '50px',
                'border': 'none', 'borderRadius': '20px', 'textAlign': 'center', 'pointerEvents': 'none',
                'cursor': 'not-allowed', 'transition': 'all 0.2s ease-in-out', 'opacity': '0.6'}, False, {'display': 'block'}


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
     Input('geo', 'position'),
     Input('mytrail-search-dropdown', 'value')],
    [State('too-far-modal', 'is_open')],
    prevent_initial_call=True
)
# @callback(
#     Output('too-far-modal', 'is_open'),
#     [Input('close-too-far-modal', 'n_clicks'),
#      Input('geo', 'position')],
#     [State('mytrail-search-dropdown', 'value'),
#      State('too-far-modal', 'is_open')],
#     prevent_initial_call=True
# )
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
        return ""
    if position_error:
        # Handle case where geolocation failed
        return "Failed to get geolocation data."
    content_type, content_string = contents[0].split(',')  # Taking the first uploaded file
    image_bytes = content_string  # base64 encoded string of the first image
    latitude = position['lat']
    longitude = position['lon']
    decoded = base64.b64decode(content_string)
    try:
        detected_labels = detect_labels(decoded)
        labels = [l.description.lower() for l in detected_labels]
        if len(set(labels).intersection(set(get_unique_species(df_trails)))):
            species = list(set(labels).intersection(set(get_unique_species(df_trails))))[0].capitalize()
        else:
            species = detected_labels[0].description
    except:
        return "There was a problem in your image, try again"
    try:
        # Attempt to fetch data within a transaction
        session.begin()  # Start a new transaction
        last_row = session.query(Uploads).order_by(Uploads.upload_id.desc()).first()
        last_row_id = last_row.upload_id
        new_upload = Uploads(
            upload_id=last_row_id+1,
            upload_lat=latitude,
            upload_long=longitude,
            upload_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            upload_img=decoded,
            upload_species=species
        )
        session.add(new_upload)
        session.commit()
        session.close()
    except SQLAlchemyError as e:
        session.rollback()  # Roll back the transaction if an error occurs
        # print("Error fetching data from the database: ", e)
        return "There was a problem in your image, try again"

    return "Image uploaded successfully!"


@callback(
    [Output('myimage-layer', 'children')],
    [Input('upload-image', 'contents'),
     Input('mytrail-search-dropdown', 'value'),
     Input('geo', 'position'),
     Input('interval-component', 'n_intervals')],
    [State('mytrail-map', 'zoom')]  # Include map zoom as state
)
def display_image_marker(contents, trail, user_position, n, zoom):
    markers = []
    if not trail:
        return [dash.no_update]

    markers = []
    if not trail:
        return [dash.no_update]

    # Extract user's latitude and longitude from the position data
    if user_position:
        user_lat = user_position['lat']
        user_lon = user_position['lon']
        # Create a marker for the user's position
        user_marker = dl.Marker(
            icon={
                "iconUrl": 'assets/hiker.png',
                "iconSize": [zoom * 4, zoom * 4]
            },
            position=(user_lat, user_lon),
            children=[
                dl.Tooltip("You are here"),
                dl.Popup(f"Your location: Latitude {user_lat}, Longitude {user_lon}")
            ])
        markers.append(user_marker)

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
    try:
        session.begin()
        # df_uploads = pd.read_sql('SELECT * FROM uploads', con=connection)
        uploads = session.query(Uploads).all()
        df_uploads = pd.DataFrame(columns=['upload_id', 'upload_lat', 'upload_long',
                                           'upload_time', 'upload_img', 'upload_species'])
        for upload in uploads:
            df_uploads.loc[upload.upload_id-1, 'upload_id'] = upload.upload_id
            df_uploads.loc[upload.upload_id-1, 'upload_lat'] = upload.upload_lat
            df_uploads.loc[upload.upload_id-1, 'upload_long'] = upload.upload_long
            df_uploads.loc[upload.upload_id-1, 'upload_time'] = upload.upload_time
            df_uploads.loc[upload.upload_id-1, 'upload_img'] = upload.upload_img
            df_uploads.loc[upload.upload_id-1, 'upload_species'] = upload.upload_species
        session.close()
    except SQLAlchemyError as e:
        session.rollback()
        df_uploads = pd.DataFrame(columns=['upload_id', 'upload_lat', 'upload_long',
                                           'upload_time', 'upload_img', 'upload_species'])
    if not df_uploads.empty:
        print(df_uploads)
        filtered_df = df_uploads[df_uploads.apply(lambda row: is_within_distance(
            (row['upload_lat'], row['upload_long']), trail_points), axis=1)]
        for _, row in filtered_df.iterrows():
            image_url = db_img(row['upload_img'])
            image_element = html.Img(src=image_url, style={'width': '100px', 'height': 'auto'})
            image_marker = dl.Marker(
                position=[row['upload_lat'], row['upload_long']],
                children=[dl.Tooltip(children=[image_element, html.P(""), row['upload_species']])],
                icon={
                    "iconUrl": 'assets/species.png',
                    "iconSize": [zoom * 7, zoom * 5],
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