#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste manual de criação de notificação para agendamento existente
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def criar_notificacao_manual():
    """Cria notificação manualmente para o agendamento existente"""
    try:
        from data.repo.notificacao_repo import criar_notificacao_confirmacao_consulta
        
        # Dados do agendamento existente (ID 32)
        id_paciente = 17
        agendamento_id = 32
        data_consulta = "2025-12-01"
        horario_consulta = "08:00"
        
        # Buscar dados do médico
        from data.repo.medico_repo import obter_medico_por_id
        medico = obter_medico_por_id(7)  # ID do médico do agendamento
        nome_medico = medico.nome if medico else "Dr. Desconhecido"  # Nome do médico
        
        print("🔔 Criando notificação de confirmação...")
        print(f"   👤 Paciente ID: {id_paciente}")
        print(f"   📅 Agendamento ID: {agendamento_id}")
        print(f"   📅 Data: {data_consulta}")
        print(f"   🕐 Horário: {horario_consulta}")
        print(f"   👨‍⚕️ Médico: {nome_medico}")
        
        notificacao_id = criar_notificacao_confirmacao_consulta(
            id_paciente=id_paciente,
            nome_medico=nome_medico,
            data_consulta=data_consulta,
            horario=horario_consulta,
            agendamento_id=agendamento_id
        )
        
        if notificacao_id:
            print(f"✅ Notificação criada com sucesso! ID: {notificacao_id}")
            
            # Verificar a notificação criada
            from data.util import get_connection
            import sqlite3
            
            conn = get_connection()
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM notificacoes WHERE idNotificacao = ?", (notificacao_id,))
            notif = cursor.fetchone()
            
            if notif:
                print(f"📧 Detalhes da notificação:")
                print(f"   Tipo: {notif['tipo']}")
                print(f"   Título: {notif['titulo'] if 'titulo' in notif.keys() else 'N/A'}")
                print(f"   Mensagem: {notif['mensagem']}")
                print(f"   Criada: {notif['dataInclusao']}")
                if 'dataExpiracao' in notif.keys() and notif['dataExpiracao']:
                    print(f"   Expira: {notif['dataExpiracao']}")
                print(f"   Lida: {'Sim' if notif.get('lida', 0) else 'Não'}")
                print(f"   Ação Requerida: {'Sim' if notif.get('acaoRequerida', 0) else 'Não'}")
            
            conn.close()
            
            # Agora testar o WebSocket
            print("\n📡 Testando WebSocket (simulação)...")
            try:
                import asyncio
                from util.websocket_manager import manager
                
                async def test_websocket():
                    result = await manager.notify_appointment_confirmation_needed(
                        patient_id=str(id_paciente),
                        agendamento_id=agendamento_id,
                        data_consulta=data_consulta,
                        horario_consulta=horario_consulta
                    )
                    return result
                
                # Executar o teste async
                result = asyncio.run(test_websocket())
                if result:
                    print(f"✅ WebSocket testado com sucesso! Nova notificação ID: {result}")
                else:
                    print("❌ Erro no teste de WebSocket")
                
            except Exception as ws_e:
                print(f"❌ Erro ao testar WebSocket: {ws_e}")
            
        else:
            print("❌ Erro ao criar notificação")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

def listar_notificacoes_paciente():
    """Lista todas as notificações do paciente 17"""
    try:
        from data.repo.notificacao_repo import obter_notificacoes_por_usuario
        
        print("📋 Notificações existentes do paciente 17:")
        print("=" * 50)
        
        notificacoes = obter_notificacoes_por_usuario(17, "paciente")
        
        if notificacoes:
            for i, notif in enumerate(notificacoes, 1):
                print(f"{i}. ID: {notif[0]}")
                print(f"   Tipo: {notif[2]}")
                print(f"   Mensagem: {notif[3][:80]}...")
                print(f"   Criada: {notif[4]}")
                if len(notif) > 5 and notif[5]:
                    print(f"   Expira: {notif[5]}")
                print()
        else:
            print("❌ Nenhuma notificação encontrada")
            
    except Exception as e:
        print(f"❌ Erro ao listar notificações: {e}")

def main():
    print("🧪 Teste Manual de Notificações")
    print("=" * 50)
    print(f"📅 Data/hora atual: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Listar notificações existentes
    listar_notificacoes_paciente()
    print()
    
    # 2. Criar nova notificação
    criar_notificacao_manual()

if __name__ == "__main__":
    main()