from flask import Flask, render_template, request, redirect, url_for, jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date

cred = credentials.Certificate("private/voltwatch-1b0a2-firebase-adminsdk-gri4l-581110b69c.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

text = open('email.txt', 'r')
email = text.read()
data = []
def assembleDataSet():
    users_ref = db.collection('users')
    query_ref = users_ref.where('email', '==', email)
    users = query_ref.stream()
    for user in users:
        uid = user.id
    today = date.today()
    collections = db.collection('users').document(f'{uid}').collections()
    for col in collections:
        data.append(col)

    print(data)

@app.route('/get-data')
def get_data():
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug = True)
    
        
