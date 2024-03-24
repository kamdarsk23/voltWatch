import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import root_mean_squared_error
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import matplotlib.pyplot as plt


def get_data():
    data = pd.read_csv('data.csv')
    data['Local_Time'] = pd.to_datetime(data['Local_Time'])
    date = datetime(2020, 4, 1)
    print(data)
    print(date.date())

    results = pd.DataFrame([], columns=['max', 'average'])

    mask = data['Local_Time'].dt.date == date.date()
    day_data = data[mask]
    day_arr = day_data['Total'].values

    while not len(day_arr) == 0:
        results.loc[len(results.index)] = [np.max(day_arr), np.mean(day_arr)]
        # print(results)
        date += timedelta(days=1)
        mask = data['Local_Time'].dt.date == date.date()
        day_data = data[mask]
        day_arr = day_data['Total'].values
        # print(day_arr)
    print(results)
    results.to_csv('Consumption Training.csv')


def create_dataset(data, look_back=1):
    X, y = [], []
    for i in range(len(data) - look_back):
        X.append(data[i:(i + look_back), :])
        y.append(data[i + look_back, :])
    return np.array(X), np.array(y)


def train_model():
    data = pd.read_csv('Consumption Training.csv')
    data = data.iloc[:, 1:]
    print(data)
    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)

    look_back = 1
    X, y = create_dataset(scaled_data, look_back)

    # Split data into training and testing sets
    train_size = int(len(X) * 0.6)
    test_size = int(len(X) * 0.8)
    X_train, X_test, X_val = X[0:train_size], X[train_size:test_size], X[train_size:len(X)]
    y_train, y_test, y_val = y[0:train_size], y[train_size:test_size], y[train_size:len(y)]

    # Define and train the LSTM model
    model = Sequential()
    model.add(LSTM(4, input_shape=(look_back, 2)))
    model.add(Dense(2))
    model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.001))
    model.fit(X_train, y_train, epochs=100, batch_size=1, verbose=2)

    # Make predictions
    # train_predict = model.predict(X_train)
    test_predict = model.predict(X_val)
    print(X_val)

    # Inverse transform the predictions
    # train_predict = scaler.inverse_transform(train_predict)
    test_predict = scaler.inverse_transform(test_predict)

    print(data['max'][train_size:len(data)][:-look_back])
    print(test_predict[:, 0])
    max_MSE = root_mean_squared_error(data['max'][train_size:len(data)][:-look_back], test_predict[:, 0])
    mean_MSE = root_mean_squared_error(data['average'][train_size:len(data)][:-look_back], test_predict[:, 1])

    print(max_MSE)
    print(mean_MSE)

    # Print the predicted values for the next day
    print("Predicted values for the next day:")
    print(test_predict[-1])
    return model


def update_vals(model):
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    users = db.collection('users').stream()
    for doc in users:
        print(f"{doc.id} => {doc.to_dict()['dateUpdated']}")
        current_date = datetime.strptime(str(doc.to_dict()['dateUpdated']).split(' ', 1)[0], "%Y-%m-%d")
        if datetime.now().day > current_date.day:
            data = db.collection('users').document(doc.id).collection(str(current_date.year) + '-' + str(int(current_date.month)) + '-' + str(current_date.day)).stream()
            vals = []
            for d in data:
                consumption_data = d.to_dict()['consumption']  # Extract the 'consumption' parameter from the
                # document
                if consumption_data is not None:
                    vals.append(consumption_data)
            maxCons = np.max(vals)
            average = np.mean(vals)

            data = pd.read_csv('Consumption Training.csv')
            data = data.iloc[:, 1:]
            scaler = MinMaxScaler(feature_range=(0, 1))
            print(data)
            data.loc[len(data.index)] = [maxCons, average]
            scaled_data = scaler.fit_transform(data)
            print(np.array([[scaled_data[len(scaled_data) - 1]]]))
            day_prediction = model.predict(np.array([[scaled_data[len(scaled_data) - 1]]]))
            day_prediction = scaler.inverse_transform(day_prediction)
            print(day_prediction)
            db.collection('users').document(doc.id).update(
                {
                    'dateUpdated': datetime.now(),
                    'maxConsumption': int(day_prediction[0][0]),
                    'averageConsumption': int(day_prediction[0][1])
                }
            )


# get_data()
model = train_model()
update_vals(model)
