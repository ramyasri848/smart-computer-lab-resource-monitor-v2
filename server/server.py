from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():

    return {
        "message": "Smart Computer Lab Resource Monitoring API Running"
    }

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }