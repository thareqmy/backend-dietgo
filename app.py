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
        0: ['Bagel', 165, 'Biscuits', 131, 'Bread (White)', 61],
        1: ['Milk', 91, 'Cheese', 210, 'Yoghurt', 225],
        2: ['Apple Pie', 501, 'Cake', 660, 'Cupcake', 260],
        3: ['Egg', 90, 'Egg Fried', 120, 'Omelette', 165],
        4: ['French Fries', 213, 'Onion Ring', 321, 'Sausage', 351],
        5: ['Beef', 330, 'Chicken', 220, 'Prok', 320],
        6: ['Macaroni', 401, 'Noodle', 210, 'Spagetti', 307],
        7: ['Rice', 200, 'Rice Cake', 327, 'Rice Bowl', 381],
        8: ['Salmon',220, 'Lobster', 192, 'Shrimp', 281],
        9: ['Cream Soup', 213, 'Porridge', 182, 'Soup', 105],
        10: ['Carrot', 31, 'Corn', 81, 'Tomato', 58]
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
        return jsonify(predict1=label[top_1[0]][0], cal1=label[top_1[0]][1], predict2=label[top_1[0]][2], cal2=label[top_1[0]][3], predict3=label[top_1[0]][4], cal3=label[top_1[0]][5])



if __name__ == '__main__':
    import os
    ENV = os.getenv("APP_ENV")
    if (ENV=='development'):
        app.run(port=os.getenv("APP_PORT"), debug=True)
    elif (ENV=='production'):
        app.run()
