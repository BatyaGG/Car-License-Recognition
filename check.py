import cv2
import numpy as np
import pytesseract
from PIL import Image
from scratch import start
from MainDetect import main

def IMshow(img):
    w = np.shape(img)[1]
    h = np.shape(img)[0]
    img = cv2.resize(img, (0, 0), fx=900.0/w, fy=600.0/h)
    cv2.imshow('license', img)
    cv2.waitKey(0)

def stringer(img):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # ret,thresh = cv2.threshold(img,127,255,0)
    # # blur = cv2.GaussianBlur(thresh, (9, 9), 0)
    # # edge = cv2.Canny(blur, 0, 255)
    # # thresh = cv2.GaussianBlur(thresh, (5, 5), 0)
    # # cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    #
    # im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    # cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    # kerek = np.zeros((1,1,1))
    # for cnt in cnts:
    #     rect = cv2.minAreaRect(cnt)
    #     box = cv2.boxPoints(rect)
    #     box = np.int0(box)
    #     x, y, w, h = cv2.boundingRect(box)
    #     if w/(h + 0.0000000001) - 3.1 <= 1:
    #         kerek = cnt
    #         break
    # # screenCnt = None
    # # for c in cnts:
    # #     peri = cv2.arcLength(c, True)
    # #     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    # #     if len(approx) == 4:
    # #         screenCnt = approx
    # #         break
    # #
    # if kerek[0,0,0] == 0:
    #     return ''
    #
    # rect = cv2.minAreaRect(kerek)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # # cv2.drawContours(img, [box], 0, (255, 255, 255), 2)
    #
    # x, y, w, h = cv2.boundingRect(box)
    # delta = 0.01
    # x = x - int(w*delta)
    # y = y - int(w*delta)
    # w = w + int(2*delta*w)
    # h = h + int(2*delta*w)
    # if x < 1 or y < 1 or w > img.shape[1] or h > img.shape[0]:
    #     x, y, w, h = cv2.boundingRect(box)
    # current = img[y:(h + y), x:(w + x)]
    # if np.absolute(current.shape[1]/(current.shape[0]+0.0000000001) - 3.1) >= 1:
    #     return 'Not correct ratio'

    current = main(img)
    if current is None:
        return ''

    dst = start(current)
    dst = start(dst)
    # cv2.drawContours(img, [cnts[0]], 0, (255, 255, 255), 2)
    #
    #
    # if current.shape[0] == 0 or current.shape[1] == 0:
    #     return ''
    # ret,thresh = cv2.threshold(current,127,255,0)
    #
    # cv2.imshow('a', current)
    # cv2.waitKey(0)
    #
    # im2,contours,hierarchy = cv2.findContours(thresh, 1, 2)
    # cnts = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
    #
    # if len(cnts) == 0:
    #     return ''
    #
    # screenCnt = None
    # for c in cnts:
    #     peri = cv2.arcLength(c, True)
    #     approx = cv2.approxPolyDP(c, 0.02 * peri, True)
    #     if len(approx) == 4:
    #         screenCnt = approx
    #         break
    # box = np.squeeze(screenCnt)
    # box2 = box
    # rect = cv2.minAreaRect(cnts[0])
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(current,[box],0,(0,0,255),2)
    # cv2.imshow('a', current)
    # cv2.waitKey(0)
    # rows = current.shape[0]
    # cols = current.shape[1]
    # if len(box.shape) == 0:
    #     return ''
    # box = box[0:3, :]
    # box = box.astype('float32')
    # wewant = np.float32([[0,box[0,1]],[0, box[1,1]],[box2[3,0]+cols*0.02, box[1,1]]])
    # warp_mat = cv2.getAffineTransform(box, wewant)
    # warp_dst = np.zeros((np.shape(current)[0], np.shape(current)[1], 3))

    # dst = cv2.warpAffine(current, warp_mat, (cols, rows))
    # cv2.drawContours(current,[box],0,(0,0,255),2)
    # cv2.imshow('a',dst)
    # cv2.waitKey(0)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)

    # doc = doc2text.Document()
    # doc.read(dst)
    # doc.process()
    # doc.extract_text()
    # text = doc.get_text()
    im = Image.fromarray(dst)
    # im.show()
    text = pytesseract.image_to_string(im)
    return text