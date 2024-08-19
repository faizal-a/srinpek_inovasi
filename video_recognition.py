# Import the InferencePipeline object
from inference import InferencePipeline
from inference.core.interfaces.stream.sinks import render_boxes
from inference.core.interfaces.camera.entities import VideoFrame

import cv2
import supervision as sv

# create a bounding box annotator and label annotator to use in our custom sink
label_annotator = sv.LabelAnnotator()
box_annotator = sv.BoxAnnotator()


def my_custom_sink(predictions: dict, video_frame: VideoFrame):
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


# initialize a pipeline object
pipeline = InferencePipeline.init(
    model_id="rice-9zz0g/1", api_key='tGs8FbJ5AVs6QQzASbd4',  # Roboflow model to use
    video_reference=0,  # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=my_custom_sink,  # Function to run after each prediction
)
pipeline.start()
pipeline.join()
