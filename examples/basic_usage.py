"""
Exemplo básico de uso do SDK Upay Python
"""

from upay import UpayClient

# Inicializar o cliente
upay = UpayClient(
    api_key="sua_api_key_aqui",
    base_url="http://localhost:3001"  # Para desenvolvimento local
)

def exemplo_payment_links():
    """Exemplo de uso de Payment Links"""
    print("=== Exemplo: Payment Links ===\n")
    
    # Criar um link de pagamento
    print("1. Criando link de pagamento...")
    payment_link = upay.payment_links.create({
        "title": "Produto Premium",
        "amount": 10000,  # R$ 100,00
        "description": "Descrição do produto",
        "status": "ACTIVE"
    })
    print(f"   Link criado: {payment_link.get('id')}")
    print(f"   Slug: {payment_link.get('slug')}")
    print(f"   URL: {upay.payment_links.get_checkout_url(payment_link['slug'])}\n")
    
    # Listar links
    print("2. Listando links de pagamento...")
    links = upay.payment_links.list(page=1, limit=5)
    print(f"   Total de links: {links['pagination'].get('total', 0)}")
    if links['data']:
        print(f"   Primeiro link: {links['data'][0].get('title')}\n")
    
    # Deletar o link de teste
    print("3. Deletando link de teste...")
    try:
        upay.payment_links.delete(payment_link['id'])
        print("   Link deletado com sucesso\n")
    except Exception as e:
        print(f"   Erro ao deletar: {e}\n")


def exemplo_transacoes():
    """Exemplo de uso de Transações"""
    print("=== Exemplo: Transações ===\n")
    
    # Listar transações
    print("1. Listando transações...")
    transactions = upay.transactions.list(page=1, limit=5)
    print(f"   Total de transações: {transactions['pagination'].get('total', 0)}")
    if transactions['data']:
        tx = transactions['data'][0]
        print(f"   Primeira transação: {tx.get('product')} - R$ {tx.get('amountCents', 0) / 100:.2f}\n")


def exemplo_produtos():
    """Exemplo de uso de Produtos"""
    print("=== Exemplo: Produtos ===\n")
    
    # Listar produtos
    print("1. Listando produtos...")
    products = upay.products.list(page=1, limit=5)
    print(f"   Total de produtos: {products['pagination'].get('total', 0)}")
    if products['data']:
        product = products['data'][0]
        print(f"   Primeiro produto: {product.get('name')} - R$ {product.get('price', 0) / 100:.2f}\n")


def exemplo_clientes():
    """Exemplo de uso de Clientes"""
    print("=== Exemplo: Clientes ===\n")
    
    # Listar clientes
    print("1. Listando clientes...")
    clients = upay.clients.list(page=1, limit=5)
    print(f"   Total de clientes: {clients['pagination'].get('total', 0)}")
    if clients['data']:
        client = clients['data'][0]
        print(f"   Primeiro cliente: {client.get('name')} - {client.get('email')}\n")


def exemplo_cupons():
    """Exemplo de uso de Cupons"""
    print("=== Exemplo: Cupons ===\n")
    
    # Validar cupom
    print("1. Validando cupom...")
    try:
        validation = upay.coupons.validate(
            code="CUPOMTESTE",
            amount_cents=10000
        )
        if validation['valid']:
            print(f"   Cupom válido!")
            print(f"   Desconto: R$ {validation['discountCents'] / 100:.2f}")
            print(f"   Valor final: R$ {validation['finalAmountCents'] / 100:.2f}\n")
        else:
            print(f"   Cupom inválido: {validation.get('message')}\n")
    except Exception as e:
        print(f"   Erro: {e}\n")


if __name__ == "__main__":
    print("🧪 Testando SDK Upay Python\n")
    
    try:
        exemplo_payment_links()
        exemplo_transacoes()
        exemplo_produtos()
        exemplo_clientes()
        exemplo_cupons()
        
        print("✅ Todos os exemplos executados com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
