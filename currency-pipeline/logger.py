import os
import csv
import json
import datetime
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==========================================
# MASTER CONFIGURATION (Set your details here!)
# ==========================================
SENDER_EMAIL = "your_email@gmail.com"
RECEIVER_EMAIL = "your_email@gmail.com" 
APP_PASSWORD = "your_16_character_app_password"  # No spaces inside quotes
CSV_FILE = "exchange_log.csv"
URL = "https://api.exchangerate-api.com/v4/latest/USD"

print("--- PIPELINE ACTIVATED ---")

try:
    # === PHASE 2: THE FETCH ===
    print("1. Querying the live web API...")
    with urllib.request.urlopen(URL) as response:
        raw_text = response.read().decode()
        data = json.loads(raw_text)
        
        # Pull live values from the API response dictionary
        inr_rate = data["rates"]["INR"]
        current_date = data["date"]
        
    print(f"   Success! Live Rate Captured: 1 USD = {inr_rate} INR")

    # === PHASE 3: THE LOG ===
    print("2. Syncing with local CSV ledger...")
    file_exists = os.path.exists(CSV_FILE)
    
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # If it's the first run, print column headers
        if not file_exists:
            print("   Ledger not found. Initializing brand new CSV file...")
            writer.writerow(["Date", "Base_Currency", "Target_Currency", "Rate"])
            
        # Append the live web data directly into the spreadsheet
        writer.writerow([current_date, "USD", "INR", inr_rate])
        
    print("   Success! Historical ledger updated.")

    # === PHASE 4: THE EMAIL ALERT ===
    print("3. Connecting to secure mail server...")
    
    # Draft a clean email layout
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = f"Daily Currency Alert: USD to INR ({current_date})"
    
    body = f"""
    Hello!
    
    Your automated data pipeline has run successfully.
    
    [LATEST METRICS]
    - Date: {current_date}
    - Base: USD
    - Target: INR
    - Conversion Rate: {inr_rate}
    
    This record has been logged to your permanent spreadsheet file: '{CSV_FILE}'.
    """
    msg.attach(MIMEText(body, 'plain'))

    # Setup the secure internet connection to the post office
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Encrypt the link
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
    server.quit()
    
    print("   Success! Notification dispatched to your inbox.")
    print("\n--- PIPELINE SUCCESSFULLY EXECUTED ---")

except Exception as error:
    print(f"\n❌ Pipeline terminated due to error: {error}")