"""
Cliente principal do SDK Upay
"""

from typing import Optional
from .http import HttpClient
from .resources.payment_links import PaymentLinksResource
from .resources.transactions import TransactionsResource
from .resources.products import ProductsResource
from .resources.clients import ClientsResource
from .resources.coupons import CouponsResource
from .utils.webhooks import verify_webhook_signature


class UpayClient:
    """
    Cliente principal para interagir com a API Upay
    
    Exemplo:
        >>> from upay import UpayClient
        >>> 
        >>> upay = UpayClient(api_key="sua_api_key_aqui")
        >>> 
        >>> # Criar um link de pagamento
        >>> payment_link = upay.payment_links.create({
        ...     "title": "Produto Premium",
        ...     "amount": 10000,  # R$ 100,00 em centavos
        ... })
        >>> 
        >>> # Listar transações
        >>> transactions = upay.transactions.list(page=1, limit=10)
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        version: str = "v1",
        timeout: int = 30
    ):
        """
        Inicializa o cliente Upay
        
        Args:
            api_key: Sua API key da Upay (obrigatório)
            base_url: URL base da API (padrão: https://upay-sistema-api.onrender.com)
            version: Versão da API (padrão: v1)
            timeout: Timeout das requisições em segundos (padrão: 30)
            
        Raises:
            ValueError: Se api_key não for fornecida
        """
        if not api_key:
            raise ValueError("API Key é obrigatória")
        
        self._http = HttpClient(
            api_key=api_key,
            base_url=base_url or "https://upay-sistema-api.onrender.com",
            version=version,
            timeout=timeout
        )
        
        # Inicializa recursos
        self.payment_links = PaymentLinksResource(self._http)
        self.transactions = TransactionsResource(self._http)
        self.products = ProductsResource(self._http)
        self.clients = ClientsResource(self._http)
        self.coupons = CouponsResource(self._http)
    
    def verify_webhook_signature(
        self,
        payload: bytes | str,
        signature: str,
        secret: str
    ) -> bool:
        """
        Verifica a assinatura de um webhook
        
        Args:
            payload: Corpo da requisição (bytes ou string)
            signature: Assinatura recebida no header
            secret: Secret da API key
            
        Returns:
            True se a assinatura for válida
            
        Exemplo:
            >>> import flask
            >>> 
            >>> @app.route('/webhook', methods=['POST'])
            >>> def webhook():
            ...     payload = flask.request.data
            ...     signature = flask.request.headers.get('x-signature')
            ...     
            ...     if upay.verify_webhook_signature(payload, signature, webhook_secret):
            ...         # Processar webhook
            ...         pass
        """
        return verify_webhook_signature(payload, signature, secret)
