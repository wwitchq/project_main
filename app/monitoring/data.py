import psutil
import pandas as pd

from config import Config


CPU_COUNT = psutil.cpu_count()

df = pd.DataFrame()

for i in range(CPU_COUNT):
    df[f'cpu{i+1}'] = [0.0] * 300

df['ram'] = [0.0] * 300
df['swap'] = [0.0] * 300
df['disk_usage'] = [0.0] * 300
df['disk_write'] = [0.0] * 300
df['disk_read'] = [0.0] * 300
df['network_sent'] = [0.0] * 300
df['network_received'] = [0.0] * 300
df['download_speed'] = [0] * 300 
df['upload_speed'] = [0] * 300
df['cpu_avg'] = [0.0] * 300 

def update_df():
    """
        Обновляет данные в глобальном dataframe для построения графиков
    """
    global df

    net_io = psutil.net_io_counters()
    disk_io = psutil.disk_io_counters()
    if df['network_sent'].iloc[-1]:
        bytes_sent_speed = (net_io.bytes_sent - df['network_sent'].iloc[-1]) / Config.UPDATE_INTERVAL
        bytes_recv_speed = (net_io.bytes_recv - df['network_received'].iloc[-1]) / Config.UPDATE_INTERVAL
    else:
        bytes_sent_speed = bytes_recv_speed = 0


    df.iloc[:-1, :] = df.iloc[1:, :]


    df.loc[df.index[-1], df.columns[:CPU_COUNT]] = psutil.cpu_percent(percpu=True)
    df.loc[df.index[-1], 'ram'] = psutil.virtual_memory().percent
    df.loc[df.index[-1], 'swap'] = psutil.swap_memory().percent
    df.loc[df.index[-1], 'disk_usage'] = psutil.disk_usage('/').percent
    df.loc[df.index[-1], 'disk_read'] = disk_io.write_bytes
    df.loc[df.index[-1], 'disk_write'] = disk_io.read_bytes
    df.loc[df.index[-1], 'network_sent'] = net_io.bytes_sent
    df.loc[df.index[-1], 'network_received'] = net_io.bytes_recv
    df.loc[df.index[-1], 'cpu_avg'] = psutil.cpu_percent()
    df.loc[df.index[-1], 'upload_speed'] = bytes_sent_speed
    df.loc[df.index[-1], 'download_speed'] = bytes_recv_speed




def get_network_connections() -> list[dict]:
    connections = psutil.net_connections()
    connections_info = []

    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        connections_info.append({
            'fd': conn.fd,
            'family': conn.family,
            'type': conn.type,
            'laddr': laddr,
            'raddr': raddr,
            'status': conn.status,
            'pid': conn.pid
        })

    return connections_info
