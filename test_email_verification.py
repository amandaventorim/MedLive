import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def teste_completo():
    print("=" * 60)
    print("🧪 TESTE DE VERIFICAÇÃO DE EMAIL")
    print("=" * 60)
    
    email_teste = "teste@demo.com"
    
    # Teste 1: Gerar código
    print("\n1️⃣ Gerando código de verificação...")
    try:
        response = requests.post(
            f"{BASE_URL}/gerar_codigo_verificacao",
            json={"email": email_teste}
        )
        data = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {json.dumps(data, indent=2)}")
        
        if data.get("success"):
            codigo = data.get("demo_code")
            print(f"   ✅ Código gerado: {codigo}")
            
            # Teste 2: Verificar código correto
            print("\n2️⃣ Verificando código correto...")
            response = requests.post(
                f"{BASE_URL}/verificar_codigo",
                json={"email": email_teste, "codigo": codigo}
            )
            data = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Resposta: {json.dumps(data, indent=2)}")
            if data.get("success"):
                print("   ✅ Código verificado com sucesso!")
            else:
                print("   ❌ Erro ao verificar código")
        else:
            print("   ❌ Erro ao gerar código")
            
    except requests.exceptions.ConnectionError:
        print("   ❌ ERRO: Servidor não está rodando!")
        print("   Execute: python -m uvicorn main:app --reload")
        return
    except Exception as e:
        print(f"   ❌ Erro: {e}")
        return
    
    # Teste 3: Código incorreto
    print("\n3️⃣ Testando código incorreto...")
    response = requests.post(
        f"{BASE_URL}/gerar_codigo_verificacao",
        json={"email": "teste2@demo.com"}
    )
    response = requests.post(
        f"{BASE_URL}/verificar_codigo",
        json={"email": "teste2@demo.com", "codigo": "000000"}
    )
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {json.dumps(data, indent=2)}")
    if not data.get("success"):
        print("   ✅ Validação de código incorreto funcionando!")
    
    # Teste 4: Código inexistente
    print("\n4️⃣ Testando código inexistente...")
    response = requests.post(
        f"{BASE_URL}/verificar_codigo",
        json={"email": "naoexiste@demo.com", "codigo": "999999"}
    )
    data = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Resposta: {json.dumps(data, indent=2)}")
    if not data.get("success"):
        print("   ✅ Validação de código inexistente funcionando!")
    
    print("\n" + "=" * 60)
    print("✅ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 60)
    print("\n📋 Próximos passos:")
    print("   1. Acesse: http://127.0.0.1:8000/cadastro_paciente")
    print("   2. Preencha os dados e teste o fluxo completo")
    print("   3. Ou acesse: http://127.0.0.1:8000/test_verificacao")
    print("      para testes interativos\n")

if __name__ == "__main__":
    teste_completo()
