#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar e testar o sistema de emails do MedLive
"""

import os
import sys
from pathlib import Path

def verificar_configuracao():
    """Verifica se o Resend está configurado corretamente"""
    print("🔍 Verificando configuração do Resend...")
    print("=" * 50)
    
    # Carregar variáveis de ambiente
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('RESEND_API_KEY')
    from_email = os.getenv('RESEND_FROM_EMAIL')
    from_name = os.getenv('RESEND_FROM_NAME')
    
    print(f"📧 RESEND_FROM_NAME: {from_name}")
    print(f"📧 RESEND_FROM_EMAIL: {from_email}")
    
    if not api_key or api_key == 'SUA_CHAVE_AQUI':
        print("❌ RESEND_API_KEY não configurada!")
        print()
        print("🚨 COMO CONFIGURAR:")
        print("1. Acesse: https://resend.com")
        print("2. Crie uma conta gratuita")
        print("3. Vá em 'API Keys' e crie uma nova chave")
        print("4. Edite o arquivo .env e substitua 'SUA_CHAVE_AQUI' pela sua chave")
        print("5. Configure um domínio verificado no Resend")
        print("6. Atualize RESEND_FROM_EMAIL com email do seu domínio")
        print()
        return False
    else:
        print(f"✅ RESEND_API_KEY: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else ''}")
        return True

def testar_envio():
    """Testa o envio de email"""
    if not verificar_configuracao():
        return False
    
    print("\n🧪 Testando envio de email...")
    print("=" * 30)
    
    try:
        from util.email_service import email_service
        
        # Email de teste
        email_teste = input("Digite seu email para teste: ").strip()
        if not email_teste:
            print("❌ Email não fornecido")
            return False
        
        print(f"📤 Enviando email de teste para: {email_teste}")
        
        sucesso = email_service.enviar_codigo_verificacao(
            para_email=email_teste,
            para_nome="Teste",
            codigo="123456"
        )
        
        if sucesso:
            print("✅ Email enviado com sucesso!")
            print("📬 Verifique sua caixa de entrada")
            return True
        else:
            print("❌ Falha no envio")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def configurar_resend():
    """Guia interativo para configurar o Resend"""
    print("🛠️  CONFIGURAÇÃO DO RESEND")
    print("=" * 40)
    
    print("📋 PASSO A PASSO:")
    print()
    print("1. 🌐 Acesse: https://resend.com")
    print("2. 📝 Crie uma conta gratuita")
    print("3. 🔑 Vá em 'API Keys' → 'Create API Key'")
    print("4. 📋 Copie a chave gerada")
    print("5. 🌍 Vá em 'Domains' → 'Add Domain'")
    print("6. ✅ Verifique seu domínio (DNS)")
    print()
    
    # Solicitar configurações
    print("💡 Digite suas configurações:")
    api_key = input("🔑 Cole sua API Key do Resend: ").strip()
    
    if not api_key:
        print("❌ API Key não fornecida")
        return False
    
    from_email = input("📧 Email remetente (ex: noreply@seudominio.com): ").strip()
    if not from_email:
        print("❌ Email não fornecido")
        return False
    
    from_name = input("👤 Nome do remetente [MedLive Sistema]: ").strip() or "MedLive Sistema"
    
    # Atualizar arquivo .env
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Substituir valores
        content = content.replace('RESEND_API_KEY=SUA_CHAVE_AQUI', f'RESEND_API_KEY={api_key}')
        content = content.replace('RESEND_FROM_EMAIL=noreply@seudominio.com', f'RESEND_FROM_EMAIL={from_email}')
        content = content.replace('RESEND_FROM_NAME=MedLive Sistema', f'RESEND_FROM_NAME={from_name}')
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Arquivo .env atualizado!")
        return True
    else:
        print("❌ Arquivo .env não encontrado")
        return False

def main():
    """Menu principal"""
    print("🏥 CONFIGURADOR DE EMAILS - MEDLIVE")
    print("=" * 60)
    
    while True:
        print("\n📋 OPÇÕES:")
        print("1. 🔍 Verificar configuração atual")
        print("2. 🛠️  Configurar Resend (interativo)")
        print("3. 🧪 Testar envio de email")
        print("4. 🚪 Sair")
        
        opcao = input("\n➤ Escolha uma opção (1-4): ").strip()
        
        if opcao == '1':
            verificar_configuracao()
            
        elif opcao == '2':
            if configurar_resend():
                print("\n✅ Configuração salva!")
                print("💡 Execute opção 3 para testar")
            
        elif opcao == '3':
            testar_envio()
            
        elif opcao == '4':
            print("👋 Até logo!")
            break
            
        else:
            print("❌ Opção inválida!")
        
        input("\n⏸️  Pressione Enter para continuar...")

if __name__ == "__main__":
    main()