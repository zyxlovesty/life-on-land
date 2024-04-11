import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html, Input, Output, State, ClientsideFunction, callback, clientside_callback
from database import *

dash.register_page(__name__, path="/")

session, connection = get_session()

external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    dbc.themes.MINTY
]


years = ['2019', '2020', '2021', '2022', '2023']
new_species_counts = [39, 19, 44, 37, 144]

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='trigger_gsap_animation'),
    Output('dummy-output', 'children'),
    [Input('dummy-input', 'children')]
)
#  Pie chart data
labels = ['Extinct', 'Critically Endangered', 'Endangered', 'Vulnerable']
values = [53, 556, 1081, 308]
# colors = ['#4d7c8a', '#cf8b86', '#836a7f', '#e7e0db']
colors = ['#836a7f', '#cf8b86', '#e7e0db', '#4d7c8a']
pie_chart = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors))])
pie_chart.update_layout(
    plot_bgcolor='#112434',  # Background color
    paper_bgcolor='#112434',  # Paper color
    font=dict(color='#ffffff'),  # Text color
    title='Endangered Species Distribution',
    title_x=0.5,

    # title_y=0.5
    # margin=dict(t=0, b=0, l=0, r=0),  # Margins
)
for i in range(len(pie_chart.layout.shapes)):
    pie_chart.layout.shapes[i].update(dict(type='circle', xref='paper', yref='paper',
                                      x0=0, y0=0, x1=1, y1=1, line=dict(color='#112434', width=2)))


layout = html.Div([

    dcc.Location(id='url', refresh=False),

    html.Section(className='parallax', children=[
        html.P('Discover the Natural Wonders of Victoria', id='text'),
        html.P('Your Gateway to Conservation and Adventure',
               id='text2'),
        html.Img(src='/assets/monutain_01.png', id='m1'),
        html.Img(src='/assets/trees_02.png', id='t2'),
        html.Img(src='/assets/monutain_02.png', id='m2'),
        html.Img(src='/assets/trees_01.png', id='t1'),
        html.Img(src='/assets/man.png', id='man'),
        html.Img(src='/assets/plants.png', id='plants')
    ]),
    html.Div(id='dummy-input', style={'display': 'none'}),
    html.Div(id='dummy-output', style={'display': 'none'}),
    # For the divs with id="right", place the icon after the text
    html.Div([
        html.H6([
            "Every trail you explore can be a step towards conservation. Learn about the unique flora and fauna that make Victoria a biodiversity hotspot.",
            html.I(className="fas fa-seedling", style={'margin-left': '10px', 'color': '#fff'})
        ], style={'margin-top': '20px', 'margin-bottom': '10px', 'color': '#fff'})
    ], id="right1", style={'background-color': '#112434', 'border': '2px solid white', 'padding': '40px', 'border-radius': '50px', 'margin-right': '150px', 'margin-top': '40px'}),

    # For the divs with id="left", place the icon before the text
    html.Div([
        html.H6([
            html.I(className="fas fa-exclamation-triangle", style={'margin-right': '10px', 'color': '#fff'}),
            "In just one year, the number of endangered species in regional Victoria has surged from 57 to 144 due to environmental changes and human activities."
        ], style={'margin-top': '20px', 'margin-bottom': '10px', 'color': '#fff', 'text-align': 'right'})
    ], id="left1", style={'background-color': '#112434', 'border': '2px solid white', 'padding': '40px', 'border-radius': '50px', 'margin-left': '150px', 'margin-top': '40px'}),

    # Use our interactive maps and filters to find trails...
    html.Div([
        html.H6([
            "Use our interactive maps and filters to find trails where you can encounter Victoria's endangered and native species in their natural habitat.",
            html.I(className="fas fa-map-marked-alt", style={'margin-left': '10px', 'color': '#fff'})
        ], style={'margin-top': '20px', 'margin-bottom': '10px', 'color': '#fff'})
    ], id="right2", style={'background-color': '#112434', 'border': '2px solid white', 'padding': '40px', 'border-radius': '50px', 'margin-right': '150px', 'margin-top': '40px'}),

    # Share your findings...
    html.Div([
        html.H6([
            html.I(className="fas fa-share-alt", style={'margin-right': '10px', 'color': '#fff'}),
            "Share your findings and get the latest updates on conservation efforts, upcoming events, and new trail discoveries. Together, we can make a difference!"
        ], style={'margin-top': '20px', 'margin-bottom': '10px', 'color': '#fff', 'text-align': 'right'})
    ], id="left2", style={'background-color': '#112434', 'border': '2px solid white', 'padding': '40px', 'border-radius': '50px', 'margin-left': '150px', 'margin-top': '40px'}),
    html.Section(children=[
        dbc.Row([
            dbc.Col(
                html.Div(children=[
                    # html.H1(children='New Endangered Species Counts Over Years'),
                    dcc.Graph(
                        id='species-line-chart',
                        figure={
                            'data': [
                                go.Scatter(
                                    x=years,
                                    y=new_species_counts,
                                    mode='lines+markers',
                                    marker=dict(color='#fff'),
                                    line=dict(color='#fff')
                                ),
                            ],
                            'layout': go.Layout(
                                plot_bgcolor='#112434',
                                paper_bgcolor='#112434',
                                font=dict(color='#fff'),
                                xaxis=dict(title='Year', color='#fff'),
                                yaxis=dict(title='New Endangered Species Count', color='#fff'),
                                title=dict(text='Endangered Species Counts Over Years', font=dict(color='#fff')),
                                margin=dict(l=100),
                            )
                        }
                    )
                ], style={'borderRadius': '50px', 'overflow': 'hidden'}), id='line_c'),
            dbc.Col(html.Div(children=[dcc.Graph(figure=pie_chart)],
                    style={'borderRadius': '50px', 'overflow': 'hidden'}), id='pie')
        ])
    ], style={'margin-top': '40px', 'padding': '40px'})
])

# if __name__ == '__main__':
#     app.run_server(debug=True)
