import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_alert_email(subject="Security Alert", body="An event occurred in your Webcam Spyware Security System."):
    sender_email = "govardhanchinta999@gmail.com"
    sender_password = "slbw ehxq koqw jzkr"  # ✅ Your App Password
    receiver_email = "govardhanchinta999@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        print("📧 Sending email...")
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent.")
    except Exception as e:
        print("❌ Failed to send email:", e)
