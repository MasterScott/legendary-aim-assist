import cv2
import os


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

    image_path = 'data/samples/x2/'
    label_path = 'data/labels/x2/labels.txt'

    output = open(label_path, "w+")

    global image
    for image_name in os.listdir(image_path):
        refPt = []
        print(image_path + image_name)
        image = cv2.imread(image_path + image_name)
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
            output.write(image_name + "|" +
                         str(refPt[0][0]) + "|" +
                         str(refPt[0][1]) + "|" +
                         str(refPt[1][0]) + "|" +
                         str(refPt[1][1]) + "\n")

        cv2.destroyAllWindows()
    output.close()


if __name__ == "__main__":
    main()
