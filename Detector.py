import math

import numpy as np
import cv2


import PossibleChar


PLATE_WIDTH_PADDING_FACTOR = 1.3
PLATE_HEIGHT_PADDING_FACTOR = 1.5
MAX_DIAG_SIZE_MULTIPLE_AWAY = 5.0
MAX_CHANGE_IN_AREA = 0.5
MAX_CHANGE_IN_WIDTH = 0.8
MAX_CHANGE_IN_HEIGHT = 0.2
MAX_ANGLE_BETWEEN_CHARS = 12.0
MIN_NUMBER_OF_MATCHING_CHARS = 3
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9


class Detector(object):
    def __init__(self, resize_factor=None, gamma_factor=None):
        self.resize_factor = resize_factor
        self.gamma_factor = gamma_factor
        self.frame = None
        self.frame_gray = None

    def process_frame(self, frame):
        self.frame = frame
        if self.resize_factor is None:
            self.resize_factor = 300.0/frame.shape[1]
        self.frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.frame_gray = cv2.resize(self.frame_gray, (0,0), fx=self.resize_factor, fy=self.resize_factor)
        if self.gamma_factor is None:
            self.gamma_factor = np.average(self.frame_gray) / 50
        self.frame_gray = gamma_correction(self.frame_gray, self.gamma_factor)
        possible_plates_characteristics = detect_plates(self.frame_gray, self.resize_factor)
        possible_plates_characteristics.sort(key=lambda characteristic: characteristic[1] * characteristic[2], reverse=True)
        try:
            lic_characteristics = possible_plates_characteristics[0]
        except:
            return
        img_original_rotated = cv2.warpAffine(self.frame, lic_characteristics[0], (self.frame.shape[1], self.frame.shape[0]))
        lic_plate = cv2.getRectSubPix(img_original_rotated, (lic_characteristics[1], lic_characteristics[2]), tuple(lic_characteristics[3]))
        return lic_plate


def gamma_correction(frame, power):
    frame = frame / 255.0
    frame = cv2.pow(frame, power)
    return np.uint8(frame * 255)


def detect_plates(frame, resize_ratio):
    possible_plates_characteristics = []
    img_thresh = thresholding(frame)
    possible_chars = find_possible_chars(img_thresh)
    list_of_lists_of_matching_chars_in_scene = find_list_of_lists_of_matching_chars(possible_chars)
    for listOfMatchingChars in list_of_lists_of_matching_chars_in_scene:
        plate_characteristics = extract_plate(listOfMatchingChars, resize_ratio)
        if plate_characteristics[1] is not None:
            possible_plates_characteristics.append(plate_characteristics)
    return possible_plates_characteristics


def extract_plate(list_of_matching_chars, resize_ratio):
    list_of_matching_chars.sort(key = lambda current_matching_char: current_matching_char.intCenterX)
    flt_plate_center_x = (list_of_matching_chars[0].intCenterX +
                          list_of_matching_chars[len(list_of_matching_chars) - 1].intCenterX) / 2.0
    flt_plate_center_y = (list_of_matching_chars[0].intCenterY +
                          list_of_matching_chars[len(list_of_matching_chars) - 1].intCenterY) / 2.0
    pt_plate_center_original = flt_plate_center_x / resize_ratio, flt_plate_center_y / resize_ratio
    int_plate_width = int((list_of_matching_chars[len(list_of_matching_chars) - 1].intBoundingRectX +
                          list_of_matching_chars[len(list_of_matching_chars) - 1].intBoundingRectWidth -
                          list_of_matching_chars[0].intBoundingRectX) * PLATE_WIDTH_PADDING_FACTOR)
    int_plate_width_original = int(int_plate_width / resize_ratio)
    int_total_of_char_heights = 0
    for matching_char in list_of_matching_chars:
        int_total_of_char_heights += matching_char.intBoundingRectHeight
    flt_average_char_height = int_total_of_char_heights / len(list_of_matching_chars)
    int_plate_height = int(flt_average_char_height * PLATE_HEIGHT_PADDING_FACTOR)
    int_plate_height_original = int(int_plate_height / resize_ratio)
    flt_opposite = list_of_matching_chars[len(list_of_matching_chars) - 1].intCenterY - list_of_matching_chars[0].intCenterY
    flt_hypotenuse = distance_between_chars(list_of_matching_chars[0], list_of_matching_chars[len(list_of_matching_chars) - 1])
    flt_correction_angle_in_rad = math.asin(flt_opposite / flt_hypotenuse)
    flt_correction_angle_in_deg = flt_correction_angle_in_rad * (180.0 / math.pi)
    rotation_matrix_original = cv2.getRotationMatrix2D(tuple(pt_plate_center_original), flt_correction_angle_in_deg, 1.0)
    return rotation_matrix_original, int_plate_width_original, int_plate_height_original, pt_plate_center_original


