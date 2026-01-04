import cv2
import time
import os
from send_email import send_alert_email
from record_video import record_intruder_video

print("[WATCHDOG] Monitoring webcam access...")

recording = False  # ✅ Flag to prevent duplicate alerts

# Loop to check webcam access every few seconds
while True:
    cam = cv2.VideoCapture(0)
    
    if cam.isOpened() and not recording:
        print("[ALERT] Webcam accessed externally!")
        
        # ✅ Trigger alert and video only if not already recording
        recording = True

        # Send Email Alert
        send_alert_email(
            subject="🚨 Unauthorized Webcam Access Detected!",
            body="Someone tried to access your webcam without permission. A video has been recorded."
        )

        # Record Intruder Video
        record_intruder_video()

        cam.release()
        print("[WATCHDOG] Recording complete. Cooling down for 10 minutes.")

        # Wait for 10 minutes to avoid repeated triggers
        time.sleep(600)
        recording = False

    else:
        cam.release()
        time.sleep(5)  # Check again in 5 seconds
