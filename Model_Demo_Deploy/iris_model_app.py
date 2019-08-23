import numpy as np
from flask import Flask, jsonify, request
import pickle

#Our model.
model = pickle.load(open('iris_model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/api', methods=['POST'])
def make_predict():
    #Get the data.
    data = request.get_json(force=True)
    #Transform/parse the data.
    predict_request = [data['SepalLengthCm'], data['SepalWidthCm'], data['PetalLengthCm'], data['PetalWidthCm']]
    predict_request = np.array(predict_request).reshape(1, -1)
    #Predictions
    y_hat = model.predict(predict_request)
    #Send back to the browser.
    output = {'y_hat': int(y_hat[0])}
    return jsonify(results=output)

if __name__ == '__main__':
    app.run(port=9000, debug=True)