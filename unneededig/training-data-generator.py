import pandas as pd
import numpy as np

np.random.seed(42)

n_samples = 20000

data = pd.DataFrame({
    'sea_temp': np.random.uniform(-5, 30, n_samples),
    'chlorophyll': np.random.uniform(0, 10, n_samples),
    'salinity': np.random.uniform(30, 37, n_samples),
    'wind_speed': np.random.uniform(0, 25, n_samples),
    'month': np.random.randint(1, 13, n_samples)
})

# target variable
data['carbon_sink'] = (
    0.5 * (10 - data['sea_temp']) +           # colder = more absorption
    2 * data['chlorophyll'] +                  # more chlorophyll = more absorption
    0.3 * (35 - data['salinity']) +            # lower salinity = more absorption
    0.1 * data['wind_speed'] +                 # wind helps gas exchange
    1.5 * np.sin(data['month'] / 12 * 2 * np.pi) +  # seasonality (boosted)
    np.random.normal(0, 1, n_samples)          # noise
)

# normalize 0-100
data['carbon_sink'] = ((data['carbon_sink'] - data['carbon_sink'].min()) /
                       (data['carbon_sink'].max() - data['carbon_sink'].min()) * 100)

data.to_csv('carbon_sink_20k.csv', index=False)

print(data.head())
print("\nStats:")
print(data.describe())