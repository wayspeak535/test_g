import numpy as np
from imutils import face_utils
import imutils
import dlib
import cv2
from FacialExpressions import FacialExpressions
from SmileAndPursing import SmileAndPursing
from OpenAndClose import OpenAndClose
import pickle
import urllib.request


class AnalysisFrame:
    def __init__(self):
        predictor = dlib.shape_predictor(
            "face_utils/shape_predictor_68_face_landmarks.dat")
        self.fa = face_utils.FaceAligner(predictor, desiredFaceWidth=500)
        self.detector = dlib.get_frontal_face_detector()
        with open('face_utils/facial_expression_recognition.pkl', 'rb') as f:
            model = pickle.load(f)
        face_cascade = cv2.CascadeClassifier("face_utils/haarcascade_frontalface_default.xml")
        self.facial_expressions = FacialExpressions()
        self.smile_and_pursing = SmileAndPursing(model, face_cascade)
        self.open_and_close = OpenAndClose(model, face_cascade)

    def download_image_from_url(self, url):
        # Download the image from the URL and return the image data
        with urllib.request.urlopen(url) as response:
            image_data = response.read()
        return image_data

    import urllib.parse
    import urllib.request



    # def download_image_from_url(self, url):
    #     # Remove query parameters from the URL
    #     parsed_url = urllib.parse.urlparse(url)
    #     clean_url = urllib.parse.urlunparse(parsed_url._replace(query=''))
    #
    #     # Remove any trailing whitespaces from the URL
    #     clean_url = clean_url.strip()
    #
    #     # Download the image data from the cleaned URL
    #     with urllib.request.urlopen(clean_url) as response:
    #         image_data = response.read()
    #     return image_data

    def lip_width_image_get(self,file):
        if 'https://' in file:
            image_data = self.download_image_from_url(file)
            image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        else:
            image = cv2.imread(file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 2)
        faceAligned = self.fa.align(image, gray, rects[0])
        frame = faceAligned
        enhanced = cv2.detailEnhance(frame, sigma_s=10, sigma_r=0.15)
        frame = imutils.resize(frame, width=500)
        result = self.facial_expressions.get_mouth_loc_with_height(enhanced)
        lip_width = 85
        message = 'Face detected!'
        if (self.checkKey(result, "error")):
            message = result['message']
            cv2.imshow("output", frame)
            cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 0, 0), 1)
        else:
            shape = result['shape']
            lip_width = self.facial_expressions.lip_width_image(shape)

        return lip_width


    def analysis_one_frame(self,frame1):
        gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 2)
        if rects is not None:
            if len(rects) > 0:
                faceAligned = self.fa.align(frame1, gray, rects[0])
                frame = faceAligned
                enhanced = cv2.detailEnhance(frame, sigma_s=10, sigma_r=0.15)
                frame = imutils.resize(frame, width=500)
                result = self.facial_expressions.get_mouth_loc_with_height(enhanced)
                message = 'Face detected!'
                if (self.checkKey(result, "error")):
                    message = result['message']
                    cv2.imshow("output", frame)
                    cv2.putText(frame, message, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (0, 0, 0), 1)
                    return None, None, None
                else:
                    shape = result['shape']
                    frame = self.facial_expressions.draw_mouth(frame, shape)
                    return shape, frame, faceAligned
            else:
                return None, None, None

        else:
            return None, None, None


    def analysis_facial_expressions(self,lip_width_normal, shape, frame, faceAligned,shape_best,  frame_best, faceAligned_best, type_result):

        ret_straight_face = self.facial_expressions.straight_face(shape)
        result_max = 0
        text = ''
        progress_bool = False
        if ret_straight_face:
            if type_result == 'mouth_open':
                ret_mouth_open, mouth_height = self.open_and_close.calculating_mouth_open(shape, faceAligned)
                result_max = mouth_height
                if shape_best is not None:
                    ret_mouth_open_image, mouth_height_image = self.open_and_close.calculating_mouth_open(shape_best,
                                                                                                          faceAligned_best)
                    progress_bool_open = self.open_and_close.progress_mouth_open(mouth_height, mouth_height_image)
                    progress_bool = progress_bool_open
                else:
                    progress_bool_open = True
                    progress_bool = True
                if ret_mouth_open:
                    text = 'open mouth'
                    cv2.putText(frame, "facial expression performed: " + text, (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (255, 255, 255), 1)
                    cv2.putText(frame, "progress: " + str(progress_bool_open), (10, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

            if type_result == 'mouth_close':
                ret_mouth_close, mouth_height = self.open_and_close.calculating_mouth_close(shape, faceAligned)
                result_max = mouth_height
                if shape_best is not None:
                    ret_mouth_open_image, mouth_height_image = self.open_and_close.calculating_mouth_open(shape_best,
                                                                                                          faceAligned_best)
                    progress_bool_close = self.open_and_close.progress_mouth_close(mouth_height, mouth_height_image)
                    progress_bool = progress_bool_close
                else:
                    progress_bool_close = True
                    progress_bool = True
                if ret_mouth_close:
                    text = 'close mouth'
                    cv2.putText(frame, "facial expression performed: " + text, (10, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (255, 255, 255), 1)

                    cv2.putText(frame, "progress: " + str(progress_bool_close), (10, 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 1)

            if type_result == 'smile':
                ret_smile, diff_smile = self.smile_and_pursing.calculating_smile(shape, faceAligned,
                                                                                 lip_width_normal)
                result_max = diff_smile
                if shape_best is not None:
                    ret_smile_image, diff_smile_image = self.smile_and_pursing.calculating_smile(shape_best, faceAligned_best,
                                                                                                 lip_width_normal)

                    progress_bool = self.smile_and_pursing.progress_smile(diff_smile, diff_smile_image)
                else:
                    progress_bool = True

                if ret_smile:
                    cv2.putText(frame, "facial expression performed: " + "smile", (10, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (255, 255, 255), 1)
                    cv2.putText(frame, "progress: " + str(progress_bool), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (255, 255, 255), 1)

            if type_result == 'lip_pursing':
                ret_lip_pursing, diff_lip_pursing = self.smile_and_pursing.calculating_lip_pursing(shape,
                                                                                                   faceAligned,
                                                                                                   lip_width_normal)
                result_max = diff_lip_pursing

                if shape_best is not None:
                    ret_lip_pursing_image, diff_lip_pursing_image = self.smile_and_pursing.calculating_lip_pursing(
                        shape_best,
                        faceAligned_best,
                        lip_width_normal)
                    progress_bool = self.smile_and_pursing.progress_lip_pursing(diff_lip_pursing,
                                                                                diff_lip_pursing_image)
                else:
                    progress_bool = True

                if ret_lip_pursing:
                    cv2.putText(frame, "facial expression performed: " + "pucker lips", (10, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                                (255, 255, 255), 1)
                    cv2.putText(frame, "progress: " + str(progress_bool), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                                0.7, (255, 255, 255), 1)
        return frame,text, progress_bool, result_max

    def checkKey(self,dict, key):
        return key in dict.keys()

