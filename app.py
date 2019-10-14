from flask import Flask, abort, jsonify, request, render_template, json
from dotenv import load_dotenv
from keras.models import model_from_json
import numpy as np
from keras.preprocessing import image as im_g

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

    label = {
        0: 'Bread',
        1: 'Dairy',
        2: 'Dessert',
        3: 'Egg',
        4: 'Fried',
        5: 'Meat',
        6: 'Noodles/Pasta',
        7: 'Rice',
        8: 'Seafood',
        9: 'Soup',
        10: 'Vegetables'
    }

    # Model reconstruction from JSON file
    with open('model/vgg16.json', 'r') as f:
        model = model_from_json(f.read())

    # Load weights into the new model
    model.load_weights('model/vgg16.h5')
    if request.files:
        img = request.files["image"]
        IMAGE_SIZE = 200
        image_path = os.path.join('static/', img.filename)
        img.save(image_path)
        img = im_g.load_img(image_path, target_size=(IMAGE_SIZE, IMAGE_SIZE))
        img = np.expand_dims(img, axis=0)
        result = model.predict(img)[0]


        top_1 = result.argsort()[-1:][::-1]
        return jsonify(predict=label[top_1[0]])



if __name__ == '__main__':
    import os
    ENV = os.getenv("APP_ENV")
    if (ENV=='development'):
        app.run(port=os.getenv("APP_PORT"), debug=True)
    elif (ENV=='production'):
        app.run()
