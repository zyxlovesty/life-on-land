# app.py

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from main_layout import layout as main_layout
from home import layout as home_layout
from my_trails import layout as my_trails_layout

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname in ['/', '/home']:
        return home_layout
    elif pathname == '/my-trail':
        return my_trails_layout
    else:
        return '404 Page Not Found'

if __name__ == '__main__':
    app.run_server(debug=True)