from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.wsgi import WSGIMiddleware
import uvicorn
import psutil

from monitoring.dash_api import dash_app
from monitoring.data import CPU_COUNT

app = FastAPI()


app.mount("/dashboard/", WSGIMiddleware(dash_app.server))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/cpu/")
async def cpu(cpu_id: int | None = None):
    if cpu_id is None:
        return {"cpu": psutil.cpu_percent()}
    else:
        if 0 <= cpu_id < CPU_COUNT:
            return {f"cpu{cpu_id+1}": psutil.cpu_percent(percpu=True)}
        raise HTTPException(status_code=404, detail=f"CPU not found. cpu_id must be between 0 and {CPU_COUNT-1}, but got {cpu_id}")


@app.get("/system/")
async def system():
    ram = psutil.virtual_memory().percent
    swap = psutil.swap_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    disk_write = psutil.disk_io_counters().write_bytes
    disk_read = psutil.disk_io_counters().read_bytes
    network_sent = psutil.net_io_counters().bytes_sent
    network_received = psutil.net_io_counters().bytes_recv

    return {
        "ram": ram,
        "swap": swap,
        "disk_usage": disk_usage,
        "disk_write": disk_write,
        "disk_read": disk_read,
        "network_sent": network_sent,
        "network_received": network_received,
        
    }

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)