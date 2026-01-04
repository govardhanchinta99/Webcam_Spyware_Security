import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os
import random
import string
import webbrowser
import datetime
import winreg
import sqlite3
import cv2
import time
from tkinter.simpledialog import askstring
from datetime import datetime
import secrets
from PIL import Image, ImageTk
from send_email import send_alert_email
import face_recognition

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASSWORD_FILE = os.path.join(BASE_DIR, "password.txt")
LOG_FILE = os.path.join(BASE_DIR, "logs.txt")
PROJECT_INFO_FILE = os.path.join(BASE_DIR, "project_info.html")
CASCADE_FILE = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
DB_FILE = os.path.join(BASE_DIR, "users.db")
LOGO_FILE = os.path.join(BASE_DIR, "logo.png")
ICON_FILE = os.path.join(BASE_DIR, "icon.ico")
RECORDINGS_DIR = os.path.join(BASE_DIR, "recordings")
FACE_DIR = os.path.join(BASE_DIR, "face")
os.makedirs(RECORDINGS_DIR, exist_ok=True)
os.makedirs(FACE_DIR, exist_ok=True)

# === Password Management ===
def generate_password(length=12):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(chars) for _ in range(length))

def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(password)

def load_password():
    if not os.path.exists(PASSWORD_FILE):
        password = generate_password()
        save_password(password)
        return password
    with open(PASSWORD_FILE, "r") as f:
        return f.read().strip()

# === Setup Database ===
def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            face_image TEXT,
            registered_on TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

# === Logging ===
def log_event(event):
    time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{event} - {time_str}\n")

# === Recording ===
def record_intruder_10_sec():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    video_filename = f"unauth_intruder_{timestamp}.avi"
    video_path = os.path.join(RECORDINGS_DIR, video_filename)

    face_cascade = cv2.CascadeClassifier(CASCADE_FILE)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Webcam not accessible")
        return

    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'XVID'), 10, (640, 480))
    start_time = time.time()
    print("🔴 Recording started for 10 seconds...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        if len(faces) > 0:
            out.write(frame)

        if time.time() - start_time >= 10:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    log_event(f"Wrong Password Intruder recorded - Saved: {video_filename}")

# === Face Recognition ===
def recognize_face():
    known_faces = []

    for file in os.listdir(FACE_DIR):
        if not (file.endswith(".jpg") or file.endswith(".png")):
            continue

        img_path = os.path.join(FACE_DIR, file)

        try:
            image = face_recognition.load_image_file(img_path)

            # ✅ Ensure image is RGB
            if image.ndim != 3 or image.shape[2] != 3:
                continue

            encodings = face_recognition.face_encodings(image)
            if encodings:
                known_faces.append(encodings[0])

        except Exception as e:
            print(f"⚠️ Skipping invalid face image: {file} | {e}")

    if not known_faces:
        print("⚠️ No valid face data found")
        return False

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return False

    ret, frame = cap.read()
    cap.release()

    if not ret:
        return False

    # ✅ Convert BGR → RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_encodings = face_recognition.face_encodings(rgb_frame)

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        if True in matches:
            return True

    return False

# === Access Verification ===
def verify_access():
    try:
        if recognize_face():
            messagebox.showinfo("Face Verified", "Access granted via facial recognition.")
            log_event("Access granted via face recognition")
            return True
    except Exception as e:
        print("Face recognition failed:", e)

    # Password fallback
    try:
        with open(PASSWORD_FILE, "r") as f:
            correct_password = f.read().strip()
    except FileNotFoundError:
        messagebox.showerror("Error", "Password file not found.")
        return False

    entered_password = askstring("Password Required", "Enter the password:", show='*')

    if entered_password == correct_password:
        return True
    else:
        messagebox.showerror("Error", "Incorrect password!")
        log_event("Unauthorized Access - Wrong Password")
        send_alert_email(
            "❌ Unauthorized Access Attempt",
            "Someone entered a wrong password. Intruder recording started."
        )
        record_intruder_10_sec()
        return False

# === GUI Button Functions ===
def open_project_info():
    if os.path.exists(PROJECT_INFO_FILE):
        webbrowser.open(f"file://{PROJECT_INFO_FILE}")
    else:
        messagebox.showerror("File Not Found", "project_info.html not found.")

def view_logs():
    if not verify_access():
        return
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            logs = f.read()
        log_window = tk.Toplevel(root)
        log_window.title("Logs")
        log_window.geometry("500x400")
        text = tk.Text(log_window)
        text.insert(tk.END, logs)
        text.pack(expand=True, fill="both")
        log_event("Logs Accessed")
        send_alert_email("📁 Logs Accessed", "The log file was accessed using verified access.")
    else:
        messagebox.showinfo("No Logs", "Log file is empty or missing.")

def disable_camera():
    if not verify_access():
        return
    try:
        subprocess.run([
            "reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Services\usbvideo",
            "/v", "Start", "/t", "REG_DWORD", "/d", "4", "/f"
        ], check=True, shell=True)
        messagebox.showinfo("Success", "Webcam Disabled. Please restart your system.")
        log_event("Camera Disabled")
        send_alert_email("🔴 Webcam Disabled", "Your webcam has been disabled.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to disable camera: {str(e)}")

def enable_camera():
    if not verify_access():
        return
    try:
        subprocess.run([
            "reg", "add", r"HKLM\SYSTEM\CurrentControlSet\Services\usbvideo",
            "/v", "Start", "/t", "REG_DWORD", "/d", "3", "/f"
        ], check=True, shell=True)
        messagebox.showinfo("Success", "Webcam Enabled. Please restart your system.")
        log_event("Camera Enabled")
        send_alert_email("🟢 Webcam Enabled", "Your webcam has been enabled.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to enable camera: {str(e)}")

def check_webcam_status():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\usbvideo", 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, "Start")
        winreg.CloseKey(key)
        status = "Enabled" if value == 3 else "Disabled"
        messagebox.showinfo("Webcam Status", f"Webcam is {status}")
        log_event(f"Checked Webcam Status: {status}")
        send_alert_email("🔍 Webcam Status Checked", f"Webcam is currently {status}.")
    except:
        messagebox.showerror("Error", "Could not read webcam status.")

def register_face():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Error", "Webcam not accessible")
        return
    ret, frame = cap.read()
    cap.release()
    if ret:
        name = simpledialog.askstring("Face Registration", "Enter name for this face:")
        if name:
            file_path = os.path.join(FACE_DIR, f"{name}.jpg")
            cv2.imwrite(file_path, frame)
            log_event(f"New Face Registered: {name}")
            send_alert_email("👤 Face Registered", f"A new face named {name} was registered.")
            messagebox.showinfo("Success", f"Face saved as {file_path}")
            # Save to DB
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, face_image) VALUES (?, ?)", (name, file_path))
            conn.commit()
            conn.close()
    else:
        messagebox.showerror("Error", "Failed to capture face")

