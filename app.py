# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 21:03:20 2025

@author: Javiera
"""

# --- Layout adaptado para móviles ---
app.layout = html.Div(style={
    'backgroundColor': '#f9f9f9',
    'fontFamily': 'Arial',
    'padding': '20px'
}, children=[

    html.H1("Interfaz monitoreo presión arterial y saturación", style={
        'textAlign': 'center',
        'color': '#555'
    }),

    # --- Tarjetas ---
    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'gap': '20px',
        'marginTop': '20px',
        'flexWrap': 'wrap'
    }, children=[
        html.Div(id='tarjeta_sis', style={
            'backgroundColor': '#a3d5ff',
            'padding': '20px',
            'borderRadius': '15px',
            'textAlign': 'center',
            'flex': '1 1 220px',
            'minWidth': '150px',
            'boxShadow': '3px 3px 15px #ccc'
        }),
        html.Div(id='tarjeta_dia', style={
            'backgroundColor': '#ffd6a3',
            'padding': '20px',
            'borderRadius': '15px',
            'textAlign': 'center',
            'flex': '1 1 220px',
            'minWidth': '150px',
            'boxShadow': '3px 3px 15px #ccc'
        }),
        html.Div(id='tarjeta_spo', style={
            'backgroundColor': '#a3ffb8',
            'padding': '20px',
            'borderRadius': '15px',
            'textAlign': 'center',
            'flex': '1 1 220px',
            'minWidth': '150px',
            'boxShadow': '3px 3px 15px #ccc'
        }),
    ]),

    html.Hr(),

    # --- Inputs y botones ---
    html.Div(style={
        'display': 'flex',
        'justifyContent': 'center',
        'gap': '15px',
        'flexWrap': 'wrap'
    }, children=[
        html.Div([
            html.Label("Presión Sistólica (mmHg)"),
            dcc.Input(id='input_sistolica', type='number', placeholder='mmHg',
                      style={'width': '100%', 'maxWidth': '100px'})
        ]),
        html.Div([
            html.Label("Presión Diastólica (mmHg)"),
            dcc.Input(id='input_diastolica', type='number', placeholder='mmHg',
                      style={'width': '100%', 'maxWidth': '100px'})
        ]),
        html.Div([
            html.Label("SpO₂ (%)"),
            dcc.Input(id='input_spo2', type='number', placeholder='%',
                      style={'width': '100%', 'maxWidth': '100px'})
        ]),
        html.Button("Guardar medición", id='guardar_btn', n_clicks=0, style={
            'backgroundColor': '#69b3e7',
            'border': 'none',
            'padding': '12px 20px',
            'borderRadius': '8px',
            'color': 'white',
            'fontWeight': 'bold',
            'cursor': 'pointer'
        }),
        html.Button("Borrar historial", id='borrar_btn', n_clicks=0, style={
            'backgroundColor': '#e76f51',
            'border': 'none',
            'padding': '12px 20px',
            'borderRadius': '8px',
            'color': 'white',
            'fontWeight': 'bold',
            'cursor': 'pointer'
        }),
        html.Button("Guardar Excel", id='guardar_excel', n_clicks=0, style={
            'backgroundColor': '#2a9d8f',
            'border': 'none',
            'padding': '12px 20px',
            'borderRadius': '8px',
            'color': 'white',
            'fontWeight': 'bold',
            'cursor': 'pointer'
        })
    ]),

    html.Hr(),

    # --- Filtros de tiempo ---
    html.Div(style={'textAlign': 'center', 'marginBottom': '20px'}, children=[
        html.Label("Filtrar por rango de tiempo: "),
        dcc.RadioItems(
            id='filtro_tiempo',
            options=[
                {'label': 'Último día', 'value': '1d'},
                {'label': 'Última semana', 'value': '7d'},
                {'label': 'Último mes', 'value': '30d'},
                {'label': 'Todo', 'value': 'all'}
            ],
            value='all',
            inline=True
        )
    ]),

    # --- Gráficos ---
    html.Div(style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'marginTop': '20px',
        'flexWrap': 'wrap'
    }, children=[
        dcc.Graph(id='grafico_sistolica', style={'flex': '1 1 300px', 'minWidth': '250px', 'height': '300px'}),
        dcc.Graph(id='grafico_diastolica', style={'flex': '1 1 300px', 'minWidth': '250px', 'height': '300px'}),
        dcc.Graph(id='grafico_spo2', style={'flex': '1 1 300px', 'minWidth': '250px', 'height': '300px'}),
    ]),

    html.Hr(),

    # --- Tabla historial ---
    html.Div(id='tabla_historial', style={'marginTop': '20px', 'overflowX': 'auto'}),

    # --- Descargar archivo ---
    dcc.Download(id="descargar_excel")
])


