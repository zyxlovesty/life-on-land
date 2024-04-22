import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import pandas as pd
import base64
import os

# Assuming you have a database connection function get_session() and a DataFrame df containing species data
from database import get_session

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash.register_page(__name__, title='WildStep Species Trails')

session, connection = get_session()

df = pd.read_sql('SELECT * FROM trails', con=connection)

def load_species_names():
    species_set = set()
    for species_list in df['trail_species'].str.split(','):
        species_set.update([species.strip() for species in species_list])
    return [{'label': species, 'value': species} for species in sorted(species_set)]

def b64_image(img_path):
    with open(img_path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode('utf-8')
    
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
    url_path = f'/species/{format_species_name_for_url(species_name)}'
    return dbc.Card(
        dbc.CardBody([
            dbc.Button([
                dbc.CardImg(src=b64_image(image_path), top=True, style={'width': '230px', 'height': '200px', 'object-fit': 'cover'}),
                html.H5(species_name, className="card-title text-center", style={'color':'#F9F1E8', 'margin-top':'10px'})
            ], id={'type': 'species-btn', 'index': species_name}, color="link", style={"text-decoration": "none", "color": "inherit"}),
        ]),
        style={"width": "18rem", "margin": "10px", "background-color": "#545646"}
    )

def build_trail_card(trail):
    trail_name = trail['trail_name']
    # image_src = f"data/trail_img/{trail_name}.jpg"  # Ensure this path is correct
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
                        html.P(f'{trail_name}', style={'margin-left': '30px', 'text-align': 'justify', 'font-size':'2em', 'color': '#545646'}),
                        html.P(description, style={'margin-left': '30px', 'text-align': 'justify', 'color':'#545646'}),
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
            ], style={'margin': '0 30px', 'display': 'flex', 'padding': '40px', 'border': '1.5px solid', 'border-color': '#545646', 'border-radius': '50px', 'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
                      'margin-top': '20px', 'margin-bottom': '20px'})
    
    return trail_card

species_list = load_species_names()
cards_per_page = 4

layout = html.Div([
    dbc.Container([
        dbc.Button("Back to all species", id="back-btn", style={'display': 'none'}),
        html.H3("",id="species-title", style={'display': 'none', 'color': '#545646'}),
        dcc.Dropdown(
            id='species-search-dropdown',
            options=load_species_names(),
            searchable=True,
            clearable=True,
            placeholder='Search for species...',
            style={
                'width': '70%',
                'margin': '0 auto',
                'borderRadius': '20px',
                'fontFamily': '"Poppins", sans-serif',
                'fontSize': '16px',
                'margin-bottom': '30px'
            }
        ),
        dbc.Row(id='card-container', children=[
            dbc.Col(create_species_card(species['value']), width=3) for species in species_list[:cards_per_page]
        ], justify="around", style={'padding': '20px', 'margin-top': '40px'}),
        dbc.Row([
            dbc.Col(dbc.Button("Previous", id="prev-btn", className="me-2", style={
                'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top': '30px'}), width="auto"),
            dbc.Col(dbc.Button("Next", id="next-btn", className="ms-2", style={
                'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top': '30px'}), width="auto")
        ], justify="center", className="my-4"),
    ], style={'padding': '50px', 'margin-top': '40px'})
])

@callback(
    [Output('card-container', 'children'),
     Output('species-search-dropdown', 'style'),
     Output('back-btn', 'style'),
     Output('prev-btn', 'style'),
     Output('next-btn', 'style'),
     Output('species-title', 'children'),
     Output('species-title', 'style')],
    [Input('next-btn', 'n_clicks'),
     Input('prev-btn', 'n_clicks'),
     Input('species-search-dropdown', 'value'),
     Input({'type': 'species-btn', 'index': ALL}, 'n_clicks'),
     Input('back-btn', 'n_clicks')],
    prevent_initial_call=True
)
def update_ui(n_clicks_next, n_clicks_prev, selected_species, species_btn_clicks, back_click):
    ctx = dash.callback_context

    if not ctx.triggered:
        raise PreventUpdate

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if 'back-btn' in button_id:
        # Reset to the default view with all species cards and controls visible
        return ([dbc.Col(create_species_card(species['value']), width=3) for species in species_list[:cards_per_page]],
                {'width': '70%','margin': '0 auto','borderRadius': '20px','fontFamily': '"Poppins", sans-serif','fontSize': '16px','margin-bottom': '30px'}, 
                {'display': 'none'},  # Hide back button
                {'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top': '30px'}, 
                {'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top': '30px'},
                "", {'display': 'none'})  # Show prev and next buttons

    if 'species-btn' in button_id:
        # Display trails for selected species and hide other controls
        species_name = eval(button_id)['index']
        return (display_trails_for_species(species_name),
                {'display': 'none'}, 
                {'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top': '30px'},  # Show back button
                {'display': 'none'}, {'display': 'none'},
                f"Trails where you can spot {species_name}", {'display': 'block', 'color': '#545646', 'margin-top': '40px', 'margin-bottom': '20px'})  # Hide prev and next buttons

    # Handle pagination or dropdown selection
    return handle_pagination_and_dropdown(button_id, selected_species)

def handle_pagination_and_dropdown(button_id, selected_species):
    page_number = getattr(update_ui, 'page_number', 0)

    if 'next-btn' in button_id:
        page_number += 1
    elif 'prev-btn' in button_id:
        page_number = max(0, page_number - 1)
    elif 'species-search-dropdown' in button_id:
        page_number = 0  # Reset the pagination on new selection

    setattr(update_ui, 'page_number', page_number)  # Save the new page number

    if selected_species:
        # Filter only the selected species
        filtered_species_list = [s for s in species_list if s['value'] == selected_species]
    else:
        filtered_species_list = species_list

    start_index = page_number * cards_per_page
    end_index = start_index + cards_per_page
    return ([dbc.Col(create_species_card(species['value']), width=3) for species in filtered_species_list[start_index:end_index]],
                {'width': '70%','margin': '0 auto','borderRadius': '20px','fontFamily': '"Poppins", sans-serif','fontSize': '16px','margin-bottom': '30px'}, 
                {'display': 'none'},  # Hide back button
                {'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top': '30px'}, 
                {'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top': '30px'},
                "", {'display': 'none'})


def display_trails_for_species(species_name):
    filtered_trails = df[df['trail_species'].str.contains(species_name, case=False)]
    trails_content = [build_trail_card(trail) for _, trail in filtered_trails.iterrows()]
    return trails_content

# if __name__ == '__main__':
#     app.run_server(debug=True)