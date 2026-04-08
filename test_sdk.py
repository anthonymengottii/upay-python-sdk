"""
Script de teste do SDK Upay Python
"""

import os
import sys

# Adiciona o diretório atual ao path para importar o módulo
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from upay import UpayClient

# API Key fornecida pelo usuário
API_KEY = "upay_23e64c303a614152f6fc0ef2a52e7a79d081d19fed1b4f50cf87444c994485fd"

# Base URL - usar localhost para desenvolvimento
BASE_URL = os.getenv("UPAY_BASE_URL", "http://localhost:3001")

def test_sdk():
    """Testa o SDK Upay Python"""
    print("Testando SDK Upay Python...\n")
    print(f"Usando base URL: {BASE_URL}\n")
    
    # Inicializar o cliente
    upay = UpayClient(
        api_key=API_KEY,
        base_url=BASE_URL,
        version="v1"
    )
    
    try:
        # Teste 1: Listar Payment Links
        print("Teste 1: Listar Payment Links...")
        try:
            links = upay.payment_links.list(page=1, limit=5)
            print(f"[OK] Sucesso! Encontrados {links['pagination'].get('total', len(links['data']))} links")
            if links['data']:
                first_link = links['data'][0]
                print(f"   Primeiro link: {first_link.get('title')} ({first_link.get('slug')})")
                print(f"   URL: {upay.payment_links.get_checkout_url(first_link['slug'])}")
        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            import traceback
            traceback.print_exc()
        
        # Teste 2: Listar Transações
        print("\nTeste 2: Listar Transacoes...")
        try:
            transactions = upay.transactions.list(page=1, limit=5)
            total = transactions['pagination'].get('total', len(transactions['data']))
            print(f"[OK] Sucesso! Encontradas {total} transacoes")
            if transactions['data']:
                tx = transactions['data'][0]
                amount = tx.get('amountCents', 0) / 100
                print(f"   Primeira transacao: {tx.get('product')} - R$ {amount:.2f} - {tx.get('status')}")
        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            import traceback
            traceback.print_exc()
        
        # Teste 3: Listar Produtos
        print("\nTeste 3: Listar Produtos...")
        try:
            products = upay.products.list(page=1, limit=5)
            total = products['pagination'].get('total', len(products['data']))
            print(f"[OK] Sucesso! Encontrados {total} produtos")
            if products['data']:
                product = products['data'][0]
                price = product.get('price', 0) / 100
                print(f"   Primeiro produto: {product.get('name')} - R$ {price:.2f}")
        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            import traceback
            traceback.print_exc()
        
        # Teste 4: Listar Clientes
        print("\nTeste 4: Listar Clientes...")
        try:
            clients = upay.clients.list(page=1, limit=5)
            total = clients['pagination'].get('total', len(clients['data']))
            print(f"[OK] Sucesso! Encontrados {total} clientes")
            if clients['data']:
                client = clients['data'][0]
                print(f"   Primeiro cliente: {client.get('name')} - {client.get('email')}")
        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            import traceback
            traceback.print_exc()
        
        # Teste 5: Validar Cupom
        print("\nTeste 5: Validar Cupom...")
        try:
            validation = upay.coupons.validate(
                code="CUPOMTESTE",
                amount_cents=10000
            )
            if validation['valid']:
                print(f"[OK] Cupom valido!")
                print(f"   Desconto: R$ {validation['discountCents'] / 100:.2f}")
                print(f"   Valor final: R$ {validation['finalAmountCents'] / 100:.2f}")
            else:
                print(f"[AVISO] Cupom invalido: {validation.get('message', 'Cupom nao encontrado')}")
        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            import traceback
            traceback.print_exc()
        
        # Teste 6: Criar e Deletar Payment Link
        print("\nTeste 6: Criar e Deletar Payment Link...")
        try:
            from datetime import datetime
            test_link = upay.payment_links.create({
                "title": f"Teste SDK Python - {datetime.now().isoformat()}",
                "description": "Link criado pelo teste do SDK Python",
                "amount": 2500,  # R$ 25,00
                "status": "INACTIVE"
            })
            print(f"[OK] Link criado com sucesso!")
            print(f"   ID: {test_link.get('id')}")
            print(f"   Slug: {test_link.get('slug')}")
            print(f"   URL: {upay.payment_links.get_checkout_url(test_link['slug'])}")
            
            # Deletar o link de teste
            try:
                upay.payment_links.delete(test_link['id'])
                print(f"   [OK] Link de teste deletado")
            except Exception as delete_error:
                print(f"   [AVISO] Nao foi possivel deletar: {delete_error}")
        except Exception as e:
            print(f"[ERRO] Erro: {e}")
            import traceback
            traceback.print_exc()
        
        print("\n[OK] Todos os testes concluidos!")
        
    except Exception as e:
        print(f"\n[ERRO] Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sdk()
