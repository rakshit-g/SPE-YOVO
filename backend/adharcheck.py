import cv2 as cv
import numpy as np
import re
import pytesseract
from PIL import Image

mult = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 0, 6, 7, 8, 9, 5], [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
        [3, 4, 0, 1, 2, 8, 9, 5, 6, 7], [4, 0, 1, 2, 3, 9, 5, 6, 7, 8], [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
        [6, 5, 9, 8, 7, 1, 0, 4, 3, 2], [7, 6, 5, 9, 8, 2, 1, 0, 4, 3], [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
        [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]]
perm = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 5, 7, 6, 2, 8, 3, 0, 9, 4], [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
        [8, 9, 1, 6, 0, 4, 3, 5, 2, 7], [9, 4, 5, 3, 1, 2, 6, 8, 7, 0], [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
        [2, 7, 9, 3, 8, 0, 6, 4, 1, 5], [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]]


def aadhar_extract(img3):
       #any picture
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