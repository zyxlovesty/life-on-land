import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate

# Register the page in the Dash app
dash.register_page(__name__)

# Assuming data is loaded into a DataFrame called df_events
df_events = pd.read_csv('data/event_data.csv')

def layout():
    # Card components for each event
    cards = dbc.Row(
        [dbc.Col(dbc.Card(
            [
                dbc.CardImg(src=df_events.loc[i, "Image"], top=True, alt="Event image", style={'height': '200px', 'object-fit': 'cover'}),
                dbc.CardBody([
                    html.H4(df_events.loc[i, "Title"], className="card-title"),
                    html.P(f"Date: {df_events.loc[i, 'Date']}", className="card-text"),
                    html.P(f"Location: {df_events.loc[i, 'Location']}", className="card-text"),
                    dbc.Button("More Info", color="primary", href=df_events.loc[i, "URL"], target="_blank")
                ])
            ],
            style={"width": "18rem"},  # Fixed width for consistency
            className="m-3"  # Margin for spacing
        )) for i in df_events.index if pd.notna(df_events.loc[i, "Image"])],  # Check if image URL is not NaN
        className="justify-content-center"
    )

    # Page layout
    return dbc.Container(
        [
            html.H1("Events", className="text-center mb-4"),
            html.P("Explore upcoming events related to conservation and community engagement.", className="text-center mb-5"),
            cards
        ],
        fluid=True  # Use the full width of the page
    )