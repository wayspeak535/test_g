import dlib
import imutils
from imutils import face_utils
import cv2
import os

class Tongue:
    def __init__(self, video_path, type_result):
        self.video_path = video_path
        self.type_result = type_result
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_predictor = dlib.shape_predictor('face_utils/shape_predictor_68_face_landmarks.dat')
        self.fa = face_utils.FaceAligner(self.landmark_predictor, desiredFaceWidth=500)
        self.delete_output()
        self.save_output_video(video_path)
        self.create_points()
        self.start_matlab()


    def delete_output(self):
        file_path = "output.mp4"

        # Check if the file exists before deleting
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} has been deleted.")
        else:
            print(f"{file_path} does not exist.")

    def save_output_video(self,video_path):


        # Open the video file
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error: Could not open the video file.")
            return
        # Define the codec and create a VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')

        out = cv2.VideoWriter('output.mp4', fourcc, 20.0, (500, 500))
        # cap = cv2.VideoCapture(r"output.mp4")

        j = 0

        while True:
            # Read a frame from the video capture
            ret, frame = cap.read()

            if ret:
                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces in the grayscale frame
                faces = self.face_detector(gray)

                # Iterate over the detected faces
                for face in faces:
                    frame = self.fa.align(frame, gray, face)
                    frame = imutils.resize(frame, width=500)
                j += 1
                # Write the frame to the output video
                out.write(frame)

                # Display the resulting frame
                cv2.imshow('Facial Landmarks', frame)

                # Check for the 'q' key to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        # Release the video capture, video writer, and close the windows
        cap.release()
        out.release()
        cv2.destroyAllWindows()

    def create_points(self):
        pointList = []
        dictpoint = []
        j = 0
        cap = cv2.VideoCapture(r"output.mp4")
        while True:
            # Read a frame from the video capture
            ret, frame = cap.read()

            if ret:
                # Convert the frame to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Detect faces in the grayscale frame
                faces = self.face_detector(gray)

                # Iterate over the detected faces
                for face in faces:
                    # Detect landmarks for the current face
                    landmarks = self.landmark_predictor(gray, face)
                    # Iterate over the landmarks and draw them on the frame
                    for i in range(3, 14):
                        x = landmarks.part(i).x
                        y = landmarks.part(i).y
                        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                        cv2.putText(frame, str(i), (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                    (255, 255, 255), 1)
                        pointList.append((i, x, y))

                    x = landmarks.part(33).x
                    y = landmarks.part(33).y
                    cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                    cv2.putText(frame, str(33), (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                (255, 255, 255), 1)
                    pointList.append((33, x, y))
                    for i in range(48, 68):
                        x = landmarks.part(i).x
                        y = landmarks.part(i).y
                        cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)
                        cv2.putText(frame, str(i), (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                                    (255, 255, 255), 1)
                        pointList.append((i, x, y))
                    dictpoint.append(pointList)
                    # dictpoint[j] = pointList
                    pointList = []
                    frame = self.fa.align(frame, gray, face)
                    frame = imutils.resize(frame, width=500)
                    message = 'Face detected!'
                    # print("frame:", frame)
                j += 1
                # Write the frame to the output video

                # Display the resulting frame
                cv2.imshow('Facial Landmarks', frame)

                # Check for the 'q' key to exit the loop
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            # Release the video capture, video writer, and close the windows
        cap.release()
        cv2.destroyAllWindows()
        # Open the file in binary mode
        with open("points.txt", "w") as file:
            # Convert the dictionary to a string representation
            dict_str = str(dictpoint)
            file.write(dict_str)


    def start_matlab(self):
        # Start MATLAB engine
        eng = matlab.engine.start_matlab()

        # Call the MATLAB function and capture the output

        if self.type_result == 'Move_tongue_to_left':
            output = eng.tracking_tongue(1)
            if output[0][0] > output[0][1]:
                self.output_tongue = 'Move_tongue_to_left'
        else:
            if self.type_result == 'move_tongue_to_right':
                output = eng.tracking_tongue(2)
                if output[0][1] > output[0][0]:
                    self.output_tongue = 'move_tongue_to_right'
            else:
                if self.type_result == 'straight_tongue_out':
                    output = eng.tracking_tongue(3)
                    if output[0][2] > 0:
                        self.output_tongue = 'straight_tongue_out'
                else:
                    if self.type_result == 'lift_tongue_to_nose':
                        output = eng.tracking_tongue(4)
                        if output[0][3] > 0:
                            self.output_tongue = 'lift_tongue_to_nose'
                    else:
                        # if self.type_result == 'down_tongue_to_chin':
                        output = eng.tracking_tongue(5)
                        if output[0][4] > 0:
                            self.output_tongue = 'down_tongue_to_chin'

        # Print the output (optional)
        print(output)
        # Quit the MATLAB engine
        eng.quit()

