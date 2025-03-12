import requests
from flask import Flask, render_template

from routes import users

app = Flask(__name__)
app.register_blueprint(users.bp)

api_url = 'http://localhost:8000/'


@app.route('/')
def root():
    products = requests.get(f'{api_url}products/').json()
    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
