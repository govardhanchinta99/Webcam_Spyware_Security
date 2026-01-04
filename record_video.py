import cv2
import time
import os  # NEW

# NEW: Create 'recordings' folder if not exist
if not os.path.exists("recordings"):
    os.makedirs("recordings")

def record_intruder_video(filename='recordings/intruder_recording.avi', duration=600):
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(filename, fourcc, 20.0, (640, 480))

    start_time = time.time()
    while int(time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
