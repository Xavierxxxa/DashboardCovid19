import dash
from dash import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

CENTER_LAT, CENTER_LON = -14.272572694355336, -51.25567404158474

# =====================================================================
# Data Load
df_states = pd.read_csv("df_states.csv")
df_brasil = pd.read_csv("df_brasil.csv")
df_muni = pd.read_csv("df_muni.csv")
df_muni = df_muni[['estado', 'municipio', 'casosAcumulado','obitosAcumulado']]

#==========================================================================
# Filtro pela data maxima
df_brasil['data'] = pd.to_datetime(df_brasil['data'])

data_max = df_brasil['data'].max()
data_max = data_max.date()
data_max = str(data_max)


token = open(".mapbox_token").read()
brazil_states = json.load(open("geojson/brazil_geo.json", "r"))

brazil_states["features"][0].keys()

df_states_ = df_states[df_states["data"] == data_max]
select_columns = {"casosAcumulado": "Casos Acumulados", 
                "casosNovos": "Novos Casos", 
                "obitosAcumulado": "Óbitos Totais",
                "obitosNovos": "Óbitos por dia"}


# =====================================================================
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])


fig = px.choropleth_mapbox(df_states_, locations="estado",
    geojson=brazil_states, center={"lat": -16.95, "lon": -47.78},  # https://www.google.com/maps/ -> right click -> get lat/lon
    zoom=4, color="casosNovos", color_continuous_scale="Pubu", opacity=0.4,
    hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "obitosAcumulado": True, "estado": True}
    )
fig.update_layout(
                # mapbox_accesstoken=token,
                paper_bgcolor="#242424",
                mapbox_style="carto-darkmatter",
                autosize=True,
                margin=go.layout.Margin(l=0, r=0, t=0, b=0),
                showlegend=False,)
df_data = df_states[df_states["estado"] == "RO"]


fig2 = go.Figure(layout={"template":"plotly_dark"})
fig2.add_trace(go.Scatter(x=df_data["data"], y=df_data["casosAcumulado"]))
fig2.update_layout(
    paper_bgcolor="#242424", ##83ccbc
    plot_bgcolor="#242424",
    autosize=True,
    margin=dict(l=10, r=10, b=10, t=10),
    )


