from imutils.video import VideoStream
import cv2
from AnalysisFrame import AnalysisFrame
from Tongue import Tongue

class AnalysisRealTime:
    def __init__(self,image_normal, image_best, type_result):
        self.vs = VideoStream(0).start()
        self.analysis_frame = AnalysisFrame()
        self.progress_bool_comparison = False
        self.result_max_comparison = 0
        self.lip_width = self.analysis_frame.lip_width_image_get(image_normal)
        self.image_best = image_best
        self.type_result = type_result
        if 'tongue' in self.type_result:
            self.analysis_tongue()
        else:
            self.analysis_every_frame_no_tongue()
        cv2.destroyAllWindows()
        self.vs.stop()

    def analysis_tongue(self):

        self.tongue = Tongue('video_analysis.mp4', self.type_result)

        if self.type_result == 'Move_tongue_to_left':
            if 'left' in self.tongue.output_tongue:
                self.progress_bool_comparison = True

        if self.type_result == 'move_tongue_to_right':
            if 'right' in self.tongue.output_tongue:
                self.progress_bool_comparison = True

        if self.type_result == 'straight_tongue_out':
            if 'straight' in self.tongue.output_tongue:
                self.progress_bool_comparison = True

        if self.type_result == 'lift_tongue_to_nose':
            if 'nose' in self.tongue.output_tongue:
                self.progress_bool_comparison = True

        if self.type_result == 'down_tongue_to_chin':
            if 'chin' in self.tongue.output_tongue:
                self.progress_bool_comparison = True

    def analysis_every_frame_no_tongue(self):
        image = cv2.imread(self.image_best)
        shape_best, frame_best, faceAligned_best = self.analysis_frame.analysis_one_frame(image)
        if self.type_result == 'mouth_open' or self.type_result == 'smile':
            self.result_max_comparison = 0
        if self.type_result == 'mouth_close' or self.type_result == 'lip_pursing':
            self.result_max_comparison = 10000000000
        while True:
            frame1 = self.vs.read()
            shape, frame, faceAligned = self.analysis_frame.analysis_one_frame(frame1)
            frame, text, progress_bool, result_max = self.analysis_frame.analysis_facial_expressions(self.lip_width, shape, frame, faceAligned,shape_best, frame_best, faceAligned_best, self.type_result)
            if text != '':
                if self.type_result == 'mouth_open':
                    progress_bool_get = self.analysis_frame.open_and_close.progress_mouth_open(result_max,
                                                                                               self.result_max_comparison)
                    if progress_bool_get:
                        self.result_max_comparison = result_max
                        self.progress_bool_comparison = progress_bool
                        cv2.imwrite("output_image.png", frame)

                if self.type_result == 'mouth_close':
                    progress_bool_get = self.analysis_frame.open_and_close.progress_mouth_close(result_max,
                                                                                                self.result_max_comparison)
                    if progress_bool_get:
                        self.result_max_comparison = result_max
                        self.progress_bool_comparison = progress_bool
                        cv2.imwrite("output_image.png", frame)

                if self.type_result == 'smile':
                    progress_bool_get = self.analysis_frame.smile_and_pursing.progress_smile(result_max,
                                                                                             self.result_max_comparison)
                    if progress_bool_get:
                        self.result_max_comparison = result_max
                        self.progress_bool_comparison = progress_bool
                        cv2.imwrite("output_image.png", frame)

                if self.type_result == 'lip_pursing':
                    progress_bool_get = self.analysis_frame.smile_and_pursing.progress_lip_pursing(result_max,
                                                                                                   self.result_max_comparison)
                    if progress_bool_get:
                        self.result_max_comparison = result_max
                        self.progress_bool_comparison = progress_bool
                        cv2.imwrite("output_image.png", frame)

            cv2.imshow("output", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break