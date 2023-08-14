from imutils import face_utils
from imutils.face_utils.helpers import FACIAL_LANDMARKS_IDXS
import numpy as np
import imutils
import dlib
import cv2
from scipy.spatial import distance as dist
import pickle


class FacialExpressions:
    def __init__(self):
        print(FacialExpressions)

    def straight_face(self, shape):
        (mStart, mEnd) = (27, 28)
        nose_center = shape[mStart:mEnd]
        (mStart, mEnd) = (39, 40)
        eye_left = shape[mStart:mEnd]
        (mStart, mEnd) = (42, 43)
        eye_right = shape[mStart:mEnd]
        difference = abs(abs(eye_left[0][0] - nose_center[0][0]) - abs(nose_center[0][0] - eye_right[0][0]))
        if difference < 20:
            return True
        return False

    def lip_width_image(self,shape):
        (mStart, mEnd) = (49, 68)
        mouth = shape[mStart:mEnd]
        x49 = mouth[0][0]
        y49 = mouth[0][1]
        x55 = mouth[6][0]
        y55 = mouth[6][1]
        dist_smilo = 0
        dist_smile = ((x49 - x55) ** 2 + (y49 - y55) ** 2) ** 0.5
        diff_smile = dist_smile - dist_smilo
        if diff_smile < 0:
            diff_smile *= -1
        return diff_smile

    def lip_width_image(self,shape):
        (mStart, mEnd) = (49, 68)
        mouth = shape[mStart:mEnd]
        x49 = mouth[0][0]
        y49 = mouth[0][1]
        x55 = mouth[6][0]
        y55 = mouth[6][1]
        dist_smilo = 0
        dist_smile = ((x49 - x55) ** 2 + (y49 - y55) ** 2) ** 0.5
        diff_smile = dist_smile - dist_smilo
        if diff_smile < 0:
            diff_smile *= -1
        return diff_smile

    def shape_to_np(self,shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
        # return the list of (x, y)-coordinates
        return coords


    def get_mouth_loc_with_height(self,image):

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("face_utils/shape_predictor_68_face_landmarks.dat")
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image using the detector
        faces = detector(gray, 0)

        # Loop over each detected face
        for rect in faces:

            # Get the face landmarks using the predictor
            shape1 = predictor(gray, rect)

            # Extract the face encoding from the landmarks
            face_encoding = np.array([])
            for i in range(68):
                x = shape1.part(i).x
                y = shape1.part(i).y
                face_encoding = np.append(face_encoding, [x, y])

            # Store the face location, face encoding, and face landmarks in lists
            face_locations = [(rect.top(), rect.right(), rect.bottom(), rect.left())]
            face_encodings = [face_encoding]
            face_landmarks_list = [shape1.parts()]

            # Compare the face encoding with the known encoding(s)
            match = []  # insert your comparison code here

        x1, y1, w1, h1, h_in, y = 1, 1, 1, 1, 1, 1
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detect faces in the grayscale image
        rects = detector(gray, 1)
        if (len(rects) > 0):
            # loop over the face detections
            for (i, rect) in enumerate(rects):
                # determine the facial landmarks for the face region, then
                # convert the landmark (x, y)-coordinates to a NumPy array
                shape1 = predictor(gray, rect)
                shape = self.shape_to_np(shape1)
                x_lowest_in_face, y_lowest_in_face = shape[9]

                # loop over the face parts individually
                for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():

                    if (name == "mouth"):
                        # extract the ROI of the face region as a separate image
                        (x1, y1, w1, h1) = cv2.boundingRect(np.array([shape[i:j]]))
                    if (name == "inner_mouth"):
                        # loop over the subset of facial landmarks, drawing the
                        # specific face part
                        # for (x, y) in shape[i:j]:
                        # 	cv2.circle(clone, (x, y), 1, (0, 0, 255), -1)
                        # extract the ROI of the face region as a separate image
                        (x, y, w, h) = cv2.boundingRect(np.array([shape[i:j]]))
                        h_in = h
            return {"mouth_x": x1,
                    "mouth_y": y1, "mouth_w": w1, "mouth_h": h1, "image_ret": image, "height_of_inner_mouth": h_in,
                    "inner_mouth_y": y, "y_lowest_in_face": y_lowest_in_face, "shape": shape}
        else:
            return {"error": "true", "message": "No Face Found!"}

    def draw_mouth(self,image, shape):
        # draw mouth points
        (j, k) = FACIAL_LANDMARKS_IDXS["mouth"]
        (r, d) = FACIAL_LANDMARKS_IDXS["left_eye"]
        (f, p) = FACIAL_LANDMARKS_IDXS["right_eye"]
        pts_mouth = shape[j:k]
        pts_left_eye = shape[r: d]
        pts_right_eye = shape[f: p]

        pts_else = shape[0:100]
        for (x, y) in pts_else:
            cv2.circle(image, (x, y), 3, (14, 14, 16), -1)
        for (x, y) in pts_mouth:
            cv2.circle(image, (x, y), 3, (0, 0, 255), -1)
        for (x, y) in pts_left_eye:
            cv2.circle(image, (x, y), 3, (0, 139, 41), -1)
        for (x, y) in pts_right_eye:
            cv2.circle(image, (x, y), 3, (0, 139, 41), -1)
        return image

    def mouth_aspect_ratio(self,shape):
        (mStart, mEnd) = (49, 68)
        mouth = shape[mStart:mEnd]
        A = dist.euclidean(mouth[2], mouth[10])  # 51, 59
        B = dist.euclidean(mouth[4], mouth[8])  # 53, 57
        C = dist.euclidean(mouth[0], mouth[6])  # 49, 55
        mar = (A + B) / (2.0 * C)
        return mar

    def mouth_aspect_ratio_open(self,shape):
        (mStart, mEnd) = (49, 68)
        mouth = shape[mStart:mEnd]
        A = dist.euclidean(mouth[12], mouth[18])  # 62, 68
        B = dist.euclidean(mouth[13], mouth[17])  # 63, 67
        C = dist.euclidean(mouth[14], mouth[16])  # 64, 66
        mar = (A + B + C) / 3.0
        return mar
