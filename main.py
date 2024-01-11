import requests
from PIL import Image
from io import BytesIO
import pytesseract
import requests
import os
import cv2
'''
input params:
{
    "username": "Jiyyo230723",
    "password": "Jiyyopass123",
    "patient_age": 23,
    "image_url": "https://firebasestorage.googleapis.com/v0/b/jiyyo-41d75.appspot.com/o/providers%2Fattachments%2F5e8b28bd27a3de2c20cb7f26%2FNewsfeed%2FmultiSelectGroups%2FEye%20Center%20Instagram%20Post.jpg?alt=media&token=2bff4b97-4009-412e-bed0-fd9dd4d3734d"
}
'''
image_url =  "https://firebasestorage.googleapis.com/v0/b/jiyyo-41d75.appspot.com/o/providers%2Fattachments%2F5e8b28bd27a3de2c20cb7f26%2FNewsfeed%2FmultiSelectGroups%2FEye%20Center%20Instagram%20Post.jpg?alt=media&token=2bff4b97-4009-412e-bed0-fd9dd4d3734d"
save_path = 'ocr_pics/img1.jpg'
def download_image(url, save_path):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        
        image = Image.open(BytesIO(response.content))
        image.show()
        image.save('ocr_pics/img1.jpg', format='JPEG')

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")

# Example Usage:
def ocr_create(save_path):
    img = cv2.imread(save_path)
    custom_config = r'--oem 3 --psm 4'
    text = pytesseract.image_to_string(img, config=custom_config)

    print(text)




download_image(image_url, save_path)
ocr_create(save_path)
