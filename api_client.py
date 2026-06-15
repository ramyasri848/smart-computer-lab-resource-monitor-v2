import requests

BASE_URL = "http://127.0.0.1:8000"


def get_summary():

    response = requests.get(
        f"{BASE_URL}/summary"
    )

    return response.json()


def get_latest_machines():

    response = requests.get(
        f"{BASE_URL}/machines/latest"
    )

    return response.json()


def get_critical_machines():

    response = requests.get(
        f"{BASE_URL}/critical"
    )

    return response.json()