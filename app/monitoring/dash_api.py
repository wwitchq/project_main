from dash import Dash, html, Input, Output
import plotly.graph_objs as go
import psutil
import dash_bootstrap_components as dbc

from monitoring.styles import *
from monitoring.data import CPU_COUNT

from monitoring.layout import layout
from monitoring.data import update_df, df, CPU_COUNT, get_network_connections


dash_app = Dash(
    __name__, 
    requests_pathname_prefix="/dashboard/", 
    title="project", 
    external_stylesheets=[dbc.themes. COSMO]
    )

dash_app.layout = layout


@dash_app.callback(
    Output("timer", "interval"),
    Input("update_interval", "value"))
def update_interval(value):
    return value

@dash_app.callback(
    Output("graph_cpu", 'figure'),
    Output("graph_cpu_avg", 'figure'),
    Output("cpu_avg_load", "children"),
    Input("timer", "n_intervals"))
def update_cpu(n):
    update_df()
    
    traces = [
        go.Scatter(
            x=df.index,
            y=df[t],
            name=f'CPU Core {i+1}',
            mode='lines',
            line=dict(shape='linear')
        ) for i, t in enumerate(df.columns[:CPU_COUNT])
    ]
    
    traces_avg = [
        go.Scatter(
            x=df.index,
            y=df['cpu_avg'],
            name='CPU Average',
            mode='lines',
            line=dict(shape='linear', color='yellow')
        )
    ]
    
    fig_cpu = {
        "data": traces,
        "layout": go.Layout(
            title='CPU Usage per Core',
            xaxis=dict(title='Time'),
            yaxis=dict(title='CPU Usage (%)'),
            template='plotly_white'
        )
    }
    
    fig_cpu_avg = {
        "data": traces_avg,
        "layout": go.Layout(
            title='Average CPU Usage',
            xaxis=dict(title='Time'),
            yaxis=dict(title='CPU Usage (%)'),
            template='plotly_white'
        )
    }
    
    cpu_avg_load_text = f"CPU Average Load: {psutil.cpu_percent()}%"
    
    return fig_cpu, fig_cpu_avg, cpu_avg_load_text


@dash_app.callback(
    Output("connections_list", "children"),
    Input("timer", "n_intervals")
)
def update_network_connections(n):
    connections = get_network_connections()
    return [html.Li(f"{conn['laddr']} -> {conn['raddr']} ({conn['status']})") for conn in connections]

@dash_app.callback(
    Output('partition_list', 'children'),
    Input('timer', 'n_intervals')
)
def update_disk_partitions(n):
    partitions = psutil.disk_partitions()
    partition_info = []
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        partition_info.append(html.Li(children=[
            html.P(f"Device: {partition.device}, \nMountpoint: {partition.mountpoint}, \nFile System Type: {partition.fstype}, "),
            html.P(f"Total Size: {round(usage.total / (1024**3), 2)} GB, \nUsed Space: {round(usage.used / (1024**3), 2)} GB, "),
            html.P(f"Free Space: {round(usage.free / (1024**3), 2)} GB, \nPercentage Used: {usage.percent}%")]
        ))
    return partition_info

@dash_app.callback(
    Output("graph_cpu", "style"),
    Output("graph_ram", "style"),
    Output("graph_swap", "style"),
    Input("display-data-checkbox", "value")
)
def update_displayed_data(value):
    cpu_style = {} if "cpu" in value else {"display": "none"}
    ram_style = {} if "ram" in value else {"display": "none"}
    swap_style = {} if "swap" in value else {"display": "none"}
    return cpu_style, ram_style, swap_style


@dash_app.callback(
    Output("graph_ram", 'figure'),
    Output("graph_swap", 'figure'),
    Input("timer", 'n_intervals'))
