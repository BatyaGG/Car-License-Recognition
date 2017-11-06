import math

import cv2

from Webcam import Webcam
from Detector import Detector
from FrameToString import FrameToString

webcam = Webcam()
detector = Detector()
frameToString = FrameToString()
font = cv2.FONT_HERSHEY_SIMPLEX
current_license = ''
x = 152
y = 40

while True:
    frame = webcam.get_current_frame()
    plate = detector.process_frame(frame)
    if plate is not None:
        try:
            frame[frame.shape[0] - plate.shape[0] : frame.shape[0], 0 : plate.shape[1]] = plate
        except:
            rows0 = int(math.ceil(0.5 * (frame.shape[0] - plate.shape[0])))
            rows1 = int(math.ceil(0.5 * frame.shape[0]))
            cols0 = 0
            cols1 = int(math.ceil(0.5 * plate.shape[1]))
            frame[rows0 : rows1, cols0 : cols1] = cv2.resize(plate, ((cols1 - cols0), (rows1 - rows0)))
        tesser_out = frameToString.process(plate)
        if tesser_out is not None: current_license = tesser_out
    frame[y:y + 80, x:x + 335, :] = frame[y:y + 80, x:x + 335, :] / 2
    cv2.putText(frame, current_license, (160, 100), font, 2, (255, 255, 255), 2)
    cv2.imshow('vidos1', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break