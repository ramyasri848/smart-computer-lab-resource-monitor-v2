from fastapi import FastAPI
from pydantic import BaseModel

from server.database import (
    create_database,
    insert_system_data,
    get_all_system_data,
    get_latest_system_data
)

app = FastAPI()


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
        "machines": data
    }
@app.get("/latest")
def get_latest():

    data = get_latest_system_data()

    return {
        "latest": data
    }