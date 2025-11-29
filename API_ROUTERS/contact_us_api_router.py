from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import HTTPStatusConstants

router = APIRouter(
    prefix="/api/contact",
    tags=["Contact Us"],
)

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    service: str
    message: str
    consent: bool

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

@router.post("/send")
async def send_contact_form(form_data: ContactForm):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Token refresh failed: {e}. Re-authenticating.")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)

        subject = f"New Contact Form Submission from {form_data.name}"
        message_body_text = f"""
        Name: {form_data.name}
        Email: {form_data.email}
        Phone: {form_data.phone}
        Service: {form_data.service}
        Message: {form_data.message}
        Consent: {"Yes" if form_data.consent else "No"}
        """
        
        message = MIMEText(message_body_text)
        message['to'] = "swapnendu2001.sc@gmail.com"
        message['from'] = "me"
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        message_body = {'raw': raw_message}

        sent_message = service.users().messages().send(userId="me", body=message_body).execute()
        
        return {"message": "Form submitted successfully", "messageId": sent_message['id']}

    except HttpError as error:
        print(f'An HTTP error occurred: {error}')
        raise HTTPException(status_code=500, detail=str(error))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))