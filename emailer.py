import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date


def send_deal_alert(deals, kind="international"):
    gmail = os.getenv("GMAIL_ADDRESS")
    app_password = os.getenv("GMAIL_APP_PASSWORD")
    recipient = os.getenv("ALERT_EMAIL") or gmail

    if not gmail or not app_password:
        print("Email not configured — skipping alert.")
        return

    subject = f"Flight Deal Alert from SLC — {date.today()}"

    if deals:
        lines = [f"Found {len(deals)} deal(s) from SLC today!\n"]
        for d in sorted(deals, key=lambda x: x["price"]):
            lines.append(f"  ${d['price']}  {d['name']} ({d['code']})  via {d.get('airline', 'Unknown')}")
            lines.append(f"  Depart: {d['depart']}  Return: {d['return']}\n")
    else:
        lines = ["No deals found today. Check back tomorrow!"]

    body = "\n".join(lines)

    msg = MIMEMultipart()
    msg["From"] = gmail
    msg["To"] = recipient
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail, app_password)
            server.sendmail(gmail, recipient, msg.as_string())
        print(f"Alert sent to {recipient}")
    except Exception as e:
        print(f"Failed to send email: {e}")
