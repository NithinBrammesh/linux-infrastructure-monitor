# Linux Infrastructure Monitor

A lightweight Linux infrastructure monitoring and troubleshooting service built with **Python, FastAPI, psutil, and Docker**.

The project collects system-level metrics such as CPU, memory, disk, network activity, running processes, and system information. It also provides basic resource alerts and demonstrates a practical Linux troubleshooting workflow.

## Project Objective

The objective is to gain practical exposure to Linux infrastructure monitoring, resource utilization, troubleshooting, REST APIs, and containerized deployment.

The monitor can:
- Monitor CPU, memory, disk, and network usage
- Inspect running processes
- Identify high CPU-consuming processes
- Generate basic resource alerts
- Expose system information through REST APIs
- Run as a Docker container

## Architecture

```text
                    Linux System
                         |
          +--------------+--------------+
          |              |              |
         CPU            RAM            Disk
          |              |              |
          +--------------+--------------+
                         |
                       psutil
                         |
                    Python App
                         |
                      FastAPI
                         |
        +----------------+----------------+
        |                |                |
     /metrics        /processes        /alerts
        |                |                |
        +----------------+----------------+
                         |
                       Docker
                         |
                  infra-monitor
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application development |
| FastAPI | REST API framework |
| Uvicorn | ASGI application server |
| psutil | System and process monitoring |
| Linux / Ubuntu | Host operating system |
| Docker | Containerization |
| Git | Version control |

## Project Structure

```text
infra-monitor/
├── app/
│   └── main.py
├── venv/
├── Dockerfile
├── requirements.txt
└── README.md
```

`venv/` is a local development environment and should not be committed to Git.

Recommended `.gitignore`:

```text
venv/
__pycache__/
*.pyc
.env
```

# API Endpoints

## Health Check

`GET /health`

```bash
curl http://127.0.0.1:8005/health
```

```json
{"status":"healthy"}
```

## System Metrics

`GET /metrics`

Reports CPU utilization, memory utilization, available memory, disk utilization/free space, and network byte/packet counters.

```bash
curl http://127.0.0.1:8005/metrics
```

## Process Monitoring

`GET /processes`

Reports the top processes by CPU utilization, including PID, process name, CPU percentage, and memory percentage.

```bash
curl http://127.0.0.1:8005/processes
```

Example:

```json
{
  "processes": [
    {"pid": 179939, "name": "yes", "cpu_percent": 99.8, "memory_percent": 0.03},
    {"pid": 156975, "name": "chrome", "cpu_percent": 20.0, "memory_percent": 3.6}
  ]
}
```

## System Information

`GET /system`

Provides hostname, operating system, kernel version, architecture, CPU model, CPU count, and boot time.

```bash
curl http://127.0.0.1:8005/system
```

## Resource Alerts

`GET /alerts`

Checks CPU, memory, and disk utilization against configured thresholds.

```bash
curl http://127.0.0.1:8005/alerts
```

Healthy response:

```json
{"status":"healthy","alerts":[]}
```

# Troubleshooting Demonstration

A controlled CPU stress test was performed using:

```bash
yes > /dev/null
```

The monitoring API identified the process consuming almost an entire CPU core:

```json
{"name":"yes","cpu_percent":99.8}
```

Troubleshooting workflow:

```text
High CPU Usage
      |
      v
Check /metrics
      |
      v
Check running processes
      |
      v
Identify high CPU process
      |
      v
Investigate / stop it
      |
      v
CPU returns to normal
```

After stopping the test process with `Ctrl+C`, `/alerts` returned to a healthy state.

# Docker Deployment

## Build the image

```bash
docker build -t infra-monitor .
```

## Check the image

```bash
docker images infra-monitor
```

The tested image used approximately **215 MB disk usage** and **52.2 MB content size**. Exact size can vary with image/dependency versions.

## Run the container

```bash
docker run -d \
  --name infra-monitor-container \
  -p 8006:8005 \
  infra-monitor:latest
```

Check it:

```bash
docker ps
```

Test it:

```bash
curl http://127.0.0.1:8006/health
curl http://127.0.0.1:8006/metrics
curl http://127.0.0.1:8006/system
curl http://127.0.0.1:8006/processes
curl http://127.0.0.1:8006/alerts
```

## Docker Architecture

```text
                    Linux Host
                        |
                  Docker Engine
                        |
              +---------+---------+
              |  infra-monitor    |
              |    Container      |
              |     FastAPI       |
              |       |           |
              |     psutil        |
              +---------+---------+
                        |
                  Host Port 8006
                        |
                     Client
```

## Important Docker Observation

The application running directly on the Linux host could see host processes such as Chrome, VS Code, Uvicorn, systemd, and the test `yes` process. When executed inside Docker, `/processes` primarily saw processes inside the container.

This demonstrates an important infrastructure concept: **containers provide process isolation, so a process inside a container does not automatically have the same process visibility as the host.**

# Development Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8005
```

Interactive API documentation:

```text
http://127.0.0.1:8005/docs
```

# Linux Commands Used

```bash
top
ps
free -h
df -h
du -sh
ip -s link
ss
ping
curl
lscpu
uname -a
systemctl
journalctl
docker ps
docker images
docker build
docker run
docker logs
```

# Learning Outcomes

- Linux system monitoring
- CPU, memory, disk, and network utilization
- Linux processes and troubleshooting
- REST API development
- Python system monitoring with psutil
- Docker image creation and container deployment
- Container process isolation
- Basic observability concepts

# Current Limitations

This is an educational infrastructure monitoring POC rather than a production monitoring platform.

- Metrics are current snapshots rather than historical data.
- No persistent time-series database is used.
- Alerts are basic threshold-based checks.
- No authentication is implemented.
- No web dashboard is implemented.
- Containerized monitoring has limited visibility into host processes because of process isolation.
- The application monitors the environment visible to the process in which it runs.

# Future Improvements

- Prometheus integration
- Grafana dashboards
- Historical metric storage
- Configurable alert thresholds
- Email/Slack notifications
- Multi-server monitoring
- Authentication and authorization
- Centralized monitoring server
- Docker Compose deployment
- Kubernetes deployment
- Cloud/EC2 deployment
- Host-level monitoring agent
- Container monitoring
- Log monitoring
- Service health monitoring

# Project Status

## Completed

- [x] Linux system monitoring
- [x] CPU monitoring
- [x] Memory monitoring
- [x] Disk monitoring
- [x] Network monitoring
- [x] Process monitoring
- [x] System information endpoint
- [x] Resource alerts
- [x] CPU stress-test demonstration
- [x] High CPU process identification
- [x] FastAPI REST API
- [x] Dockerfile
- [x] Docker image
- [x] Docker container deployment
- [x] Docker endpoint testing

## Planned

- [ ] Add `.gitignore`
- [ ] Add architecture diagram/image
- [ ] Improve alert configuration
- [ ] Add persistent metric storage
- [ ] Add dashboard
- [ ] Add Prometheus/Grafana
- [ ] Add multi-server monitoring

# Author

**Nithin B**

Backend Engineer

Technical interests:
- Python
- Linux
- Backend Engineering
- Distributed Systems
- Docker
- Cloud Infrastructure
- Infrastructure Monitoring

GitHub: https://github.com/NithinBrammesh