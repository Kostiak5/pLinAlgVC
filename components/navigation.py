# components/navigation.py
from dash import html, dcc

def navbar():
    return html.Div([
        # dcc.Link changes the page without refreshing the browser
        dcc.Link('Home', href='/', style={'marginRight': '20px', 'fontWeight': 'bold', 'textDecoration': 'none', 'color': '#007BFF'}),
        dcc.Link('Analytics', href='/analytics-page', style={'fontWeight': 'bold', 'textDecoration': 'none', 'color': '#007BFF'}),
    ], style={'padding': '15px', 'backgroundColor': '#f8f9fa', 'borderBottom': '2px solid #dee2e6', 'marginBottom': '20px'})