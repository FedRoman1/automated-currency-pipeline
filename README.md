# Automated Currency Data Pipeline & Alert System

A lightweight, native Python data microservice that extracts real-time exchange rate metrics from a web API, structures and appends the observations locally to a CSV database, and dispatches an automated notification summary via secure SMTP connection.

## 🛠️ Tech Stack & Architecture
- **Language:** Python (3.x)
- **Built-in Modules:** `urllib.request` (Web Requests), `json` (Data Parsing), `csv` (Storage Engineering), `smtplib` (Network Alerts)
- **Data Source:** Open Exchange Rate API

## 📋 Features
- **Automated Ingestion:** Programmatically parses JSON payloads from the web without heavy external web scraping libraries.
- **Incremental Data Logging:** Employs defensive file validation routines to append records without overwriting historical lines.
- **Secure Communication:** Implements standard TLS encryption handshakes to interface securely with corporate mail protocols (Gmail SMTP).
