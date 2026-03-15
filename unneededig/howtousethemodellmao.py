import pickle
import pandas as pd

with open('model\carbon_sink_model.pkl', 'rb') as f:
    model = pickle.load(f)



# keep above (ts the model)

# use this 
#load a dict
new_df = pd.DataFrame([{
    'sea_temp': 18.5,
    'chlorophyll': 4.2,
    'salinity': 31.5,
    'wind_speed': 7.3,
    'month': 1
}])
model['sea_temp'].describe()
#init a variable
preds = model.predict(new_df)
# print something
print(preds)  # e.g. [45.2]