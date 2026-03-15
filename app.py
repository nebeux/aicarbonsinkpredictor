from flask import Flask, request, jsonify, render_template
import requests
import pickle
import pickle
import pandas as pd
from datetime import datetime, timedelta

month = datetime.now().month
month_names = {
    1: "JAN", 2: "FEB", 3: "MAR", 4: "APR",
    5: "MAY", 6: "JUN", 7: "JUL", 8: "AUG",
    9: "SEP", 10: "OCT", 11: "NOV", 12: "DEC"
}
app = Flask(__name__)
with open('model\carbon_sink_model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

# if i plan to change the app route then change it in app.js as well and i should be fine lmao
@app.route("/", methods=['POST'])
# yay api stuff
def predict():
    month2 = datetime.now().month
    appdata = request.get_json()
    lat = appdata['lat']
    lng = appdata['lng']
    print(str(lat) + " " + str(lng))
    if isWater(lat,lng):
        sea_temp, chlorophyll, salinity, wind_speed, monthnum = getvaluesfromAPIS(lat,lng)
        print(sea_temp)
        print(chlorophyll)
        print(salinity)
        print(wind_speed)
        print(month2)
        new_df = pd.DataFrame([{
        'sea_temp': sea_temp,
        'chlorophyll': chlorophyll,
        'salinity': salinity,
        'wind_speed': wind_speed,
        'month': month2 #plz dont use monthnum its bugged i dont wanna fix it lmao
        }])
        if chlorophyll != 1.5 and salinity != 34.0:
            prediction = model.predict(new_df)
            print("final pred" + str(prediction))
            return jsonify({'prediction': prediction[0], 'extra_info': "fallback", 'chlorophyll': chlorophyll, 'salinity': salinity, 'wind_speed': wind_speed, 'sea_temp': sea_temp})
        else:
            prediction = model.predict(new_df)
            print("final pred" + str(prediction))
            return jsonify({'prediction': prediction[0], 'extra_info': "fallback", 'chlorophyll': chlorophyll, 'salinity': salinity, 'wind_speed': wind_speed, 'sea_temp': sea_temp})
    else:
        print("unable to get values, not in water!")
        return jsonify({'prediction': "670notinwater", "extra_info":"notinwater"})
    
def isWater(lat,lng):
    api = "https://is-on-water.balbona.me/api/v1/get/"
    response = requests.get(api+str(lat)+"/"+str(lng))
    data = response.json()
    if data["isWater"]:
        return True

def getvaluesfromAPIS(lat, lng):
    # nasa fetch
    nasaapi = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    params = {
    "parameters": "T2M,WS10M",
    "latitude": lat,
    "longitude": lng,
    "community": "RE",
    "format": "JSON"
    }
    response = requests.get(nasaapi, params=params)
    nasdata = response.json()
    print("data:")
    print(nasdata['properties']['parameter'])
    sea_temp = nasdata['properties']['parameter']['T2M'][month_names[month]] # this is the sea temp
    wind_speed = nasdata['properties']['parameter']['WS10M'][month_names[month]]
    chlorophyll, salinity = get_chlorophyll_salinity(lat,lng)
    return sea_temp, chlorophyll, salinity, wind_speed, month

def get_chlorophyll_salinity(lat, lng):
    # erddap api calls lowkey tuffffffffffffff
    # chlorophyll - URL format: variable[(time)][(lat)][(lng)]
    chl_url = f"https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1chla8day.json?chlorophyll[(last)][({lat}):1:({lat})][({lng}):1:({lng})]"
    response1 = requests.get(chl_url)
    print(response1.status_code)
    print(response1.text[:500])  # first 500 chars
    # fallbacks for now
    salinity = 34.0
    chlorophyll = 1.5
    if response1.status_code == 200:
        data = response1.json()
        chlorophyll = data['table']['rows'][0][-1]  # last column is the value
        try:
            response1 = requests.get(chl_url)
            data = response1.json()
            chlorophyll = data['table']['rows'][0][-1]
            if chlorophyll is None:
                chlorophyll = 1.5
        except:
            chlorophyll = 1.5
    # salinity - URL format: variable[(time)][(lat)][(lng)] (same thing twin)
    sal_url = f"https://coastwatch.noaa.gov/erddap/griddap/noaacwSMAPsssDaily.json?sss[(last)][(0.0)][({lat}):1:({lat})][({lng}):1:({lng})]"

    try:
        response2 = requests.get(sal_url)
        data2 = response2.json()
        salinity = data2['table']['rows'][0][-1]
        if salinity is None:
            salinity = 34.0
    except:
        salinity = 34.0 
    return chlorophyll, salinity
if __name__ == '__main__':
    app.run(debug=True)