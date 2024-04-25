import dash
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
 
import base64
import pandas as pd
import numpy as np
import os
 
from database import get_session
 
_, connection = get_session()
 
dash.register_page(__name__, title='WildStep Species Trails')
 
df = pd.read_sql('SELECT * FROM trails', con=connection)
 
def load_species_names():
    species_path = 'data/species/'
    species_files = [f.split('.')[0] for f in os.listdir(species_path) if os.path.isfile(os.path.join(species_path, f))]
    return [{'label': s.replace('_', ' ').title(), 'value': s} for s in species_files]
 
def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
 
 
def filter_trails(selected_species, difficulty, duration, distance):

    formatted_selected_species = [x.replace('_',' ') for x in selected_species]

    conditions = [
        (df['trail_distance'] <= 5) & (df['trail_ele_gain'] <= 500),  # Easy
        (df['trail_distance'].between(5, 10)) & (df['trail_ele_gain'].between(500, 1000)),  # Medium
        (df['trail_distance'].between(10, 15)) & (df['trail_ele_gain'].between(1000, 1500)),  # Hard
        (df['trail_distance'] > 15) | (df['trail_ele_gain'] > 1500)  # Very Hard
    ]
    choices = ['easy', 'medium', 'hard', 'very hard']
    df['calculated_difficulty'] = np.select(conditions, choices, default='easy')
    
    # Initial strict filtering
    initial_filtered = df[
        (df['trail_species'].apply(lambda x: all(species in x for species in formatted_selected_species))) &
        (df['calculated_difficulty'] == difficulty) &
        (df['trail_duration'] <= int(duration)) &
        (df['trail_dist_mel'] <= int(distance))
    ]

    print("debug:", initial_filtered)
 
    if not initial_filtered.empty:
        print("debug@@")
        return initial_filtered, False  # Return False indicating no relaxation was needed
 
    # If no trails are found, relax to filtering by all selected species
    if selected_species:
        
        species_filter = df['trail_species'].apply(lambda x: all(species in x for species in formatted_selected_species))

        # Use the combined filter to select rows from the DataFrame
        species_filtered = df[species_filter]

        if not species_filtered.empty:
            
            return species_filtered, True  # Return True indicating some relaxation was needed
 
    # If still no trails, relax further to any one of the selected species
    for species in selected_species:
        single_species_filtered = df[df['trail_species'].str.contains(species, case=False, na=False)]
        if not single_species_filtered.empty:
            return single_species_filtered, True  # True to indicate relaxation to single species
 
    return pd.DataFrame(), True
 
 
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
    looped = ''
    if loop == 'one way':
        looped = 'No'
    elif loop == 'closed loop':
        looped = 'Yes'
       
    trail_card = dbc.Row([

        dbc.Col([
            html.Img(src=b64_image(f"data/trail_img/{trail_name}.jpg"),
                     style={'max-width': '100%', 'height': 'auto', 'max-height': '1000px', 'display': 'block', 'border-radius': '10px'})],width=3),
        dbc.Col([
            html.P(f'{trail_name}', style={'margin-left': '30px', 'text-align': 'justify', 'font-size':'1em', 'color': '#545646'}),
            html.P(description, style={'margin-left': '30px', 'text-align': 'justify', 'color':'#545646', 'font-size':'0.9em'})
        ], width=9),
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.I(
                        className="fas fa-clock", style={'color': '#808080', 'margin-right': '5px', 'margin-top': '20px', 'margin-left': '30px'}),
                    html.Span(f"How long you'll be hiking for: {duration}hours", style={'color': '#808080'}),
                    html.Div(""),
                    # Mountain icon
                    html.I(
                        className="fas fa-mountain", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '30px', 'margin-top': '15px'}),
                    html.Span(f"How steep it is: {elevation_gain}m", style={'color': '#808080'}),
                    html.Div(""),
                    # Route icon
                    html.I(
                        className="fas fa-route", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '30px', 'margin-top': '15px'}),
                    html.Span(f" How much distance you're covering: {distance}km", style={'color': '#808080'}),
                ], width=12),
                dbc.Col([
                    html.I(className="fas fa-solid fa-car",
                           style={'color': '#808080', 'margin-right': '5px',  'margin-left': '30px', 'margin-top': '15px'}),
                    html.Span(f"How long before you should leave from Melbourne: {time_mel}hours", style={'color': '#808080'}),
                    html.Div(""),
                    html.I(
                        className="fas fa-map-pin", style={'color': '#808080', 'margin-right': '5px',  'margin-left': '30px', 'margin-top': '15px'}),
                    html.Span(f"How far it is from Melbourne: {dist_mel}km", style={'color': '#808080'}),
                    html.Div(""),
                    html.I(
                        className="fas fa-redo", style={'color': '#808080', 'margin-right': '5px',  'margin-left': '30px', 'margin-top': '15px'}),
                    html.Span(f"Will you come back to the same place you parked: {looped}", style={'color': '#808080'}),
                ], width=12),
            ], style={'display': 'flex'}),
        ], width=12)
    ], style={'margin': '15%', 'display': 'flex', 'padding': '30px', 'border': '1.5px solid', 'border-color': '#545646', 'border-radius': '50px', 'box-shadow': '0 2px 4px rgba(0, 0, 0, 0.1)',
              'margin-top': '2%', 'margin-bottom': '5%'})
 
    return trail_card
 
