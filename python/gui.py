# import the necessary packages
import cv2
import numpy as np
import time

from actor import ReferenceManager

# 'optional' argument is required for trackbar creation parameters

hul = 0
huh = 0
sal = 0
sah = 0
val = 0
vah = 0


def set_hul(x):
    global hul
    hul = x
def set_huh(x):
    global huh
    huh = x
def set_sal(x):
    global sal
    sal = x
def set_sah(x):
    global sah
    sah = x
def set_val(x):
    global val
    val = x
def set_vah(x):
    global vah
    vah = x


# Capture video from the stream
cv2.namedWindow('Colorbars')

# assign strings for ease of coding
hh = 'Hue High'
hl = 'Hue Low'
sh = 'Saturation High'
sl = 'Saturation Low'
vh = 'Value High'
vl = 'Value Low'
wnd = 'Colorbars'
# Begin Creating trackbars for each
cv2.createTrackbar(hl, wnd, 0, 179, set_hul)
cv2.createTrackbar(hh, wnd, 0, 179, set_huh)
cv2.createTrackbar(sl, wnd,0,255, set_sal)
cv2.createTrackbar(sh, wnd, 0, 255, set_sah)
cv2.createTrackbar(vl, wnd, 0, 255, set_val)
cv2.createTrackbar(vh, wnd,0,255,set_vah)

# begin our 'infinite' while loop
while (1):
    frame = cv2.imread('out/1551644032232.png')

    # it is common to apply a blur to the frame
    # frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # convert from a BGR stream to an HSV stream
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.bitwise_and(hsv, hsv, mask=ReferenceManager.get_mask(ReferenceManager.Scope.x2))

    # create a mask for that range
    mask = cv2.inRange(hsv, np.array([hul, sal, val]), np.array([huh, sah, vah]))

    res = cv2.bitwise_and(frame, frame, mask=mask)

    c = cv2.Canny(res, 100, 200)
    small_mask = cv2.erode(mask, np.ones((2, 2), np.uint8), iterations=2)
    small_c = cv2.bitwise_and(c, c, mask=small_mask)
    small_c = cv2.dilate(small_c, np.ones((3, 3), np.uint8), iterations=3)

    cv2.imshow('mask', mask)
    cv2.imshow('small_mask', small_mask)
    cv2.imshow('final', small_c)

    k = cv2.waitKey(5)
    if k == ord('q'):
        break

cv2.destroyAllWindows()
