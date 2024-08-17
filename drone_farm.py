from MainWindow import Ui_MainWindow as Ui
from PyQt5.QtWidgets import QMainWindow, QApplication
from ultralytics import YOLO
from djitellopy import Tello

import os
import cv2
import sys
import supervision as sv

# Define the frame width and height for video capture
frame_width = 1280
frame_height = 720


class App(QMainWindow, Ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.main_window = Ui()
        self.pushButton_plot1.clicked.connect(self.cropMonitoring)

    def cropMonitoring(self):
        # Initialize video capture from default camera
        # cap = cv2.VideoCapture(0)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        aircraft = Tello()
        aircraft.connect()
        aircraft.streamoff()
        aircraft.streamon()
        img = aircraft.get_frame_read().frame
        cv2.imshow("Tello", img)

        # # Load the custom YOLOv8 model from the local drive
        # model_path = os.path.join(".", "models", "blb_detector.pt")
        # model = YOLO(model_path)
        # # model = YOLO("yolov8n.pt")
        #
        # # Initialize box annotator for visualization
        # tracker = sv.ByteTrack()
        # box_annotator = sv.BoundingBoxAnnotator()
        #
        # # Main loop for video processing
        while True:
            # Read frame from video capture
            # ret, frame = cap.read()
            img = aircraft.get_frame_read().frame
            #
            #     # Perform object detection using YOLOv8
            #     result = model(img)[0]
            #     detections = sv.Detections.from_ultralytics(result)
            #     detections = tracker.update_with_detections(detections)
            #
            #     labels = [
            #         f"#{tracker_id} {result.names[class_id]}"
            #         for class_id, tracker_id in zip(
            #             detections.class_id, detections.tracker_id
            #         )
            #     ]
            #
            #     print(labels)
            #
            #     # Annotate frame with bounding boxes and labels
            #     annotated_frame = box_annotator.annotate(img.copy(), detections=detections)
            #
            #     # Display annotated frame
            #     cv2.imshow("yolov8", img)
            #
            #     # Check for quit key
            #     if cv2.waitKey(1) & 0xFF == ord("q"):
            #         break
            #
            #     # Release video capture
            # # cap.release()
            # cv2.destroyAllWindows()
            cv2.imshow("Tello", img)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = App()
    win.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing Window")
