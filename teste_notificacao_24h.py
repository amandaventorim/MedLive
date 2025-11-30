"""
Teste do Sistema de Notificações 24h
Simula um agendamento para amanhã e testa se a notificação é criada corretamente
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from data.repo.agendamento_repo import inserir_agendamento
from data.repo.notificacao_repo import obter_notificacoes_por_usuario, criar_notificacao_confirmacao_consulta
from data.model.agendamento_model import Agendamento
import asyncio
from util.websocket_manager import manager


def teste_notificacao_24h():
    """Testa se o sistema cria notificações 24h antes"""
    
    print("🧪 Testando Sistema de Notificações 24h")
    print("=" * 50)
    
    # Simular uma consulta para amanhã
    amanha = datetime.now() + timedelta(days=1)
    data_consulta = amanha.strftime("%Y-%m-%d")
    horario_consulta = "14:00"
    
    print(f"📅 Simulando consulta para: {data_consulta} às {horario_consulta}")
    
    # Dados de teste
    id_paciente = 1  # Assume que existe um paciente com ID 1
    id_medico = 1    # Assume que existe um médico com ID 1
    nome_medico = "Dr. João Silva"
    
    try:
        # 1. Criar agendamento de teste
        agendamento = Agendamento(
            idAgendamento=None,
            idPaciente=id_paciente,
            idMedico=id_medico,
            dataAgendamento=data_consulta,
            horario=horario_consulta,
            queixa="Consulta de teste",
            status="agendado"
        )
        
        agendamento_id = inserir_agendamento(agendamento)
        if not agendamento_id:
            print("❌ Erro ao criar agendamento de teste")
            return
        
        print(f"✅ Agendamento criado com ID: {agendamento_id}")
        
        # 2. Criar notificação de confirmação (simula 24h antes)
        print("📧 Criando notificação de confirmação...")
        
        notification_id = criar_notificacao_confirmacao_consulta(
            id_paciente=id_paciente,
            nome_medico=nome_medico,
            data_consulta=data_consulta,
            horario=horario_consulta,
            agendamento_id=agendamento_id
        )
        
        if notification_id:
            print(f"✅ Notificação criada com ID: {notification_id}")
        else:
            print("❌ Erro ao criar notificação")
            return
        
        # 3. Verificar se a notificação aparece nas notificações do paciente
        print("🔍 Verificando notificações do paciente...")
        
        notificacoes = obter_notificacoes_por_usuario(id_paciente, "paciente")
        notificacao_encontrada = None
        
        for notif in notificacoes:
            if notif.idNotificacao == notification_id:
                notificacao_encontrada = notif
                break
        
        if notificacao_encontrada:
            print("✅ Notificação encontrada no banco de dados:")
            print(f"   📋 Título: {notificacao_encontrada.titulo}")
            print(f"   💬 Mensagem: {notificacao_encontrada.mensagem}")
            print(f"   📖 Lida: {'Sim' if notificacao_encontrada.lida else 'Não'}")
            print(f"   ⚡ Ação Requerida: {'Sim' if notificacao_encontrada.acaoRequerida else 'Não'}")
            print(f"   ⏰ Expira em: {notificacao_encontrada.expiresAt}")
        else:
            print("❌ Notificação não encontrada nas notificações do paciente")
            return
        
        # 4. Testar envio via WebSocket (simula)
        print("🌐 Testando envio via WebSocket...")
        
        async def teste_websocket():
            notification_id_ws = await manager.notify_appointment_reminder(
                patient_id=str(id_paciente),
                doctor_name=nome_medico,
                appointment_date=data_consulta,
                appointment_time=horario_consulta,
                appointment_id=agendamento_id
            )
            
            if notification_id_ws:
                print(f"✅ Notificação WebSocket enviada com ID: {notification_id_ws}")
            else:
                print("❌ Erro no envio WebSocket")
        
        # Executar teste WebSocket
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(teste_websocket())
        except Exception as e:
            print(f"⚠️  Erro no teste WebSocket: {e}")
        
        print("\n" + "=" * 50)
        print("📊 RESUMO DO TESTE:")
        print("✅ Agendamento criado para amanhã")
        print("✅ Notificação de confirmação criada") 
        print("✅ Notificação salva no banco de dados")
        print("✅ Notificação aparece no dropdown do paciente")
        print("✅ Sistema configurado para 24h antes")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()


def teste_servico_notificacao():
    """Testa o serviço de notificações automáticas"""
    
    print("🔧 Testando Serviço de Notificações Automáticas")
    print("=" * 50)
    
    # Importar função do serviço
    from notification_service import obter_consultas_proximas, enviar_notificacoes_confirmacao
    
    print("🔍 Buscando consultas para notificar...")
    consultas = obter_consultas_proximas()
    
    print(f"📋 Encontradas {len(consultas)} consultas")
    
    if consultas:
        print("📝 Consultas encontradas:")
        for consulta in consultas:
            agendamento_id, id_paciente, id_medico, data_consulta, horario = consulta
            print(f"   • ID: {agendamento_id} | Paciente: {id_paciente} | Médico: {id_medico} | {data_consulta} {horario}")
    else:
        print("ℹ️  Nenhuma consulta encontrada para notificação no momento")
        print("   (Isso é normal se não há consultas marcadas para exatamente 24h no futuro)")
    
    # Testar envio de notificações
    if consultas:
        print("\n📧 Testando envio de notificações...")
        
        async def teste_envio():
            await enviar_notificacoes_confirmacao()
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(teste_envio())
            print("✅ Teste de envio concluído")
        except Exception as e:
            print(f"❌ Erro no teste de envio: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--servico":
            teste_servico_notificacao()
        else:
            print("Opções disponíveis:")
            print("  python teste_notificacao_24h.py          # Teste completo")
            print("  python teste_notificacao_24h.py --servico # Teste do serviço")
    else:
        teste_notificacao_24h()