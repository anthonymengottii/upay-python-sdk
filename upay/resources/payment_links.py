"""
Recurso de Payment Links
"""

from typing import Optional, Dict, Any
from ..http import HttpClient


class PaymentLinksResource:
    """Recurso para gerenciar Payment Links"""
    
    def __init__(self, http: HttpClient):
        self.http = http
    
    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo link de pagamento
        
        Args:
            data: Dados do link de pagamento
                - title: Título do link (obrigatório, min 3 caracteres)
                - amount: Valor em centavos (obrigatório se não houver products)
                - description: Descrição do link
                - currency: Moeda (padrão: BRL)
                - expiresAt: Data de expiração (ISO string)
                - redirectUrl: URL de redirecionamento
                - settings: Configurações de pagamento
                - status: Status (ACTIVE ou INACTIVE)
                - products: Lista de produtos
                
        Returns:
            Link de pagamento criado
        """
        # Validação básica
        if not data.get("title") or len(data["title"].strip()) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres")
        
        if not data.get("amount") and not data.get("products"):
            raise ValueError("É necessário fornecer amount ou products")
        
        if data.get("amount") and data.get("amount", 0) < 100:
            raise ValueError("Valor mínimo é R$ 1,00 (100 centavos)")
        
        # Prepara dados para envio
        request_data = {
            "title": data["title"],
            "description": data.get("description"),
            "amount": data.get("amount"),
            "products": data.get("products"),
            "currency": data.get("currency", "BRL"),
            "expiresAt": data.get("expiresAt"),
            "redirectUrl": data.get("redirectUrl"),
            "settings": data.get("settings"),
            "status": data.get("status", "ACTIVE"),
            "metaPixelCode": data.get("metaPixelCode"),
            "stockQuantity": data.get("stockQuantity"),
            "stockEnabled": data.get("stockEnabled"),
        }
        
        # Remove valores None
        request_data = {k: v for k, v in request_data.items() if v is not None}
        
        return self.http.post("/payment-links", request_data)
    
    def list(
        self,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        order_by: Optional[str] = None,
        order_direction: Optional[str] = None,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Lista links de pagamento
        
        Args:
            page: Número da página
            limit: Limite de itens por página
            cursor: Cursor para paginação
            order_by: Campo para ordenação
            order_direction: Direção da ordenação (ASC ou DESC)
            status: Filtrar por status
            
        Returns:
            Dicionário com 'data' (lista) e 'pagination'
        """
        params = {
            "page": page,
            "limit": limit,
            "cursor": cursor,
            "orderBy": order_by,
            "orderDirection": order_direction,
            "status": status,
        }
        
        return self.http.get("/payment-links", params)
    
    def get(self, link_id: str) -> Dict[str, Any]:
        """
        Obtém um link de pagamento por ID
        
        Args:
            link_id: ID do link de pagamento
            
        Returns:
            Link de pagamento
        """
        if not link_id:
            raise ValueError("ID é obrigatório")
        
        return self.http.get(f"/payment-links/{link_id}")
    
    def get_by_slug(self, slug: str) -> Dict[str, Any]:
        """
        Obtém um link de pagamento por slug
        
        Args:
            slug: Slug do link de pagamento
            
        Returns:
            Link de pagamento
        """
        if not slug:
            raise ValueError("Slug é obrigatório")
        
        return self.http.get(f"/payment-links/slug/{slug}")
    
    def update(self, link_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um link de pagamento
        
        Args:
            link_id: ID do link de pagamento
            data: Dados para atualizar
            
        Returns:
            Link de pagamento atualizado
        """
        if not link_id:
            raise ValueError("ID é obrigatório")
        
        # Prepara dados para envio
        update_data = {}
        if "title" in data:
            update_data["title"] = data["title"]
        if "description" in data:
            update_data["description"] = data["description"]
        if "amount" in data:
            update_data["amount"] = data["amount"]
        if "status" in data:
            update_data["status"] = data["status"]
        if "expiresAt" in data:
            update_data["expiresAt"] = data["expiresAt"]
        if "redirectUrl" in data:
            update_data["redirectUrl"] = data["redirectUrl"]
        if "settings" in data:
            update_data["settings"] = data["settings"]
        
        return self.http.patch(f"/payment-links/{link_id}", update_data)
    
    def delete(self, link_id: str) -> None:
        """
        Deleta um link de pagamento
        
        Args:
            link_id: ID do link de pagamento
        """
        if not link_id:
            raise ValueError("ID é obrigatório")
        
        self.http.delete(f"/payment-links/{link_id}")
    
    def get_checkout_url(self, slug: str, base_url: Optional[str] = None) -> str:
        """
        Obtém a URL pública do checkout
        
        Args:
            slug: Slug do link de pagamento
            base_url: URL base do checkout (padrão: https://checkout.upaybr.com)
            
        Returns:
            URL completa do checkout
        """
        checkout_base = base_url or "https://checkout.upaybr.com"
        return f"{checkout_base}/{slug}"
