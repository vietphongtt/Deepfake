from tensorflow.keras.models import load_model
from efficientnet.keras import EfficientNetB2
import os
import cv2
import numpy as np
from mtcnn import MTCNN
import copy
import tensorflow as tf
def main():
    model = load_model("model/Moblide_net.h5")
    dim = (224,224)
    cap = cv2.VideoCapture("Mydata_Test/Data/G9c5cnUtzkLTnjOp1SQTEMpiWnsZoKNRM4uT.mp4")

    while(1): 
        ret, frame  = cap.read()
        if not ret:
            break
        img = frame.copy()
        detector = MTCNN()
        detections = detector.detect_faces(img)
        min_cof = 0.9
        for det in detections:
            if det['confidence'] >= min_cof:
                x,y,w,h = det['box']
                crop_img = img[y:y+h, x:x+w]
                face = cv2.resize(crop_img, dim)
                face = face.astype("float") / 255.0
                face = np.array(face)
                face = np.expand_dims(face, axis=0)
                pred = model.predict(face)[0]
                j = np.argmax(pred)
                real = "{}: {:.4f}".format("real", pred[j])
                fake = "{}: {:.4f}".format("fake", pred[j])
                if(j==1):
                    cv2.putText(img,real, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2)
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),2)
                else:
                    cv2.putText(img,fake, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,255),2)
                    cv2.rectangle(img, (x,y), (x+w, y+h), (0,0,255),2)                    

        cv2.imshow("Face", img)
        key = cv2.waitKey(50)
        if key == ord('q'):
            break

if __name__ == "__main__":
    with tf.device('/device:GPU:0'):
        main()