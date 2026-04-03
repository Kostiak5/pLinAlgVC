# main.py
import dash
from dash import html
from app import app
from components.navigation import navbar

# Define the root layout that surrounds all pages
app.layout = html.Div([
    navbar(),             # The navigation bar stays at the top
    dash.page_container   # Dash injects home_layout or analytics_layout here!
])

if __name__ == '__main__':
    # Run this file with: python main.py
    app.run(debug=True)