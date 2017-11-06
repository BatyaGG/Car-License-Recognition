# Car-License-Recognition

<p align="center"> 
<img src="https://github.com/BatyaGG/Car-License-Recognition/blob/master/recognized.JPG?raw=true"/>
</p>

Car License recognition project implemented on Python using OpenCV and Tesseract. Code consists of 2 main modules: License Detection
and License to String classes. OpenCV is mainly used to detect possible characters in a video stream frames and Tesseract is mainly used
to translate cutted license images to string. License Plates are detected for any country plates, however current recognition works only for Kazakhstan license plate kinds. It can be easily modified to be working for different country plates.

# Installation

Clone or download the project

Install the following packages: numpy <1.11.3>, OpenCV <3.2.0>, Pillow <4.1.1>, Pytesseract <3.02>

Other versions of the packages were not tested, but higher versions are welcome. Report me to b.saduanov@gmail.com if you have any problems.

# Usage

Import local module classes:

```
from Webcam import Webcam
from Detector import Detector
from FrameToString import FrameToString'
```

Initiate them and declare global candidate string:

```
webcam = Webcam()
detector = Detector()
frameToString = FrameToString()
current_license = ''
```

Create mainloop:

```
while True:
    frame = webcam.get_current_frame()
    plate = detector.process_frame(frame)
```

If candidate plate is detected, start scanning it using frameToString object:

```
    if plate is not None:
        tesser_out = frameToString.process(plate)
        if tesser_out is not None: current_license = tesser_out
```

With such pipeline, current_license string will have always most probable license characters.
May be printed, but in my example I just draw it on frame itself.

Use main.py file as an example.

# License Plate Detection

<p align="center"> 
<img src="https://github.com/BatyaGG/Car-License-Recognition/blob/master/how_detector_works.JPG?raw=true" width = '48'>
</p>

Edges are detected using CannyEdge function from OpenCV. Frames are preprocessed beforehand using gaussian bluring to increase signal to noize ratio and adaptive thresholding of images to highlight characters in scene. All edges are stored in a list and their height to width ratios are found. If ratio is set to be 2:1, all edges of ratio close to 2:1 are considered as candidate characters. Only neighbouring candidate characters areas are considered as a candidate plate. All candidate plates are stored in a list and sorted by their area. Biggest possible plate is considered as License Plate and returned by the function.

# License Plate Recognition

License recognition works only for Kazakhstan plates. Since, tesseract-ocr was created for other purposes, it is not so accurate in recognition of characters in license plates. To decrease inaccuracy of the library, its outputs are filtered to have 3 consequtive numbers, 2 or 3 consequtive letters and 2 censequtive numbers. That's why recognition module works only for Kazakhstani plate format. Format can be easily modified to other country patterns in FrameToString class. Also, recognition is done on every single candidate plate detected on video stream frames. Variating results are all stored in HashTable in a form (plate string : occurence_number integer) and the most frequent one is chosen as the best candidate and returned. HashTable is not cleared, hence to test the code on new car, code should be run again.

# Optimization of performance in Plate Detector

Video stream frames are resized to 200:300 shape, without any effects on accuracy of algorithm. Candidate plates are not cropped from frame each time they detected. Only center coordinates, width and height of them are stored in a list of tuples. Finally, the list is sorted by width X height parameter and the parameters having greatest area is chosen from the list. Parameters are rescaled to original size of frame and candidate plate is cropped from original frame only once and returned. This optimization increased performance of plate detection from 20 seconds to 0.2-0.5 seconds per frame.
