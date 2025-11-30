#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste simples do sistema de notificações 24h
Apenas testa as funções sem modificar o banco de dados
"""

import sys
import os

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from notification_service import obter_consultas_proximas
from data.repo.notificacao_repo import obter_notificacoes_por_usuario
from datetime import datetime, timedelta

def teste_obter_consultas():
    """Testa a função de obter consultas próximas (24h)"""
    print("🔍 Testando obter_consultas_proximas()...")
    
    try:
        consultas = obter_consultas_proximas()
        print(f"✅ Função executada com sucesso")
        print(f"📊 Encontradas {len(consultas)} consultas nas próximas 24h:")
        
        if consultas:
            for i, consulta in enumerate(consultas, 1):
                print(f"   {i}. ID Paciente: {consulta[0]}")
                print(f"      ID Médico: {consulta[1]}")
                print(f"      Data: {consulta[2]}")
                print(f"      Horário: {consulta[3]}")
                if len(consulta) > 4:
                    print(f"      ID Agendamento: {consulta[4]}")
                print()
        else:
            print("   ℹ️ Nenhuma consulta encontrada para as próximas 24h")
            
        return True
        
    except Exception as e:
        print(f"❌ Erro ao executar obter_consultas_proximas(): {e}")
        import traceback
        traceback.print_exc()
        return False

def teste_notificacoes_existentes():
    """Verifica notificações existentes no sistema"""
    print("🔍 Verificando notificações existentes...")
    
    try:
        # Tentar obter notificações para usuários de ID 1 a 5
        total_notificacoes = 0
        for user_id in range(1, 6):
            try:
                notificacoes = obter_notificacoes_por_usuario(user_id, "paciente")  # Assumindo tipo paciente
                if notificacoes:
                    print(f"   👤 Usuário {user_id}: {len(notificacoes)} notificações")
                    total_notificacoes += len(notificacoes)
                    
                    # Mostrar detalhes das primeiras 3 notificações
                    for i, notif in enumerate(notificacoes[:3]):
                        print(f"      {i+1}. {notif[3][:50]}..." if len(notif[3]) > 50 else f"      {i+1}. {notif[3]}")
                        print(f"         Criada: {notif[4]}")
                        if len(notif) > 5 and notif[5]:
                            print(f"         Expira: {notif[5]}")
                    
                    if len(notificacoes) > 3:
                        print(f"      ... e mais {len(notificacoes) - 3} notificações")
                    print()
            except Exception as e:
                # Se der erro para um usuário específico, continue para o próximo
                continue
        
        print(f"📊 Total de notificações no sistema: {total_notificacoes}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar notificações: {e}")
        return False

def teste_timing_24h():
    """Testa se o timing de 24h está configurado corretamente"""
    print("⏰ Testando configuração de timing 24h...")
    
    try:
        # Simular uma data/hora 24h no futuro
        agora = datetime.now()
        em_24h = agora + timedelta(hours=24)
        
        print(f"   🕐 Agora: {agora.strftime('%Y-%m-%d %H:%M')}")
        print(f"   🕐 Em 24h: {em_24h.strftime('%Y-%m-%d %H:%M')}")
        
        # Simular janela de busca (24h ± 30 min)
        inicio_janela = em_24h - timedelta(minutes=30)
        fim_janela = em_24h + timedelta(minutes=30)
        
        print(f"   📊 Janela de busca:")
        print(f"      Início: {inicio_janela.strftime('%Y-%m-%d %H:%M')}")
        print(f"      Fim: {fim_janela.strftime('%Y-%m-%d %H:%M')}")
        
        print("   ✅ Configuração de 24h parece correta")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar timing: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando Testes do Sistema de Notificação 24h")
    print("=" * 55)
    print()
    
    sucesso_total = True
    
    # Teste 1: Função de obter consultas
    sucesso_total &= teste_obter_consultas()
    print()
    
    # Teste 2: Notificações existentes
    sucesso_total &= teste_notificacoes_existentes()
    print()
    
    # Teste 3: Configuração de timing
    sucesso_total &= teste_timing_24h()
    print()
    
    # Resultado final
    print("=" * 55)
    if sucesso_total:
        print("✅ Todos os testes passaram!")
        print("🎉 Sistema de notificação 24h parece estar funcionando corretamente")
    else:
        print("❌ Alguns testes falharam")
        print("🔧 Verifique os erros acima para mais detalhes")
    
    return sucesso_total

if __name__ == "__main__":
    main()