import time

import cv2

from Webcam import Webcam
from Detector import Detector
from FrameToString import FrameToString


webcam = Webcam()
detector = Detector()
frameToString = FrameToString()
webcam.start()
font = cv2.FONT_HERSHEY_SIMPLEX
current_license = ''
x = 152
y = 40

while True:
    frame = webcam.get_current_frame()
    plate = detector.process_frame(frame)
    if plate is not None:
        cv2.imshow('plate', plate)
        tesser_out = frameToString.process(plate)
        if tesser_out is not None: current_license = tesser_out
    frame[y:y + 80, x:x + 335, :] = frame[y:y + 80, x:x + 335, :] / 2
    cv2.putText(frame, current_license, (160, 100), font, 2, (255, 255, 255), 2)
    cv2.imshow('vidos1', frame)
    time.sleep(0.04)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break