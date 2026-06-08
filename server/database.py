import sqlite3

DATABASE = "database/monitoring.db"


def create_database():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS system_data (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            machine_name TEXT,

            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            cpu_usage REAL,

            ram_usage REAL,

            disk_usage REAL,

            process_count INTEGER
        )
        """
    )

    connection.commit()

    connection.close()