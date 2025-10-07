#!/usr/bin/env python3
"""
Teste do fluxo de login para médico
"""
import requests

def testar_login_medico():
    # Criar sessão para manter cookies
    session = requests.Session()
    
    print("Testando login do médico...")
    
    try:
        # 1. Obter página de login
        print("1. Acessando página de login...")
        login_page = session.get("http://127.0.0.1:8000/login")
        print(f"   Status: {login_page.status_code}")
        
        # 2. Fazer login com médico
        print("2. Fazendo login como médico...")
        login_data = {
            "email": "dr.carlos@email.com",
            "senha": "senha123"
        }
        
        login_response = session.post(
            "http://127.0.0.1:8000/login", 
            data=login_data,
            allow_redirects=False
        )
        print(f"   Status: {login_response.status_code}")
        print(f"   Location: {login_response.headers.get('location', 'Nenhum')}")
        
        # 3. Se redirecionou, seguir o redirecionamento
        if login_response.status_code == 303:
            redirect_url = login_response.headers.get('location')
            if redirect_url:
                print(f"3. Seguindo redirecionamento para: {redirect_url}")
                
                # Construir URL completa se necessário
                if redirect_url.startswith('/'):
                    full_url = f"http://127.0.0.1:8000{redirect_url}"
                else:
                    full_url = redirect_url
                    
                dashboard_response = session.get(full_url)
                print(f"   Status: {dashboard_response.status_code}")
                
                if dashboard_response.status_code == 404:
                    print("   ERRO: Página não encontrada!")
                elif dashboard_response.status_code == 200:
                    print("   SUCESSO: Dashboard médico carregado!")
                else:
                    print(f"   Status inesperado: {dashboard_response.status_code}")
        else:
            print("   ERRO: Login não redirecionou corretamente")
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    testar_login_medico()