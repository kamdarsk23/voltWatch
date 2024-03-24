import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime
from time import sleep
import pandas as pd

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

solar_data = pd.read_excel('Solar Data.xlsx')
house_data = pd.read_excel('House Data.xlsx')
solar_data['Local_Time'] = solar_data['Local_Time'].astype(str)
house_data['Local_Time'] = house_data['Local_Time'].astype(str)
print(house_data)

while True:
    users = db.collection('users').stream()
    for doc in users:
        print(f"{doc.id} => {doc.to_dict()}")
        y = str(datetime.now().year)
        m = str(datetime.now().month)
        d = str(datetime.now().day)
        h = str(datetime.now().hour)
        mm = str(datetime.now().minute)
        time = ''
        if len(h) != 2:
            time = '0'
        time += h + ':'
        if len(mm) != 2:
            time += '0'
        time += mm
        time_data_solar = solar_data[solar_data['Local_Time'].str[-5:] == time]
        time += ':00'
        time_data_house = house_data[house_data['Local_Time'].str[-8:] == time]
        print(time)
        print(time_data_house)
        solar_power = 0
        if len(time_data_solar) != 0:
            solar_power = time_data_solar.iloc[0]['Power']
        house_power = time_data_house.iloc[0]['Total']
        print(house_power)
        data = {"production": solar_power, "consumption": house_power}
        db.collection("users").document(doc.id).collection(str(datetime.now().year) +
        '-' + str(datetime.now().month) + '-' + str(datetime.now().day)).document(str(datetime.now())).set(data)
    sleep(60)

