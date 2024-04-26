# app.py

import dash
from dash import dcc
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State
from dash import callback

# External CSS
external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    dbc.themes.MINTY
]

                
app = dash.Dash(__name__, 
                use_pages=True,
                external_stylesheets=external_stylesheets,
                external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/gsap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/ScrollTrigger.min.js'],
                suppress_callback_exceptions=True,
                prevent_initial_callbacks="initial_duplicate", update_title=None,
                title='WildStep')


from pages import home
from pages import my_trails
from pages import explore_species


server = app.server

# Define modal content
modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Password Required", close_button=False),
                dbc.ModalBody(
                    [
                        html.Label("Password:"),
                        dcc.Input(id="password-input", type="password", autoComplete="off"),
                        html.Div(id="password-error-message", style={"color": "red"})
                    ]
                ),
                dbc.ModalFooter(
                    dbc.Button("Submit", id="submit-button", color="primary")
                ),
            ],
            id="modal",
            is_open=True,  # Open the modal by default
            centered=True,
            backdrop="static",  # Disable clicking outside to close
            keyboard=False, #Disable pressing escape key to close

        ),
    ]
)

app.layout = html.Div([
    modal,
    dcc.Location(id='url', refresh=False),  # Add dcc.Location component
    dbc.Row([
        dbc.Col(
            html.Header([
                html.A('WildStep', href='#', className='logo'),
                html.Ul([
                    html.Li(dcc.Link('Home', href='/', id='home-link', className='navigation-link')),
                    html.Li(dcc.Link('My Trail', href='/my-trails', id='my-trails-link', className='navigation-link')),
                    html.Li(dcc.Link('Explore Species', href='/explore-species', id='explore-species-link', className='navigation-link')),
                    html.Li(dcc.Link('Events', href='/events', id='events-link', className='navigation-link')),
                ], className='navigation'),
            ], className='fixed-top', style={
                'background-color': '#F9F1E8',  # Light beige background
                'box-shadow': '0 4px 6px rgba(0,0,0,0.1)',  # Soft shadow for depth
                'border-bottom': '2px solid #333'  # Dark border for definition
            })  # Updated style with shadow and border
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
    [
     Output('home-link', 'className'),
     Output('my-trails-link', 'className'),
     Output('explore-species-link', 'className'),
     Output('events-link', 'className')
     ],
    [Input('url', 'pathname')]
)

def update_active_link(pathname):
    home_class = 'active' if pathname == '/home' or pathname == "/" else ''
    my_trails_class = 'active' if pathname == '/my-trails' else ''
    explore_species_class = 'active' if pathname == '/explore-species' else ''
    events_class = 'active' if pathname == '/events' else ''
    return home_class, my_trails_class, explore_species_class, events_class


# Callback to handle password submission
@app.callback(
    [Output("modal", "is_open"),
    Output("password-error-message", "children")],
    [Input("submit-button", "n_clicks")],
    [State("password-input", "value")],
)

def check_password(n_clicks, password):
    if n_clicks:
        # Check if the password is correct
        #if password == "314x~7!ZPGy!":
        if password == "abc":
            return False, ""  # Close the modal if password is correct
        else:
            return True, "Incorrect password entered"  # Keep the modal open if password is incorrect, display error message
    return True, ""  # Keep the modal open if the button hasn't been clicked yet

if __name__ == '__main__':
    #app.run_server(debug=False, host="0.0.0.0", port=8080)
    app.run_server(debug=True)