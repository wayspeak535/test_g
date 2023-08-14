import numpy as np
import dlib
import cv2
import pickle
from OpenAndClose import OpenAndClose


class SmileAndPursing:
    def __init__(self, model, face_cascade):
        self.open_and_close = OpenAndClose(model, face_cascade)
        self.model = model
        self.face_cascade = face_cascade

    def make_prediction(self, unknown):
        unknown = cv2.resize(unknown, (48, 48))
        unknown = unknown / 255.0
        unknown = np.array(unknown).reshape(-1, 48, 48, 1)
        predict = np.argmax(self.model.predict(unknown), axis=1)
        return predict[0]

    def machine_learning_smile(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            sub_face = gray[y:y + h, x:x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            res = self.make_prediction(sub_face)
            if res == 3:
                return True
        return False


    def calculating_lip_pursing(self,shape, faceAligned, lip_width):
        ret_smile, diff_smile = self.calculating_smile(shape, faceAligned, lip_width)
        error_range_lip_pursing = 4
        mouth_height_error = 25
        # 84
        if (lip_width >= 80 and lip_width < 90):
            error_range_smile = 5
            error_range_lip_pursing = error_range_smile + 5
            mouth_height_error = 25

        elif (lip_width >= 70 and lip_width < 80):
            error_range_smile = 3
            error_range_lip_pursing = error_range_smile
            mouth_height_error = 20

        elif lip_width >= 90:
            error_range_smile = 5
            error_range_lip_pursing = error_range_smile + 5
            mouth_height_error = 30

        ret_mouth_open, mouth_height = self.open_and_close.calculating_mouth_open(shape, faceAligned)
        if diff_smile < (lip_width - error_range_lip_pursing) and mouth_height < mouth_height_error:
            return True, diff_smile
        else:
            return False, diff_smile

    def calculating_smile(self, shape, faceAligned, lip_width):
        ret_mouth_open, mouth_height = self.open_and_close.calculating_mouth_open(shape, faceAligned)
        error_range_smile = 4
        mouth_height_error = 25
        if (lip_width >= 80 and lip_width < 90):
            error_range_smile = 5
            mouth_height_error = 25
        elif (lip_width >= 70 and lip_width < 80):
            error_range_smile = 3
            mouth_height_error = 20

        elif lip_width >= 90:
            error_range_smile = 5
            mouth_height_error = 30
        (mStart, mEnd) = (49, 68)
        mouth = shape[mStart:mEnd]
        x49 = mouth[0][0]
        y49 = mouth[0][1]
        x55 = mouth[6][0]
        y55 = mouth[6][1]
        # dist_smilo = 0
        dist_smile = ((x49 - x55) ** 2 + (y49 - y55) ** 2) ** 0.5
        diff_smile = (dist_smile)
        if diff_smile < 0:
            diff_smile *= -1
        if self.machine_learning_smile(faceAligned):
            return True, diff_smile
        if diff_smile > (lip_width + error_range_smile) and mouth_height < mouth_height_error:
            return True, diff_smile
        else:
            return False, diff_smile


    def progress_smile(self,diff_smile, diff_smile_image):
        if diff_smile > diff_smile_image:
            return True
        else:
            return False

    def progress_lip_pursing(self,diff_lip_pursing, diff_lip_pursing_image):
        if diff_lip_pursing < diff_lip_pursing_image:
            return True
        else:
            return False