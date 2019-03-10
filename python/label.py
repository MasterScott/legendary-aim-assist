import cv2
import os
import time
from actor import Engine, StateManager, ReferenceManager
from adt.Screenshot import Screenshot

def click_and_crop(event, x, y, flags, param):
    global refPt, cropping
    if event == cv2.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False
        cv2.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv2.imshow("image", image)

def main():
    global refPt, cropping

    StateManager.scope = ReferenceManager.Scope.x1t
    image_path = 'data/samples/' + ReferenceManager.scope_string(StateManager.scope) + '/'
    label_path = 'data/labels/' + ReferenceManager.scope_string(StateManager.scope) + '/labels.txt'

    output = open(label_path, "w+")

    global image
    c = 0
    for image_name in os.listdir(image_path):
        refPt = []
        print(image_path + image_name, c)
        c += 0
        image = cv2.imread(image_path + image_name)
        target = Engine.get_target(Screenshot(image, time.time()))
        for i in [(0, 0), (0, 1), (1, 0), (0, -1), (-1, 0)]:
            image[target.y + i[0], target.x + i[1]] = [0, 255, 0]
        clone = image.copy()
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", click_and_crop)
        while True:
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("r"):
                image = clone.copy()
                refPt = []
            elif key == ord("c"):
                break

        if len(refPt) == 2:
            confidence = 1
        else:
            confidence = 0
            refPt = [[-1, -1], [-1, -1]]
        output.write(image_name + "|" +
                     str(confidence) + "|" +
                     str(refPt[0][0]) + "|" +
                     str(refPt[0][1]) + "|" +
                     str(refPt[1][0]) + "|" +
                     str(refPt[1][1]) + "\n")

        cv2.destroyAllWindows()
    output.close()


if __name__ == "__main__":
    main()
