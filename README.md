# 🔒 Webcam Spyware Security

A Python-based desktop security tool that protects your webcam from unauthorized access and spyware threats. It detects intruders, records suspicious activity, sends real-time email alerts, and gives you full control over your webcam — all through a simple GUI.

---

## 🚀 Features

- **Dual Authentication** — Face recognition (primary) + password-based fallback access
- **Intruder Recording** — Automatically records a 10-second video when an unauthorized access attempt is detected
- **Real-time Email Alerts** — Sends instant email notifications for all security events (wrong password, camera enable/disable, logs accessed, etc.)
- **Webcam Enable / Disable** — Control webcam access directly via Windows Registry
- **Webcam Status Check** — Instantly check if the webcam is currently enabled or disabled
- **Face Registration** — Register authorized faces captured live from webcam; stored locally and in SQLite DB
- **Event Logging** — All actions are timestamped and logged to `logs.txt`
- **Password Management** — Change password manually or auto-generate a secure random password
- **User Database** — SQLite-backed user management for registered faces
- **Project Info Viewer** — Opens `project_info.html` in browser for documentation

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.9+ |
| GUI | Tkinter |
| Face Recognition | `face_recognition`, `dlib`, OpenCV (`cv2`) |
| Video Recording | OpenCV (`cv2`), Haar Cascade |
| Email Alerts | `smtplib` (via `send_email.py`) |
| Database | SQLite3 |
| Image Handling | Pillow (`PIL`) |
| Registry Control | `winreg` (Windows only) |

---

## 📁 Project Structure

```
Webcam_Spyware_Security/
│
├── webcam_security.py          # Main application — GUI + all core logic
├── send_email.py               # Email alert module
├── watchdog.py                 # Background webcam monitoring
├── record_video.py             # Video recording utility
├── setup_db.py                 # Database initialization
├── test_db.py                  # Database testing utility
│
├── haarcascade_frontalface_default.xml   # OpenCV face detection model
├── password.txt                # Encrypted/stored password file
├── logs.txt                    # Event log file
├── camera_logs.txt             # Webcam-specific logs
├── project_info.html           # Project documentation (opens in browser)
│
├── face/                       # Registered face images
├── recordings/                 # Intruder recordings saved here
├── users.db                    # SQLite database for registered users
├── webcam_logs.db              # Webcam event database
│
├── logo.png                    # App logo
├── icon.png                    # App icon
└── dlib-19.22.1-cp39-cp39-win_amd64.whl   # Prebuilt dlib wheel for Windows
```

---

## ⚙️ Installation

### Prerequisites
- Windows OS (required for webcam registry control)
- Python 3.9
- Webcam

### Step 1 — Clone the repository
```bash
git clone https://github.com/govardhanchinta99/Webcam_Spyware_Security.git
cd Webcam_Spyware_Security
```

### Step 2 — Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### Step 3 — Install dlib (use the prebuilt wheel)
```bash
pip install dlib-19.22.1-cp39-cp39-win_amd64.whl
```

### Step 4 — Install remaining dependencies
```bash
pip install opencv-python face_recognition pillow
```

### Step 5 — Configure email alerts

Open `send_email.py` and set your sender email credentials:
```python
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"   # Use Gmail App Password
RECEIVER_EMAIL = "receiver@gmail.com"
```

> **Note:** Use a [Gmail App Password](https://support.google.com/accounts/answer/185833), not your regular Gmail password.

---

## ▶️ Usage

```bash
python webcam_security.py
```

The GUI will launch with the following controls:

| Button | Description |
|---|---|
| Project Info | Opens project documentation in browser |
| View Logs | Shows all event logs (requires authentication) |
| Check Status | Checks if webcam is currently enabled or disabled |
| Disable Camera | Disables webcam via Windows Registry (requires auth) |
| Enable Camera | Re-enables webcam via Windows Registry (requires auth) |
| Register Face | Captures and registers your face for future login |
| Change Password | Manually update the access password (requires auth) |
| Generate Random Password | Auto-generates and sets a secure password (requires auth) |
| View Users (Debug) | Lists all registered users from the database |

---

## 🔐 How Authentication Works

1. **Face Recognition (Primary):** The app scans registered face images from the `face/` folder. If your face matches, access is granted instantly.
2. **Password Fallback:** If face recognition fails or no faces are registered, a password prompt appears.
3. **Intruder Response:** On wrong password entry:
   - An email alert is sent immediately
   - A 10-second intruder video is recorded and saved to `recordings/`
   - The event is logged with timestamp

---

## 📧 Email Alerts Triggered For

- Wrong password attempt (with intruder recording)
- Webcam disabled
- Webcam enabled
- Logs accessed
- Face registered
- Password changed
- Webcam status checked

---

## ⚠️ Important Notes

- **Windows Only** — Webcam enable/disable uses `winreg` and requires **Administrator privileges**
- Run the app as Administrator for registry operations to work
- The `dlib` wheel included is for **Python 3.9 on Windows 64-bit** only; for other versions, build dlib from source
- Keep `password.txt` secure — it stores the raw access password

---

## 📸 Screenshots

> *(Add screenshots of the GUI here)*

---

## 👨‍💻 Author

**Govardhan Chinta**
- GitHub: [@govardhanchinta99](https://github.com/govardhanchinta99)
- LinkedIn: [govardhan-chinta-000b0528b](https://www.linkedin.com/in/govardhan-chinta-000b0528b/)

---

## 📄 License

This project is intended for educational and personal security purposes only. Use responsibly.
