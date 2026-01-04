import cv2
import face_recognition
import os
import time

# Create "faces" folder if not exist
faces_folder = "faces"
if not os.path.exists(faces_folder):
    os.makedirs(faces_folder)

# Get user's name
user_name = input("Enter your name: ").strip().lower()

# Start webcam
video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("[ERROR] Could not access the camera. Please check it.")
    exit()

print("[INFO] Please look at the camera. Press 's' to save your face or 'q' to quit.")

error_shown = False

while True:
    ret, frame = video_capture.read()

    # Skip if frame not captured
    if not ret or frame is None:
        if not error_shown:
            print("[WARNING] Frame capture failed. Trying again...")
            error_shown = True
        continue
    error_shown = False  # reset if next frame is good

    try:
        # Resize and convert to RGB
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect face locations
        face_locations = face_recognition.face_locations(rgb_frame)
    except Exception as e:
        if not error_shown:
            print(f"[EXCEPTION] Could not process the frame: {e}")
            error_shown = True
        continue

    # Draw rectangles on detected faces
    for (top, right, bottom, left) in face_locations:
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("Register Face - Press 's' to Save", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('s'):
        if face_locations:
            save_path = os.path.join(faces_folder, f"{user_name}.jpg")
            cv2.imwrite(save_path, frame)
            print(f"[SUCCESS] Face saved at: {save_path}")
        else:
            print("[INFO] No face detected. Please try again while looking clearly at the camera.")

    elif key == ord('q'):
        print("[INFO] Quitting face registration.")
        break

# Cleanup
video_capture.release()
cv2.destroyAllWindows()
