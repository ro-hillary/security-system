import re
import cv2
import imutils
import numpy as np
import pytesseract
import matplotlib.pyplot as plt
from database import DB

class Processor:
    def __init__(self, width, height, box_width, box_height):
        """Initialize the processor"""
        self.cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        self.width = width
        self.height = height
        self.box_width = box_width
        self.box_height = box_height

        self.cap.set(3, self.width)
        self.cap.set(4, self.height)

        #Database stuff
        self.db = DB()
        # self.db.create()
        # self.data = [
        #      ('01112581680', 'Robert')
        # ]
        # self.db.insert(self.data)


    def visualize(self):
        """Get the current frame"""
        if self.cap is not None:
            ret, frame = self.cap.read()
            if ret:
                cv2.rectangle(frame,
                              (int(self.width / 2 - self.box_width / 2), int(self.height / 2 - self.box_height / 2)),
                              (int(self.width / 2 + self.box_width / 2), int(self.height / 2 + self.box_height / 2)),
                              (0, 255, 0), 2)
                return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def find_text(self, image):
        """Scan the image finding text"""
        pytesseract.pytesseract.tesseract_cmd = 'D:\\UNI\\Progamación\\Python\\IDE\\Tesseract\\tesseract.exe'

        image = image[int(self.height / 2 - self.box_height / 2): int(self.height / 2 + self.box_height / 2),
                int(self.width / 2 - self.box_width / 2 ): int(self.width / 2 + self.box_width / 2), :]


        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        umbral = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        close = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(close, cv2.MORPH_OPEN, kernel)

        kernel = np.ones((3, 1), np.uint8)
        erode = cv2.erode(opening, kernel, iterations=1)

        contours = cv2.findContours(erode.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        chars = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            if w >= 16 and h >= 8:
                chars.append(contour)

        chars = np.vstack([chars[i] for i in range(len(chars))])
        hull = cv2.convexHull(chars)

        mask = np.zeros(image.shape[:2], dtype="uint8")
        cv2.drawContours(mask, [hull], -1, 255, -1)
        mask = cv2.dilate(mask, None, iterations=2)

        final = cv2.bitwise_and(erode, erode, mask=mask)

        config = "--psm 1"

        return pytesseract.image_to_string(final, config=config)

    def get_id(self):
        """Get the id of someone people in the image"""
        text = self.find_text(self.visualize())
        number = ''.join(re.findall(r'\d+', text))

        if len(number) != 11:
            return 'Try again'
        else:
            data = self.db.search(number)
            if len(data) > 0:
                return f'Welcome {data[0][1]}'
            else:
                return 'Not Allowed!'