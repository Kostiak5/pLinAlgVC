# pages/home_layout.py
import dash
from dash import html

# path='/' makes this the default home page
dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1("Welcome to the Matrix Portal", style={'fontFamily': 'Arial'}),
    html.P("Use the navigation bar above to view the 2D and 3D matrix visualizations.", 
           style={'fontSize': '18px', 'color': '#555'}),
], style={'padding': '20px', 'textAlign': 'center'})