layout = html.Div([
    html.Img(src=b64_image("assets/element2.png"),
                style={'width':'30%', 'height':'auto', 'z-index':'-1', 'margin-left':'83%', 'top':'0', 'position':'absolute'}),
   
    dbc.Container(children=[
        html.H1("Discover Your Next Hiking Adventure", className="text-center", style={"margin-top": "5%"}),
        html.P(
            "Embark on a journey tailored just for you! Answer a series of questions about what you're looking for in a hike, "
            "and we'll recommend the best trails that match your preferences.",
            className="lead", style={"padding": "5%", "font-size": "1.2em", 'text-align':'center'}
        ),
        dbc.Button("Customize your Trail", id="next-to-species", color="primary", className="d-block mx-auto", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}),
    ], id='home-container', style={"margin-top": "5%", 'padding':'5%', 'margin-bottom':'10%'}),
   
    dbc.Container(children=[
        html.H3("What specie(s) you want to see on your hike?", className='text-center'),
        dcc.Dropdown(
            id='species-search-dropdown',
            options=load_species_names(),
            searchable=True,
            clearable=True,
            multi=True,
            placeholder='Search for species...',
            style={
                'width': '50%',
                'height': '10%',
                'margin': '0 auto',
                'borderRadius': '20px',
                'fontFamily': '"Poppins", sans-serif',
                'fontSize': '16px',
                'margin-bottom': '5%',
                'margin-top': '5%'
            }
        ),
        html.Div(id='species-cards-container', style={'margin-right':'5%', 'margin-left':'18%'}),
        dbc.Button("Next: Difficulty Level >", id="next-to-difficulty", className="d-block mx-auto",
                   style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'5%'})
    ], id='species-container', style={"display":"none"}),
   
    dbc.Container(children=[
        html.H3("How much do you want to challenge yourself?", className='text-center'),
        dcc.RadioItems(
            options=[
                {'label': ' Take it easy', 'value': 'easy'},
                {'label': ' Push a Bit', 'value': 'medium'},
                {'label': ' Push further', 'value': 'hard'},
                {'label': ' Go all out', 'value': 'very hard'}
            ],
            value='Moderate',
            id='difficulty-radio',
            style={'margin-left':'35%', 'margin-top':'5%', 'margin-bottom':'5%', "font-size": "1.2em"}
        ),
        dbc.Row([
            dbc.Col(dbc.Button("< Back: Species", id="back-to-species", color="primary", className="d-block mx-auto", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}), width="auto"),
            dbc.Col(dbc.Button("Next: Duration of Hike >", id="next-to-duration", color="primary", className="d-block mx-auto", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}), width="auto")
        ], justify="center", className="my-4")
    ], id='difficulty-container', style={"display":"none"}),
   
    dbc.Container(children=[
        html.H3("For how long do you want to hike?", className='text-center'),
        dcc.RadioItems(
            options=[
                {'label': '  Less than 1 hour', 'value': '1'},
                {'label': '  Between 1 to 5 hours', 'value': '5'},
                {'label': '  Between 5 to 10 hours', 'value': '10'},
                {'label': '  More than 10 hours', 'value': '30'}
            ],
            value='1',
            id='duration-radio',
            style={'margin-left':'35%', 'margin-top':'5%', 'margin-bottom':'5%', "font-size": "1.2em"}
        ),
        dbc.Row([
            dbc.Col(dbc.Button("< Back: Difficulty", id="back-to-difficulty", color="primary", className="d-block mx-auto", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}), width="auto"),
            dbc.Col(dbc.Button("Next: Distance from Melbourne >", id="next-to-dist-mel", color="primary", className="d-block mx-auto", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}), width="auto")
        ], justify="center", className="my-4")
    ], id='duration-container', style={"display":"none"}),
       
    dbc.Container(children=[
        html.H3("How far you are willing to travel", className='text-center'),
        dcc.RadioItems(
            options=[
                {'label': '  Within 50km', 'value': '50'},
                {'label': '  Within 100km', 'value': '100'},
                {'label': '  Within 300km', 'value': '300'}
            ],
            value='50',
            id='distance-radio',
            style={'margin-left':'35%', 'margin-top':'5%', 'margin-bottom':'5%', "font-size": "1.2em"}
        ),
        dbc.Row([
            dbc.Col(dbc.Button("< Back: Duration", id="back-to-duration", color="primary", className="d-block mx-auto", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}), width="auto"),
            dbc.Col(dbc.Button("Recommend Hikes!", id="finish-quiz", color="primary", className="d-block mx-auto", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}), width="auto")
        ], justify="center", className="my-4")
    ], id='distance-container', style={"display":"none"}),
   
    dbc.Container(children=[
        dbc.Button("< Get new recommendations", id="new-recomm", color="primary", style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'0%'}),
        html.H3(id='text-result', children="Placeholder", style={'font-size':'1.2em', 'text-align':'left', 'margin-top':'5%', 'margin-bottom':'5%'}),
        html.Div(id='trail-cards')
    ], id='answer-container', style={"display":"none"}),
 
    html.Img(src=b64_image("assets/element3.png"),
             style={'width': '30%', 'height': 'auto', 'z-index': '-1', 'position': 'absolute', 'bottom': '2%', 'left': '-15%'}),
])
 
