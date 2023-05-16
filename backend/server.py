from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from flask_mail import Mail, Message
from PIL import Image
import base64
import io
import numpy as np
import time
import cv2 as cv
import pytesseract
import re
import logging
from PIL import Image
# pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR/tesseract.exe'
import re
import random
import pymongo
from pymongo import MongoClient
from flask_cors import cross_origin

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
logging.debug('Loading networks...')
ageNet = cv.dnn.readNet(ageModel, ageProto)
genderNet = cv.dnn.readNet(genderModel, genderProto)
faceNet = cv.dnn.readNet(faceModel, faceProto)

padding = 20

def getFaceBox(net, frame, conf_threshold=0.7):
    logging.debug('Getting face bounding boxes...')

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
    logging.debug('Detecting age and gender...')

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
    logging.debug('Extracting Aadhar details...')

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
    logging.debug('Validating Aadhar number...')

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
    logging.debug('Performing credit card check...')

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
    logging.debug('Received API request...')

    if data:
        logging.debug('Data received: %s', data)
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
    logging.debug('Received credit API request...')
    if data:
        logging.debug('Data received: %s', data)
        y = json.dumps(data)
        logging.debug('Length of data: %d', len(data['data']))

        check = creditcheck(int(data['data'][1:len(data['data'])-1]))
        if(check == 0):
            logging.debug('Valid credit card')
            return "Valid Credit Card"
        else:
            logging.debug('Invalid credit card')
            return "Invalid credit card"
       
    else:
        logging.debug('No data received')
        return "re enter credit card number"
  
# from config import GMAIL_USERNAME, GMAIL_PASSWORD
GMAIL_USERNAME = "yovo.ageverify@gmail.com"
GMAIL_PASSWORD = "yhlbvoqfaeyazagm"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = GMAIL_USERNAME
app.config['MAIL_PASSWORD'] = GMAIL_PASSWORD
mail = Mail(app)

@app.route('/otp', methods = ['GET','POST'])
def otp():
    logging.debug('Received OTP API request...')
    data = request.get_json()
    logging.debug('Data received: %s', data)
    
    email = data['email']
    password = data['password']

    # Generate a random 6-digit OTP
    otp = str(random.randint(100000, 999999))
    logging.debug('Generated OTP: %s', otp)

    # Send the OTP to the email
    send_otp_email(email, otp)
    logging.debug('OTP sent to email: %s', email)

    response = {
        'otp': otp,
        'message': 'OTP sent successfully.',
    }
    logging.debug('Sending OTP response: %s', response)
    return jsonify(response)


def send_otp_email(email, otp):
    logging.debug('Sending OTP email...')
    msg = Message('OTP Verification', sender='yovo.ageverify@example.com', recipients=[email])
    msg.body = f'Your OTP: {otp}'
    mail.send(msg)
    return



@app.route('/login', methods=['GET', 'POST'])
def login():
    logging.debug('Received login API request...')
    myclient = pymongo.MongoClient("mongodb+srv://speyovo:speyovo123@specluster.cdvtofr.mongodb.net/users?retryWrites=true&w=majority")
    mydb = myclient["users"]
    mycol = mydb['details']

    data = request.get_json()
    logging.debug('Data received: %s', data)

    email = data["email"]
    password = data["password"]

    # Check if the email and password match in the collection
    user = mycol.find_one({"email": email, "password": password})
    if user:
        logging.debug('Login successful.')
        return jsonify({"message": "Login successful."}), 200
    else:
        logging.debug('Invalid email or password.')
        return jsonify({"message": "Invalid email or password."}), 401


@app.route('/verifyage', methods = ['GET','POST'])
@cross_origin(origins=['https://localhost:3000'])
def verifyage():
    logging.debug('Received verifyage API request...')
    myclient = pymongo.MongoClient("mongodb+srv://speyovo:speyovo123@specluster.cdvtofr.mongodb.net/users?retryWrites=true&w=majority")
    mydb = myclient["users"]
    mycol = mydb['details']

    email = request.json['email']
    password = request.json['password']

    mycol.insert_one({
        'email': email,
        'password': password,
        'isVerified': True
    })

    logging.debug('Email and password stored successfully.')
    response = jsonify(message='Email and password stored successfully.')
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response,200

if __name__ == '__main__':
    logging.basicConfig(filename='backend.log', level=logging.DEBUG)
    logging = logging.getLogger()
    app.run(debug=True)


