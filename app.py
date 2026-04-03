import dash
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.BOOTSTRAP]

# Add suppress_callback_exceptions=True here!
app = dash.Dash(
    __name__, 
    use_pages=True, 
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True 
)

app.title = "Minimal Dash App"