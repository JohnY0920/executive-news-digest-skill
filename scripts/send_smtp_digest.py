#!/usr/bin/env python3
"""
SMTP Email Sender for Executive News Digest
Uses Gmail SMTP directly
"""

import smtplib
import json
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict

def send_smtp_email(recipients: str, subject: str, html_body: str) -> bool:
    """Send email via Gmail SMTP"""
    try:
        # Gmail SMTP settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "wotb.spt@gmail.com"
        # Note: This should be an app password, not regular password
        app_password = "kaho mwqy nwyx sorq"
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = recipients
        
        # Add HTML content
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)
        
        # Create secure context and send
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipients.split(","), message.as_string())
        
        print(f"✅ Email sent successfully to {recipients}!")
        return True
        
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False

def load_and_send_digest():
    """Load the generated content and send email"""
    try:
        # Load content
        with open('news_digest_raw.json', 'r') as f:
            news_digest = json.load(f)
        with open('commentary_output.json', 'r') as f:
            commentaries = json.load(f)
        with open('translated_digest.json', 'r', encoding='utf-8') as f:
            translated = json.load(f)
            
        # Load HTML preview
        with open('digest_preview.html', 'r', encoding='utf-8') as f:
            html_body = f.read()
            
        # Prepare email
        subject = f"📰 Executive News Digest - {datetime.now().strftime('%b %d, %Y')}"
        recipients = "phoestia0920@hotmail.com,johnyin@aisemble.ca,donald.fang@forwardsynergies.com"
        
        # Send email
        success = send_smtp_email(recipients, subject, html_body)
        
        if success:
            print("🎉 Digest sent successfully!")
        else:
            print("❌ Failed to send digest")
            
        return success
        
    except FileNotFoundError as e:
        print(f"Error: {e}. Make sure all digest files are generated.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    load_and_send_digest()