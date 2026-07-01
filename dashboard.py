import dash
from dash import dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
import numpy as np
from datetime import datetime

# Load data from database
def load_data():
    conn = sqlite3.connect('../data/nuwara_data.db')
    climate_df = pd.read_sql('SELECT * FROM climate_data', conn)
    wq_df = pd.read_sql('SELECT * FROM water_quality', conn)
    biodiv_df = pd.read_sql('SELECT * FROM biodiversity', conn)
    reports_df = pd.read_sql('SELECT * FROM reports', conn)
    conn.close()
    
    climate_df['date'] = pd.to_datetime(climate_df['date'])
    wq_df['date'] = pd.to_datetime(wq_df['date'])
    biodiv_df['date'] = pd.to_datetime(biodiv_df['date'])
    
    return climate_df, wq_df, biodiv_df, reports_df

climate_df, wq_df, biodiv_df, reports_df = load_data()

# Initialize Dash app
app = dash.Dash(__name__, title='Nuwara Eliya Environmental Dashboard')

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('🌿 Nuwara Eliya Environmental Dashboard', 
                style={'textAlign': 'center', 'color': '#1a3c34', 'padding': '20px 0'}),
        html.P('Environmental Monitoring & Data Analysis Platform', 
               style={'textAlign': 'center', 'color': '#555', 'marginBottom': '30px'})
    ], style={'backgroundColor': '#f0f4f3', 'borderBottom': '3px solid #2d6a4f'}),
    
    # Stats Row
    html.Div([
        html.Div([
            html.H3(f"{len(climate_df)}", style={'color': '#2d6a4f', 'margin': '0'}),
            html.P("Climate Records", style={'color': '#666', 'margin': '0'})
        ], style={'display': 'inline-block', 'width': '23%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 10px rgba(0,0,0,0.05)', 'margin': '0 1%'}),
        html.Div([
            html.H3(f"{len(wq_df)}", style={'color': '#2d6a4f', 'margin': '0'}),
            html.P("Water Quality Records", style={'color': '#666', 'margin': '0'})
        ], style={'display': 'inline-block', 'width': '23%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 10px rgba(0,0,0,0.05)', 'margin': '0 1%'}),
        html.Div([
            html.H3(f"{biodiv_df['species'].nunique()}", style={'color': '#2d6a4f', 'margin': '0'}),
            html.P("Total Species", style={'color': '#666', 'margin': '0'})
        ], style={'display': 'inline-block', 'width': '23%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 10px rgba(0,0,0,0.05)', 'margin': '0 1%'}),
        html.Div([
            html.H3(f"{len(reports_df)}", style={'color': '#2d6a4f', 'margin': '0'}),
            html.P("Reports Submitted", style={'color': '#666', 'margin': '0'})
        ], style={'display': 'inline-block', 'width': '23%', 'textAlign': 'center', 
                  'backgroundColor': 'white', 'padding': '15px', 'borderRadius': '10px',
                  'boxShadow': '0 2px 10px rgba(0,0,0,0.05)', 'margin': '0 1%'}),
    ], style={'padding': '20px', 'backgroundColor': 'white', 'marginBottom': '20px'}),
    
    # Filter Controls
    html.Div([
        html.Label('Select Time Period:', style={'fontWeight': 'bold'}),
        dcc.RangeSlider(
            id='year-slider',
            min=1990,
            max=2026,
            step=1,
            value=[2000, 2025],
            marks={i: str(i) for i in range(1990, 2027, 5)},
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px', 
              'marginBottom': '20px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'}),
    
    # Charts Row 1
    html.Div([
        html.Div([
            dcc.Graph(id='temperature-chart')
        ], style={'display': 'inline-block', 'width': '49%'}),
        html.Div([
            dcc.Graph(id='water-quality-chart')
        ], style={'display': 'inline-block', 'width': '49%', 'float': 'right'})
    ]),
    
    # Charts Row 2
    html.Div([
        html.Div([
            dcc.Graph(id='biodiversity-chart')
        ], style={'display': 'inline-block', 'width': '49%'}),
        html.Div([
            dcc.Graph(id='correlation-heatmap')
        ], style={'display': 'inline-block', 'width': '49%', 'float': 'right'})
    ]),
    
    # Reports Section
    html.Div([
        html.H3('📝 Recent Reports', style={'color': '#1a3c34'}),
        html.Div(id='reports-table', style={'maxHeight': '300px', 'overflowY': 'auto'})
    ], style={'padding': '20px', 'backgroundColor': 'white', 'borderRadius': '10px',
              'marginTop': '20px', 'boxShadow': '0 2px 10px rgba(0,0,0,0.05)'}),
    
    # Footer
    html.Div([
        html.P('Data Source: Nuwara Eliya Environmental Database | Academic Project 2026',
               style={'textAlign': 'center', 'color': '#888', 'fontSize': '12px', 'padding': '20px 0'})
    ])
])

