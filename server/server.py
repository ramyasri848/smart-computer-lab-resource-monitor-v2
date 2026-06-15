from fastapi import FastAPI
from pydantic import BaseModel

from server.database import (
    create_database,
    insert_system_data,
    get_all_system_data,
    get_latest_system_data,
    get_latest_machines
)

app = FastAPI()


def format_machine(row):

    return {
        "id": row[0],
        "machine_name": row[1],
        "timestamp": row[2],
        "cpu_usage": row[3],
        "ram_usage": row[4],
        "disk_usage": row[5],
        "process_count": row[6]
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