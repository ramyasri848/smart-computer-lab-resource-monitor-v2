from fastapi import FastAPI

from server.database import (
    create_database
)

app = FastAPI()


@app.on_event("startup")
def startup():

    create_database()


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