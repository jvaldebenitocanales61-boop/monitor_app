# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 21:03:20 2025

@author: Javiera
"""

import pandas as pd
from dash import Dash, html, dcc, Input, Output, State
import plotly.express as px
from datetime import datetime, timedelta
import os

ARCHIVO = "mediciones.csv"

# --- Crear o limpiar archivo inicial ---
if os.path.exists(ARCHIVO):
    df = pd.read_csv(ARCHIVO)
    if not df.empty:
        df = df[['Fecha', 'Sistólica', 'Diastólica', 'SpO2']]
        df = df.dropna()
        df = df[(df['Sistólica'] != 0) & (df['Diastólica'] != 0) & (df['SpO2'] != 0)]
        df.to_csv(ARCHIVO, index=False)
else:
    df = pd.DataFrame(columns=["Fecha", "Sistólica", "Diastólica", "SpO2"])
    df.to_csv(ARCHIVO, index=False)

# --- Crear app Dash ---
app = Dash(__name__)
app.title = "Monitor PA & SpO₂"

# --- Layout ---
app.layout = html.Div(style={'backgroundColor': '#f9f9f9', 'fontFamily': 'Arial', 'padding': '20px'}, children=[
    html.H1("Interfaz monitoreo presión arterial y saturación", style={'textAlign': 'center', 'color': '#555'}),

    # Tarjetas
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '30px', 'marginTop': '20px'}, children=[
        html.Div(id='tarjeta_sis', style={'backgroundColor': '#a3d5ff', 'padding': '30px', 'borderRadius': '15px',
                                          'textAlign': 'center', 'width': '220px', 'boxShadow': '3px 3px 15px #ccc'}),
        html.Div(id='tarjeta_dia', style={'backgroundColor': '#ffd6a3', 'padding': '30px', 'borderRadius': '15px',
                                          'textAlign': 'center', 'width': '220px', 'boxShadow': '3px 3px 15px #ccc'}),
        html.Div(id='tarjeta_spo', style={'backgroundColor': '#a3ffb8', 'padding': '30px', 'borderRadius': '15px',
                                          'textAlign': 'center', 'width': '220px', 'boxShadow': '3px 3px 15px #ccc'}),
    ]),

    html.Hr(),

    # Entradas y botones
    html.Div(style={'display': 'flex', 'justifyContent': 'center', 'gap': '15px', 'flexWrap': 'wrap'}, children=[
        html.Div([
            html.Label("Presión Sistólica (mmHg)"),
            dcc.Input(id='input_sistolica', type='number', placeholder='mmHg', style={'width': '100px'})
        ]),
        html.Div([
            html.Label("Presión Diastólica (mmHg)"),
            dcc.Input(id='input_diastolica', type='number', placeholder='mmHg', style={'width': '100px'})
        ]),
        html.Div([
            html.Label("SpO₂ (%)"),
            dcc.Input(id='input_spo2', type='number', placeholder='%', style={'width': '100px'})
        ]),
        html.Button("Guardar medición", id='guardar_btn', n_clicks=0,
                    style={'backgroundColor': '#69b3e7', 'border': 'none', 'padding': '12px 20px',
                           'borderRadius': '8px', 'color': 'white', 'fontWeight': 'bold', 'cursor': 'pointer'}),
        html.Button("Borrar historial", id='borrar_btn', n_clicks=0,
                    style={'backgroundColor': '#e76f51', 'border': 'none', 'padding': '12px 20px',
                           'borderRadius': '8px', 'color': 'white', 'fontWeight': 'bold', 'cursor': 'pointer'}),
        html.Button("Guardar Excel", id='guardar_excel', n_clicks=0,
                    style={'backgroundColor': '#2a9d8f', 'border': 'none', 'padding': '12px 20px',
                           'borderRadius': '8px', 'color': 'white', 'fontWeight': 'bold', 'cursor': 'pointer'})
    ]),

    html.Hr(),

    # Filtros de tiempo
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

    # Gráficos
    html.Div(style={'display': 'flex', 'justifyContent': 'space-around', 'marginTop': '20px', 'flexWrap': 'wrap'}, children=[
        dcc.Graph(id='grafico_sistolica', style={'width': '30%'}),
        dcc.Graph(id='grafico_diastolica', style={'width': '30%'}),
        dcc.Graph(id='grafico_spo2', style={'width': '30%'})
    ]),

    html.Hr(),

    # Tabla historial
    html.Div(id='tabla_historial', style={'marginTop': '20px'}),

    # Descargar archivo
    dcc.Download(id="descargar_excel")
])

# --- Callbacks ---
@app.callback(
    Output('grafico_sistolica', 'figure'),
    Output('grafico_diastolica', 'figure'),
    Output('grafico_spo2', 'figure'),
    Output('tarjeta_sis', 'children'),
    Output('tarjeta_dia', 'children'),
    Output('tarjeta_spo', 'children'),
    Output('tabla_historial', 'children'),
    Output("descargar_excel", "data"),
    Input('guardar_btn', 'n_clicks'),
    Input('borrar_btn', 'n_clicks'),
    Input('guardar_excel', 'n_clicks'),
    Input('filtro_tiempo', 'value'),
    State('input_sistolica', 'value'),
    State('input_diastolica', 'value'),
    State('input_spo2', 'value')
)
def actualizar_dashboard(n_guardar, n_borrar, n_excel, filtro, sistolica, diastolica, spo2):
    ctx = dash.callback_context
    triggered = ctx.triggered_id if ctx.triggered else None
    descargar = None

    if os.path.exists(ARCHIVO):
        df = pd.read_csv(ARCHIVO)
    else:
        df = pd.DataFrame(columns=["Fecha", "Sistólica", "Diastólica", "SpO2"])

    # Guardar medición
    if triggered == 'guardar_btn' and sistolica and diastolica and spo2:
        nueva = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), sistolica, diastolica, spo2]],
                             columns=["Fecha", "Sistólica", "Diastólica", "SpO2"])
        nueva.to_csv(ARCHIVO, mode='a', header=False, index=False)
        df = pd.read_csv(ARCHIVO)

    # Borrar historial
    elif triggered == 'borrar_btn':
        df = pd.DataFrame(columns=["Fecha", "Sistólica", "Diastólica", "SpO2"])
        df.to_csv(ARCHIVO, index=False)

    # Guardar Excel
    elif triggered == 'guardar_excel':
        if not df.empty:
            nombre_excel = "mediciones_guardadas.xlsx"
            df.to_excel(nombre_excel, index=False)
            descargar = dcc.send_file(nombre_excel)

    # Filtrar por tiempo
    if not df.empty:
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        ahora = datetime.now()
        if filtro == '1d':
            df = df[df['Fecha'] >= (ahora - timedelta(days=1))]
        elif filtro == '7d':
            df = df[df['Fecha'] >= (ahora - timedelta(days=7))]
        elif filtro == '30d':
            df = df[df['Fecha'] >= (ahora - timedelta(days=30))]

    # Gráficos
    colores = ['#a3d5ff', '#ffd6a3', '#a3ffb8']
    fig_sis = px.line(df, x="Fecha", y="Sistólica", title="Presión Sistólica (mmHg)", markers=True)
    fig_dia = px.line(df, x="Fecha", y="Diastólica", title="Presión Diastólica (mmHg)", markers=True)
    fig_spo = px.line(df, x="Fecha", y="SpO2", title="Saturación de Oxígeno (%)", markers=True)

    for fig, color in zip([fig_sis, fig_dia, fig_spo], colores):
        fig.update_traces(line=dict(color=color, width=3), marker=dict(size=8, color=color))
        fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9', font_color='#555',
                          xaxis_title='Fecha', yaxis_title='Valor')

    # Tarjetas
    if not df.empty:
        ultima = df.iloc[-1]
        tarjeta_sis = [html.H2(f"{ultima['Sistólica']} mmHg"), html.P("Sistólica")]
        tarjeta_dia = [html.H2(f"{ultima['Diastólica']} mmHg"), html.P("Diastólica")]
        tarjeta_spo = [html.H2(f"{ultima['SpO2']} %"), html.P("SpO₂")]
    else:
        tarjeta_sis = tarjeta_dia = tarjeta_spo = [html.H2("--"), html.P("Sin datos")]

    # Tabla
    tabla = html.Table(
        [html.Tr([html.Th(col) for col in df.columns])] +
        [html.Tr([html.Td(df.iloc[i][col]) for col in df.columns]) for i in range(len(df))]
    )

    return fig_sis, fig_dia, fig_spo, tarjeta_sis, tarjeta_dia, tarjeta_spo, tabla, descargar


# --- Ejecutar app ---
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000)
