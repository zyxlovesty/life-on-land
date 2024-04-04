import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import pandas as pd

external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',  # Font Awesome link
    '/assets/style.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('data/50_trails.csv', encoding='utf-8')

def load_trail_names():
    return [{'label': name, 'value': name} for name in df['name'].unique()]

def create_trail_card(trail_name, duration, elevation_gain, distance):
    return dbc.Card(
        dbc.CardBody([
            html.H3(html.A(trail_name, href=f'/{trail_name.replace(" ", "-")}', 
                           style={'color': '#112434', 'text-decoration': 'none', 'margin-bottom': '8px'})),  # Trail name in main color
            html.Div([
                html.I(className="fas fa-clock", style={'color': '#808080', 'margin-right': '5px'}),
                html.Span(f"Duration: {duration}hours", style={'color': '#808080'}),  # Light grey color
                html.I(className="fas fa-mountain", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '10px'}),  # Mountain icon
                html.Span(f"Elevation Gain: {elevation_gain}m", style={'color': '#808080'}),
                html.I(className="fas fa-route", style={'color': '#808080', 'margin-right': '5px', 'margin-left': '10px'}),  # Route icon
                html.Span(f" Distance: {distance}km", style={'color': '#808080'}),
            ], style={'font-size': '14px', 'margin-bottom': '30px'})  # Smaller font size
        ])
    )

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
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
    
    html.Section(className='sec', children=[
        html.H2('Trails in Victoria'),
        dcc.Dropdown(
            id='trail-search-dropdown',
            options=load_trail_names(),
            searchable=True,
            placeholder='Search for trails...',
            style={
                'width':'600px',
                'padding': '12px',
                'margin-top': '10px',
                'margin-right': '16px',
                'font-size': '16px',
                'border-radius': '30px'
            }
        )
    ]),

    html.Div(id='trail-cards-row'),  # Add an empty Div element with id 'trail-cards-row'

    html.Div(id='trail-info')
])


@app.callback(
    [Output('trail-cards-row', 'children'),
     Output('trail-info', 'children')],
    [Input('url', 'pathname'),
     Input('trail-search-dropdown', 'value')]
)
def update_trail_info(pathname, search_input):
    # Extract trail name from pathname (assuming pathname is '/<trail_name>')
    url = pathname[1:]  # Remove the leading '/'
    if len(url) == 0:
        # Display trail cards based on search dropdown value
        if search_input is None or search_input == '':
            filtered_trails = df
        else:
            filtered_trails = df[df['name'].str.contains(search_input, case=False)]

        cards = [
            dbc.Col(create_trail_card(row['name'], row['duration'], row['elevation_gain'], row['distance']), width=4)
            for index, row in filtered_trails.iterrows()
        ]
        return html.Div(className='trail-cards', style={'padding-top': '20px', 'margin-left': '20px'}, children=[
            dbc.Row(id='trail-cards-row', children=cards)
        ]), None
    else:
        # Display trail info based on URL pathname
        splitname = [x.split('-') for x in url.split('---')]
        trail_name = ' - '.join([' '.join(x) for x in splitname])
        trail_info = df[df['name'] == trail_name]['description'].values[0]
        return None, html.Div([
            html.H2(trail_name, style={'color': '#112434', 'text-decoration': 'none', 'margin-bottom': '8px'}),
            html.P(trail_info)
        ], style={'max-width': '800px', 'margin': '0 auto', 'padding': '20px', 'padding-top': '50px'})

if __name__ == '__main__':
    app.run_server(debug=True)
