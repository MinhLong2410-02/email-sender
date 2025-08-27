# app/services/gmail_sender.py
import base64, os
from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def build_gmail_service(sa_key_file: str, delegated_user: str):
    creds = service_account.Credentials.from_service_account_file(
        sa_key_file, scopes=SCOPES
    ).with_subject(delegated_user)  # impersonate Workspace user
    return build("gmail", "v1", credentials=creds, cache_discovery=False)

def send_html(to_email: str, subject: str, html: str,
              sa_key_file: str, sender_email: str = None, sender_name: str = "IX Health"):

    service = build_gmail_service(sa_key_file, delegated_user=sender_email)

    msg = EmailMessage()
    msg["To"] = to_email
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["Subject"] = subject
    msg.set_content("Your mail client does not support HTML.")
    msg.add_alternative(html, subtype="html")

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    return service.users().messages().send(userId=sender_email, body={"raw": raw}).execute()
