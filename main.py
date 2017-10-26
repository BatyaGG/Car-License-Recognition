from PIL import Image
import pytesseract
import numpy as np
import cv2
from check import stringer
from webcam import Webcam
import thread

# 34/150 ratio

def gamma_correction(img, correction):
    img = img/255.0
    img = cv2.pow(img, correction)
    return np.uint8(img*255)

def IMshow(img):
    w = np.shape(img)[1]
    h = np.shape(img)[0]
    img = cv2.resize(img, (0, 0), fx=500.0/w, fy=200.0/h)
    cv2.imshow('license', img)
    cv2.waitKey(0)

cap = cv2.VideoCapture()
out = cv2.VideoWriter('output.avi',-1, 20.0, (640,480))

webcam = Webcam()
webcam.start()
go = True
font = cv2.FONT_HERSHEY_SIMPLEX
def someFunc():
    global go
    global carlicense2
    font = cv2.FONT_HERSHEY_SIMPLEX
    while go:
        record = webcam.get_current_frame()
        cv2.putText(record, carlicense2, (160, 100), font, 2, (255, 255, 255), 2)
        out.write(record)

thread.start_new_thread(someFunc, ())

#
current = ''
carlicense = ''
carlicense2 = ''
factor = 1
dicionary = {}


while True:
    image = webcam.get_current_frame()
    # image = cv2.imread('licence7.jpg')
    image = cv2.resize(image, (0,0), fx=factor, fy=factor)
    image = gamma_correction(image, 2)

    try:
        text = stringer(image)
        if text != '':
            current = ''
            uwsancount = 0
            uwaripcount = 0
            ekisancount = 0
            for char in text:
                if uwsancount < 3 and (char == '0' or char == '1' or char == '2' or char == '3' or char == '4' or char == '5' or char == '6' or char == '7' or char == '8' or char == '9'):
                        current += char
                        uwsancount += 1
                elif uwaripcount < 3 and uwsancount == 3:
                    if char.isalpha():
                        current += char
                        uwaripcount += 1
                elif ekisancount < 2 and uwaripcount == 3:
                    if char == '0' or char == '1' or char == '2' or char == '3' or char == '4' or char == '5' or char == '6' or char == '7' or char == '8' or char == '9':
                        current += char
                        ekisancount += 1
            if uwaripcount == 3 and uwsancount == 3 and ekisancount == 2:
                carlicense = current
    except:
        continue

    if len(carlicense)==8:
        if dicionary.has_key(carlicense):
                dicionary.update({carlicense:(dicionary[carlicense]+1)})
        else:
            dicionary.update({carlicense:1})
        dicionary.update({carlicense: dicionary[carlicense] + 1})
        keys = dicionary.keys()
        values = dicionary.values()
        carlicense2 = keys[values.index(max(values))]
        carlicense = ''
    # print dicionary


    x = 152
    y = 40
    image[y:y + 80, x:x + 335, :] = image[y:y + 80, x:x + 335, :] / 2;
    cv2.putText(image, carlicense2, (160, 100), font, 2, (255, 255, 255), 2)
    cv2.imshow('vidos1', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        go = False
        break
cap.release()
out.release()
cv2.destroyAllWindows()
        # print 'division by zero'
    # cv2.imshow('vidos1',image)
    # cv2.waitKey(1)
    # factor += 0.1
# print 'finish'
# ----------------------------------------------------------------------------------------------------------------------/
# crop_img.append(image[y:h + y, x:w + x])
# if np.absolute((w/h)**2 - (150/34)**2) <= 100:
#     # cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     crop_img.append(image[y:h + y, x:w + x])
#     # cv2.imshow('wind',image[y:h + y, x:w + x])
#     # cv2.waitKey(0)
#-----------------------------------------------------------------------------------------------------------------------/