from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Process the login form
        user_name = request.form['name']
        # In a real application, you'd verify the user details here
        return render_template('greet.html', name=user_name)
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
