import random
import time
from datetime import datetime
from pathlib import Path
import database

SIM_FILE = "fake_sensor.csv"
DELAY = 10
db = database.SensorDatabase()

def sim_temp():
    return random.uniform(27, 43)

def sim_hum():
    return random.uniform(27, 43)

def sim_motion():
    return random.choice([True, False])

def values():
    temp = random.uniform(27, 43)
    humidity = random.uniform(27, 43)
    return temp, humidity

print("Starting IOT Sensor Simulator now...")
print("Press Ctrl+C to stop.\n")

def get_data():
    try:
        file_path = Path("fake_sensor.csv")
        if not file_path.exists():
            with open(SIM_FILE, "a") as file:
                file.write("Timestamp, Temp, Humidity, Motion\n")

        while True:
            temp = sim_temp()
            hum = sim_hum()
            motion = sim_motion()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            if motion:
                motion_status = "Motion Detected"
            else: 
                motion_status = "No Motion"
        
            with open(SIM_FILE, "a") as file:
                file.write(f"{timestamp}, {temp:.2f}, {hum:.2f}, {motion}\n")

            temp = round(temp, 2)
            hum = round(hum, 2)
            db.insert_readings(timestamp, temp, hum, motion)
            
            time.sleep(DELAY)

    except KeyboardInterrupt:
        print("\nSimulation stopped. Readings saved to", SIM_FILE)

def main():
    get_data()

if __name__ == "__main__":
    main()