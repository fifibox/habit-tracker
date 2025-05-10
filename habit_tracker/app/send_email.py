import os.path
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

# 1. Define required Gmail scope
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

# 2. Authenticate the user and return Gmail service
def gmail_authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# 3. Create a message object
def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

# 4. Send the email
def send_email():
    service = gmail_authenticate()
    message = create_message(
        sender="your_email@gmail.com",  # Must be your Gmail
        to="recipient@example.com",
        subject="Password Reset Link",
        message_text="Click here to reset your password: https://your-reset-link"
    )
    sent = service.users().messages().send(userId="me", body=message).execute()
    print(f'Message sent! ID: {sent["id"]}')

# Run the send_email function
if __name__ == '__main__':
    send_email()