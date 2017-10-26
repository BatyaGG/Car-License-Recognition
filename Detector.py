import numpy as np
import cv2


class Detector(object):

    def __init__(self, resize_factor, gamma_factor):
        self.resize_factor = resize_factor
        self.gamma_factor = gamma_factor
        self.frame = None

    def process_frame(self, frame):
        self.frame = cv2.resize(frame, (0,0), fx=self.resize_factor, fy=self.resize_factor)
        self.frame = gamma_correction(self.frame, self.gamma_factor)

def gamma_correction(frame, power):
    frame /= 255.0
    frame = cv2.pow(frame, power)
    return np.uint8(frame * 255)

def train_knn():
    kNearest = cv2.ml.KNearest_create()
    npaClassifications = np.loadtxt("classifications.txt", np.float32)  # read in training classifications
    npaFlattenedImages = np.loadtxt("flattened_images.txt", np.float32)  # read in training images
    npaClassifications = npaClassifications.reshape(
        (npaClassifications.size, 1))  # reshape numpy array to 1d, necessary to pass to call to train
    kNearest.setDefaultK(1)  # set default K to 1
    kNearest.train(npaFlattenedImages, cv2.ml.ROW_SAMPLE, npaClassifications)  # train KNN object

def detectPlatesInScene(imgOriginalScene):
    listOfPossiblePlates = []

    height, width, numChannels = imgOriginalScene.shape
    imgContours = np.zeros((height, width, 3), np.uint8)

    imgGrayscaleScene, imgThreshScene = preprocess(imgOriginalScene)         # preprocess to get grayscale and threshold images

    listOfPossibleCharsInScene = findPossibleCharsInScene(imgThreshScene)
    listOfListsOfMatchingCharsInScene = DetectChars.findListOfListsOfMatchingChars(listOfPossibleCharsInScene)

    for listOfMatchingChars in listOfListsOfMatchingCharsInScene:                   # for each group of matching chars
        possiblePlate = extractPlate(imgOriginalScene, listOfMatchingChars)         # attempt to extract plate

        if possiblePlate.imgPlate is not None:                          # if plate was found
            listOfPossiblePlates.append(possiblePlate)                  # add to list of possible plates

    return listOfPossiblePlates

def preprocess(imgOriginal):
    imgGrayscale = extractValue(imgOriginal)

    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)

    height, width = imgGrayscale.shape

    imgBlurred = np.zeros((height, width, 1), np.uint8)

    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    return imgGrayscale, imgThresh

def findPossibleCharsInScene(imgThresh):
    listOfPossibleChars = []                # this will be the return value

    intCountOfPossibleChars = 0

    imgThreshCopy = imgThresh.copy()

    imgContours, contours, npaHierarchy = cv2.findContours(imgThreshCopy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)   # find all contours

    height, width = imgThresh.shape


    return listOfPossibleChars