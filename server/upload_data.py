import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime, timedelta
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

# counter = 0

while True:
    # counter += 1
    users = db.collection('users').stream()
    for doc in users:
        print(f"{doc.id} => {doc.to_dict()}")
        date = datetime.now()
        # date += timedelta(minutes=counter)
        # date -= timedelta(days=1)
        # date -= timedelta(hours=11)
        y = str(date.year)
        m = str(date.month)
        d = str(date.day)
        h = str(date.hour)
        mm = str(date.minute)
        time = ''
        if len(h) != 2:
            time = '0'
        time += h + ':'
        if len(mm) != 2:
            time += '0'
        time += mm
        time += ':00'
        time_data_solar = solar_data[solar_data['Local_Time'].str[-8:] == time]
        time_data_house = house_data[house_data['Local_Time'].str[-8:] == time]
        print(time)
        print(time_data_house)
        solar_power = 0
        if len(time_data_solar) != 0:
            solar_power = time_data_solar.iloc[0]['Power']
            print(solar_power)
        house_power = time_data_house.iloc[0]['Total']
        print(house_power)
        data = {"timestamp": datetime.now(), "production": solar_power, "consumption": house_power}
        db.collection("users").document(doc.id).collection(str(date.year) +
        '-' + str(date.month) + '-' + str(date.day)).document(str(date)).set(data)
    sleep(60)

