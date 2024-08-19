import cv2

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Code for webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

model = load_model('riceplantdetectionmodel.h5')

while True:
    success, img = cap.read()

    prediction = model.predict(img)[0]
    # img = me.get_frame_read().frame
    # classIds, confs, bbox = net.detect(img, confThreshold=thres, nmsThreshold=nmsThres) # To remove duplicates / declare accuracy
    # try:
    #     for classId, conf, box in zip(classIds.flatten(), confs.flatten(), bbox):
    #         cvzone.cornerRect(img, box)
    #         cv2.putText(img, f'{classNames[classId - 1].upper()} {round(conf * 100, 2)}',
    #                     (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_COMPLEX_SMALL,
    #                     1, (0, 255, 0), 2)
    #         print(classNames[classId - 1])
    # except:
    #     pass

    # me.send_rc_control(0, 0, 0, 0)

    cv2.imshow("Image", img)
    cv2.waitKey(1)