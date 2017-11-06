import cv2


class Webcam:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]

    # get the current frame
    def get_current_frame(self):
        self.current_frame = self.video_capture.read()[1]
        return self.current_frame