def update_ram_graphs(n):
    update_df()
    
    ram_trace = [
        go.Scatter(
            x=df.index,
            y=df['ram'],
            name='RAM',
            mode='lines',
            line=dict(shape='linear')
        )
    ]
    
    swap_trace = [
        go.Scatter(
            x=df.index,
            y=df['swap'],
            name='SWAP',
            mode='lines',
            line=dict(shape='linear')
        )
    ]
    
    fig_ram = {
        "data": ram_trace,
        "layout": go.Layout(
            title='RAM Usage',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Usage (%)'),
            template='plotly_white',
        )
    }
    
    fig_swap = {
        "data": swap_trace,
        "layout": go.Layout(
            title='SWAP Usage',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Usage (%)'),
            template='plotly_white',
        )
    }
    
    return fig_ram, fig_swap

@dash_app.callback(
    Output("graph_usage", 'figure'),
    Output("graph_disk_io", 'figure'),
    Input("timer", 'n_intervals'))
def update_rom_graph(n):
    update_df()
    
    traces_usage = [
        go.Scatter(
            x=df.index,
            y=df['disk_usage'],
            name='Disk Usage (%)',
            mode='lines',
            line=dict(shape='linear')
        )
    ]

    traces_io = [
        go.Scatter(
            x=df.index,
            y=df['disk_read'] / (1024 ** 2),
            name='Disk Read (MB)',
            mode='lines',
            line=dict(shape='linear', color='blue')
        ),
        go.Scatter(
            x=df.index,
            y=df['disk_write'] / (1024 ** 2),
            name='Disk Write (MB)',
            mode='lines',
            line=dict(shape='linear', color='red')
        )
    ]
    
    fig_usage = {
        "data": traces_usage,
        "layout": go.Layout(
            title='Disk Usage %',
            template='plotly_white',
            yaxis={"range": (0, 100), "title": "Usage (%)"},
            xaxis={"title": "Time"}
        )
    }
    
    fig_io = {
        "data": traces_io,
        "layout": go.Layout(
            title='Disk I/O',
            template='plotly_white',
            yaxis={"title": "Megabytes"},
            xaxis={"title": "Time"}
        )
    }
    
    return fig_usage, fig_io

@dash_app.callback(
    Output("network_bytes", 'figure'), 
    Output("network_speed", 'figure'),
    Input("timer", 'n_intervals')
)
def update_network_graph(n):
    update_df()

    # График с данными о передаче
    bytes_traces = [
        go.Scatter(
            x=df.index,
            y=df['network_sent'] / 1024,  # Конвертируем байты в килобайты
            mode='lines',
            name='Sent (KB)'
        ),
        go.Scatter(
            x=df.index,
            y=df['network_received'] / 1024,  # Конвертируем байты в килобайты
            mode='lines',
            name='Received (KB)'
        )
    ]

    # График с данными о скорости
    speed_traces = [
        go.Scatter(
            x=df.index,
            y=df['upload_speed'] / 1024,  # Конвертируем байты в килобайты
            mode='lines+markers',
            name='Upload Speed (KB/s)',
            text=[f"{speed / 1024:.2f} KB/s" for speed in df['upload_speed']],
            textposition='bottom center'
        ),
        go.Scatter(
            x=df.index,
            y=df['download_speed'] / 1024,  # Конвертируем байты в килобайты
            mode='lines+markers',
            name='Download Speed (KB/s)',
            text=[f"{speed / 1024:.2f} KB/s" for speed in df['download_speed']],
            textposition='bottom center'
        )
    ]

    return (
        {"data": bytes_traces, "layout": {
            "template": "plotly_dark",
            "title": "Total bytes sent/received",
            "xaxis": {"title": "Time"},
            "yaxis": {"title": "Data (KB)"}
        }},
        {"data": speed_traces, "layout": {
            "template": "plotly_dark",
            "title": "Network Data Speed",
            "xaxis": {"title": "Type"},
            "yaxis": {"title": "Speed (KB/s)"}
        }}
    )

if __name__ == "__main__":
    dash_app.run_server(debug=True)