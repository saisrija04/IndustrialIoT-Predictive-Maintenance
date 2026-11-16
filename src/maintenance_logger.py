
import pandas as pd
import os
from datetime import datetime

FILE_PATH = "data/maintenance_history.csv"

def log_maintenance(reading, health_status, probability, recommendation):

    record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": reading["temperature"],
        "vibration": reading["vibration"],
        "rpm": reading["rpm"],
        "operating_hours": reading["operating_hours"],
        "health_status": health_status,
        "failure_probability": round(probability * 100, 2),
        "recommendation": recommendation
    }

    new_record = pd.DataFrame([record])

    if os.path.exists(FILE_PATH):
        new_record.to_csv(
            FILE_PATH,
            mode="a",
            header=False,
            index=False
        )
    else:
        new_record.to_csv(FILE_PATH, index=False)

    return record
