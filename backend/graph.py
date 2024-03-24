# from flask import Flask, render_template, request, redirect, url_for, jsonify

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
# from datetime import date

# cred = credentials.Certificate("C:\\Users\\rahil\\Documents\\voltWatch\\cred\\cred_voltWatch.json")
# firebase_admin.initialize_app(cred)

# db = firestore.client()

# app = Flask(__name__)

# text = open('email.txt', 'r')
# email = text.read()
# def assembleDataSet():
#     users_ref = db.collection('users')
#     query_ref = users_ref.where('email', '==', email)
#     users = query_ref.stream()
#     d = []
#     for user in users:
#         uid = user.id
#     today = date.today()
#     collections = db.collection('users').document(f'{uid}').collections()
#     for col in collections:
#         d.append(col)

#     print(d)

# @app.route('/get-data')
# def get_data():
#     data = assembleDataSet()
#     return jsonify(data)

# if __name__ == "__main__":
#     app.run(debug = True)
    
        
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import date

cred = credentials.Certificate("C:\\Users\\rahil\\Documents\\voltWatch\\cred\\cred_voltWatch.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/get-data/<email>')
def get_data(email):
    data = []
    users_ref = firestore.client().collection('users')
    user = users_ref.where('email', '==', email).get()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    for u in user:
        uid = u.id
        collections = users_ref.document(uid).collections()
        for col in collections:
            for doc in col.stream():
                data.append(doc.to_dict())
    print(data)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
