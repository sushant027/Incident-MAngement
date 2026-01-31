import smtplib
from email.mime.text import MIMEText

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "bank.alerts@gmail.com"
    msg["To"] = to

    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.starttls()
    s.login("bank.alerts@gmail.com", "APP_PASSWORD")
    s.send_message(msg)
    s.quit()
