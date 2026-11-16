
import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Number of sensor readings
n = 5000

# Generate industrial machine sensor data
data = {
    "temperature": np.random.normal(70, 10, n),
    "vibration": np.random.normal(4, 1.5, n),
    "rpm": np.random.normal(1500, 200, n),
    "operating_hours": np.random.randint(100, 10000, n)
}

df = pd.DataFrame(data)

# Generate failure labels
df["failure"] = (
    (df["temperature"] > 85) |
    (df["vibration"] > 6) |
    (df["rpm"] > 1800)
).astype(int)

# Save dataset
os.makedirs("data", exist_ok=True)
df.to_csv("data/machine_data.csv", index=False)

print("Industrial sensor dataset generated successfully!")
print(df.head())
print("\nDataset shape:", df.shape)
print("\nFailure distribution:")
print(df["failure"].value_counts())