@app.callback(
    [Output('temperature-chart', 'figure'),
     Output('water-quality-chart', 'figure'),
     Output('biodiversity-chart', 'figure'),
     Output('correlation-heatmap', 'figure'),
     Output('reports-table', 'children')],
    [Input('year-slider', 'value')]
)
def update_dashboard(selected_years):
    # Filter data by year
    start_year, end_year = selected_years
    filtered_climate = climate_df[
        (climate_df['date'].dt.year >= start_year) & 
        (climate_df['date'].dt.year <= end_year)
    ]
    
    # 1. Temperature Chart
    temp_fig = go.Figure()
    temp_fig.add_trace(go.Scatter(
        x=filtered_climate['date'], 
        y=filtered_climate['temperature'],
        mode='lines',
        name='Temperature',
        line=dict(color='#e74c3c', width=2)
    ))
    # Add trend line
    x_vals = np.arange(len(filtered_climate))
    if len(filtered_climate) > 0:
        z = np.polyfit(x_vals, filtered_climate['temperature'], 1)
        p = np.poly1d(z)
        temp_fig.add_trace(go.Scatter(
            x=filtered_climate['date'],
            y=p(x_vals),
            mode='lines',
            name='Trend Line',
            line=dict(color='blue', width=2, dash='dash')
        ))
    temp_fig.update_layout(
        title='Temperature Trend',
        xaxis_title='Year',
        yaxis_title='Temperature (°C)',
        template='plotly_white',
        height=400
    )
    
    # 2. Water Quality Chart
    wq_fig = px.box(
        wq_df, 
        x='site', 
        y='water_quality_index',
        color='site',
        title='Water Quality by Site',
        labels={'site': '', 'water_quality_index': 'WQI Score'},
        template='plotly_white'
    )
    # Add threshold lines
    wq_fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Good")
    wq_fig.add_hline(y=60, line_dash="dash", line_color="orange", annotation_text="Moderate")
    wq_fig.update_layout(height=400, showlegend=False)
    
    # 3. Biodiversity Chart
    species_by_site = biodiv_df.groupby('site')['species'].nunique().reset_index()
    biodiv_fig = px.bar(
        species_by_site,
        x='site',
        y='species',
        color='site',
        title='Species Count by Site',
        labels={'site': '', 'species': 'Species Count'},
        template='plotly_white'
    )
    biodiv_fig.update_layout(height=400, showlegend=False)
    
    # 4. Correlation Heatmap
    corr_cols = ['temperature', 'humidity', 'rainfall', 'wind_speed', 'pressure']
    corr_matrix = filtered_climate[corr_cols].corr()
    corr_fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_cols,
        y=corr_cols,
        colorscale='RdBu_r',
        zmin=-1,
        zmax=1,
        text=[[f"{val:.2f}" for val in row] for row in corr_matrix.values],
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    corr_fig.update_layout(
        title='Correlation Matrix',
        template='plotly_white',
        height=400
    )
    
    # 5. Reports Table
    if len(reports_df) > 0:
        reports_table = html.Table([
            html.Thead(
                html.Tr([
                    html.Th('Location', style={'padding': '8px', 'border': '1px solid #ddd'}),
                    html.Th('Type', style={'padding': '8px', 'border': '1px solid #ddd'}),
                    html.Th('Description', style={'padding': '8px', 'border': '1px solid #ddd'}),
                    html.Th('Date', style={'padding': '8px', 'border': '1px solid #ddd'})
                ])
            ),
            html.Tbody([
                html.Tr([
                    html.Td(row['location'], style={'padding': '8px', 'border': '1px solid #ddd'}),
                    html.Td(row['report_type'], style={'padding': '8px', 'border': '1px solid #ddd'}),
                    html.Td(row['description'][:50] + '...', style={'padding': '8px', 'border': '1px solid #ddd'}),
                    html.Td(row['date'][:10], style={'padding': '8px', 'border': '1px solid #ddd'})
                ]) for _, row in reports_df.iterrows()
            ])
        ], style={'width': '100%', 'borderCollapse': 'collapse'})
    else:
        reports_table = html.P('No reports submitted yet.')
    
    return temp_fig, wq_fig, biodiv_fig, corr_fig, reports_table

# 
if __name__ == '__main__':
    app.run(debug=True, port=8050)