"""
SDK oficial da Upay para Python
"""

from .client import UpayClient
from .utils import (
    UpayError,
    UpayAuthenticationError,
    UpayValidationError,
    UpayNotFoundError,
    UpayRateLimitError,
    UpayServerError,
    verify_webhook_signature,
    extract_webhook_signature,
    WebhookEventType,
)

__version__ = "1.0.0"

__all__ = [
    "UpayClient",
    "UpayError",
    "UpayAuthenticationError",
    "UpayValidationError",
    "UpayNotFoundError",
    "UpayRateLimitError",
    "UpayServerError",
    "verify_webhook_signature",
    "extract_webhook_signature",
    "WebhookEventType",
]
