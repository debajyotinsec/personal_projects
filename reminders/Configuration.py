
import os
from dotenv import load_dotenv

class Configuration:
    def __init__(self):
        self.gemini_api_key = None
        self.imap_server = None
        self.email_user = None
        self.email_pass = None
        self.target_domain = None
        self.log_level = None
        self.log_file = None
        self.email_server = None
        self.email_port = None
        self.twilio_account_sid = None
        self.twilio_auth_token = None
        self.twilio_from_phone_number = None
        self.twilio_to_phone_number = None
        self.email_receiver = None
        self.text_message_service = None 

    def load_from_env(self):
        load_dotenv()  # Load environment variables from .env file
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.imap_server = os.getenv('IMAP_SERVER')
        self.email_server = os.getenv('EMAIL_SERVER')
        self.email_port = int(os.getenv('EMAIL_PORT', 465))  # Default to 465 if not set
        self.email_user = os.getenv('EMAIL_USER')
        self.email_pass = os.getenv('EMAIL_PASS')
        self.target_domain = os.getenv('TARGET_DOMAIN')
        self.log_level = os.getenv('LOG_LEVEL', 'DEBUG')  # Default to DEBUG if not set
        self.log_file = os.getenv('LOG_FILE')  # Default to app.log if not set
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_from_phone_number = os.getenv('TWILIO_FROM_PHONE_NUMBER')
        self.twilio_to_phone_number = os.getenv('TWILIO_TO_PHONE_NUMBER')
        self.email_receiver = os.getenv('EMAIL_RECEIVER')  # Added for email-to-SMS functionality
        self.text_message_service = os.getenv('TEXT_MESSAGE_SERVICE')  # Default to email-to-sms if not set




