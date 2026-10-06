from Configuration import *
from twilio.rest import Client
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from constants import *
import logging

logger = logging.getLogger(__name__)


class SendTexts:
    def __init__(self):
        pass  # Placeholder for any future initialization if needed

    def send_sms_via_twilio(self, config, message_body):
        # Credentials from your Twilio Console dashboard
        account_sid = config.twilio_account_sid
        auth_token = config.twilio_auth_token
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=message_body,
            from_=config.twilio_from_phone_number,
            to=config.twilio_to_phone_number
        )

        logger.info(f"Message sent! ID: {message.sid}")


    def send_sms_via_email(self, config, message_body):
        """        
            Send an email as a text message using SMTP
            use mobile carrier's email-to-SMS gateway (e.g., for Xfinity Mobile:
            '1234567890@vtext.com'
        """
        # 1. Configure configuration details
        smtp_server = config.email_server  # Replace with your provider's SMTP server
        smtp_port = config.email_port  # Port for SSL connections
        sender_email = config.email_user  # Your email address
        sender_password = config.email_pass  # Your 16-character App Password

        # To text an Xfinity Mobile number, use: "1234567890@vtext.com"
        receiver_email = config.email_receiver  # Use the email receiver from the configuration

        # 2. Construct the message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Automated Alert"

        # message_body = "This is a text message sent from my Python script!"
        message.attach(MIMEText(message_body, "plain"))

        try:
            # 3. Establish a secure connection and send the email
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, receiver_email, message.as_string())

            logger.info("Success: Message sent successfully!")

        except Exception as e:
            logger.error(f"Error: Could not send message. Reason: {e}")