# =====================================================================
# Layout 
app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Row([
                dbc.Col([
                    html.Img(id="logo", src=app.get_asset_url("protecao.png"), height=150)
                ], width=3),
                dbc.Col([
                    html.H3(children="PAINEL DE INDICADORES COVID-19", style={
                        "font-family": "Quicksand", "font-weight": "800",
                        "margin-top": "60px", 'textAlign' : 'left', 'margin-right' : '350px', "color": "#FFFFFF"})
                ]),
            ],style={"background-color": "#3b5998", "width": "100%", "margin-left": "5px"}),
            html.Hr(style = {'size' : '50', 'borderColor':'#389fd6','borderHeight': "30vh", "width": "100%", "margin-top": "20px"}),
             html.P("Navegue pelos dados do Sistema Único de Saúde - SUS, com informações\
              estratégicas e conheça tudo sobre a COVID-19 de forma transparente e analítica.", style={"color": "#000000", "font-family": "Quicksand" , "font-weight": "800"}),
              html.P(f"Última Atualização: {data_max}", style={"color": "#000000", "font-family": "Quicksand" , "font-weight": "800"}),
            dbc.Col([
                    dbc.Button("BRASIL", color="primary", id="location-button", size="lg"),
                    html.H5(children="Informe a data na qual deseja obter informações:", style={"margin-top": "40px"}),
                    html.Div(
                            className="div-for-dropdown",
                            id="div-test",
                            children=[
                                dcc.DatePickerSingle(
                                    id="date-picker",
                                    min_date_allowed=df_states.groupby("estado")["data"].min().max(),
                                    max_date_allowed=df_states.groupby("estado")["data"].max().min(),
                                    initial_visible_month=df_states.groupby("estado")["data"].min().max(),
                                    date=df_states.groupby("estado")["data"].max().min(),
                                    display_format="MMMM D, YYYY",
                                    style={"border": "0px solid black"},
                                )
                            ],
                        ),

                    dbc.Row([
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Casos recuperados", className="card-text"),
                                    html.H3(style={"color": "#FFFFFF"}, id="casos-recuperados-text"),
                                    html.Span("Em acompanhamento", className="card-text"),
                                    html.H5(id="em-acompanhamento-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF", "background-color": "#8b9dc3"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Casos confirmados totais", className="card-text"),
                                    html.H3(style={"color": "#FFFFFF"}, id="casos-confirmados-text"),
                                    html.Span("Novos casos na data", className="card-text"),
                                    html.H5(id="novos-casos-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF", "background-color": "#8b9dc3"})], md=4),
                        dbc.Col([dbc.Card([   
                                dbc.CardBody([
                                    html.Span("Óbitos confirmados", className="card-text"),
                                    html.H3(style={"color": "#FFFFFF"}, id="obitos-text"),
                                    html.Span("Óbitos na data", className="card-text"),
                                    html.H5(id="obitos-na-data-text"),
                                    ])
                                ], color="light", outline=True, style={"margin-top": "10px",
                                        "box-shadow": "0 4px 4px 0 rgba(0, 0, 0, 0.15), 0 4px 20px 0 rgba(0, 0, 0, 0.19)",
                                        "color": "#FFFFFF", "background-color": "#8b9dc3"})], md=4),
                    ]),

                    html.Div([
                        html.H5(children="Selecione que tipo de dado deseja visualizar:", style={"margin-top": "25px"}),
                        dcc.Dropdown(
                                        id="location-dropdown",
                                        options=[{"label": j, "value": i}
                                            for i, j in select_columns.items()
                                        ],
                                        value="casosNovos",
                                        style={"margin-top": "10px", 'backgroundColor': 'rgb(30, 30, 30)', "border": "0px solid black", 
                                        'fontWeight': 'bold'}
                                    ),
                        dcc.Graph(id="line-graph", figure=fig2, style={'line': {'color': '#156879'},
                            "background-color": "#000000",
                            }),
                        ], id="teste")
                ], md=5, style={
                          "padding": "25px",
                          "background-color": "#3b5998"
                          }), 

            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[dcc.Graph(id="choropleth-map", figure=fig, 
                            style={'height': '100vh', 'margin-right': '10px'})],
                    ),
                ], md=7),
            dbc.Row([
                html.H5(children="Síntese de casos e óbitos por UF - Municipio", style={"margin-left": "10px", "alignment": "center",  "color": "#000000"}),
                dash_table.DataTable(
                        id='idAssignedToDataTable',
                        columns=[
                            {'name': 'Estado', 'id': 'estado', 'type': 'text'},
                            {'name': 'Municipio', 'id': 'municipio', 'type': 'text'},
                            {'name': 'Casos Totais', 'id': 'casosAcumulado', 'type': 'numeric' },
                            {'name': 'Obitos Totais', 'id': 'obitosAcumulado', 'type': 'numeric'}
                        ],
                        data=df_muni.to_dict('records'),  # Dados da tabela
                        style_cell={'textAlign': 'left','padding': '5px'},
                        style_header={
                            'backgroundColor': '#3b5998',
                            'color': 'white',
                            'fontSize': '20px',
                            'fontWeight': 'bold'
                        },
                        style_filter={
                            'backgroundColor': '#3b5998',
                            'fontSize': '16px'
                        },  
                        style_data={
                            'backgroundColor': '#8b9dc3',
                            'color': 'white',
                            'fontSize': '16px'
                        },
                        filter_action='native',
                        sort_action="native",
                        page_size=20 
                    )
            ]),
            ], className="g-0")
    ], fluid=True, 
)


