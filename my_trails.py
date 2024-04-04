import dash
from dash import dcc, html, Input, Output, State
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import xml.etree.ElementTree as ET
from shapely.geometry import LineString, Point
import os
import pandas as pd
from geopy.distance import geodesic
import base64

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# Dummy DataFrame for storing uploads - for demonstration purposes
df_uploads = pd.DataFrame(columns=['timestamp', 'latitude', 'longitude', 'image_bytes'])
# Adding a dummy entry
df_uploads = pd.DataFrame({
    'timestamp': ['2023-01-01 12:00:00', '2023-01-02 13:00:00', '2023-01-03 14:00:00'],
    'latitude': [-39.03112, -39.12374, -38.94000],
    'longitude': [146.32135, 146.42132, 146.35000],
    'image_bytes': [
        'https://via.placeholder.com/150/0000FF/808080',
        'https://via.placeholder.com/150/FF0000/FFFFFF',
        'https://via.placeholder.com/150/008000/FFFFFF'
    ]
})

def gpx_to_points(gpx_path):
    tree = ET.parse(gpx_path)
    root = tree.getroot()
    namespaces = {'default': 'http://www.topografix.com/GPX/1/1'}
    route_points = [(float(pt.attrib['lat']), float(pt.attrib['lon'])) for pt in root.findall('.//default:trkpt', namespaces)]
    return LineString(route_points)

def load_trail_names():
    df = pd.read_csv('data/50_trails.csv', encoding='utf-8')
    return [{'label': name, 'value': name} for name in df['name'].unique()]

def is_within_distance(point, trail_points, max_distance=500):
    return any(geodesic(point, trail_point).meters <= max_distance for trail_point in trail_points)

def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


app.layout = dbc.Container(fluid=True, children=[
    dbc.Row(justify="center", className="mb-3", children=[
        dbc.Col([
            dcc.Dropdown(
                id='trail-search-dropdown',
                options=load_trail_names(),
                searchable=True,
                placeholder='Search for trails...',
            )
        ], width=12, lg=6, style={'margin-bottom': '20px', 'margin-top': '20px'})
    ]),
    dbc.Row(justify="center", className="mb-3", children=[
        dbc.Col([
            dl.Map(
                id='trail-map',
                children=[dl.TileLayer(), dl.LayerGroup(id='trail-layer'), dl.LayerGroup(id='image-layer')],
                style={'width': '100%', 'height': '500px'},
                center=(-37.8136, 144.9631),
                zoom=12
            )
        ], width=12, lg=10)
    ]),
    dbc.Row(justify="center", className="mb-3", children=[
        dbc.Col([
            dbc.Button('Found something interesting? Upload your find!', id='find-btn', n_clicks=0, 
                       color="primary", className="me-1", 
                       style={'margin-left': '550px'}),
            html.Div(id='location-div', style={'display': 'none'}),
        dcc.Upload(
            id='upload-image',
            children=html.Div(['Drag and Drop or ', html.A('Select Files')]),
            style={
                'width': '100%', 'height': '60px', 'lineHeight': '60px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px auto', 'display': 'none'
            },
            accept='.png,.jpg,.jpeg,.heic',  # Limit file types
            multiple=True
            )

        ])
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
    ], id="too-far-modal", is_open=False),  # Changed ID here
    html.Div(id='upload-status', style={'display': 'none'})


])

@app.callback(
    Output('modal', 'is_open'),
    [Input('find-btn', 'n_clicks'), Input('close-modal', 'n_clicks')],
    [State('trail-search-dropdown', 'value'), State('modal', 'is_open')],
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

@app.callback(
    Output('location-div', 'children'),
    [Input('find-btn', 'n_clicks')],
    [State('trail-search-dropdown', 'value')]
)
def display_geolocation(n, selected_trail):
    if n > 0 and selected_trail:
        return dcc.Geolocation(id='geo')
    return []

@app.callback(
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

@app.callback(
    Output('too-far-modal', 'is_open'),
    [Input('close-too-far-modal', 'n_clicks'),
     Input('geo', 'position')],
    [State('trail-search-dropdown', 'value'),
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
        # Assuming you have a function to check if the user is within a certain distance to the trail
        if is_within_distance(user_position, trail_points):
            return False
        else:
            return True
    return is_open

@app.callback(
    [Output('find-btn', 'style'), Output('upload-image', 'style')],
    [Input('geo', 'local_date'), Input('geo', 'position_error'), Input('close-too-far-modal', 'n_clicks')],
    prevent_initial_call=True
)
def update_button_visibility(local_date, position_error, close_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # When the user has successfully shared location and not too far
    if triggered_id == 'geo' and local_date and not position_error:
        return {'display': 'none'}, {
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'display': 'block'
        }

    # When the user is too far and closes the modal, or if there's a position error
    if triggered_id in ('close-too-far-modal', 'geo') and (position_error or close_clicks > 0):
        return {'display': 'block', 'marginLeft': '550px'}, {'display': 'none'}

    return {'display': 'block', 'marginLeft': '550px'}, {'display': 'none'}

@app.callback(
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
    global df_uploads
    df_uploads = df_uploads.append({
        'timestamp': local_date,  # Use the date provided by the geolocation component
        'latitude': latitude,
        'longitude': longitude,
        'image_bytes': image_bytes
    }, ignore_index=True)
    print(df_uploads)
    return "Image uploaded successfully!"

@app.callback(
    [Output('image-layer', 'children')],
    [Input('upload-image', 'contents'),
     Input('trail-search-dropdown', 'value')],
    [State('trail-map', 'zoom')]  # Include map zoom as state
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
            "className": "dynamic-icon"
        }
    )
    finish_marker = dl.Marker(
        position=trail_points[-1],
        children=[dl.Tooltip("Finish")],
        icon={
            "iconUrl": 'assets/finish.png',
            "iconSize": [zoom * 10, zoom * 10],  # Dynamically adjust based on zoom
            "className": "dynamic-icon"
        }
    )
    markers.extend([start_marker, finish_marker])
    # Image markers
    if contents and not df_uploads.empty:
        filtered_df = df_uploads[df_uploads.apply(lambda row: is_within_distance((row['latitude'], row['longitude']), trail_points), axis=1)]
        for _, row in filtered_df.iterrows():
            image_url = row['image_bytes']
            image_element = html.Img(src=image_url, style={'width': '100px', 'height': 'auto'})
            image_marker = dl.Marker(
                position=[row['latitude'], row['longitude']],
                children=[dl.Popup(children=[image_element])],
                icon={
                    "iconUrl": image_url,
                    "iconSize": [zoom * 5, zoom * 5],  # Adjust size dynamically based on zoom
                    "className": "dynamic-icon"  # Use this class to adjust the icon size via JS if needed
                }
            )
            markers.append(image_marker)

    return [markers]




@app.callback(
    [Output('trail-layer', 'children'), Output('trail-map', 'center')],
    [Input('trail-search-dropdown', 'value')]
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


if __name__ == '__main__':
    app.run_server(debug=True)