def change_password():
    if not verify_access():
        return
    new_pass = askstring("Change Password", "Enter new password:", show="*")
    if new_pass:
        save_password(new_pass)
        messagebox.showinfo("Success", "Password changed successfully.")
        log_event("Password Changed")
        send_alert_email("🔐 Password Changed", "Password was manually changed.")

def generate_random_password():
    if not verify_access():
        return
    password = generate_password()
    save_password(password)
    messagebox.showinfo("Generated Password", f"New Random Password Set:\n{password}")
    log_event("Random Password Generated")
    send_alert_email("🔑 Random Password Generated", "A new random password was generated and set.")

def view_users_from_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, face_image, registered_on FROM users")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        info = "\n".join([f"{r[0]} | {r[1]} | {r[2]} | {r[3]}" for r in rows])
    else:
        info = "No users found in database."
    messagebox.showinfo("Users in Database", info)

# === GUI Setup ===
root = tk.Tk()
root.title("WebCam Spyware Security")
root.geometry("400x750")
root.configure(bg="lightblue")

if os.path.exists(ICON_FILE):
    root.iconbitmap(ICON_FILE)
if os.path.exists(LOGO_FILE):
    logo_image = Image.open(LOGO_FILE)
    logo_image = logo_image.resize((100, 100))
    logo_photo = ImageTk.PhotoImage(logo_image)
    tk.Label(root, image=logo_photo, bg="light blue").pack(pady=10)

tk.Label(root, text="WebCam Spyware Security", fg="Black", bg="light blue", font=("Arial", 18, "bold")).pack(pady=5)
button_style = {"width": 25, "bg": "Dark Orange", "fg": "white", "font": ("Arial", 10, "bold")}
button_style1 = {"width": 25, "bg": "Goldenrod", "fg": "white", "font": ("Arial", 10, "bold")}
button_style2 = {"width": 25, "bg": "Forest Green", "fg": "white", "font": ("Arial", 10, "bold")}
button_style3 = {"width": 25, "bg": "Royal Blue", "fg": "white", "font": ("Arial", 10, "bold")}
button_style4 = {"width": 25, "bg": "Dark Violet", "fg": "white", "font": ("Arial", 10, "bold")}
button_style5 = {"width": 25, "bg": "Crimson", "fg": "white", "font": ("Arial", 10, "bold")}
tk.Button(root, text="Project Info", command=open_project_info, **button_style3).pack(pady=10)
tk.Button(root, text="View Logs", command=view_logs, **button_style1).pack(pady=10)
tk.Button(root, text="Check Status", command=check_webcam_status, **button_style).pack(pady=10)
tk.Button(root, text="Disable Camera", command=disable_camera, **button_style2).pack(pady=10)
tk.Button(root, text="Enable Camera", command=enable_camera, **button_style4).pack(pady=10)
tk.Button(root, text="Register Face", command=register_face, **button_style5).pack(pady=10)
tk.Button(root, text="Change Password", command=change_password, **button_style3).pack(pady=10)
tk.Button(root, text="Generate Random Password", command=generate_random_password, **button_style2).pack(pady=10)
tk.Button(root, text="View Users (Debug)", command=view_users_from_db, **button_style4).pack(pady=10)

root.mainloop()
