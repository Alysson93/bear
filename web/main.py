from flask import Flask, render_template
import requests

app = Flask(__name__)

api_url = 'http://localhost:8000/'

@app.route('/')
def root():
    products = requests.get(f'{api_url}products/').json()
    return render_template('index.html', products=products)


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)