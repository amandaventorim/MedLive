import requests
import json

def testar_api_urias():
    """Testa a API de horários para o médico Urias"""
    
    base_url = "http://127.0.0.1:8000"
    url = f"{base_url}/api/horarios-disponiveis"
    
    # Testes para diferentes dias da semana
    testes = [
        {"data": "2025-10-06", "desc": "Segunda-feira"},  # 06/10/2025 é segunda
        {"data": "2025-10-07", "desc": "Terça-feira"},   # 07/10/2025 é terça  
        {"data": "2025-10-08", "desc": "Quarta-feira"},  # 08/10/2025 é quarta
        {"data": "2025-10-09", "desc": "Quinta-feira"},  # 09/10/2025 é quinta
        {"data": "2025-10-10", "desc": "Sexta-feira"},   # 10/10/2025 é sexta
        {"data": "2025-10-11", "desc": "Sábado"},        # 11/10/2025 é sábado
        {"data": "2025-10-12", "desc": "Domingo"},       # 12/10/2025 é domingo
    ]
    
    print("🚀 TESTE DA API DE HORÁRIOS PARA URIAS (ID: 3)")
    print("=" * 60)
    
    for teste in testes:
        print(f"\n📅 Testando {teste['desc']} ({teste['data']})")
        print("-" * 40)
        
        try:
            response = requests.get(url, params={
                "idMedico": 3,  # ID do Urias
                "data": teste["data"]
            })
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    horarios = data.get("horarios", [])
                    if horarios:
                        print(f"✅ {len(horarios)} horários disponíveis:")
                        # Mostrar os primeiros 6 horários
                        for i, horario in enumerate(horarios[:6]):
                            print(f"   {horario}")
                        if len(horarios) > 6:
                            print(f"   ... e mais {len(horarios) - 6} horários")
                    else:
                        print("❌ Nenhum horário disponível")
                else:
                    print(f"❌ Erro: {data.get('message', 'Erro desconhecido')}")
            else:
                print(f"❌ Status HTTP {response.status_code}: {response.text}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Erro: Aplicação não está rodando ou não conseguiu conectar")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    print(f"\n{'='*60}")
    print("✨ Teste concluído!")

if __name__ == "__main__":
    testar_api_urias()