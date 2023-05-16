from distutils.log import debug
import email
from tkinter import Y
from attr import validate
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from PIL import Image
import base64
import io
import os
import shutil
import numpy as np
import time
import cv2 as cv
import pytesseract
import re
import dateutil.parser as dparser
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
import os.path
import re
import string
import random
import pymongo
 
# Make a regular expression
# for validating an Email
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

app = Flask(__name__)
CORS(app)

# AUTOMATED AGE ESTIMATION MODEL
faceProto = "modelNweight/opencv_face_detector.pbtxt"
faceModel = "modelNweight/opencv_face_detector_uint8.pb"

ageProto = "modelNweight/age_deploy.prototxt"
ageModel = "modelNweight/age_net.caffemodel"

genderProto = "modelNweight/gender_deploy.prototxt"
genderModel = "modelNweight/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['Not above 18', 'Not above 18', 'Not above 18', 'Above 18','Above 18', 'Above 18', 'Above 18', 'Above 18']
genderList = ['' , '']

mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]


# Load network
ageNet = cv.dnn.readNet(ageModel, ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
faceNet = cv.dnn.readNet(faceModel, faceProto)

padding = 20

def getFaceBox(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)

    net.setInput(blob)
    detections = net.forward()
    bboxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            bboxes.append([x1, y1, x2, y2])
            cv.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, bboxes

def age_gender_detector(frame):
    # Read frame
    t = time.time()
    frameFace, bboxes = getFaceBox(faceNet, frame)
    for bbox in bboxes:
        # print(bbox)
        face = frame[max(0,bbox[1]-padding):min(bbox[3]+padding,frame.shape[0]-1),max(0,bbox[0]-padding):min(bbox[2]+padding, frame.shape[1]-1)]

        blob = cv.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
        genderNet.setInput(blob)
        genderPreds = genderNet.forward()
        gender = genderList[genderPreds[0].argmax()]
        ageNet.setInput(blob)
        agePreds = ageNet.forward()
        age = ageList[agePreds[0].argmax()]

        label = "{},{}".format(gender, age)
        cv.putText(frameFace, label, (bbox[0], bbox[1]-10), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv.LINE_AA)
    return frameFace, label

def aadhar_extract():
    img3 = cv.imread('./aadhar/adhar.jpg')   #any picture
# print(img3.shape)

# removing shadow/noise from image which can be taken from phone camera

    rgb_planes = cv.split(img3)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv.dilate(plane, np.ones((10, 10), np.uint8))        #change the value of (10,10) to see different results
        bg_img = cv.medianBlur(dilated_img, 21)
        diff_img = 255 - cv.absdiff(plane, bg_img)
        norm_img = cv.normalize(diff_img, None, alpha=0, beta=250, norm_type=cv.NORM_MINMAX,
                                                    dtype=cv.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)

    result = cv.merge(result_planes)
    result_norm = cv.merge(result_norm_planes)
    dst = cv.fastNlMeansDenoisingColored(result_norm, None, 10, 10, 7, 11)             # removing noise from image

    text = pytesseract.image_to_string(dst).upper().replace(" ", "")
    data=[]
    date = str(re.findall(r"[\d]{1,4}[/-][\d]{1,4}[/-][\d]{1,4}", text)).replace("]", "").replace("[","").replace("'", "")
    data.append(date)
    number = str(re.findall(r"[0-9]{11,12}", text)).replace("]", "").replace("[","").replace("'", "")
    data.append(number)
    sex = str(re.findall(r"MALE|FEMALE", text)).replace("[","").replace("'", "").replace("]", "")
    data.append(sex)

    # cv.imshow('original',img3)
    # cv.imshow('edited',dst)
    # cv.waitKey(0)
    # cv.destroyAllWindows()


    # crop_pic from ID card

    gray = cv.cvtColor(img3, cv.COLOR_BGR2GRAY)
    face_cascade = cv.CascadeClassifier(cv.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.3, 7)
    for (x, y, w, h) in faces:
        ix = 0
        cv.rectangle(img3, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = img3[y:y + h, x:x + w]
        #crop_pic = cv.imwrite('croppic10.jpg', roi_color)
        # crop_pic = cv.imshow('croppicds', roi_color)
        # cv.waitKey(0)
        # cv2.destroyAllWindows()
    return data

def Validate(aadharNum):
    try:
        i = len(aadharNum)
        if(i!=12):
            return 'short Aadhar Number'
        else:
            j = 0
            x = 0

            while i > 0:
                i -= 1
                x = mult[x][perm[(j % 8)][int(aadharNum[i])]]
                j += 1
            if x == 0:
                return 'Valid Aadhar Number'
            else:
                return 'Invalid Aadhar Number'

    except ValueError:
        return 'Invalid Aadhar Number'
    except IndexError:
        return 'Invalid Aadhar Number'

def creditcheck(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10


@app.route('/api', methods = ['GET','POST'])
def api():
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

@app.route('/aadhar', methods = ['GET','POST'])
def aadhar():
    data = request.get_json()
    if data: 
        time.sleep(1)
        result = data['data']
        b = bytes(result, 'utf-8')
        image = b[b.find(b'/9'):]
        im = Image.open(io.BytesIO(base64.b64decode(image)))
        im.save('./aadhar'+'/adhar.jpg')
        data = aadhar_extract()
        print(data[0])
        y = (data[0][-4:]) 
        print(y)
        print(type(y)) 
        age = 2023 - int(y)
        vali = Validate(data[1])
        print(data)
        vali = vali + " , age:"+str(age)
    
    return (vali) ,200

@app.route('/credit', methods = ['GET','POST'])
def credit():
    data = request.get_json()
    if data:
        y = json.dumps(data)
        print (len(data['data']))
        check = creditcheck(int(data['data'][1:len(data['data'])-1]))
        if(check == 0):
            return "Valid Credit Card"
        else:
            return "Invalid credit card"
       
    else:
        return "re enter credit card number"

import random
import smtplib
import math
import string    
import random
from flask_mail import Mail, Message
from config import GMAIL_USERNAME, GMAIL_PASSWORD

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = GMAIL_USERNAME
app.config['MAIL_PASSWORD'] = GMAIL_PASSWORD
mail = Mail(app)

@app.route('/otp', methods = ['GET','POST'])
def otp():
    data = request.get_json()
    email = data['email']
    password = data['password']

    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Send the OTP to the email
    send_otp_email(email, otp)

    response = {
        'otp': otp,
        'message': 'OTP sent successfully.',
    }
    return jsonify(response)

def send_otp_email(email, otp):
    msg = Message('OTP Verification', sender='your-email@example.com', recipients=[email])
    msg.body = f'Your OTP: {otp}'
    mail.send(msg)

# @app.route('/token', methods = ['GET','POST'])
# def token():
#     data = request.get_json()
#     emailid = data['data'][1:len(data['data'])-1]
#     print((emailid))
#     res = ''.join(random.choices(string.ascii_uppercase +
#                              string.digits, k = 16))
#     s = smtplib.SMTP('smtp.gmail.com', 587)
#     s.starttls()
#     s.login("anturakshit83@gmail.com", "dsci@123")
   
#     s.sendmail('Your YOVO AGE-TOKEN ',emailid,(res))
#     myclient= pymongo.MongoClient("mongodb+srv://dsci:<dsci123>@cluster0.xbsr3.mongodb.net/user?retryWrites=true&w=majority")
#     mydb= myclient["user"]
#     mycol = mydb['agetokens']
#     record = {
#         # "_id": 1,
#         "emailID": emailid,
#         "token": res
#     }
#     mycol.insert_one(record)

#     print(res)
#     return res,200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json  # Assuming the data is sent as JSON
        
        # Retrieve the email and password from the request data
        email = data.get('email')
        password = data.get('password')
        
        # Perform your login validation logic here
        # Example: Check if email and password are valid
        
        if email and password:
            # Login validation logic goes here
            # Example: Check if the email and password are correct
            
            # If the login is successful, you can return a success message
            response = {"message": "Login successful"}
            return jsonify(response), 200
        else:
            # If the login fails, you can return an error message
            response = {"message": "Invalid email or password"}
            return jsonify(response), 401
    else:
        # Handle GET requests if necessary
        # ...
        pass

from pymongo import MongoClient

@app.route('/verifyage', methods = ['GET','POST'])
def verifyage():
    myclient= pymongo.MongoClient("mongodb+srv://speyovo:<speyovo123>@specluster.cdvtofr.mongodb.net/?retryWrites=true&w=majority")
    mydb= myclient["users"]
    mycol = mydb['details']

    email = request.json['email']
    password = request.json['password']

    mycol.insert_one({
        'email': email,
        'password': password,
        'isVerified': True
    })

   
    return jsonify(message='Email and password stored successfully.')

if __name__ == '__main__':
    app.run()


if __name__=="__main__":
    app.run(debug= True)

