from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import csv
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry


def predictSolar(model):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 32.7357,
        "longitude": -97.1081,
        "hourly": ["temperature_2m", "cloud_cover"],
        "timezone": "America/Chicago",
        "forecast_days": 1
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    # print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # print(f"Elevation {response.Elevation()} m asl")
    # print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(1).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "temperature_2m": hourly_temperature_2m, "cloud_cover": hourly_cloud_cover}

    temp_avg = 0.0;
    cloud_avg = 0.0;
    for i in hourly_data["temperature_2m"]:
        temp_avg += i
    temp_avg / len(hourly_data["temperature_2m"])
    for i in hourly_data["cloud_cover"]:
        cloud_avg += i
    cloud_avg / len(hourly_data["cloud_cover"])

    return model.predict(np.array([[temp_avg, cloud_avg]]))[0]


def modelMaker():
    with open('train.csv', mode='r') as file:
        csvFile = csv.reader(file)
        data = list(csvFile)

    data.remove(['temp', 'cloudcover', 'energy'])
    data_array = np.array(data, dtype=float)

    # Split data into input features and target variable
    X = data_array[:, :2]  # Input features (temperature and cloud cover)
    y = data_array[:, 2]  # Output (energy)

    # Split data into training, testing, and validation sets
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.4, random_state=42)  # 60% training
    X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5,
                                                    random_state=42)  # 20% testing, 20% validation

    # Initialize and train MLPRegressor
    model = MLPRegressor(hidden_layer_sizes=(200, 200), activation='relu', solver='adam', random_state=42)
    model.fit(X_train, y_train)

    # Predict on validation set
    print(X_val)
    print(type(X_val))
    y_val_pred = model.predict(X_val)

    # Calculate RMSE on validation set
    rmse = np.sqrt(mean_squared_error(y_val, y_val_pred))
    print("Root Mean Squared Error (RMSE) on validation set:", rmse)

    return model


print(predictSolar(modelMaker()))
