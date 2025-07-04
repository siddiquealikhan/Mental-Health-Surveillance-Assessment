import cv2
import os
import time

output_dir = "labeled_dataset"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

fps = int(cap.get(cv2.CAP_PROP_FPS))
original_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
original_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
last_capture_time = None

custom_ratio = (16, 9)
output_width = 800
output_height = int(output_width * custom_ratio[1] / custom_ratio[0])

print("Hold 'c' -> capture, 'q' -> quit")

capturing = False
capture_buffer = []

while True:
    start_time = time.time()
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame. Exiting...")
        break

    frame_resized = cv2.resize(frame, (output_width, output_height))

    overlay_text = [
        f"FPS: {fps}",
        "Hold 'c' -> capture",
        "Press 'q' to quit"
    ]
    y = 20
    for text in overlay_text:
        cv2.putText(frame_resized, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        y += 30

    if capturing:
        cv2.putText(frame_resized, f"Capturing {len(capture_buffer)} images...", (10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Live Video Feed", frame_resized)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c') and not capturing:
        capturing = True
        capture_buffer.clear()
        print("Capturing started...")

        num_images = 20       
        interval = 0.2        

        for i in range(num_images):
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break
            frame_resized = cv2.resize(frame, (output_width, output_height))
            capture_buffer.append(frame_resized)
            cv2.imshow("Live Video Feed", frame_resized)
            cv2.waitKey(1)
            time.sleep(interval)

        capturing = False
        print("Capturing completed.")
        
        label = input("Enter the label for these images").strip().lower()
        label_folder = os.path.join(output_dir, label)
        os.makedirs(label_folder, exist_ok=True)

        for idx, img in enumerate(capture_buffer):
            timestamp = int(time.time() * 1000)
            filename = f"{label}_{timestamp}_{idx}.jpg"
            filepath = os.path.join(label_folder, filename)
            cv2.imwrite(filepath, img)
            print(f"Saved: {filepath}")
        last_capture_time = time.time()

    elif key == ord('q'):
        print("Exiting...")
        break

    end_time = time.time()
    fps = int(1 / (end_time - start_time + 1e-6))

cap.release()
cv2.destroyAllWindows()