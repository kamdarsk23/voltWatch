from flask import Flask, render_template, request, redirect, url_for

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("private/voltwatch-1b0a2-firebase-adminsdk-gri4l-581110b69c.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

app = Flask(__name__)

def updateDb(name, address, avgConsumption, date, email, maxConsumption, phone, solarConsumption, solarProvider):
    data = {
        'name': name,
        'address': address,
        'averageConsumption': avgConsumption,
        'dateUpdated': date,
        'email': email,
        'maxConsumption': maxConsumption,
        'sms': phone,
        'solarConsumption': solarConsumption,
        'solar_provider': solarProvider
    }

    doc_ref = db.collection('users').document()
    doc_ref.set(data)
    print('document id: ', doc_ref.id)

def checkForSameEmail(email):
    #query the users collection where 
    users_ref = db.collection('users')
    query_ref = users_ref.where('email', '==', email)
    users = query_ref.stream()

    #email must be unique across users
    #iterate through all users to check if same email exists
    user_counter = 0

    for user in users:
        user_counter += 1
        print(user.to_dict())

    # update database with new registration only if no duplicate emails
    if (user_counter == 0):
        return True
    else: 
        return False

# by default, avgConsumption, maxConsumption, and solarConsumption are Null 
# until user links data
avgConsumption = None
maxConsumption = None
solarConsumption = None


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("trying to login...")
        # Process the login form
        # check user auth 
        # send to dashboard if success, else send back to login
        email = request.form['email']
        password = request.form['password']
        # form data is stored in email and password variables

        print("submitted email = " + email)
        print("submitted password = " + password)
        # note: uses "name" HTML attribute to pull data


        # assuming auth, send to dashboard 
        return redirect(url_for('dashboard'))
    elif request.method == 'GET':
        return render_template('login.html')

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print('trying to sign up...')
        # all user info send to firebase
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']
        provider = request.form['provider']

        print(name, email, phone, password, address, provider)
        print("sign up test")

        if (checkForSameEmail(email)):
            updateDb(name, address, avgConsumption, None, email, maxConsumption, phone, solarConsumption, provider)
        else:
            print("email already in use")
        # assume valid, send to login
        return redirect(url_for('login'))
    elif request.method == 'GET':
        return render_template('signup.html')
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    # Dashboard page logic
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
