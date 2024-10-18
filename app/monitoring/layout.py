from dash import html, dcc
import dash_bootstrap_components as dbc
import psutil

from monitoring.styles import *
from config import Config
from monitoring.data import CPU_COUNT

 
layout = dbc.Container(
    [
        header,
        dcc.Tabs(
            [
                dcc.Tab(label='CPU', children=[
                    dcc.Graph(id="graph_cpu"),
                    dcc.Graph(id="graph_cpu_avg"),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("CPU Information", className="card-title"),
                                html.P(f"Number of CPU Cores: {CPU_COUNT}"),
                                html.P(f"CPU max frequency: {psutil.cpu_freq().max} Mhz"),
                            ]
                        )
                    ),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("CPU average load", className="card-title"),
                                html.P(id="cpu_avg_load"),
                            ]
                        )
                    ),       
                ], style=tab_style, selected_style=tab_selected_style),

                dcc.Tab(label='RAM', children=[
                    dcc.Graph(id="graph_ram"),
                    dcc.Graph(id="graph_swap"),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("RAM Information", className="card-title"),
                                html.P(f"Total memory: {((psutil.virtual_memory().total / 1024) / 1024):.2f} MB"),
                                html.P(f"Total SWAP: {((psutil.swap_memory().total / 1024) / 1024):.2f} MB"),
                            ]
                        )
                    ),
                ], style=tab_style, selected_style=tab_selected_style),
                
                dcc.Tab(label='Disk memory', children=[
                    dcc.Graph(id="graph_usage"),
                    dcc.Graph(id="graph_disk_io"),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("Disk information", className="card-title"),
                                html.Ul(id="partition_list"),
                            ]
                        )
                    ),
                ], style=tab_style, selected_style=tab_selected_style),
                
                dcc.Tab(label='Network', children=[
                    dcc.Graph(id="network_speed"),
                    dcc.Graph(id="network_bytes"),
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H4("List of connections", className="card-title"),
                                html.Ul(id="connections_list"),
                            ]
                        )
                    ),
                ], style=tab_style, selected_style=tab_selected_style),
                
                dcc.Tab(label='Settings', children=[
                    html.Div([
                        html.Label('Update Interval (ms):'),
                        dcc.Slider(
                            id='update_interval',
                            min=Config.MIN_UPDATE_INTERVAL,
                            max=Config.MAX_UPDATE_INTERVAL,
                            step=100,
                            value=Config.UPDATE_INTERVAL,
                            marks={i: f'{i} ms' for i in range(0, Config.MAX_UPDATE_INTERVAL+1, 500)}
                        ),
                        html.Div(id='slider_value', style={'margin-top': 20})
                    ])
                ], style=tab_style, selected_style=tab_selected_style),
            
            ], style=tabs_styles
        ),
        dcc.Interval(id="timer", interval=Config.UPDATE_INTERVAL),
    ],
    fluid=True,
)

