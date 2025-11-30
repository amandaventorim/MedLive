#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificação de agendamentos e notificações
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.util import get_connection
import sqlite3

def verificar_agendamentos_amanha():
    """Verifica agendamentos para amanhã"""
    try:
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Verificar agendamentos para 2025-12-01
        cursor.execute("SELECT * FROM agendamento WHERE dataAgendamento = ?", ("2025-12-01",))
        agendamentos = cursor.fetchall()
        
        print(f"🔍 Agendamentos para 2025-12-01:")
        print("=" * 50)
        
        if agendamentos:
            for row in agendamentos:
                print(f"📅 ID: {row['idAgendamento']}")
                print(f"   👤 Paciente ID: {row['idPaciente']}")
                print(f"   👨‍⚕️ Médico ID: {row['idMedico']}")
                print(f"   🕐 Horário: {row['horario']}")
                print(f"   📊 Status: {row['status']}")
                print(f"   📝 Queixa: {row.get('queixa', 'N/A')}")
                print(f"   📅 Criado em: {row.get('dataInclusao', 'N/A')}")
                print()
                
                # Verificar se há notificações para este agendamento
                verificar_notificacoes_agendamento(cursor, row['idAgendamento'], row['idPaciente'])
        else:
            print("❌ Nenhum agendamento encontrado para amanhã")
        
        conn.close()
        return agendamentos
        
    except Exception as e:
        print(f"❌ Erro ao verificar agendamentos: {e}")
        return []

def verificar_notificacoes_agendamento(cursor, agendamento_id, paciente_id):
    """Verifica notificações relacionadas ao agendamento"""
    try:
        # Buscar notificações que mencionam este agendamento
        cursor.execute("""
            SELECT * FROM notificacoes 
            WHERE idUsuario = ? 
            AND (dadosAdicionais LIKE ? OR dadosAdicionais LIKE ?)
            ORDER BY dataInclusao DESC
        """, (paciente_id, f'%"agendamento_id":{agendamento_id}%', f'%agendamento_id": {agendamento_id}%'))
        
        notificacoes = cursor.fetchall()
        
        print(f"🔔 Notificações para agendamento {agendamento_id}:")
        if notificacoes:
            for notif in notificacoes:
                print(f"   📧 ID: {notif['idNotificacao']}")
                print(f"   📝 Tipo: {notif['tipo']}")
                print(f"   💬 Mensagem: {notif['mensagem'][:100]}...")
                print(f"   📅 Criada: {notif['dataInclusao']}")
                print(f"   ⏰ Expira: {notif.get('dataExpiracao', 'N/A')}")
                print(f"   📊 Status: {notif.get('status', 'N/A')}")
                print()
        else:
            print("   ❌ Nenhuma notificação encontrada")
            
    except Exception as e:
        print(f"   ❌ Erro ao verificar notificações: {e}")

def verificar_servico_notificacoes():
    """Testa o serviço de notificações manualmente"""
    try:
        from notification_service import obter_consultas_proximas
        
        print(f"🧪 Testando serviço de notificações:")
        print("=" * 50)
        
        consultas = obter_consultas_proximas()
        
        if consultas:
            print(f"✅ Encontradas {len(consultas)} consultas para notificar:")
            for consulta in consultas:
                print(f"   📅 Paciente: {consulta[0]}, Médico: {consulta[1]}")
                print(f"   📅 Data: {consulta[2]}, Horário: {consulta[3]}")
                if len(consulta) > 4:
                    print(f"   📅 Agendamento ID: {consulta[4]}")
                print()
        else:
            print("❌ Nenhuma consulta encontrada para notificar")
            print("💡 Isso pode significar:")
            print("   - Não há consultas 24h no futuro")
            print("   - Já foram enviadas notificações")
            print("   - Horário não está na janela de ±30min")
        
    except Exception as e:
        print(f"❌ Erro ao testar serviço: {e}")

def main():
    print("🔍 Diagnóstico do Sistema de Notificações")
    print("=" * 60)
    print(f"📅 Data atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Verificar agendamentos para amanhã
    agendamentos = verificar_agendamentos_amanha()
    print()
    
    # 2. Testar o serviço de notificações
    verificar_servico_notificacoes()
    print()
    
    if agendamentos:
        print("💡 Sugestões:")
        print("   1. Execute o serviço de notificações manualmente:")
        print("      python notification_service.py --test")
        print("   2. Verifique se o horário está na janela de ±30min")
        print("   3. Confirme se não há notificações duplicadas")
    else:
        print("💡 Primeiro crie um agendamento para testar o sistema")

if __name__ == "__main__":
    main()