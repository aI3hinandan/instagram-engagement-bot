import cv2
import numpy as np
import urllib.request
from Initialization import *
from selenium import *


def getColor(image):
    cutout = None

    CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
               "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
               "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
               "sofa", "train", "tvmonitor"]
    net = cv2.dnn.readNetFromCaffe('personDetection/MobileNetSSD_deploy.prototxt.txt',
                                   'personDetection/MobileNetSSD_deploy.caffemodel')
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843,
                                 (300, 300), 127.5)
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    for i in np.arange(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]

        idx = int(detections[0, 0, i, 1])
        if idx == 15 and confidence >0.1:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            person_img = image[startY:endY, startX:endX].copy()
            nx, ny = int(abs((endX - startX) / 2)), int(abs((endX - startX) / 2))

            blue, green, red = image[ny,nx,0], image[ny,nx,1], image[ny,nx,2]
            print(CLASSES[idx])
            print(red,green,blue)
            cv2.imshow("test image", person_img)
            cv2.waitKey(0)




def load_caffe_models():
    gender_net = cv2.dnn.readNetFromCaffe('genderDetection/deploy_gender.prototxt', 'genderDetection/gender_net.caffemodel')

    return gender_net


def imageDetector(gender_net, url):
    gender = []
    MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    age_list = ['(0, 2)', '(4, 6)', '(8, 12)', '(15, 20)', '(25, 32)', '(38, 43)', '(48, 53)', '(60, 100)']
    gender_list = ['Male', 'Female']
    try:
        req = urllib.request.urlopen(url)
    except:
        print("link issue")
        return -1
    ba = np.asarray(bytearray(req.read()), dtype=np.uint8)
    image = cv2.imdecode(ba, cv2.IMREAD_COLOR)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

    faces = face_cascade.detectMultiScale(image, 1.1, 5)
    if (len(faces) > 0):
        print("Found {} faces".format(str(len(faces))))
    else:
        print("not found")
        return -1

    for (x, y, w, h) in faces:
        # get face
        face_img = image[y:y + h, h:h + w].copy()
        blob = cv2.dnn.blobFromImage(face_img, 1, (227, 227), MODEL_MEAN_VALUES, swapRB=False)

        # PREDICT GENDER
        gender_net.setInput(blob)
        gender_preds = gender_net.forward()
        gender.append(gender_list[gender_preds[0].argmax()])
    if "Male" in gender:
        return 1
    else:
        return 0






def getGender(url):
    gender_net = load_caffe_models()
    url = f'{url}media/?size=l'

    gender = imageDetector(gender_net, url)
    print(gender)
    return gender
