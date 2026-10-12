import logging
import sys
import structlog

REDACTED = "[REDACTED]"


def mask_name(value):
    if not isinstance(value, str) or not value:
        return REDACTED if value else value
    return f"{value[0]}***"


def mask_email(value):
    if not isinstance(value, str) or "@" not in value:
        return REDACTED if value else value
    local_part, domain = value.split("@", 1)
    return f"{local_part[0] if local_part else '*'}***@{domain}"


def mask_phone(value):
    if not isinstance(value, str):
        return REDACTED if value else value
    digits = "".join(character for character in value if character.isdigit())
    return f"***-***-{digits[-4:]}" if len(digits) >= 4 else REDACTED


def mask_card_number(value):
    if not isinstance(value, str):
        return REDACTED if value else value
    digits = "".join(character for character in value if character.isdigit())
    return f"{'*' * (len(digits) - 4)}{digits[-4:]}" if len(digits) >= 4 else REDACTED


SENSITIVE_FIELD_MASKERS = {
    "first_name": mask_name,
    "last_name": mask_name,
    "cardholder_name": mask_name,
    "email": mask_email,
    "phone_number": mask_phone,
    "date_of_birth": lambda value: REDACTED if value else value,
    "address_line1": lambda value: REDACTED if value else value,
    "address_line2": lambda value: REDACTED if value else value,
    "address_line3": lambda value: REDACTED if value else value,
    "address_line_1": lambda value: REDACTED if value else value,
    "address_line_2": lambda value: REDACTED if value else value,
    "address_line_3": lambda value: REDACTED if value else value,
    "city": lambda value: REDACTED if value else value,
    "state": lambda value: REDACTED if value else value,
    "zip_code": lambda value: REDACTED if value else value,
    # "country": lambda value: REDACTED if value else value,
    "card_number": mask_card_number,
    "expiration_date": lambda value: REDACTED if value else value,
}


def _mask_nested(value):
    if isinstance(value, dict):
        return {
            key: SENSITIVE_FIELD_MASKERS[key.lower()](item)
            if isinstance(key, str) and key.lower() in SENSITIVE_FIELD_MASKERS
            else _mask_nested(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_mask_nested(item) for item in value]
    return value


def mask_sensitive_data(logger, log_method, event_dict):
    return _mask_nested(event_dict)


def order_keys_processor(logger, log_method, event_dict):
    """Custom processor to enforce a strict key order in the output JSON."""
    # Define your preferred key sequence
    key_order = ["timestamp", "level", "filename", "lineno", "event"]
    
    # Rebuild the dictionary in the preferred order
    ordered_dict = {k: event_dict[k] for k in key_order if k in event_dict}
    
    # Append any remaining dynamic context keys that weren't explicitly ordered
    for k, v in event_dict.items():
        if k not in ordered_dict:
            ordered_dict[k] = v
            
    return ordered_dict

# Tell structlog how to handle and format your logs step-by-step
structlog.configure(
    processors=[
        # Step 1: Add a timestamp string to each log item
        structlog.processors.TimeStamper(fmt="iso"),
        # Step 2: Add the log label severity (info, warn, error)
        structlog.processors.add_log_level,
        # Step 3: Handle error traceback info cleanly if an app crashes
        structlog.processors.format_exc_info,
        # Step 4: Add source location details before rendering the event
        structlog.processors.CallsiteParameterAdder(
            [
                structlog.processors.CallsiteParameter.FILENAME,
                structlog.processors.CallsiteParameter.LINENO,
                structlog.processors.CallsiteParameter.FUNC_NAME,
            ]
        ),
        # Step 5: Mask sensitive fields in nested event data
        mask_sensitive_data,
        # Step 6: Enforce a strict key order in the output JSON
        order_keys_processor,
        # Step 7: Turn the final dictionary structure into a JSON text line
        structlog.processors.JSONRenderer(),
        # # structlog.processors.key_ordering(
        #     ["timestamp", "level", "logger", "line_number", "filename", "event"]
        
    ],
    # Tell it to print directly to the console output (stdout)
    logger_factory=structlog.PrintLoggerFactory(sys.stdout),
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()
# logger.info("payment_processed", amount=49.99, currency="USD")
