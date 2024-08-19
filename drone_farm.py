import os
import cv2
import sys
import cvzone
import supervision as sv
from inference import get_model

from MainWindow import Ui_MainWindow as Ui
from PyQt5.QtWidgets import QMainWindow, QApplication
from inference import InferencePipeline
from inference.core.interfaces.stream.sinks import render_boxes
from inference.core.interfaces.camera.entities import VideoFrame
from ultralytics import YOLO
from djitellopy import Tello

# Define the frame width and height for video capture
frame_width = 1280
frame_height = 720

# create a bounding box annotator and label annotator to use in our custom sink
label_annotator = sv.LabelAnnotator()
box_annotator = sv.BoxAnnotator()


class App(QMainWindow, Ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main_window = Ui()
        self.pushButton_plot1.clicked.connect(self.cropMonitoringDrone)
        self.pushButton_plot1_2.clicked.connect(self.cropMonWebCam)

    def custom_sink(predictions: dict, video_frame: VideoFrame):
        # get the text labels for each prediction
        labels = [p["class"] for p in predictions["predictions"]]
        # load our predictions into the Supervision Detections api
        detections = sv.Detections.from_inference(predictions)
        # annotate the frame using our supervision annotator, the video_frame, the predictions (as supervision Detections), and the prediction labels
        image = label_annotator.annotate(
            scene=video_frame.image.copy(), detections=detections, labels=labels
        )
        image = box_annotator.annotate(image, detections=detections)
        print(labels)
        # display the annotated image
        cv2.imshow("Predictions", image)
        cv2.waitKey(1)

    def cropMonitoringDrone(self, custom_sink):
        # Initialize video capture from default camera
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        # tello = Tello()
        # tello.connect()
        # tello.streamon()

        # Load the custom YOLOv8 model from the local drive
        # model_path = os.path.join(".", "models", "blb_detector.pt")
        # model = YOLO(model_path)
        # model = YOLO("yolov8n.pt")

        # load a pre-trained yolov8n model
        model = get_model(model_id="rice-9zz0g/1", api_key='tGs8FbJ5AVs6QQzASbd4')

        # # Initialize box annotator for visualization
        tracker = sv.ByteTrack()
        box_annotator = sv.BoxAnnotator()

        # Main loop for video processing
        while True:
            # Read frame from video capture
            # ret, frame = cap.read()
            # img = cap.read()
            # img = tello.get_frame_read().frame

            # initialize a pipeline object
            pipeline = InferencePipeline.init(
                model_id="rice-9zz0g/1", api_key='tGs8FbJ5AVs6QQzASbd4',  # Roboflow model to use
                video_reference=0,  # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
                on_prediction=custom_sink,  # Function to run after each prediction
            )
            pipeline.start()
            pipeline.join()

    def cropMonWebCam(self):
        thres = 0.50
        nmsThres = 0.2

        # Code for webcam
        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        classNames = []
        classFile = 'ss.names'  # Contains a totoal of 91 different objects which can be recognized by the code
        with open(classFile, 'rt') as f:
            classNames = f.read().split('\n')

        # print(classNames)
        configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        weightsPath = "frozen_inference_graph.pb"

        net = cv2.dnn_DetectionModel(weightsPath, configPath)

        net.setInputSize(320, 320)
        net.setInputScale(1.0 / 127.5)
        net.setInputMean((127.5, 127.5, 127.5))
        net.setInputSwapRB(True)

        # me = Tello()
        # me.connect()
        # print(me.get_battery())
        # me.streamoff()
        # me.streamon()

        # me.takeoff()
        # me.move_up(90)

        while True:
            success, img = cap.read()
            # img = me.get_frame_read().frame
            classIds, confs, bbox = net.detect(img, confThreshold=thres,
                                               nmsThreshold=nmsThres)  # To remove duplicates / declare accuracy
            try:
                for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    cvzone.cornerRect(img, box)
                    cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
                                (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                1, (0, 255, 0), 2)
            except:
                pass

            cv2.imshow("Image", img)
            cv2.waitKey(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window")
