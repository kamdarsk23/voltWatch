from time import sleep

import firebase_admin
from firebase_admin import credentials, firestore, auth
from twilio.rest import Client
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

# Initialize Twilio client
account_sid = 'SKd18b275a92f445acdc28d4def7e0ed41'
auth_token = 'J82hapZ5dDzgwimdteM18EaertS6rgVd'
client = Client(account_sid, auth_token)

# Your web app's Firebase configuration
firebase_config = {
  "apiKey": "AIzaSyARWJaT9XwXvPryLn9v15oezFJ7VphnWBE",
  "authDomain": "voltwatch2.firebaseapp.com",
  "projectId": "voltwatch2",
  "storageBucket": "voltwatch2.appspot.com",
  "messagingSenderId": "696119764243",
  "appId": "1:696119764243:web:89ed18774b791e1fe026e6",
  "measurementId": "G-L3LZ084PWS"
}

while True:
    users = db.collection('users').stream()
    for doc in users:
        print(f"{doc.id} => {doc.to_dict()}")
        date = datetime.now()
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
        docs = db.collection("users").document(doc.id).collection(str(date.year) +
                                                           '-' + str(date.month) + '-' + str(date.day)).stream()
        print('hi')
        for minute in docs:
            print(str(minute.to_dict()['timestamp'])[:16])
            time = datetime.strptime(str(minute.to_dict()['timestamp'])[:16], "%Y-%m-%d %H:%M")
            if datetime.now().min == time.min and datetime.now().hour == time.hour:
                if minute.to_dict()['consumption'] > minute.to_dict()['production']:
                    try:
                        user = db.collection("users").document(doc.id).get()
                        print(user.to_dict()['sms'])
                        message = client.messages.create(
                            body='Warning! Your consumption is exceeding the production capacity of your solar panels.',
                            from_='+18449993079',
                            to=user.to_dict()['sms']
                        )
                        print('Message sent successfully, SID: {0}'.format(message.sid))
                    except Exception as e:
                        print('Error sending message: {0}'.format(e))
                break
            # if (minute.to_dict()['timestamp'])

    sleep(60)
