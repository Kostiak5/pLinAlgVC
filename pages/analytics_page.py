import dash
from dash import dcc, html, Input, Output, callback, State
import plotly.graph_objects as go
import numpy as np
from pages.analytics_eval.evaluator import Evaluator

dash.register_page(__name__, name="Analytics")

STYLE_PRESETS = {
    'font_wide': 'Michroma, sans-serif'
}

tab_style = {
    'padding': '10px', 'fontWeight': 'bold', 'border': 'none', 
    'backgroundColor': '#e9e9e9', 'color': '#888',
    'fontFamily': STYLE_PRESETS['font_wide'], 'cursor': 'pointer',
    'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
}

tab_selected_style = {
    'padding': '10px', 'fontWeight': 'bold', 'border': 'none',
    'backgroundColor': '#333333', 'color': 'white',
    'fontFamily': STYLE_PRESETS['font_wide'], 'cursor': 'default',
    'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'
}

evaluator = []

# --- 1. Graph Logic (Now accepts dynamic vectors) ---
def create_2d_vectors(custom_title, vectors):
    fig = go.Figure()
    
    # Define a color palette for dynamic vectors
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'cyan']
    
    for i, v in enumerate(vectors):
        color = colors[i % len(colors)]
        # Add dummy trace for legend
        fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(color=color, width=3), name=f'Vector {i+1}'))
        # Draw Arrow
        fig.add_annotation(
            x=v[0], y=v[1], ax=0, ay=0, xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor=color
        )

    fig.update_layout(
        title=custom_title,
        xaxis=dict(title='X Axis', range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='black'),
        yaxis=dict(title='Y Axis', range=[-10, 10], zeroline=True, zerolinewidth=2, zerolinecolor='black'),
        margin=dict(l=40, r=40, b=40, t=40), showlegend=True
    )
    return fig

def create_3d_vectors(custom_title, vectors):
    fig = go.Figure()
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'cyan']
    
    for i, v in enumerate(vectors):
        color = colors[i % len(colors)]
        # Ensure 3D (pad with 0 if user only typed X and Y)
        z_val = v[2] if len(v) > 2 else 0.0 
        
        # Line
        fig.add_trace(go.Scatter3d(
            x=[0, v[0]], y=[0, v[1]], z=[0, z_val],
            mode='lines', name=f'Vector {i+1}', line=dict(color=color, width=6)
        ))
        # Arrowhead (Cone)
        fig.add_trace(go.Cone(
            x=[v[0]], y=[v[1]], z=[z_val], u=[v[0]], v=[v[1]], w=[z_val], 
            sizemode="absolute", sizeref=0.8, anchor="tip", 
            colorscale=[[0, color], [1, color]], showscale=False, showlegend=False, hoverinfo='skip'
        ))
        
    fig.update_layout(
        title=custom_title,
        scene=dict(
            xaxis=dict(range=[-10, 10], title='X'), 
            yaxis=dict(range=[-10, 10], title='Y'), 
            zaxis=dict(range=[-10, 10], title='Z')
        ),
        margin=dict(l=40, r=40, b=40, t=40)
    )
    return fig

