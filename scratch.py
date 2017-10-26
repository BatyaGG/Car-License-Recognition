# import the necessary packages
import numpy as np
import cv2


def order_points(pts):
    # pts =np.asarray(pts, dtype=np.float32)
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    for i in range(0, 4):
        rect[i][0] = pts[i][1]
        rect[i][1] = pts[i][0]

    # # the top-left point will have the smallest sum, whereas
    # # the bottom-right point will have the largest sum
    # s = pts.sum(axis=1)
    # rect[0] = pts[np.argmin(s)]
    # rect[2] = pts[np.argmax(s)]
    #
    # # now, compute the difference between the points, the
    # # top-right point will have the smallest difference,
    # # whereas the bottom-left will have the largest difference
    # diff = np.diff(pts, axis=1)
    # rect[1] = pts[np.argmin(diff)]
    # rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # tl = pts[0]
    # tr = pts[1]
    # br = pts[2]
    # bl = pts[3]
    # rect = tl,tr,br,bl
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    # return the warped image
    return warped

# img = cv2.imread('rara2.jpg');
# cv2.imshow('a',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (5, 5), 0)
#
#
# # gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,151,2)
# # gray = cv2.equalizeHist(gray,gray)
#
# cv2.imshow('a',gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# ret,gray = cv2.threshold(gray,190,255,0)
# edged = cv2.Canny(gray, 75, 200)
# cv2.imshow('a',edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

def choose(img,li):
    Q = list();
    Q.append((0, 0));
    Q.append((0, len(img[0]) - 1))
    Q.append((len(img) - 1, len(img[0]) - 1))
    Q.append((len(img[0]) - 1, 0))
    points = list();
    for k in range(0, 4):
        er = 100000000000.0;
        point = (0, 0);
        for i in li:
            error = np.sqrt((Q[k][0] - i[0]) ** 2 + (Q[k][1] - i[1]) ** 2)
            if (er > error):
                er = error
                pt = i
        points.append(pt)

    return points;


def circle_TF(img,x_c,y_c,R):
    count = 0
    l = list()
    for r in range(0, R):
        for x in range(-r, r):
            Y = np.sqrt(r ** 2 - x ** 2)
            Y = round(Y)
            Y = int(Y)
            for y in range(-Y, Y):
                if x_c + x < img.shape[0] and y_c + y < img.shape[1]:
                    count += 1
                    if img[x_c + x][y_c + y] > 0:
                        l.append((x_c + x, y_c + y))
    ratio = float(len(l)) / count

    if (ratio > 0.9):
        return True
    return False;

def find_points(img,R):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(img, (5, 5), 0)
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 201, 2)
    # cv2.imshow('k', gray)
    # cv2.waitKey(0)
    l = []
    xmax = gray.shape[0] - 1;
    ymax = gray.shape[1] - 1;
    for q in range(0, 4):
        for r in range(0, 50):
            for x in range(0, r):
                if q == 0:
                    y = np.sqrt(r ** 2 - x ** 2);
                    y = round(y);
                    x = int(x)
                    y = int(y)
                    if gray[x][y] > 0:
                        if circle_TF(gray, x, y, R):
                            l.append((x, y));

                            q = 1;

                elif q == 1:
                    y = np.sqrt(r ** 2 - x ** 2);
                    y = round(y);
                    x = xmax - x;
                    x = int(x)
                    y = int(y)
                    if gray[x][y] > 0:
                        if circle_TF(gray, x, y, R):
                            l.append((x, y))

                            q = 2;

                elif q == 2:
                    y = np.sqrt(r ** 2 - x ** 2);
                    y = ymax - round(y);
                    x = xmax - x;
                    x = int(x)
                    y = int(y)
                    if gray[x][y] > 0:
                        if circle_TF(gray, x, y, R):
                            l.append((x, y));

                            q = 3;

                elif q == 3:
                    y = np.sqrt(r ** 2 - x ** 2);
                    y = ymax - round(y);
                    x = int(x)
                    y = int(y)
                    if gray[x][y] > 0:
                        if circle_TF(gray, x, y, R):
                            l.append((x, y))
                            r = 50
                            q = 4

    s = set(l)
    l = list(s)
    # for a in l:
    #     x,y = a
    #     img[x-1][y-1] = [255, 0, 0]
    #     img[x-1][y]=[255,0,0]
    #     img[x][y-1] = [255, 0, 0]
    #     img[x][y] = [255, 0, 0]

    # cv2.imshow('k', img)
    # cv2.waitKey(0)
    return l;

def start(ii):
    # ii = cv2.imread('rara1.jpg')
    # cv2.imshow('k',ii)
    # cv2.waitKey(0)
    L = find_points(ii,int(0.02*ii.shape[1]))
    po = choose(ii,L)
    # for a in po:
    #     x, y = a
    #     ii[x - 1][y - 1] = [0, 0, 255]
    #     ii[x - 1][y] = [0, 0,255]
    #     ii[x][y - 1] = [0, 0, 255]
    #     ii[x][y] = [0, 0, 255]
    # cv2.imshow('k',ii)
    # cv2.waitKey(0)
    asd = four_point_transform(ii,po)
    # cv2.imshow('k',asd)
    # cv2.waitKey(0)
    return asd