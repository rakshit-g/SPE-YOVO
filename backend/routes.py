from flask import Blueprint, request, jsonify
import time
from PIL import Image
import io
import base64
import cv2 as cv
from autoage import getFaceBox, age_gender_detector
from adharcheck import aadhar_extract, Validate
routes = Blueprint('routes', __name__)


@routes.route('/', methods=['GET'])
def index():
    return jsonify(message='Welcome to the Flask application!')

#for automated age estimation
@routes.route('/autoage',method=['GET', 'POST'])
def autoage():
    data = request.get_json()
    if data:
        time.sleep(1)
        result = data['data']
        b = bytes(result, 'utf-8')
        image = b[b.find(b'/9'):]
        im = Image.open(io.BytesIO(base64.b64decode(image)))
        im.save('./faces'+'/stranger.jpg')
        
        input = cv.imread('./faces/stranger.jpg')

        cascPath = "haarcascade_frontalface_default.xml"

        # Create the haar cascade
        faceCascade = cv.CascadeClassifier(cascPath)
        gray = cv.cvtColor(input, cv.COLOR_BGR2GRAY)

        # Detect faces in the images
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            # flags = cv2.cv.CV_HAAR_SCALE_IMAGE
        )

        if(len(faces)==0):
            return "No Face Detected", 200

        elif(len(faces)>1):
            return "More Than 1 Face Detected", 200
        
        else:

            output, label = age_gender_detector(input)
            print(label)
            cv.imwrite('./faces/linesDetected.jpg', output)
            return label, 200
        
#for automated age estimation
@routes.route('/aadhar',method=['GET', 'POST'])
def aadhar():
    data = request.get_json()
    if data:
        time.sleep(1)
        result = data['data']
        b = bytes(result, 'utf-8')
        image = b[b.find(b'/9'):]
        im = Image.open(io.BytesIO(base64.b64decode(image)))
        im.save('./aadhar'+'/adhar.jpg')
        data = aadhar_extract(im)
        print(data[0])
        y = (data[0][-4:]) 
        print(y)
        print(type(y)) 
        age = 2022 - int(y)
        vali = Validate(data[1])
        print(data)
        vali = vali + " , age:"+str(age)
    
    return (vali) ,200