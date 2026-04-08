"""
Recurso de Cupons
"""

from typing import Optional, Dict, Any, List
import requests
from ..http import HttpClient


class CouponsResource:
    """Recurso para validar cupons"""
    
    def __init__(self, http: HttpClient):
        self.http = http
    
    def validate(
        self,
        code: str,
        amount_cents: int,
        product_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Valida um cupom de desconto
        
        Nota: Este endpoint é público e não requer autenticação
        Endpoint: POST /api/coupons/validate (não /api/v1)
        
        Args:
            code: Código do cupom (obrigatório)
            amount_cents: Valor em centavos (obrigatório, min 100)
            product_ids: Lista de IDs de produtos (opcional)
            
        Returns:
            Resultado da validação com:
                - valid: Se o cupom é válido
                - discountCents: Valor do desconto em centavos
                - discountPercentage: Percentual de desconto
                - finalAmountCents: Valor final após desconto
                - message: Mensagem de erro ou sucesso
        """
        if not code or len(code.strip()) == 0:
            raise ValueError("Código do cupom é obrigatório")
        
        if not amount_cents or amount_cents < 100:
            raise ValueError("Valor mínimo é R$ 1,00 (100 centavos)")
        
        # Endpoint público em /api/coupons/validate (sem /v1)
        base_url = self.http.base_url
        url = f"{base_url}/api/coupons/validate"
        
        # Faz requisição sem autenticação
        try:
            # Prepara dados - productIds deve ser array (mesmo que vazio)
            data = {
                "code": code.strip(),
                "amount": amount_cents,
                "productIds": product_ids if product_ids else [],
            }
            
            response = requests.post(
                url,
                json=data,
                headers={
                    "Content-Type": "application/json",
                },
                timeout=self.http.timeout
            )
            
            try:
                result = response.json()
            except Exception:
                result = None

            if not result:
                raise Exception(f"HTTP {response.status_code}")

            # 400 com { valid: false } é uma resposta válida (cupom inválido/não encontrado)
            if not response.ok and result.get("valid") is None:
                raise Exception(result.get("message") or result.get("error") or f"HTTP {response.status_code}")
            
            # Normalizar resposta para o formato esperado
            return {
                "valid": result.get("valid", False),
                "discountCents": result.get("discountAmount", 0),
                "discountPercentage": result.get("coupon", {}).get("discountPercentage"),
                "finalAmountCents": result.get("finalAmount", amount_cents),
                "message": result.get("error") or result.get("message"),
            }
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na requisição: {str(e)}")
