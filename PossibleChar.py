import math
import cv2


MIN_PIXEL_WIDTH = 2
MIN_PIXEL_HEIGHT = 8
MIN_ASPECT_RATIO = 0.25
MAX_ASPECT_RATIO = 1
MIN_PIXEL_AREA = 80


class PossibleChar:
    def __init__(self, contour):
        self.contour = contour
        self.boundingRect = cv2.boundingRect(self.contour)
        self.intBoundingRectX, self.intBoundingRectY, self.intBoundingRectWidth, self.intBoundingRectHeight = self.boundingRect
        self.intBoundingRectArea = self.intBoundingRectWidth * self.intBoundingRectHeight
        self.intCenterX = (self.intBoundingRectX + self.intBoundingRectX + self.intBoundingRectWidth) / 2
        self.intCenterY = (self.intBoundingRectY + self.intBoundingRectY + self.intBoundingRectHeight) / 2
        self.fltDiagonalSize = math.sqrt((self.intBoundingRectWidth ** 2) + (self.intBoundingRectHeight ** 2))
        self.fltAspectRatio = float(self.intBoundingRectWidth) / float(self.intBoundingRectHeight)
        self.if_possible = True if (self.intBoundingRectArea > MIN_PIXEL_AREA and
            self.intBoundingRectWidth > MIN_PIXEL_WIDTH and self.intBoundingRectHeight > MIN_PIXEL_HEIGHT and
            MIN_ASPECT_RATIO < self.fltAspectRatio < MAX_ASPECT_RATIO) else False