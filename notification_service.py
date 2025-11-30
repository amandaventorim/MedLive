"""
Sistema de Notificações Automáticas - MedLive
Executa verificações periódicas para enviar notificações de confirmação
24 horas antes das consultas agendadas.

Este script deve ser executado como um serviço em background.
"""

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from data.repo.agendamento_repo import obter_todos_agendamentos
from data.repo.medico_repo import obter_medico_por_id  
from data.repo.paciente_repo import obter_paciente_por_id
from util.websocket_manager import manager
import sqlite3


def obter_consultas_proximas():
    """
    Obtém consultas que acontecerão em 24 horas e ainda não foram notificadas
    """
    try:
        from data.util import get_connection
        
        # Data/hora atual + 24 horas (com tolerância de ±30 minutos)
        agora = datetime.now()
        vinte_quatro_horas_depois = agora + timedelta(hours=24)
        
        # Intervalo de busca: 23h30min a 24h30min no futuro
        inicio_intervalo = agora + timedelta(hours=23, minutes=30)
        fim_intervalo = agora + timedelta(hours=24, minutes=30)
        
        data_busca = vinte_quatro_horas_depois.strftime("%Y-%m-%d")
        hora_inicio = inicio_intervalo.strftime("%H:%M")
        hora_fim = fim_intervalo.strftime("%H:%M")
        
        print(f"[{agora.strftime('%H:%M:%S')}] Buscando consultas entre {hora_inicio} e {hora_fim} do dia {data_busca}")
        
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Buscar agendamentos que:
            # 1. São de amanhã (24h no futuro)
            # 2. Estão no intervalo de 24 horas
            # 3. Têm status 'agendado'
            # 4. Ainda não receberam notificação de confirmação nas últimas 25 horas
            query = """
            SELECT a.idAgendamento, a.idPaciente, a.idMedico, a.dataAgendamento, a.horario
            FROM agendamento a
            WHERE a.dataAgendamento = ? 
            AND a.horario BETWEEN ? AND ?
            AND a.status = 'agendado'
            AND NOT EXISTS (
                SELECT 1 FROM notificacoes n 
                WHERE n.dadosAdicionais LIKE '%"agendamento_id":' || a.idAgendamento || '%'
                AND n.tipo = 'confirmacao_consulta'
                AND n.dataInclusao > datetime('now', '-25 hours')
            )
            """
            
            cursor.execute(query, (data_busca, hora_inicio, hora_fim))
            consultas = cursor.fetchall()
            
            print(f"[{agora.strftime('%H:%M:%S')}] Encontradas {len(consultas)} consultas para notificar")
            
            return consultas
            
    except Exception as e:
        print(f"Erro ao buscar consultas próximas: {e}")
        return []


async def enviar_notificacoes_confirmacao():
    """
    Envia notificações de confirmação para pacientes
    """
    consultas = obter_consultas_proximas()
    
    for consulta in consultas:
        try:
            agendamento_id, id_paciente, id_medico, data_consulta, horario = consulta
            
            # Buscar dados do médico
            medico = obter_medico_por_id(id_medico)
            if not medico:
                print(f"Médico ID {id_medico} não encontrado")
                continue
            
            # Buscar dados do paciente  
            paciente = obter_paciente_por_id(id_paciente)
            if not paciente:
                print(f"Paciente ID {id_paciente} não encontrado")
                continue
            
            print(f"Enviando notificação de confirmação para {paciente.nome} - Consulta com Dr(a). {medico.nome} (24h antes)")
            
            # Enviar notificação
            notification_id = await manager.notify_appointment_reminder(
                patient_id=str(id_paciente),
                doctor_name=medico.nome,
                appointment_date=data_consulta,
                appointment_time=horario,
                appointment_id=agendamento_id
            )
            
            if notification_id:
                print(f"✅ Notificação enviada com sucesso (ID: {notification_id})")
            else:
                print(f"❌ Falha ao enviar notificação")
                
        except Exception as e:
            print(f"Erro ao processar consulta {consulta}: {e}")


def executar_verificacao():
    """
    Executa verificação síncrona
    """
    print(f"\n=== VERIFICAÇÃO DE CONSULTAS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===")
    
    try:
        # Criar loop de eventos se não existir
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Executar função assíncrona
        loop.run_until_complete(enviar_notificacoes_confirmacao())
        
    except Exception as e:
        print(f"Erro na verificação: {e}")


def iniciar_servico():
    """
    Inicia o serviço de notificações automáticas
    """
    print("🚀 Iniciando serviço de notificações automáticas...")
    print("⏰ Verificações a cada 5 minutos")
    print("📧 Notificações enviadas 24 horas antes das consultas")
    print("=" * 60)
    
    # Agendar verificação a cada 5 minutos
    schedule.every(5).minutes.do(executar_verificacao)
    
    # Executar uma verificação inicial
    executar_verificacao()
    
    # Loop principal
    while True:
        try:
            schedule.run_pending()
            time.sleep(10)  # Verificar a cada 10 segundos
        except KeyboardInterrupt:
            print("\n🛑 Serviço interrompido pelo usuário")
            break
        except Exception as e:
            print(f"Erro no loop principal: {e}")
            time.sleep(30)  # Aguardar 30 segundos antes de tentar novamente


def teste_notificacao():
    """
    Função para testar o sistema de notificações manualmente
    """
    print("🧪 Executando teste de notificação...")
    
    # Buscar uma consulta futura para teste
    try:
        from data.util import get_connection
        
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT a.idAgendamento, a.idPaciente, a.idMedico, a.dataAgendamento, a.horario
                FROM agendamento a
                WHERE a.status = 'agendado'
                AND a.dataAgendamento >= date('now')
                LIMIT 1
            """)
            
            consulta = cursor.fetchone()
            
            if consulta:
                agendamento_id, id_paciente, id_medico, data_consulta, horario = consulta
                print(f"Testando com consulta: {agendamento_id} - {data_consulta} {horario}")
                
                # Simular notificação
                async def teste():
                    await enviar_notificacoes_confirmacao()
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(teste())
            else:
                print("Nenhuma consulta encontrada para teste")
                
    except Exception as e:
        print(f"Erro no teste: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Modo de teste
        teste_notificacao()
    else:
        # Modo normal de serviço
        iniciar_servico()