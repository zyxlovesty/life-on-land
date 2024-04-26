from dash_extensions.enrich import DashProxy
from dash_extensions import Purify, DeferScript
from dash import html
import pandas as pd
import dash
import base64
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path="/events", title='WildStep Events')

df_events = pd.read_csv('data/event_data.csv')
# Group the cards into chunks of 4
chunks = [df_events.iloc[i:i+4] for i in range(0, df_events.shape[0], 4)]

# Create a list of dbc.Rows, each containing 4 cards
tabs = dbc.Tabs(
    [
        dbc.Tab(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardImg(src=row["Image"], top=True, alt="Event image", style={'height': '200px', 'object-fit': 'cover'}),
                                dbc.CardBody([
                                    html.H4(row["Title"], className="card-title"),
                                    html.P(f"Date: {row['Date']}", className="card-text"),
                                    html.P(f"Location: {row['Location']}", className="card-text"),
                                    dbc.Button("More Info", color="primary", href=row["URL"], target="_blank")
                                ])
                            ],
                            style={"width": "18rem"},  # Fixed width for consistency
                            className="m-3"  # Margin for spacing
                        )
                    ) for _, row in chunk.iterrows() if pd.notna(row["Image"])  # Check if image URL is not NaN
                ],
                className="justify-content-center"
            ), 
            label=f"{i+1}", tab_class_name="tab-label"
        ) for i, chunk in enumerate(chunks)
    ]  
)

def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

#app = DashProxy(assets_folder='assets')

layout = html.Div([
    
    
    html.Div(className="content", children=[
        html.Div(
            className="heading",
            children=[
                html.H1("Welcome to the Conservation Events page!", className="text-center mb-5"),
                html.P("Here you can find upcoming events related to conservation and community engagement.", className="text-center mb-5"),
                html.P("Discover, Participate, and Make a Difference!", className="text-center mb-5")
            ]
        ),
        html.Img(src=b64_image("assets/EVENT.png"), className='img')
    ]),

            
            
    dbc.Container([tabs 
        ],
        fluid=True,
        style={'marginTop': '50px'}  
    ),
    html.Div(className="card card-calendar", style={"height": "10%"}, children=[
        html.Div(className="card-body p-3", children=[
            html.Div(id="calendar", **{"data-bs-toggle": "calendar"})
        ])
    ]),
    DeferScript(src='assets/full_calendar_deferscript.js')              
])

