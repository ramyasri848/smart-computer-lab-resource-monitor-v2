from fastapi import FastAPI
from pydantic import BaseModel

from server.database import (
    create_database,
    insert_system_data,
    get_all_system_data,
    get_latest_system_data,
    get_latest_machines,
    get_summary_data,
    get_critical_machines,
    get_machine_history
)

app = FastAPI()


def get_health_status(
    cpu_usage,
    ram_usage
):

    if cpu_usage >= 90 or ram_usage >= 90:

        return "Critical"

    elif cpu_usage >= 70 or ram_usage >= 70:

        return "Warning"

    else:

        return "Healthy"


def format_machine(row):

    return {
        "id": row[0],
        "machine_name": row[1],
        "timestamp": row[2],
        "cpu_usage": row[3],
        "ram_usage": row[4],
        "disk_usage": row[5],
        "process_count": row[6],
        "health_status": get_health_status(
            row[3],
            row[4]
        )
    }


@app.on_event("startup")
def startup():

    create_database()


class SystemData(BaseModel):

    machine_name: str

    cpu_usage: float

    ram_usage: float

    disk_usage: float

    process_count: int


@app.get("/")
def home():

    return {
        "message":
        "Smart Computer Lab Resource Monitoring API Running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/submit-data")
def submit_data(
    data: SystemData
):

    insert_system_data(
        data.machine_name,
        data.cpu_usage,
        data.ram_usage,
        data.disk_usage,
        data.process_count
    )

    return {
        "message":
        "Data stored successfully"
    }


@app.get("/machines")
def get_machines():

    data = get_all_system_data()

    return {
        "machines": [
            format_machine(row)
            for row in data
        ]
    }


@app.get("/latest")
def get_latest():

    data = get_latest_system_data()

    if not data:

        return {
            "latest": None
        }

    return {
        "latest": format_machine(data)
    }


@app.get("/machines/latest")
def latest_machines():

    data = get_latest_machines()

    return {
        "machines": [
            format_machine(row)
            for row in data
        ]
    }


@app.get("/summary")
def summary():

    data = get_summary_data()

    return {
        "total_machines": data[0],
        "average_cpu_usage": round(data[1], 2) if data[1] else 0,
        "average_ram_usage": round(data[2], 2) if data[2] else 0,
        "average_disk_usage": round(data[3], 2) if data[3] else 0
    }
@app.get("/critical")
def critical_machines():

    data = get_critical_machines()

    critical = []

    for row in data:

        machine = format_machine(row)

        if machine["health_status"] != "Healthy":

            critical.append(machine)

    return {
        "critical_machines": critical
    }
@app.get("/machine-history/{machine_name}")
def machine_history(
    machine_name: str
):

    data = get_machine_history(
        machine_name
    )

    return {
        "history": [
            format_machine(row)
            for row in data
        ]
    }