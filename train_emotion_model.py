import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.optimizers import Adam


DATA_DIR = "labeled_dataset"
IMG_SIZE = 48  
NUM_CLASSES = 0  

X = []
y = []
label_map = {}
label_counter = 0

for root, dirs, files in os.walk(DATA_DIR):
    for filename in files:
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            label = os.path.basename(root).lower()  # folder name is the label

            if label not in label_map:
                label_map[label] = label_counter
                label_counter += 1

            img_path = os.path.join(root, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                print(f"Warning: Failed to load {img_path}")
                continue
            img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))

            X.append(img)
            y.append(label_map[label])

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1) / 255.0  
y = to_categorical(y, num_classes=len(label_map))


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_SIZE, IMG_SIZE, 1)),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Dropout(0.25),

    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(label_map), activation='softmax')
])

model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])


print("Training started...")
model.fit(X_train, y_train, epochs=15, batch_size=32, validation_split=0.1)


loss, acc = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {acc * 100:.2f}%")


model.save("custom_emotion_model.h5")


import json
with open("label_map.json", "w") as f:
    json.dump(label_map, f)

print("Model and label map saved!")
