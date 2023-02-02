import string
import secrets
import re
from urllib.parse import urlparse
from datetime import datetime

# --- Configuration Imports ---
# These settings are ideally defined in config.py for easy management.
# We provide fallbacks here in case config.py doesn't define them,
# but in a production environment, ensure config.py is properly configured.
try:
    from config import SHORT_CODE_LENGTH, SHORT_CODE_CHARS
except ImportError:
    # Fallback defaults if config.py is missing or doesn't define these.
    # In a real application, you might log a warning here.
    SHORT_CODE_LENGTH = 6  # Default length for generated short codes
    # Default character set: alphanumeric characters (a-z, A-Z, 0-9)
    # Consider removing easily confused characters (e.g., '0OolI1') for better readability
    # if short code length allows for it. For general use, this set is common.
    SHORT_CODE_CHARS = string.ascii_letters + string.digits


# --- Short Code Generation Utilities ---

def generate_short_code(length: int = SHORT_CODE_LENGTH) -> str:
    """
    Generates a random, alphanumeric short code of a specified length.

    This function uses Python's `secrets` module, which is cryptographically strong
    and suitable for generating tokens, passwords, and other security-sensitive data.
    The character set used for generation is defined by `SHORT_CODE_CHARS` (from config.py).

    Args:
        length (int): The desired length of the short code. Defaults to `SHORT_CODE_LENGTH`
                      as defined in `config.py` or the fallback.

    Returns:
        str: A randomly generated short code.

    Raises:
        ValueError: If `SHORT_CODE_CHARS` is empty, preventing an infinite loop or error
                    during character selection.
    """
    if not SHORT_CODE_CHARS:
        raise ValueError("SHORT_CODE_CHARS cannot be empty. Define it in config.py or provide a default.")
    return ''.join(secrets.choice(SHORT_CODE_CHARS) for _ in range(length))


# --- URL Validation Utilities ---

def is_valid_url(url: str) -> bool:
    """
    Validates if a given string is a well-formed and accessible URL.

    This function parses the URL to check for a valid scheme (e.g., 'http', 'https')
    and a network location (domain). It helps prevent storing malformed or
    potentially malicious URLs.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL is considered valid, False otherwise.
    """
    if not isinstance(url, str) or not url:
        return False

    try:
        result = urlparse(url)
        # A valid web URL should have both a scheme and a network location.
        # We also explicitly check that the scheme is 'http' or 'https'.
        if all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']:
            # Further check: ensure the netloc isn't just whitespace or empty after parsing.
            if result.netloc.strip():
                return True
        return False
    except ValueError:
        # `urlparse` can raise ValueError for extremely malformed URLs, though it's rare.
        return False
    except Exception:
        # Catch any other unexpected errors during parsing. In a production app,
        # you would log this exception for debugging.
        return False


# --- Input Sanitization Utilities ---

def sanitize_custom_short_code(code: str) -> str:
    """
    Sanitizes a custom short code provided by the user.

    This function removes any characters that are not alphanumeric (a-z, A-Z, 0-9).
    This ensures that custom codes only contain valid and safe characters for URLs
    and database storage,