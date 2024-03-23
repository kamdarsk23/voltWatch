from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    welcome_message = "Welcome to our simple Flask app!"
    if request.method == 'POST':
        user_name = request.form['name']
        return render_template('dashboard.html', name=user_name)
    else:
      return render_template('index.html', message=welcome_message)

if __name__ == "__main__":
    app.run(debug=True)
