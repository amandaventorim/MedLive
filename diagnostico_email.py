#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Diagnóstico rápido do problema de email
"""

import os
import sys
from dotenv import load_dotenv

def diagnosticar():
    print("\n🔍 DIAGNÓSTICO RÁPIDO DO EMAIL")
    print("=" * 40)
    
    # Carregar .env
    load_dotenv()
    
    api_key = os.getenv('RESEND_API_KEY')
    from_email = os.getenv('RESEND_FROM_EMAIL')
    from_name = os.getenv('RESEND_FROM_NAME')
    
    print(f"📧 RESEND_FROM_EMAIL: {from_email}")
    print(f"👤 RESEND_FROM_NAME: {from_name}")
    
    if not api_key or api_key == 'SUA_CHAVE_AQUI':
        print("❌ PROBLEMA ENCONTRADO: API Key não configurada!")
        print()
        print("🔧 SOLUÇÃO RÁPIDA:")
        print("1. Você precisa configurar sua chave do Resend")
        print("2. Acesse: https://resend.com")
        print("3. Crie conta gratuita e obtenha API Key")
        print("4. Edite o arquivo .env:")
        print("   - Substitua 'SUA_CHAVE_AQUI' pela sua chave real")
        print("   - Configure um email de domínio verificado")
        print()
        print("💡 OU use o comando: python configurar_email.py")
        return False
    else:
        print(f"✅ API Key: {api_key[:10]}...{api_key[-4:]}")
        
        # Testar envio
        print("\n🧪 Testando envio...")
        try:
            from util.email_service import email_service
            result = email_service.enviar_codigo_verificacao(
                'teste@exemplo.com', 
                'Usuario Teste', 
                'ABC123'
            )
            print(f"Resultado: {'✅ Sucesso' if result else '❌ Falha'}")
            return result
        except Exception as e:
            print(f"❌ Erro: {e}")
            return False

if __name__ == "__main__":
    diagnosticar()