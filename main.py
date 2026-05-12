import socket
import time as time

import cv2 as cv
import mediapipe as mp
import numpy as np
import os

HOST = "127.0.0.1"
PORT = 6767

model_path = os.path.dirname(os.path.realpath(__file__)) + "/../pose_landmarker_heavy.task"

BaseOptions = mp.tasks.BaseOptions
PoseLandmarker = mp.tasks.vision.PoseLandmarker
PoseLandmarkerOptions = mp.tasks.vision.PoseLandmarkerOptions
PoseLandmarkerResult = mp.tasks.vision.PoseLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

print('Starting client on {}:{}'.format(HOST, PORT))

def get_conn():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

conn = get_conn()

#Create a pose landmarker instance with the live stream mode:
def print_result(result: PoseLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    data = []
    for pose_landmark in result.pose_landmarks[0]:
        data.append(pose_landmark.x)
        data.append(pose_landmark.y)
        data.append(pose_landmark.z)
    conn.sendall(np.array(data))
    if conn.recv(1)[0] == 1:
        print("Disconnected due to server message")
        killl()
        print("Released camera")
        cv.destroyAllWindows()
        print("Closed window")
        conn.close()
        print("Closed connection")
        exit()


options = PoseLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

with PoseLandmarker.create_from_options(options) as landmarker:
    cap = cv.VideoCapture(0)
    frameCount = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    frameWidth = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    def killl():
        cap.release()
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while conn:
        # Capture frame-by-frame
        ret, frame = cap.read()
        timee = time.time()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Our operations on the frame come here
        flipped = cv.flip(frame, 1)
        # Display the resulting frame
        cv.imshow('frame', flipped)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(flipped))
        landmarker.detect_async(mp_image, int(timee * 1000))
        if cv.waitKey(1) == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()