# =====================================================================
# Interactivity
@app.callback(
    [
        Output("casos-recuperados-text", "children"),
        Output("em-acompanhamento-text", "children"),
        Output("casos-confirmados-text", "children"),
        Output("novos-casos-text", "children"),
        Output("obitos-text", "children"),
        Output("obitos-na-data-text", "children"),
    ], [Input("date-picker", "date"), Input("location-button", "children")]
)
def display_status(date, location):
    # print(location, date)
    if location == "BRASIL":
        df_data_on_date = df_brasil[df_brasil["data"] == date]
    else:
        df_data_on_date = df_states[(df_states["estado"] == location) & (df_states["data"] == date)]

    recuperados_novos = "-" if df_data_on_date["Recuperadosnovos"].isna().values[0] else f'{int(df_data_on_date["Recuperadosnovos"].values[0]):,}'.replace(",", ".") 
    acompanhamentos_novos = "-" if df_data_on_date["emAcompanhamentoNovos"].isna().values[0]  else f'{int(df_data_on_date["emAcompanhamentoNovos"].values[0]):,}'.replace(",", ".") 
    casos_acumulados = "-" if df_data_on_date["casosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["casosAcumulado"].values[0]):,}'.replace(",", ".") 
    casos_novos = "-" if df_data_on_date["casosNovos"].isna().values[0]  else f'{int(df_data_on_date["casosNovos"].values[0]):,}'.replace(",", ".") 
    obitos_acumulado = "-" if df_data_on_date["obitosAcumulado"].isna().values[0]  else f'{int(df_data_on_date["obitosAcumulado"].values[0]):,}'.replace(",", ".") 
    obitos_novos = "-" if df_data_on_date["obitosNovos"].isna().values[0]  else f'{int(df_data_on_date["obitosNovos"].values[0]):,}'.replace(",", ".") 
    return (
            recuperados_novos, 
            acompanhamentos_novos, 
            casos_acumulados, 
            casos_novos, 
            obitos_acumulado, 
            obitos_novos,
            )


@app.callback(
        Output("line-graph", "figure"),
        [Input("location-dropdown", "value"), Input("location-button", "children")]
)
def plot_line_graph(plot_type, location):
    if location == "BRASIL":
        df_data_on_location = df_brasil.copy()
    else:
        df_data_on_location = df_states[(df_states["estado"] == location)]
    fig2 = go.Figure(layout={"template":"plotly_dark"})
    bar_plots = ["casosNovos", "obitosNovos"]

    if plot_type in bar_plots:
        fig2.add_trace(go.Bar(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    else:
        fig2.add_trace(go.Scatter(x=df_data_on_location["data"], y=df_data_on_location[plot_type]))
    
    fig2.update_layout(
        paper_bgcolor="#242424",
        plot_bgcolor="#242424",
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=10),
        )
    return fig2


@app.callback(
    Output("choropleth-map", "figure"), 
    [Input("date-picker", "date")]
)
def update_map(date):
    df_data_on_states = df_states[df_states["data"] == date]

    fig = px.choropleth_mapbox(df_data_on_states, locations="estado", geojson=brazil_states, 
        center={"lat": CENTER_LAT, "lon": CENTER_LON},  # https://www.google.com/maps/ -> right click -> get lat/lon
        zoom=4, color="casosAcumulado", color_continuous_scale="Pubu", opacity=0.55,
        hover_data={"casosAcumulado": True, "casosNovos": True, "obitosNovos": True, "obitosAcumulado": True, "estado": True}
        )

    fig.update_layout(title_text = 'Totais de Casos e Óbitos por Estado',paper_bgcolor="#f7f7f7",
                        mapbox_style="carto-darkmatter", autosize=True,
                        margin=go.layout.Margin(l=0, r=0, t=0, b=0), showlegend=False)
    return fig


@app.callback(
    Output("location-button", "children"),
    [Input("choropleth-map", "clickData"), Input("location-button", "n_clicks")]
)
def update_location(click_data, n_clicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if click_data is not None and changed_id != "location-button.n_clicks":
        state = click_data["points"][0]["location"]
        return "{}".format(state)
    
    else:
        return "BRASIL"

if __name__ == "__main__":
    app.run_server(debug=False, port=8051)