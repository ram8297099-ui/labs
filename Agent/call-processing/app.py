import os
import time
import socket
from datetime import datetime

DATABASE_HOST = os.getenv("DATABASE_HOST", "database")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))


def log(level, message):
    timestamp = datetime.now().isoformat()
    print(f"{timestamp} {level} {message}", flush=True)


def check_database_connection():
    try:
        log(
            "INFO",
            f"Connecting to database {DATABASE_HOST}:{DATABASE_PORT}"
        )

        connection = socket.create_connection(
            (DATABASE_HOST, DATABASE_PORT),
            timeout=3
        )

        connection.close()

        log("INFO", "Database connection successful")
        return True

    except Exception as error:
        log(
            "ERROR",
            f"Database connection timeout: {error}"
        )
        return False


def main():
    log("INFO", "911 call-processing service started")

    while True:
        check_database_connection()
        time.sleep(10)


if __name__ == "__main__":
    main()