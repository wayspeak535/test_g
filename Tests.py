import unittest
import cv2
from AnalysisFrame import AnalysisFrame


class Tests(unittest.TestCase):
    analysis_frame = AnalysisFrame()
    lip_width_normal = analysis_frame.lip_width_image_get('normal.png')

    def test_open_mouth(self, analysis_frame=analysis_frame):
        frame1 = cv2.imread('open_mouth.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_mouth_open, mouth_height = analysis_frame.open_and_close.calculating_mouth_open(shape, faceAligned)
            self.assertTrue(ret_mouth_open)

        frame1 = cv2.imread('no_open_mouth.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_mouth_open, mouth_height = analysis_frame.open_and_close.calculating_mouth_open(shape, faceAligned)
            self.assertFalse(ret_mouth_open)


    def test_close_mouth(self, analysis_frame=analysis_frame):
        frame1 = cv2.imread('close_mouth.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_mouth_close, mouth_height = analysis_frame.open_and_close.calculating_mouth_close(shape, faceAligned)
            self.assertTrue(ret_mouth_close)

        frame1 = cv2.imread('no_close_mouth.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_mouth_close, mouth_height = analysis_frame.open_and_close.calculating_mouth_close(shape, faceAligned)
            self.assertFalse(ret_mouth_close)

    def test_smile(self, analysis_frame=analysis_frame, lip_width_normal=lip_width_normal):
        frame1 = cv2.imread('smile.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_smile, diff_smile = analysis_frame.smile_and_pursing.calculating_smile(shape, faceAligned,
                                                                                           lip_width_normal)
            self.assertTrue(ret_smile)

        frame1 = cv2.imread('no_smile.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_smile, diff_smile = analysis_frame.smile_and_pursing.calculating_smile(shape, faceAligned,
                                                                                           lip_width_normal)
            self.assertFalse(ret_smile)

    def test_pucker_lips(self, analysis_frame=analysis_frame, lip_width_normal=lip_width_normal):
        frame1 = cv2.imread('pucker_lips.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_lip_pursing, diff_lip_pursing = analysis_frame.smile_and_pursing.calculating_lip_pursing(shape,
                                                                                lip_width_normal)
            self.assertTrue(ret_lip_pursing)

        frame1 = cv2.imread('no_pucker_lips.png')
        shape, frame, faceAligned = analysis_frame.analysis_one_frame(frame1)
        ret_straight_face = analysis_frame.facial_expressions.straight_face(shape)
        if ret_straight_face:
            ret_lip_pursing, diff_lip_pursing = analysis_frame.smile_and_pursing.calculating_lip_pursing(shape,
                                                                                                             lip_width_normal)
            self.assertTrue(ret_lip_pursing)


if __name__ == '__main__':
    unittest.main()