
import joblib
import pandas as pd

# Load trained model
model = joblib.load(
    "models/predictive_maintenance_model.pkl"
)

print("INDUSTRIAL MACHINE FAILURE PREDICTION")
print("--------------------------------------")

# Get sensor readings
temperature = float(input("Enter temperature (°C): "))
vibration = float(input("Enter vibration: "))
rpm = float(input("Enter RPM: "))
operating_hours = float(input("Enter operating hours: "))

# Prepare input
machine_data = pd.DataFrame([{
    "temperature": temperature,
    "vibration": vibration,
    "rpm": rpm,
    "operating_hours": operating_hours
}])

# Predict
prediction = model.predict(machine_data)[0]
probability = model.predict_proba(machine_data)[0][1]

print("\nPREDICTION RESULT")

if prediction == 1:
    print("WARNING: Machine failure risk detected!")
else:
    print("Machine condition: NORMAL")

print(f"Predicted failure probability: {probability * 100:.2f}%")
