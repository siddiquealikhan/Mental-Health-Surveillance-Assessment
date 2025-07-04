import sys
import json
import numpy as np
import cv2
import base64
import os
from keras.models import Sequential, model_from_json
from keras.saving import register_keras_serializable

# 🔇 Disable TensorFlow info logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# ✅ Register custom class if needed
@register_keras_serializable()
class RegisteredSequential(Sequential):
    pass

# ✅ Absolute paths to model files (update if needed)
MODEL_JSON_PATH = "D:/Desktop/FACE EMOTIONS/facialemotionmodel.json"
MODEL_WEIGHTS_PATH = "D:/Desktop/FACE EMOTIONS/facialemotionmodel.h5"

# ✅ Load model architecture
try:
    with open(MODEL_JSON_PATH, "r") as json_file:
        model_json_str = json_file.read()
        model_json = json.loads(model_json_str)
        if model_json.get("class_name") == "Sequential":
            model_json["class_name"] = "RegisteredSequential"

    model = model_from_json(json.dumps(model_json), custom_objects={'RegisteredSequential': RegisteredSequential})
    model.load_weights(MODEL_WEIGHTS_PATH)
except Exception as e:
    print("error loading model:", str(e))
    sys.exit()

# ✅ Load face detector
haar_file = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)

# ✅ Labels (must match training)
labels = {
    0: 'angry',
    1: 'disgust',
    2: 'fear',
    3: 'happy',
    4: 'neutral',
    5: 'sad',
    6: 'surprise'
}

def extract_features(image):
    feature = np.array(image)
    feature = feature.reshape(1, 48, 48, 1)
    return feature / 255.0

def decode_base64_image(b64_string):
    try:
        if "," in b64_string:
            b64_string = b64_string.split(",")[1]  # Strip data URI prefix
        image_data = base64.b64decode(b64_string)
        nparr = np.frombuffer(image_data, np.uint8)
        return cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"error: decode_base64 - {str(e)}")
        return None

# ✅ Main logic
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("error: no input")
        sys.exit()

    b64_input = sys.argv[1]
    image = decode_base64_image(b64_input)

    if image is None:
        print("error: cannot decode base64")
        sys.exit()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)

    if len(faces) == 0:
        print("error: no face detected")
        sys.exit()

    for (x, y, w, h) in faces:
        print(f"Detected face at x:{x}, y:{y}, w:{w}, h:{h}")  # Debug

        # Add padding
        margin = 10
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(gray.shape[1], x + w + margin)
        y2 = min(gray.shape[0], y + h + margin)

        roi = gray[y1:y2, x1:x2]

        try:
            roi_resized = cv2.resize(roi, (48, 48))
            img = extract_features(roi_resized)
            prediction = model.predict(img, verbose=0)
            emotion_idx = int(np.argmax(prediction))
            emotion = labels.get(emotion_idx, "unknown")
            print(emotion)
            sys.exit()
        except Exception as e:
            print(f"error: prediction failed - {str(e)}")
            sys.exit()

    print("error: unexpected condition")