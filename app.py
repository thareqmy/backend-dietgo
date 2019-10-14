from flask import Flask, abort, jsonify, request, render_template, json
from dotenv import load_dotenv
from keras.models import model_from_json

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

@app.route('/predict', methods=['GET','POST'])
def predict_food():

    # Model reconstruction from JSON file
    with open('model/vgg16.json', 'r') as f:
        model = model_from_json(f.read())

    # Load weights into the new model
    model.load_weights('model/vgg16.h5')
    if request.files:
        image = request.files["image"]
        IMAGE_SIZE = 200
        image = np.expand_dims(image, axis=0)
        result = model.predict(image)[0]
        return jsonify(result)



if __name__ == '__main__':
    import os
    ENV = os.getenv("APP_ENV")
    if (ENV=='development'):
        app.run(port=os.getenv("APP_PORT"), debug=True)
    elif (ENV=='production'):
        app.run()
