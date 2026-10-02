# SMS Reminders

A small command-line tool for sending event-based reminders by SMS. It supports Twilio and email-to-SMS gateways. Each run sends one message for the requested event; scheduling is handled externally.

## Requirements

- Python 3
- A configured Twilio account, or an email account and carrier email-to-SMS gateway

Install the Python dependencies:

```bash
python -m pip install python-dotenv twilio
```

## Setup

From the project directory, create a local environment file from the sample:

```bash
cp .env-sample .env
```

Edit `.env` and set `TEXT_MESSAGE_SERVICE` to either `twilio` or `email-to-sms`. Fill in the credentials and destination settings for the selected service.

### Twilio

Set these values in `.env`:

```dotenv
TEXT_MESSAGE_SERVICE=twilio
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_PHONE_NUMBER=your_twilio_number
TWILIO_TO_PHONE_NUMBER=recipient_number
```

Use phone numbers in the format required by your Twilio account, typically E.164 (for example, `+15551234567`).

### Email-to-SMS

Set these values in `.env`:

```dotenv
TEXT_MESSAGE_SERVICE=email-to-sms
EMAIL_SERVER=smtp.gmail.com
EMAIL_PORT=465
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_app_password
EMAIL_RECEIVER=recipient_number@carrier_gateway
```

Use your mobile carrier's email-to-SMS gateway address for `EMAIL_RECEIVER`. Gateway availability and behavior vary by carrier. The current implementation uses SMTP over SSL; port `465` is the default. For Gmail, use an app password if required by your account's security settings.

## Run

Run the tool from the project directory and provide an event name:

```bash
python main.py --event vitamin_d
```

The only event currently configured is `vitamin_d`, defined in `constants.py`. Add additional event names and message text to `dict_of_message_bodies` there. If an event name is not configured, the program sends a fallback message identifying the unknown event.

## Logs

The application writes logs to `logs/app.log` and to the terminal. The log level can be set with `LOG_LEVEL` in `.env`; it defaults to `DEBUG`.

## Security

Keep credentials in `.env` and never commit that file. The repository's `.gitignore` excludes it. Review staged files before pushing, and use `.env-sample` only for placeholders, not real credentials.
