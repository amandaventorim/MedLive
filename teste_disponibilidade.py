"""
Script de teste para verificar a integração de disponibilidade
"""
import requests
import json

def testar_api_disponibilidade():
    """Testa a API de horários disponíveis"""
    
    # URL base da aplicação
    base_url = "http://127.0.0.1:8000"
    
    # Parâmetros de teste
    id_medico = 1  # Assumindo que existe um médico com ID 1
    data = "2024-12-30"  # Data futura
    
    # URL da API
    url = f"{base_url}/api/horarios-disponiveis"
    params = {
        "idMedico": id_medico,
        "data": data
    }
    
    try:
        print(f"🔍 Testando API: {url}")
        print(f"📋 Parâmetros: {params}")
        print("-" * 50)
        
        # Fazer requisição
        response = requests.get(url, params=params)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Resposta recebida:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            
            if data.get("success"):
                horarios = data.get("horarios", [])
                print(f"⏰ Total de horários disponíveis: {len(horarios)}")
                if horarios:
                    print(f"🕐 Primeiros horários: {horarios[:5]}")
                else:
                    print(f"❓ Motivo: {data.get('message', 'Nenhum motivo especificado')}")
            else:
                print(f"❌ Falha na API: {data.get('message', 'Erro não especificado')}")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"💬 Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à aplicação.")
        print("💡 Certifique-se de que a aplicação está rodando em http://127.0.0.1:8000")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

def testar_diferentes_cenarios():
    """Testa diferentes cenários de disponibilidade"""
    
    base_url = "http://127.0.0.1:8000"
    url = f"{base_url}/api/horarios-disponiveis"
    
    cenarios = [
        {"idMedico": 1, "data": "2024-12-30", "desc": "Médico 1, data futura"},
        {"idMedico": 999, "data": "2024-12-30", "desc": "Médico inexistente"},
        {"idMedico": 1, "data": "2024-01-01", "desc": "Médico 1, data passada"},
        {"idMedico": 1, "data": "2024-12-29", "desc": "Médico 1, domingo"},
    ]
    
    for i, cenario in enumerate(cenarios, 1):
        print(f"\n📋 Cenário {i}: {cenario['desc']}")
        print("-" * 40)
        
        try:
            response = requests.get(url, params={
                "idMedico": cenario["idMedico"], 
                "data": cenario["data"]
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    horarios = data.get("horarios", [])
                    print(f"✅ {len(horarios)} horários disponíveis")
                    if horarios:
                        print(f"   Exemplos: {horarios[:3]}")
                else:
                    print(f"❌ {data.get('message', 'Erro não especificado')}")
            else:
                print(f"❌ Status {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print("🚀 Teste de Integração - Disponibilidade de Médicos")
    print("=" * 60)
    
    # Teste básico
    testar_api_disponibilidade()
    
    # Testes de diferentes cenários
    print(f"\n{'='*60}")
    print("🔬 Testando diferentes cenários...")
    testar_diferentes_cenarios()
    
    print(f"\n{'='*60}")
    print("✨ Teste concluído!")
    print("💡 Para testar o frontend, acesse: http://127.0.0.1:8000")