# import all libraries

import pickle
from flask  import Flask, request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd


app = Flask(__name__)
# load model
regmodel = pickle.load(open('regmodel.pkl','rb'))
scaler = pickle.load(open('scaling.pkl','rb'))

# load my pickle file
model = pickle.load(open('regmodel.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')


# Creating predict api
@app.route('/predict_api',methods = ['POST'])

def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1,-1))
    new_data = scaler.transform(np.array(list(data.values())).reshape(1,-1))
    output = regmodel.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods = ['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scaler.transform(np.array(data).reshape(1, -1))  # Make input 2D here
    print(final_input)
    output = regmodel.predict(final_input)[0]
    return render_template("home.html",prediction_text = "The house price prediction is  {}".format(output))

if __name__ =='__main__':
    app.run(debug = True)

