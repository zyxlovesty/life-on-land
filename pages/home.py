import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
from dash import dcc, html, Input, Output, State, ClientsideFunction, callback, clientside_callback
from database import *
import base64

dash.register_page(__name__, path="/")

session, connection = get_session()

external_stylesheets = [
    'https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700,800,900&display=swap',
    '/assets/style.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css',
    dbc.themes.MINTY
]

def b64_image(img):
    with open(img, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')

years = ['2019', '2020', '2021', '2022', '2023']
new_species_counts = [39, 19, 44, 37, 144]
graph_component = dcc.Graph(
    id='species-line-chart',
    figure={
        'data': [
            go.Scatter(
                x=years,
                y=new_species_counts,
                mode='lines+markers',
                marker=dict(color='#F9F1E8'),
                line=dict(color='#F9F1E8')
            ),
        ],
        'layout': go.Layout(
            plot_bgcolor='#545646',
            paper_bgcolor='#545646',
            font=dict(color='#F9F1E8'),
            xaxis=dict(title='Year', color='#F9F1E8'),
            yaxis=dict(title='New Endangered Species Count', color='#F9F1E8'),
            title=dict(text='Endangered Species Counts Over Years', font=dict(color='#F9F1E8')),
            margin=dict(l=100),
        )
    }
)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='trigger_gsap_animation'),
    Output('dummy-output', 'children'),
    [Input('dummy-input', 'children')]
)

clientside_callback(
    ClientsideFunction(namespace='clientside', function_name='scroll_to_text'),
    # Dummy output, we don't actually need to update anything in the layout
    Output('dummy-output-2', 'children'),
    [Input('learn-more-btn', 'n_clicks')]
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
        dbc.Row([
            dbc.Col([
                # html.Img(src='/assets/element1.png', style={'margin-right':'2500px', 'height':'100%', 'width':'70%', 'margin-left':'0px'}),
                html.H1('Discover.', style={'font-size': '3em'}),
                html.P(""),
                html.H1('Educate.', style={'font-size': '3em'}),
                html.P(""),
                html.H1('Conserve.', style={'font-size': '3em'}),
                html.P(""),
                html.P("Join us in exploring and", style={'font-size': '2em'}),
                html.P("protecting Victoria's biodiversity", style={'font-size': '2em'}),
                html.Button("Learn More", id="learn-more-btn", n_clicks=0, 
                            style={'text-decoration': 'none', 'padding': '6px 15px', 'background': '#545646', 'color': '#F9F1E8', 'border-radius': '20px', 'margin-top':'30px'}),
            ], id='t1', width=6, lg=7, style={'margin-right':'900px'}),  # This sets the column to take half of the row (6 out of 12 columns)
            dbc.Col([
                html.Img(src='/assets/element2.png', id='t2', style={'height': '85%', 'width': '55%', 'margin-left':'1150px', 'margin-bottom':'170px'}),
                html.Img(src='/assets/home.png', id='t2', style={'height': '60%', 'width': '37%', 'margin-left':'1000px', 'margin-right':'30%', 'margin-bottom':'120px', 'border': '10px solid #545646', 'border-radius': '20px'})
            ], width=6, lg=5)  # This sets the other column also to take half of the row
        ], style={'display': 'flex'})
        # html.Button()
    ]),
    html.Div([
        html.Div([
            html.Div([
                html.P("The number of endangered species in Victoria rose significantly in the past year.", style={'padding': '30px', 'color': '#F9F1E8', 'font-size': '1.5em', 'margin-top': '40px'}),
                html.P(""),
                html.P("> Participate in conservation and seasonal activities around you to safeguard endangered species in Victoria.", style={'color': '#F9F1E8', 'font-size':'1em', 'margin-left':'40px'}),
                html.P(""),
                html.P("> Navigate through the diverse flora and fauna around you through the myriad of hiking options.", style={'color': '#F9F1E8', 'font-size':'1em', 'margin-left':'40px'}),
                html.P(""),
                html.P("> Get updated with species found on your hike real-time.", style={'color': '#F9F1E8', 'font-size':'1em', 'margin-left':'40px'}),
                html.P(""),
                html.P("> Explore the Victorian biodiversity with us.", style={'color': '#F9F1E8', 'font-size':'1em', 'margin-left':'40px'}),
                # html.P(""),
                # Position the retract button absolutely within the relatively positioned parent div
                html.Button("^", id="retract-btn", style={
                    'position': 'absolute',
                    'top': '10px',
                    'right': '10px',
                    'padding': '10px 20px',
                    'font-size': '16px',
                    'cursor': 'pointer',
                    'background-color': '#545646',
                    'color': '#F9F1E8',
                    'border': 'none',
                    'border-radius': '5px'
                })
            ], style={'position': 'relative', 'flex': '1', 'padding': '20px'}),  # Parent div must be positioned relatively
            html.Div([graph_component], style={'flex': '1', 'padding': '20px'})
        ], style={'display': 'flex'})
    ], id="additional-content", style={'display': 'none'}),
    html.Div([
        html.Div([
            html.A(href="/my-trails", children=[
                html.Img(src=b64_image('assets/circle1.png'), style={'width': '100%', 'height': 'auto'}),
                html.P("Over 30 venomous species", className="default-text", style={'top': '50%', 'left': '55%'}),
                html.P("Get real-time updates on your hike", className="hover-text", style={'top': '50%', 'left': '55%'})
            ], className="circle", id='right2'),
            html.A(href="/all-trails", children=[
                html.Img(src=b64_image('assets/circle2.png'), style={'width': '100%', 'height': 'auto'}),
                html.P("140 new endangered species", className="default-text", style={'top': '50%', 'left': '50%'}),
                html.P("Get trails based on species you want to see", className="hover-text", style={'top': '50%', 'left': '50%'})
            ], className="circle"),
            html.A(href="/page3", children=[
                html.Img(src=b64_image('assets/circle3.png'), style={'width': '100%', 'height': 'auto'}),
                html.P("2700 conservation parks", className="default-text", style={'top': '55%', 'left': '55%'}),
                html.P("Discover conservation events around you", className="hover-text", style={'top': '55%', 'left': '55%'})
            ], className="circle", id='left1')
        ], style={'display': 'flex', 'justify-content': 'space-around', 'align-items': 'center', 'padding': '50px'})
    ]),
    
    html.Div(id='dummy-input', style={'display': 'none'}),
    html.Div(id='dummy-output', style={'display': 'none'}),
    html.Div(id='dummy-output-2', style={'display': 'none'})
])

@callback(
    Output('additional-content', 'style'),
    [Input('learn-more-btn', 'n_clicks'), Input('retract-btn', 'n_clicks')],
    [State('additional-content', 'style')]
)
def toggle_additional_content(learn_more_clicks, retract_clicks, current_style):
    triggered_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'learn-more-btn' and learn_more_clicks:
        return {
                'background-color': '#545646',
                'border': '2px solid white',
                'padding': '10px',
                'border-radius': '15px',
                'margin-left': '20px',
                'margin-right': '20px'
                } if current_style['display'] == 'none' else {'display': 'none'}
    elif triggered_id == 'retract-btn':
        return {'display': 'none'}
    return current_style


# if __name__ == '__main__':
#     app.run_server(debug=True)
