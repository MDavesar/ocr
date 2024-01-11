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


image_url =  "https://firebasestorage.googleapis.com/v0/b/jiyyo-41d75-custom-06062019/o/providers%2Fimages%2F613adce4aaaa5f57bb01d951%2FIMG-20230206-WA0005.jpg?alt=media&token=aa2f03ef-8960-4e78-994e-fad29d6395b5"
save_path = 'ocr_pics/img1.jpg'

## logging 
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level to process
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log message format
    handlers=[logging.StreamHandler()]  # Send log messages to the console
)




class Model:
    def __init__(self, save_path, image_url):
        self.save_path = save_path
        self.image_url = image_url
        self.ocr_text = ""

    def download_image(self, url, save_path):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            
            image = Image.open(BytesIO(response.content))
            image.show()
            image.save(save_path, format='JPEG')

        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")

    def ocr_create(self, save_path):
        img = cv2.imread(save_path)
        custom_config = r'--oem 3 --psm 4'
        text = pytesseract.image_to_string(img, config=custom_config)
        print(text)
        return text

    def run(self):
        self.download_image(url=self.image_url, save_path=self.save_path)
        ## reading the image and returning the ocr
        self.ocr_text = self.ocr_create(save_path=self.save_path)
        return self.ocr_text


app = Flask(__name__)

@app.route('/',methods=['GET','POST'])

def welcome():
    #if request.method == 'POST':
    try:
        ## assuming the api to get a json file
        logging.info('Trying to access the json file')
        # response =request.get_json()
        # ## decrypting the json file 
        # data = json.load(response)
        '''
            Create an authenticaton/ authorization process 
            comparing the usernames and the passwords
        '''
        ## geting the image url from the json file
        logging.info('Extracting url from the json file')

        # image_url  = data['image_url']

        ## calling our model
        logging.info('Calling our Model')
        model =  Model(save_path, image_url)
        logging.info('Model working completed')
        text =model.run()
        return text
    except Exception as e:
        #lgr.exception(e)
        logging.error('This is an error message')

        error_m1 = "It's either that you have rendered some inputs empty or its values are out of the range."
        error_m2 = "Please try again with apt values!"
        return "error"


if __name__ == '__main__':
    app.run(debug=True)