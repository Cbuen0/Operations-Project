import numpy as np
import pandas as pd

np.random.seed(42)
n = 500 
t = np.linspace(0, 500, n)

altitude = np.where(t < 100, t * 3,
           np.where(t < 350, 300.0,
           300 - (t - 350) * 2))
altitude += np.random.normal(0, 2, n)  # sensor noise

airspeed = np.where(t < 80, t * 1.5,
           np.where(t < 380, 120.0,
           120 - (t - 380) * 0.8))
airspeed += np.random.normal(0, 1.5, n)

gz = np.ones(n) + np.random.normal(0, 0.05, n)

vibration = np.random.normal(0, 0.8, n)

# Anomalies
# Vibration Spike
vibration[148:153] += np.array([3.2, 6.8, 9.1, 7.4, 4.0])

# Airspeed Glitched
airspeed[278:282] -= 40

# Heavy Manuever
gz[419:423] += np.array([2.1, 3.8, 3.2, 1.9])

df = pd.DataFrame({
    "time_s":      np.round(t, 2),
    "altitude_ft": np.round(altitude, 2),
    "airspeed_kts": np.round(airspeed, 2),
    "gz_g":        np.round(gz, 4),
    "vibration_in_s2": np.round(vibration, 4) 
})

df.to_csv("flight_data.csv", index=False)
print(f"Generated {len(df)} rows of flight test data at flight_data.csv")
