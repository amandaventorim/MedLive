#!/usr/bin/env python3
"""
Teste simulando requisição POST com dados inválidos para verificar resposta
"""

import requests
import json

def test_form_errors():
    print("=== TESTANDO ERROS NO FORMULÁRIO WEB ===\n")
    
    # URL da aplicação
    url = "http://127.0.0.1:8000/paciente/cadastro"
    
    # Dados inválidos para teste
    dados_invalidos = {
        'nome': '',  # Nome vazio
        'cpf': '111.111.111-11',  # CPF inválido
        'email': 'email_invalido',  # Email sem @
        'senha': '123',  # Senha muito curta
        'genero': 'masculino',
        'dataNascimento': 'data_invalida',  # Data inválida
        'endereco': 'Rua Teste, 123',
        'convenio': 'Particular'
    }
    
    print("1. Enviando dados inválidos para o formulário...")
    print(f"Dados: {json.dumps(dados_invalidos, indent=2)}")
    
    try:
        # Fazer requisição POST
        response = requests.post(url, data=dados_invalidos)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Formulário retornou status 200 (provavelmente com erros)")
            
            # Verificar se há indicadores de erro na resposta
            content = response.text
            
            if 'is-invalid' in content:
                print("✅ Encontrado classe 'is-invalid' na resposta")
            else:
                print("❌ NÃO encontrado classe 'is-invalid' na resposta")
                
            if 'invalid-feedback' in content:
                print("✅ Encontrado classe 'invalid-feedback' na resposta")
            else:
                print("❌ NÃO encontrado classe 'invalid-feedback' na resposta")
                
            if 'alert-danger' in content:
                print("✅ Encontrado alerta de erro geral na resposta")
            else:
                print("❌ NÃO encontrado alerta de erro geral na resposta")
                
        else:
            print(f"❌ Erro inesperado: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - certifique-se de que a aplicação está rodando")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_form_errors()