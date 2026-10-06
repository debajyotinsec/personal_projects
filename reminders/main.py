from Configuration import *
from constants import *
# from send_texts import *
import argparse
import logging
from pathlib import Path
from SendTexts import *

def main():
    # setup the argument parser
    parser = argparse.ArgumentParser(description="Send SMS reminders.", allow_abbrev=False)

    # add the arguments
    parser.add_argument("--event", type=str, required=True, help="Event name for the reminder (e.g., 'vitamin_d').")
    
    # parse the arguments from the command line
    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code != 0:
            logging.error("Error: Missing or invalid arguments.")
            logging.info("Usage: python main.py --event <event_name>")
        raise

    event_name = args.event


    config = Configuration()
    config.load_from_env()

    # Place logs in the same directory
    log_file = Path(__file__).resolve().parent / "logs" / "app.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=getattr(logging, config.log_level.upper()),
        format="%(asctime)s | %(levelname)s | %(name)s | %(lineno)d | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler()
        ],
    force=True
    )

    logger = logging.getLogger(__name__)
    logger.info("Application started")


    message_body = dict_of_message_bodies.get(event_name, f"No reminder message for event '{event_name}'.")

    send_texts = SendTexts()

    if config.text_message_service == "twilio":
        send_texts.send_sms_via_twilio(config, message_body)
    elif config.text_message_service == "email-to-sms":
        send_texts.send_sms_via_email(config, message_body)
    else:
        logger.error(f"Error: Unknown text message service '{config.text_message_service}'. Please check your configuration.")


if __name__ == "__main__":
    main()