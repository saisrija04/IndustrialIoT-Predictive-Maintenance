
import numpy as np
from datetime import datetime

def generate_sensor_reading():

    # Simulate industrial machine sensor readings
    temperature = np.random.normal(75, 8)
    vibration = np.random.normal(4.5, 1.2)
    rpm = np.random.normal(1500, 180)
    operating_hours = np.random.randint(1000, 10000)

    # Keep values within reasonable limits
    temperature = round(float(np.clip(temperature, 30, 120)), 2)
    vibration = round(float(np.clip(vibration, 0.5, 10)), 2)
    rpm = round(float(np.clip(rpm, 500, 2500)), 2)

    reading = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": temperature,
        "vibration": vibration,
        "rpm": rpm,
        "operating_hours": operating_hours
    }

    return reading


if __name__ == "__main__":
    print("INDUSTRIAL IoT SENSOR SIMULATOR")
    print("--------------------------------")

    for i in range(5):
        reading = generate_sensor_reading()
        print(reading)
