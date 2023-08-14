import numpy as np
import dlib
import cv2
import math


class OpenAndClose:
    def __init__(self, model, face_cascade):
        self.model = model
        self.face_cascade = face_cascade

    def calculating_mouth_open(self, shape, faceAligned):
        (mStart, mEnd) = (49, 56)
        top_lip1 = shape[mStart:mEnd]
        (mStart, mEnd) = (60, 65)  # Adjusted values of mStart and mEnd
        top_lip2 = shape[mStart:mEnd][::-1]
        top_lip = np.concatenate((top_lip1, top_lip2))
        (mStart, mEnd) = (55, 61)
        bottom_lip1 = shape[mStart:mEnd]
        (mStart, mEnd) = (49, 50)
        bottom_lip2 = shape[mStart:mEnd]
        (mStart, mEnd) = (61, 62)
        bottom_lip3 = shape[mStart:mEnd]
        (mStart, mEnd) = (64, 68)
        bottom_lip4 = shape[mStart:mEnd][::-1]
        bottom_lip = np.concatenate((bottom_lip1, bottom_lip2))
        bottom_lip = np.concatenate((bottom_lip, bottom_lip3))
        bottom_lip = np.concatenate((bottom_lip, bottom_lip4))
        top_lip_height = self.get_lip_height(top_lip)
        bottom_lip_height = self.get_lip_height(bottom_lip)
        mouth_height = self.get_mouth_height(top_lip, bottom_lip)
        ratio = 0.5
        if self.machine_learning_open(faceAligned):
            return (True, mouth_height)
        if mouth_height > min(top_lip_height, bottom_lip_height) * ratio:
            return (True, mouth_height)
        else:
            return (False, mouth_height)


    def calculating_mouth_close(self, shape, faceAligned):
        (mStart, mEnd) = (49, 56)
        top_lip1 = shape[mStart:mEnd]
        (mStart, mEnd) = (60, 65)  # Adjusted values of mStart and mEnd
        top_lip2 = shape[mStart:mEnd][::-1]
        top_lip = np.concatenate((top_lip1, top_lip2))
        (mStart, mEnd) = (55, 61)
        bottom_lip1 = shape[mStart:mEnd]
        (mStart, mEnd) = (49, 50)
        bottom_lip2 = shape[mStart:mEnd]
        (mStart, mEnd) = (61, 62)
        bottom_lip3 = shape[mStart:mEnd]
        (mStart, mEnd) = (64, 68)
        bottom_lip4 = shape[mStart:mEnd][::-1]
        bottom_lip = np.concatenate((bottom_lip1, bottom_lip2))
        bottom_lip = np.concatenate((bottom_lip, bottom_lip3))
        bottom_lip = np.concatenate((bottom_lip, bottom_lip4))
        top_lip_height = self.get_lip_height(top_lip)
        bottom_lip_height = self.get_lip_height(bottom_lip)
        mouth_height = self.get_mouth_height(top_lip, bottom_lip)
        ratio = 0.5
        if self.machine_learning_open(faceAligned):
            return (False, mouth_height)
        if mouth_height > min(top_lip_height, bottom_lip_height) * ratio:
            return (False, mouth_height)
        else:
            return (True, mouth_height)


    def make_prediction(self,unknown):
        unknown = cv2.resize(unknown, (48, 48))
        unknown = unknown / 255.0
        unknown = np.array(unknown).reshape(-1, 48, 48, 1)
        predict = np.argmax(self.model.predict(unknown), axis=1)
        return predict[0]


    def machine_learning_open(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sub_face = gray[y:y + h, x:x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            res = self.make_prediction(sub_face)
            if res == 5:
                return True
        return False

    def progress_mouth_open(self, mouth_height, mouth_height_image):
        if mouth_height > mouth_height_image:
            return True
        else:
            return False

    def progress_mouth_close(self, mouth_height, mouth_height_image):
        if mouth_height < mouth_height_image:
            return True
        else:
            return False


    def get_lip_height(self, lip):
        sum = 0
        for i in [2, 3, 4]:
            distance = math.sqrt((lip[i][0] - lip[12 - i][0]) ** 2 +
                                 (lip[i][1] - lip[12 - i][1]) ** 2)
            sum += distance
        return sum / 3

    def get_mouth_height(self, top_lip, bottom_lip):
        sum = 0
        for i in [8, 9, 10]:
            # distance between two near points up and down
            distance = math.sqrt((top_lip[i][0] - bottom_lip[18 - i][0]) ** 2 +
                                 (top_lip[i][1] - bottom_lip[18 - i][1]) ** 2)
            sum += distance
        return sum / 3

    def check_mouth_open(self, top_lip, bottom_lip):
        top_lip_height = self.get_lip_height(top_lip)
        bottom_lip_height = self.get_lip_height(bottom_lip)
        mouth_height = self.get_mouth_height(top_lip, bottom_lip)
        ratio = 0.5
        if mouth_height > min(top_lip_height, bottom_lip_height) * ratio:
            return True
        else:
            return False

