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


def insert_system_data(
    machine_name,
    cpu_usage,
    ram_usage,
    disk_usage,
    process_count
):

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO system_data (
            machine_name,
            cpu_usage,
            ram_usage,
            disk_usage,
            process_count
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            machine_name,
            cpu_usage,
            ram_usage,
            disk_usage,
            process_count
        )
    )

    connection.commit()

    connection.close()


def get_all_system_data():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM system_data
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    connection.close()

    return data
def get_latest_system_data():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM system_data
        ORDER BY id DESC
        LIMIT 1
        """
    )

    data = cursor.fetchone()

    connection.close()

    return data
def get_latest_machines():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM system_data
        WHERE id IN (
            SELECT MAX(id)
            FROM system_data
            GROUP BY machine_name
        )
        ORDER BY id DESC
        """
    )

    data = cursor.fetchall()

    connection.close()

    return data
def get_summary_data():

    connection = sqlite3.connect(
        DATABASE
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(DISTINCT machine_name),
            AVG(cpu_usage),
            AVG(ram_usage),
            AVG(disk_usage)
        FROM system_data
        """
    )

    data = cursor.fetchone()

    connection.close()

    return data