import requests

BASE_URL = "https://smart-computer-lab-resource-monitor-v2.onrender.com"


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