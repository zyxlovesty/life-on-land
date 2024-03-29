import dash
from dash import html, dcc
import dash_leaflet as dl
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, ClientsideFunction
import galah # Import the galah package
import pandas as pd

# Initialize galah session (replace with actual commands for galah session initialization)
'''galah.galah_config(atlas="Australia",email="yzha0317@student.monash.edu",reason='education')

# Example function to fetch species occurrence data
def fetch_species_data(species_name):
    # Fetch data for a given species (adjust query as needed)
    occurrences = galah.atlas_occurrences(taxa=species_name,filters="year=2023")
    
    # Convert to DataFrame
    df = pd.DataFrame(occurrences)
    return df

species_data = fetch_species_data("Litoria fallax")'''
# Initialize the Dash app
app = dash.Dash(__name__)

# External CSS
external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets,external_scripts=[
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/gsap.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/gsap/3.5.1/ScrollTrigger.min.js'
])

'''markers = [
    dl.Marker(position=[row['latitude'], row['longitude']],
              children=[dl.Tooltip(row['species_name']), dl.Popup("Additional info here")])
    for index, row in species_data.iterrows()
]'''

# App layout
app.layout = html.Div([
    html.Header([
        html.A('InSync', href='#', className='logo'),
        html.Ul([
            html.Li(html.A('Home', href='#', className='active')),
            html.Li(html.A('My Trail', href='#')),
            html.Li(html.A('About', href='#')),
        ], className='navigation')
    ]),
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
        html.H2('Trail in Vic'),
        dcc.Input(type='text', placeholder='Search another trail...'
        ),
        html.P('Start your journey'),
    ]),
    html.Section([
        dl.Map([dl.TileLayer(),  dl.LayerGroup(id="layer")], id='mapid', style={'width': '100%', 'height': '500px'}, center=(-37.4713, 144.7852), zoom=9)
    ])
])

#app.layout = app.layout + gdc.Import(src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js") + gdc.Import(src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/ScrollTrigger.min.js")


app.clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='trigger_gsap_animation'),
    Output('dummy-output', 'children'),
    [Input('dummy-input', 'children')]
)

if __name__ == '__main__':
    app.run_server(debug=True)
