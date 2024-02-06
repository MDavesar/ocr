from flask import Flask,redirect,render_template,request,jsonify
import requests
from PIL import Image
from io import BytesIO
import pytesseract
import requests
import os
import cv2
import logging
## logging 
logging.basicConfig(
    level=logging.DEBUG,  # Set the minimum level to process
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define log message format
    handlers=[logging.StreamHandler()]  # Send log messages to the console
)


class Model:
    def __init__(self, image_url):
        self.image_path = None
        self.image_url = image_url
        self.ocr_text = ""

    def download_image(self, url):
        try:
            logging.info('Sending Get request to the url')
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            ## creating a new directory t save the data
            logging.info('Checking the directory path')
            directory_path = 'ocr_pics'

            # Check if the directory exists
            if not os.path.exists('ocr_pics'):
                # Create the directory if it doesn't exist
                os.makedirs(directory_path)
                print(f'Directory "{directory_path}" created.')
            else:
                print(f'Directory "{directory_path}" already exists.')
            self.image_path = os.path.join(directory_path,'ocr_image.jpg')
            logging.info('Trying I/O open the image')
            image = Image.open(BytesIO(response.content))
            logging.info('Showing the Image')
            '''
                If we want to display the image
                image.show()
            '''
            logging.info('Saving the Image')
            image.save(self.image_path)

        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")

    def ocr_create(self):
        logging.info('Inside OCR create')
        img = cv2.imread(self.image_path)
        custom_config = r'--oem 3 --psm 4'
        text = pytesseract.image_to_string(img, config=custom_config)
        return text

    def run(self):
        self.download_image(url=self.image_url)
        ## reading the image and returning the ocr
        self.ocr_text = self.ocr_create()
        return self.ocr_text
