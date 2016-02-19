from sense_hat import SenseHat
import sqlite3
import os.path

sense = SenseHat()

DB_NAME = "sense.db"


def init_db():
    """Creates all the necessary tables."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE measurements (
            time DATETIME PRIMARY KEY,
            humidity REAL,
            pressure REAL,
            temperature_humidity REAL,
            temperature_pressure REAL,
            cpu_temperature REAL
        )
        """
    )

    connection.commit()
    connection.close()


def write_measurements():
    """Writes current measurements into the database."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO measurements (time, humidity, pressure, temperature_humidity, temperature_pressure, cpu_temperature)
             VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s)
        """ % (
            sense.get_humidity(),
            sense.get_pressure(),
            sense.get_temperature_from_humidity(),
            sense.get_temperature_from_pressure(),
            get_cpu_temperature(),
        )
    )

    connection.commit()
    connection.close()


def get_cpu_temperature():
    """Returns CPU temperature in Celsius."""
    with open("/sys/class/thermal/thermal_zone0/temp") as temp:
        return float(temp.readline()) / 1000


if __name__ == "__main__":
    if not os.path.isfile(DB_NAME):
        init_db()
    write_measurements()