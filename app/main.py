from fastapi import FastAPI
import psutil
import platform
import socket
from datetime import datetime
import subprocess

app = FastAPI(title="Linux Infrastructure Monitor")


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/metrics")
def metrics():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    network = psutil.net_io_counters()

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),

        "memory_percent": memory.percent,
        "memory_available_mb": round(
            memory.available / (1024 * 1024), 2
        ),

        "disk_percent": disk.percent,
        "disk_total_gb": round(
            disk.total / (1024 ** 3), 2
        ),
        "disk_free_gb": round(
            disk.free / (1024 ** 3), 2
        ),

        "network_bytes_sent": network.bytes_sent,
        "network_bytes_received": network.bytes_recv,
        "network_packets_sent": network.packets_sent,
        "network_packets_received": network.packets_recv
    }


@app.get("/processes")
def processes():
    processes = []

    for process in psutil.process_iter(
        ["pid", "name", "memory_percent"]
    ):
        try:
            cpu_percent = process.cpu_percent(interval=0.1)

            processes.append({
                "pid": process.info["pid"],
                "name": process.info["name"],
                "cpu_percent": round(cpu_percent, 2),
                "memory_percent": round(
                    process.info["memory_percent"], 2
                )
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    processes.sort(
        key=lambda process: process["cpu_percent"],
        reverse=True
    )

    return {
        "processes": processes[:10]
    }

@app.get("/system")
def system_info():
    cpu_model = "Unknown"

    try:
        output = subprocess.check_output(
            ["lscpu"],
            text=True
        )

        for line in output.splitlines():
            if line.startswith("Model name:"):
                cpu_model = line.split(":", 1)[1].strip()
                break

    except Exception:
        pass

    return {
        "hostname": socket.gethostname(),
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine(),
        "cpu_model": cpu_model,
        "cpu_count": psutil.cpu_count(),
        "boot_time": datetime.fromtimestamp(
            psutil.boot_time()
        ).isoformat()
    }



@app.get("/alerts")
def alerts():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    cpu = psutil.cpu_percent(interval=1)

    alerts = []

    if cpu > 80:
        alerts.append({
            "resource": "cpu",
            "level": "warning",
            "message": f"CPU usage is high: {cpu}%"
        })

    if memory.percent > 80:
        alerts.append({
            "resource": "memory",
            "level": "warning",
            "message": f"Memory usage is high: {memory.percent}%"
        })

    if disk.percent > 80:
        alerts.append({
            "resource": "disk",
            "level": "warning",
            "message": f"Disk usage is high: {disk.percent}%"
        })

    if not alerts:
        return {
            "status": "healthy",
            "alerts": []
        }

    return {
        "status": "warning",
        "alerts": alerts
    }