def find_list_of_lists_of_matching_chars(possible_chars):
    list_of_lists_of_matching_chars = []
    for possible_char in possible_chars:
        list_of_matching_chars = find_list_of_matching_chars(possible_char, possible_chars)
        list_of_matching_chars.append(possible_char)
        if len(list_of_matching_chars) < MIN_NUMBER_OF_MATCHING_CHARS:
            continue
        list_of_lists_of_matching_chars.append(list_of_matching_chars)
        chars_with_current_matches_removed = list(set(possible_chars) - set(list_of_matching_chars))
        recursive_matrix_of_matching_chars = find_list_of_lists_of_matching_chars(chars_with_current_matches_removed)
        for recursive_vector_of_matching_chars in recursive_matrix_of_matching_chars:
            list_of_lists_of_matching_chars.append(recursive_vector_of_matching_chars)
        break
    return list_of_lists_of_matching_chars


def find_list_of_matching_chars(possible_char, list_of_chars):
    list_of_matching_chars = []
    for possible_matching_char in list_of_chars:  # for each char in big list
        if possible_matching_char == possible_char:
            continue
        flt_distance_between_chars = distance_between_chars(possible_char, possible_matching_char)
        flt_angle_between_chars = angle_between_chars(possible_char, possible_matching_char)
        flt_change_in_area = float(
            abs(possible_matching_char.intBoundingRectArea - possible_char.intBoundingRectArea)) / float(
            possible_char.intBoundingRectArea)
        flt_change_in_width = float(
            abs(possible_matching_char.intBoundingRectWidth - possible_char.intBoundingRectWidth)) / float(
            possible_char.intBoundingRectWidth)
        flt_change_in_height = float(
            abs(possible_matching_char.intBoundingRectHeight - possible_char.intBoundingRectHeight)) / float(
            possible_char.intBoundingRectHeight)
        if (flt_distance_between_chars < (possible_char.fltDiagonalSize * MAX_DIAG_SIZE_MULTIPLE_AWAY) and
                flt_angle_between_chars < MAX_ANGLE_BETWEEN_CHARS and
                flt_change_in_area < MAX_CHANGE_IN_AREA and
                flt_change_in_width < MAX_CHANGE_IN_WIDTH and
                flt_change_in_height < MAX_CHANGE_IN_HEIGHT):
            list_of_matching_chars.append(possible_matching_char)
    return list_of_matching_chars


def distance_between_chars(first_char, second_char):
    int_x = abs(first_char.intCenterX - second_char.intCenterX)
    int_y = abs(first_char.intCenterY - second_char.intCenterY)
    return math.sqrt((int_x ** 2) + (int_y ** 2))


def angle_between_chars(first_char, second_char):
    flt_adj = float(abs(first_char.intCenterX - second_char.intCenterX))
    flt_opp = float(abs(first_char.intCenterY - second_char.intCenterY))
    flt_angle_in_rad = math.atan(flt_opp / flt_adj) if flt_adj != 0.0 else 1.5708
    flt_angle_in_deg = flt_angle_in_rad * (180.0 / math.pi)
    return flt_angle_in_deg


def find_possible_chars(img_thresh):
    possible_chars = []
    count_possible_chars = 0
    img_thresh_copy = img_thresh.copy()
    img_contours, contours, npa_hierarchy = cv2.findContours(img_thresh_copy, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(0, len(contours)):
        possible_char = PossibleChar.PossibleChar(contours[i])
        if possible_char.if_possible:
            count_possible_chars += 1
            possible_chars.append(possible_char)
    return possible_chars


def thresholding(img_gray):
    img_contrast = maximize_contrast(img_gray)
    img_blur = cv2.GaussianBlur(img_contrast, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
    img_thresh = cv2.adaptiveThreshold(img_blur, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)
    return img_thresh


def maximize_contrast(img_gray):
    structuring_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    img_top_hat = cv2.morphologyEx(img_gray, cv2.MORPH_TOPHAT, structuring_element)
    img_black_hat = cv2.morphologyEx(img_gray, cv2.MORPH_BLACKHAT, structuring_element)
    img_gray_plus_top_hat = cv2.add(img_gray, img_top_hat)
    img_gray_plus_top_hat_minus_black_hat = cv2.subtract(img_gray_plus_top_hat, img_black_hat)
    return img_gray_plus_top_hat_minus_black_hat


if __name__ == '__main__':
    imgFile = cv2.imread('licence2.jpg')
    detector = Detector()
    plate = detector.process_frame(imgFile)
    cv2.namedWindow('plate', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('plate', 600, 150)
    cv2.imshow('plate', plate)
    cv2.imwrite('plate2.jpg', plate)
    cv2.waitKey(0)
