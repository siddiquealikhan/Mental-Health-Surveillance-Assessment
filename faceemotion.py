import json
import numpy as np
import cv2
from keras.models import Sequential, model_from_json
from keras.saving import register_keras_serializable

@register_keras_serializable()
class RegisteredSequential(Sequential):
    pass


with open("facialemotionmodel.json", "r") as json_file:
    model_json_str = json_file.read()
    model_json = json.loads(model_json_str)

    if model_json.get("class_name") == "Sequential":
        model_json["class_name"] = "RegisteredSequential"


model = model_from_json(json.dumps(model_json), custom_objects={'RegisteredSequential': RegisteredSequential})
model.load_weights("facialemotionmodel.h5")


haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)


def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0


labels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'neutral', 5: 'sad', 6: 'surprise'}


webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    print("Error: Could not access webcam.")
    exit()

print("Press ESC to exit...")

while True:
    success, frame = webcam.read()
    if not success:
        print("Error: Failed to capture frame.")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        roi = gray[y:y + h, x:x + w]
        roi_resized = cv2.resize(roi, (48, 48))
        img = extract_features(roi_resized)
        pred = model.predict(img, verbose=0)
        emotion = labels[pred.argmax()]
        
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Facial Emotion Recognition", frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

webcam.release()
cv2.destroyAllWindows()