# Upay Python SDK

SDK oficial da Upay para Python - Integração fácil com a API de pagamentos.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 📦 Instalação

```bash
pip install upay-python
```

## 🚀 Início Rápido

```python
from upay import UpayClient

# Inicializar o cliente
upay = UpayClient(
    api_key="sua_api_key_aqui"
)

# Criar um link de pagamento
payment_link = upay.payment_links.create({
    "title": "Produto Premium",
    "amount": 10000,  # R$ 100,00 em centavos
    "description": "Descrição do produto"
})

print(f"Link criado: {upay.payment_links.get_checkout_url(payment_link['slug'])}")

# Listar transações
transactions = upay.transactions.list(page=1, limit=10)
print(f"Total de transações: {transactions['pagination']['total']}")
```

## 📚 Recursos Disponíveis

### Payment Links

```python
# Criar link
link = upay.payment_links.create({
    "title": "Produto",
    "amount": 10000,
    "status": "ACTIVE"
})

# Listar links
links = upay.payment_links.list(page=1, limit=10)

# Obter por ID
link = upay.payment_links.get(link_id)

# Obter por slug
link = upay.payment_links.get_by_slug("meu-link")

# Atualizar
upay.payment_links.update(link_id, {"status": "INACTIVE"})

# Deletar
upay.payment_links.delete(link_id)

# Obter URL do checkout
url = upay.payment_links.get_checkout_url(link["slug"])
```

### Transações

```python
# Criar transação
transaction = upay.transactions.create({
    "product": "Produto Teste",
    "amountCents": 10000,
    "paymentMethod": "PIX"
})

# Listar transações
transactions = upay.transactions.list(
    page=1,
    limit=10,
    status="PAID"
)

# Obter transação
transaction = upay.transactions.get(transaction_id)

# Processar pagamento
upay.transactions.process(transaction_id, {
    "cardData": {...},
    "installments": 3
})

# Capturar transação
upay.transactions.capture(transaction_id)

# Cancelar transação
upay.transactions.cancel(transaction_id)

# Estornar transação
upay.transactions.refund(transaction_id, amount_cents=5000)
```

### Produtos

```python
# Criar produto
product = upay.products.create({
    "name": "Produto Teste",
    "price": 10000,
    "description": "Descrição"
})

# Listar produtos
products = upay.products.list(page=1, limit=10)

# Obter produto
product = upay.products.get(product_id)

# Atualizar produto
upay.products.update(product_id, {"price": 15000})

# Deletar produto
upay.products.delete(product_id)
```

### Clientes

```python
# Criar cliente
client = upay.clients.create({
    "name": "João Silva",
    "email": "joao@example.com",
    "document": "12345678900"
})

# Listar clientes
clients = upay.clients.list(page=1, limit=10)

# Obter cliente
client = upay.clients.get(client_id)

# Atualizar cliente
upay.clients.update(client_id, {"email": "novo@example.com"})
```

### Cupons

```python
# Validar cupom (endpoint público)
validation = upay.coupons.validate(
    code="CUPOM10",
    amount_cents=10000,
    product_ids=["produto-id-1", "produto-id-2"]
)

if validation["valid"]:
    print(f"Desconto: R$ {validation['discountCents'] / 100:.2f}")
    print(f"Valor final: R$ {validation['finalAmountCents'] / 100:.2f}")
```

### Webhooks

```python
from flask import Flask, request
from upay import UpayClient

app = Flask(__name__)
upay = UpayClient(api_key="sua_api_key")

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.data
    signature = request.headers.get('X-Upay-Signature')
    secret = "seu_webhook_secret"
    
    if upay.verify_webhook_signature(payload, signature, secret):
        # Processar webhook
        data = request.json
        print(f"Evento: {data.get('type')}")
        return {"status": "ok"}, 200
    else:
        return {"error": "Invalid signature"}, 401
```

## ⚙️ Configuração

```python
from upay import UpayClient

upay = UpayClient(
    api_key="sua_api_key",
    base_url="https://upay-sistema-api.onrender.com",  # Opcional
    version="v1",  # Opcional
    timeout=30  # Opcional, em segundos
)
```

## 🔑 Obter API Key

Para usar o SDK, você precisa de uma API Key:

1. Acesse o [Dashboard Upay](https://app.upaybr.com)
2. Vá em **Configurações** > **API Keys**
3. Crie uma nova API Key
4. Copie e use no seu código

## 🛠️ Tratamento de Erros

```python
from upay import (
    UpayClient,
    UpayError,
    UpayAuthenticationError,
    UpayValidationError,
    UpayNotFoundError,
    UpayRateLimitError,
)

try:
    link = upay.payment_links.create({"title": "Teste"})
except UpayValidationError as e:
    print(f"Erro de validação: {e.message}")
    print(f"Detalhes: {e.details}")
except UpayAuthenticationError as e:
    print(f"Erro de autenticação: {e.message}")
except UpayError as e:
    print(f"Erro: {e.message} (Código: {e.code})")
```

## 📝 Exemplos Completos

Veja a pasta `examples/` para exemplos mais detalhados.

## 🔗 Links Úteis

- [Documentação da API](https://docs.upaybr.com)
- [Dashboard](https://app.upaybr.com)
- [Suporte](mailto:suporte@upaybr.com)
- [Repositório](https://github.com/anthonymengottii/upay-python-sdk)
- [Issues](https://github.com/anthonymengottii/upay-python-sdk/issues)

## 📄 Licença

MIT

## 🤝 Contribuindo

Contribuições são bem-vindas! Veja as [issues abertas](https://github.com/anthonymengottii/upay-python-sdk/issues) para sugestões.
