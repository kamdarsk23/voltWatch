from flask import Flask, render_template, request, redirect, url_for
from propelauth_flask import init_auth, current_user

app = Flask(__name__)

auth = init_auth(
    "https://819084454.propelauthtest.com",
    "62dd60c6603bce218dafc55b479fe94d09fa07ecbfa95db18ec4843f2a472722ce05372b4ba59a8e1534f00510752d3d",
)

@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         # Process the login form
#         user_name = request.form['name']
#         # In a real application, you'd verify the user details here
#         return render_template('greet.html', name=user_name)
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     return render_template('signup.html')

@app.route('/dashboard')
@auth.require_user
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(debug=True)
