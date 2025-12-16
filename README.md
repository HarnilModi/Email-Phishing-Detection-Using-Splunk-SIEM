# Email Phishing Detection Using Splunk SIEM

## 📌 Project Overview
This project demonstrates a SOC-oriented approach to detecting phishing emails using **Splunk SIEM**.  
Email messages are processed automatically, their **body content and URLs are extracted**, and phishing indicators are identified using keyword-based and URL-based detection logic.

The goal of this project is to simulate **real-world email security monitoring** and generate alerts for suspicious or phishing emails.

---

## 🎯 Objectives
- Extract email body content from `.eml` files automatically
- Identify suspicious URLs embedded in email bodies
- Detect phishing-related keywords commonly used in attacks
- Analyze processed email data in Splunk SIEM
- Generate phishing detection results suitable for alerting

---

## 🛠️ Tools & Technologies Used
- **hMailServer** – Local mail server for email simulation
- **Python** – Email parsing and URL extraction
- **Splunk Enterprise** – Log indexing and analysis
- **HTTP Event Collector (HEC)** – Data ingestion into Splunk
- **Windows OS**

---

## 🔄 Project Workflow
1. Email is received by hMailServer
2. Email is saved as a `.eml` file automatically
3. Python script extracts:
   - Email body
   - Embedded URLs
   - Phishing-related keywords
4. Parsed data is sent to Splunk via HEC
5. Splunk query analyzes the data and identifies phishing indicators

---

## 🔍 Splunk Phishing Detection Query

```spl
index=mail sourcetype="email:eml"
| where risk="HIGH"
| eval reason=case(
    mvcount(urls)>0, "Suspicious URL detected",
    mvcount(phish_keywords)>0, "Phishing keywords detected"
)
| table _time from to subject urls phish_keywords reason

<img width="1920" height="1040" alt="image" src="https://github.com/user-attachments/assets/34b836b9-8226-4bfb-a860-5135c41b6f3a" />

