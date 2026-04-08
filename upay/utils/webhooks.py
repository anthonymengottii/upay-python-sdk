"""
Utilitários para verificação de webhooks
"""

import hmac
import hashlib
from typing import Dict, Optional, Union
from enum import Enum


class WebhookEventType(str, Enum):
    """Tipos de eventos de webhook"""
    TRANSACTION_CREATED = "transaction.created"
    TRANSACTION_PAID = "transaction.paid"
    TRANSACTION_FAILED = "transaction.failed"
    TRANSACTION_CANCELLED = "transaction.cancelled"
    TRANSACTION_REFUNDED = "transaction.refunded"
    PAYMENT_LINK_CREATED = "payment_link.created"
    PAYMENT_LINK_UPDATED = "payment_link.updated"
    PAYMENT_LINK_DELETED = "payment_link.deleted"


def verify_webhook_signature(
    payload: Union[bytes, str],
    signature: str,
    secret: str
) -> bool:
    """
    Verifica a assinatura de um webhook usando HMAC SHA256
    
    Args:
        payload: Corpo da requisição (bytes ou string)
        signature: Assinatura recebida no header
        secret: Secret da API key
        
    Returns:
        True se a assinatura for válida
    """
    if not payload or not signature or not secret:
        return False
    
    try:
        # Converte payload para bytes se necessário
        if isinstance(payload, str):
            payload_bytes = payload.encode('utf-8')
        else:
            payload_bytes = payload
        
        # Gera o hash HMAC SHA256
        hash_obj = hmac.new(
            secret.encode('utf-8'),
            payload_bytes,
            hashlib.sha256
        )
        expected_signature = hash_obj.hexdigest()
        
        # Comparação segura para prevenir timing attacks
        return hmac.compare_digest(expected_signature, signature)
    except Exception:
        return False


def extract_webhook_signature(headers: Dict[str, Union[str, list, None]]) -> Optional[str]:
    """
    Extrai a assinatura do header da requisição
    
    Args:
        headers: Headers da requisição
        
    Returns:
        A assinatura ou None se não encontrada
    """
    # Tenta diferentes formatos de header
    signature_header = (
        headers.get("x-upay-signature") or
        headers.get("x-upay-signature-256") or
        headers.get("upay-signature") or
        headers.get("signature")
    )
    
    if not signature_header:
        return None
    
    # Se for lista, pega o primeiro
    if isinstance(signature_header, list):
        signature_header = signature_header[0] if signature_header else None
    
    if not signature_header:
        return None
    
    # Remove prefixo "sha256=" se existir
    return signature_header.replace("sha256=", "")
