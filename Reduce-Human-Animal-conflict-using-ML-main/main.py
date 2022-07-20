import numpy as np
import cv2
from twilio.rest import Client
import keys
import os
from datetime import datetime

def animal(name):
    threats = ['cow','horse','dog','cat','bird','sheep']
    if name in threats:
        with open('animals.csv','r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
                message = client.messages.create(
                body=name+" Detected near your field",
                from_=keys.twilio_number,
                to=keys.my_phone_number
                )
                print(message.body)
    
client = Client(keys.account_sid,keys.auth_token)
prototxt_path = 'MobileNetSSD_deploy.prototxt'
model_path = 'MobileNetSSD_deploy.caffemodel'

min_confidence = 0.7

classes = ['background',
           'aeroplane', 'bicycle', 'bird', 'boat',
           'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse',
           'motorbike', 'person', 'pottedplant',
           'sheep', 'sofa', 'train', 'tvmonitor',
           'tiger', 'lion']

np.random.seed(543210)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

cap = cv2.VideoCapture(0)

while True:
    ret, image = cap.read()

    height, width = image.shape[0], image.shape[1]

    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007, (300, 300), 130)

    net.setInput(blob)

    detected_objects = net.forward()

    for i in range(detected_objects.shape[2]):
        confidence = detected_objects[0][0][i][2]

        if confidence > min_confidence:
            
            class_index = int(detected_objects[0, 0, i, 1])
            
            upper_left_x = int(detected_objects[0, 0, i, 3] * width)
            upper_left_y = int(detected_objects[0, 0, i, 4] * height)
            lower_right_x = int(detected_objects[0, 0, i, 5] * width)
            lower_right_y = int(detected_objects[0, 0, i, 6] * height)
            roundConfi = confidence * 100 
            predection_text = f"{classes[class_index]}: {roundConfi:.2f}%"
            animal(classes[class_index])

            cv2.rectangle(image, (upper_left_x, upper_left_y), (lower_right_x, lower_right_y), colors[class_index], 3)
            cv2.putText(image, predection_text, (upper_left_x, upper_left_y - 15 if upper_left_y > 30 else upper_left_y + 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, colors[class_index], 2)

            cv2.imshow("Detected", image)
            cv2.waitKey(1)
            
