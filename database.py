from asyncio.windows_events import NULL
import re
import sqlite3
from unittest import result

db_name = "sensor_data.db"
READINGS_PER_WEEK = 100800

class SensorDatabase:

    def __init__(self):
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()

        curs.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT ,
            timestamp TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            motion INTEGER NOT NULL
            )
            """
        )

        conn.commit()
        conn.close()
        print(f"Database has been initialized: {db_name}")

    def insert_readings(self, timestamp, temperature, humidity, motion):
        conn =sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute(
            " INSERT INTO sensor_readings (timestamp, temperature, humidity, motion) VALUES(?,?,?,?)", (timestamp, temperature, humidity, motion) 
        )
        conn.commit()
        conn.close()

    def get_latest_reading(self):
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute("SELECT timestamp, temperature, humidity, motion FROM sensor_readings ORDER BY id DESC LIMIT 1")
        data = curs.fetchone()
        conn.close()

        if data:
            result = {'timestamp': data[0], 'temperature': data[1], 'humidity': data[2], 'motion': bool(data[3])}
        else:
            result = None

        return result

    def get_recent_readings(self, limit):
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute("SELECT timestamp, temperature, humidity, motion FROM sensor_readings ORDER BY id DESC LIMIT ?", (limit, ))
        data = curs.fetchall()
        conn.close()

        readings = []
        for row in data:
            readings.append({'timestamp': row[0], 'temperature': row[1], 'humidity': row[2], 'motion': bool(row[3])})

        return readings

    def get_all_readings(self):
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute("SELECT id, timestamp, temperature, humidity, motion FROM sensor_readings ORDER BY id ASC")
        data = curs.fetchall()
        conn.close()

        readings = []
        for row in data:
            readings.append({'id': row[0], 'timestamp': row[1], 'temperature': row[2], 'humidity': row[3], 'motion': bool(row[4])})

        return readings

    def clear_old_readings(self, READINGS_PER_WEEK):
        conn = sqlite3.connect(db_name)
        curs = conn.cursor()
        curs.execute("DELETE FROM sensor_readings WHERE id NOT IN (SELECT id FROM sensor_readings ORDER BY id DESC LIMIT READINGS_PER_WEEK)")
        data = curs.fetchall()
        conn.commit()
        conn.close()
        count = 0

        for row in data:
            count += 1

        num_days = (count/ READINGS_PER_WEEK) * 7

        return num_days