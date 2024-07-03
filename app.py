from flask import Flask,redirect,render_template,request,jsonify
import requests
from PIL import Image
from io import BytesIO
import pytesseract
import requests
import os
import cv2
import json
import logging
from src.model import Model
from flask_basicauth import BasicAuth
import time


## logging 
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level to process
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log message format
    handlers=[logging.StreamHandler()]  # Send log messages to the console
)




app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'Jiyyo230723'
app.config['BASIC_AUTH_PASSWORD'] = 'Jiyyopass123'
basic_auth = BasicAuth(app)

@app.route('/ocr_extraction',methods=['GET','POST'])

def welcome():
#    if request.method == 'POST':
    try:
        
        model_response = {}
        model_response['model_name'] = "Google Tesseract"
        ## assuming the api to get a json file
        logging.info('Trying to access the json file')
        response =request.get_json()
        # decrypting the json file 
  
        ## geting the image url from the json file
        logging.info('Extracting url from the json file')

        image_url  = response['image_url']
        print(image_url)

        ## calling our model
        start_time = time.time()
        logging.info('Calling our Model')
        model =  Model(image_url)
        logging.info('Model working completed')
        text =model.run()
        end_time = time.time()
        execution_time = end_time - start_time
        model_response['execution_time'] = round(execution_time,2)
        model_response['text'] = text
        return jsonify(model_response)
    except Exception as e:
        #lgr.exception(e)
        logging.error('This is an error message')

        error_m1 = "It's either that you have rendered some inputs empty or its values are out of the range."
        error_m2 = "Please try again with apt values!"
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
