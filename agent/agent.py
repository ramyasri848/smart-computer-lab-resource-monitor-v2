import psutil
import requests
import platform
import time


SERVER_URL = "http://127.0.0.1:8000/submit-data"


def collect_system_data():

    machine_name = platform.node()

    cpu_usage = psutil.cpu_percent(
        interval=1
    )

    ram_usage = psutil.virtual_memory().percent

    disk_usage = psutil.disk_usage(
        "/"
    ).percent

    process_count = len(
        psutil.pids()
    )

    return {
        "machine_name": machine_name,
        "cpu_usage": cpu_usage,
        "ram_usage": ram_usage,
        "disk_usage": disk_usage,
        "process_count": process_count
    }


while True:

    try:

        data = collect_system_data()

        response = requests.post(
            SERVER_URL,
            json=data
        )

        print(
            "Data Sent:",
            response.json()
        )

    except Exception as e:

        print(
            "Error:",
            e
        )

    time.sleep(10)