# --- 2. Page Layout ---
def layout():
    evaluator = Evaluator()
    return html.Div([
        # LEFT COLUMN
        html.Div([
            html.H3("Settings", style={'color': '#333333', 'borderBottom': '1px solid #ccc', 'paddingBottom': '10px'}),

            html.Div([
                html.Label("View Mode:", style={'fontWeight': 'bold', 'color': '#333333', 'display': 'block', 'marginBottom': '10px'}),
                html.Div([
                    dcc.Tabs(id='view-toggle', value='3D', children=[
                            dcc.Tab(label='2D', value='2D', style=tab_style, selected_style=tab_selected_style),
                            dcc.Tab(label='3D', value='3D', style=tab_style, selected_style=tab_selected_style),
                        ], style={'height': '40px'})
                ], style={'borderRadius': '6px', 'overflow': 'hidden', 'border': '1px solid #ccc'})
            ], style={'marginBottom': '30px'}),
            
            # --- NEW: Smart Matrix Input ---
            html.Div([
                html.Label("Data Matrix (Space = Col, Enter = Row):", style={'fontWeight': 'bold', 'color': '#333333', 'display': 'block', 'marginBottom': '5px', 'fontSize': '12px'}),
                dcc.Textarea(
                    id='matrix-input-area',
                    value="", # Default starting vectors
                    style={'width': '100%', 'height': '250px', 'padding': '10px', 'boxSizing': 'border-box', 'borderRadius': '4px', 'border': '1px solid #ccc', 'fontFamily': 'monospace', 'fontSize': '16px'}
                ),
                dcc.Input(
                    id='command-input',
                    type='text',
                    placeholder='Type here and press Enter to clear...',
                    style={'width': '100%', 'padding': '10px', 'marginTop': '10px', 'boxSizing': 'border-box'}
                ),
                # Visual feedback area showing parsed cells
                html.Div(id='parsed-cells-feedback', style={'marginTop': '10px', 'padding': '10px', 'backgroundColor': '#fff', 'borderRadius': '4px', 'border': '1px solid #eee', 'minHeight': '50px'})
            ])
            
        ], style={
            'width': '320px', 'minHeight': '100vh', 'backgroundColor': "#f9f9f9",
            'borderRight': '1px solid #ddd', 'padding': '20px', 'boxSizing': 'border-box',
            'display': 'flex', 'flexDirection': 'column'
        }),
        
        # RIGHT COLUMN
        html.Div([
            html.H2("Vector Visualization Tool", style={'textAlign': 'center', 'marginTop': '20px', 'color': '#333'}),
            dcc.Graph(id='matrix-graph', style={'height': '75vh'}) 
        ], style={'flex': 1, 'padding': '20px', 'backgroundColor': '#ffffff'})
        
    ], style={'display': 'flex', 'flexDirection': 'row', 'fontFamily': STYLE_PRESETS['font_wide'], 'margin': '-8px'})



# --- 3. The Callbacks ---
@callback(
    Output('matrix-graph', 'figure'),
    Output('parsed-cells-feedback', 'children'),
    Output('matrix-input-area', 'value'),
    Output('command-input', 'value'),
    Input('view-toggle', 'value'),         
    State('matrix-input-area', 'value'),
    State('command-input', 'value'),
    Input('command-input', 'n_submit')
)
def e_update_graph_and_matrix(selected_view, matrix_text, command_text, enter_pressed):
    processed_title = command_text.strip().upper() if command_text else "UNTITLED VECTORS"
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None
    # 1. Parse the text area into numerical vectors
    vectors = []
    informator_rows = [] # To build the visual cell feedback
    
    if triggered_id == 'command-input' and enter_pressed:
        # default_fig = create_3d_vectors("CLEARED", [[1, 1, 1]]) if selected_view == '3D' else create_2d_vectors("CLEARED", [[1, 1, 1]])
        
        if matrix_text:
            lines = matrix_text.strip().split('\n')
            vectors, informator_rows = create_graph_from_matrix(lines)
        # Fallback if empty or invalid
        if not vectors or len(vectors) == 0:
            vectors = [] 
            informator_rows = [html.Div("Awaiting valid numbers...", style={'color': '#999', 'fontStyle': 'italic'})]

        # Generate Graph
        if selected_view == '2D':
            fig = create_2d_vectors(processed_title, vectors)
        else:
            fig = create_3d_vectors(processed_title, vectors)
        return fig, informator_rows, "", ""
    
    return fig, informator_rows, 

def create_graph_from_matrix(lines):
    vectors = []
    informator_rows = []
    for line in lines:
        try:
            # Split by space and convert to float
            line_params = line.split()
            # if line_params[0] in evaluator.get_commands():
            #     new_line = evaluator.parse_line_input(line_params)
            # else:
            vec = [float(val) for val in line.split() if val.strip()]
            if len(vec) >= 2: # Need at least X and Y
                vectors.append(vec[:3]) # Cap at 3 dimensions (Z)
                # Create the visual HTML cells for feedback
                cells = [html.Span(str(val), style={'padding': '4px 8px', 'marginRight': '5px', 'backgroundColor': '#e0e0e0', 'borderRadius': '4px', 'display': 'inline-block'}) for val in vec[:3]]
                informator_rows.append(html.Div(cells, style={'marginBottom': '5px'}))
        except ValueError:
            pass # Ignore lines with incomplete typing
    return vectors, informator_rows

