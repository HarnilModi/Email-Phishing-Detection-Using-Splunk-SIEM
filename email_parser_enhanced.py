import os
import time
import json
import re
import requests
from email import policy
from email.parser import BytesParser

# ================= CONFIG =================
EML_FOLDER = r"C:\email_logs\inbound_eml"
PROCESSED_FOLDER = r"C:\email_logs\processed_eml"

SPLUNK_HEC = "https://localhost:8088/services/collector"
SPLUNK_TOKEN = "<YOUR_SPLUNK_HEC_TOKEN>"
"
INDEX = "mail"

CHECK_INTERVAL = 5
# ==========================================

HEADERS = {
    "Authorization": f"Splunk {SPLUNK_TOKEN}",
    "Content-Type": "application/json"
}

PHISH_KEYWORDS = [
    "verify", "password", "urgent", "login",
    "reset", "account", "bank", "invoice"
]

URL_REGEX = re.compile(r"https?://[^\s]+")

os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def send_to_splunk(event):
    payload = {
        "event": event,
        "index": INDEX,
        "sourcetype": "email:eml"
    }
    r = requests.post(
        SPLUNK_HEC,
        headers=HEADERS,
        json=payload,
        verify=False
    )
    print("[Splunk]", r.status_code, r.text)

def parse_eml(path):
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    urls = URL_REGEX.findall(body)
    keywords = [k for k in PHISH_KEYWORDS if k in body.lower()]

    event = {
        "from": msg.get("From"),
        "to": msg.get("To"),
        "subject": msg.get("Subject"),
        "body": body.strip(),
        "urls": urls,
        "phish_keywords": keywords,
        "risk": "HIGH" if urls or keywords else "LOW"
    }

    return event

def main():
    print("📧 Email → Splunk monitor started")
    while True:
        for file in os.listdir(EML_FOLDER):
            if not file.endswith(".eml"):
                continue

            full_path = os.path.join(EML_FOLDER, file)

            try:
                event = parse_eml(full_path)
                send_to_splunk(event)

                os.rename(
                    full_path,
                    os.path.join(PROCESSED_FOLDER, file)
                )

            except Exception as e:
                print("Error:", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

