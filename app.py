from flask import Flask, abort, jsonify, request, render_template, json
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

@app.route('/', methods=['GET'])
def display_form():
    return render_template('index.html')

@app.route('/username', methods=['GET'])
def get_username():
    data = jsonify(
        username='thareqyusuf',
        email='thareqmyha@gmail.com',
        id=1234
    )
    return data

if __name__ == '__main__':
    import os
    ENV = os.getenv("APP_ENV")
    if (ENV=='development'):
        app.run(port=os.getenv("APP_PORT"), debug=True)
    elif (ENV=='production'):
        app.run()