@callback(
    [
        Output('home-container', 'style'),
        Output('species-container', 'style'),
        Output('difficulty-container', 'style'),
        Output('duration-container', 'style'),
        Output('distance-container', 'style'),
        Output('answer-container', 'style')
    ],
    [
        Input('next-to-species', 'n_clicks'),
        Input('back-to-species', 'n_clicks'),
        Input('next-to-difficulty', 'n_clicks'),
        Input('back-to-difficulty', 'n_clicks'),
        Input('next-to-duration', 'n_clicks'),
        Input('back-to-duration', 'n_clicks'),
        Input('next-to-dist-mel', 'n_clicks'),
        Input('finish-quiz', 'n_clicks'),
        Input('new-recomm', 'n_clicks')
    ],
    prevent_initial_call=True
)
def update_quiz_content(start_clicks, back_species_clicks, next_difficulty_clicks, back_difficulty_clicks, next_dist_clicks, next_duration, back_duration, finish_clicks, new_recomm):
    ctx = dash.callback_context
 
    if not ctx.triggered:
        # If no button was clicked yet (this should never happen due to prevent_initial_call=True)
        raise PreventUpdate
 
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
 
    if button_id == 'next-to-species' or button_id == 'back-to-species' or button_id == 'new-recomm':
        return {"display":"none"}, {"margin-top": "5%", 'padding':'5%', 'margin-bottom':'10%'}, {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}
    elif button_id == 'next-to-difficulty' or button_id == 'back-to-difficulty':
        return {"display":"none"}, {"display":"none"}, {"margin-top": "5%", 'padding':'5%', 'margin-bottom':'10%'}, {"display":"none"}, {"display":"none"}, {"display":"none"}
    elif button_id == 'next-to-duration' or button_id == 'back-to-duration':
        return {"display":"none"}, {"display":"none"}, {"display":"none"}, {"margin-top": "5%", 'padding':'5%', 'margin-bottom':'10%'}, {"display":"none"}, {"display":"none"}
    elif button_id == 'next-to-dist-mel':
        return {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}, {"margin-top": "5%", 'padding':'5%', 'margin-bottom':'10%'}, {"display":"none"}
    elif button_id == 'finish-quiz':
        # Here you can handle the completion of the quiz, maybe showing results or a thank you message
        return {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}, {"display":"none"}, {"margin-top": "5%", 'padding':'5%', 'margin-bottom':'10%'}
 
    raise PreventUpdate
 
@callback(
    Output('species-cards-container', 'children'),
    Input('species-search-dropdown', 'value')
)
def update_species_cards(selected_species):
    if not selected_species:
        return []
    return [
            dbc.Card([
                # Convert the species name back to the filename format
                dbc.CardImg(src=b64_image(f"data/species/{species.replace(' ', '_').lower()}.jpg"), top=True, style={'width': '180px', 'height': '150px', 'object-fit': 'cover', 'margin-top':'5%', 'margin-left':'12%'}),
                dbc.CardBody([
                    # Display the species name as it appears in the dropdown
                    html.P(species.replace("_", " "), className="card-title text-center", style={'color':"#545646", 'text-align':'center'}),
                ])
            ], className="d-inline-flex m-2", style={"width": "15rem", "margin": "5px", "background-color": "#F9F1E8", 'border':'2.5px solid #545646', 'borderRadius': '15px'})
        for species in selected_species
    ]
   
@callback(
    [Output('trail-cards', 'children'),
     Output('text-result', 'children')],  # Assuming 'match-info' is an element to display match info
    [Input('finish-quiz', 'n_clicks')],
    [State('species-search-dropdown', 'value'),
     State('difficulty-radio', 'value'),
     State('duration-radio', 'value'),
     State('distance-radio', 'value')]
)
def display_results(n_clicks, selected_species, selected_difficulty, selected_duration, selected_distance):
    if not n_clicks:
        raise PreventUpdate
 
    filtered_trails, was_relaxed = filter_trails(selected_species, selected_difficulty, selected_duration, selected_distance)
    if filtered_trails.empty:
        return [], "Can't find matches for your preferences, retake the quiz & adjust them!"
 
    cards = [build_trail_card(trail) for index, trail in filtered_trails.iterrows()]
    match_message = "Trails based on your preferences" if not was_relaxed else "Can't find matches for your preferences, but we think you should check this out!"
    return cards, match_message
 