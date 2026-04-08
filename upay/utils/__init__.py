"""
Utilitários do SDK Upay
"""

from .errors import (
    UpayError,
    UpayAuthenticationError,
    UpayValidationError,
    UpayNotFoundError,
    UpayRateLimitError,
    UpayServerError,
    handle_api_error
)
from .webhooks import verify_webhook_signature, extract_webhook_signature, WebhookEventType

__all__ = [
    'UpayError',
    'UpayAuthenticationError',
    'UpayValidationError',
    'UpayNotFoundError',
    'UpayRateLimitError',
    'UpayServerError',
    'handle_api_error',
    'verify_webhook_signature',
    'extract_webhook_signature',
    'WebhookEventType',
]
