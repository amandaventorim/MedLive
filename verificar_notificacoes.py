#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verificação simples das notificações criadas
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_notificacoes():
    try:
        from data.util import get_connection
        import sqlite3
        
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Buscar todas as notificações do paciente 17
        cursor.execute("SELECT * FROM notificacoes WHERE idUsuario = 17 ORDER BY dataInclusao DESC")
        notificacoes = cursor.fetchall()
        
        print("🔔 Notificações do Paciente 17:")
        print("=" * 50)
        
        if notificacoes:
            for i, notif in enumerate(notificacoes, 1):
                print(f"{i}. ID: {notif['idNotificacao']}")
                print(f"   Tipo: {notif['tipo']}")
                print(f"   Mensagem: {notif['mensagem'][:100]}...")
                print(f"   Criada: {notif['dataInclusao']}")
                print(f"   Lida: {'Sim' if notif['lida'] else 'Não'}")
                
                # Verificar dados adicionais
                if notif['dadosAdicionais']:
                    import json
                    dados = json.loads(notif['dadosAdicionais'])
                    if 'agendamento_id' in dados:
                        print(f"   Agendamento ID: {dados['agendamento_id']}")
                print()
        else:
            print("❌ Nenhuma notificação encontrada")
        
        conn.close()
        
        # Verificar o agendamento também
        print("📅 Agendamento relacionado:")
        print("=" * 30)
        
        conn = get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agendamento WHERE idAgendamento = 32")
        agendamento = cursor.fetchone()
        
        if agendamento:
            print(f"✅ Agendamento ID 32:")
            print(f"   Paciente: {agendamento['idPaciente']}")
            print(f"   Médico: {agendamento['idMedico']}")
            print(f"   Data: {agendamento['dataAgendamento']}")
            print(f"   Horário: {agendamento['horario']}")
            print(f"   Status: {agendamento['status']}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    verificar_notificacoes()