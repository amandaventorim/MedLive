"""
Script de teste para o Sistema de Notificações - MedLive
Testa todas as funcionalidades implementadas
"""

import json
from datetime import datetime, timedelta

def testar_criacao_tabela():
    """Testa a criação da tabela de notificações"""
    print("📋 Testando criação da tabela...")
    
    try:
        from data.repo.notificacao_repo import criar_tabela_notificacoes
        resultado = criar_tabela_notificacoes()
        
        if resultado:
            print("✅ Tabela criada com sucesso!")
            return True
        else:
            print("❌ Erro ao criar tabela")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def testar_inserir_notificacao():
    """Testa a inserção de uma notificação"""
    print("\n📝 Testando inserção de notificação...")
    
    try:
        from data.model.notificacao_model import Notificacao
        from data.repo.notificacao_repo import inserir_notificacao
        
        # Criar notificação de teste
        notificacao = Notificacao(
            idNotificacao=None,
            idUsuario=1,
            tipoUsuario="medico",
            tipo="teste",
            titulo="Teste de Notificação",
            mensagem="Esta é uma notificação de teste do sistema",
            lida=False,
            dadosAdicionais=json.dumps({"teste": True}),
            acaoRequerida=False
        )
        
        notification_id = inserir_notificacao(notificacao)
        
        if notification_id:
            print(f"✅ Notificação criada com ID: {notification_id}")
            return notification_id
        else:
            print("❌ Erro ao criar notificação")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


def testar_buscar_notificacoes():
    """Testa a busca de notificações"""
    print("\n🔍 Testando busca de notificações...")
    
    try:
        from data.repo.notificacao_repo import obter_notificacoes_por_usuario, contar_notificacoes_nao_lidas
        
        # Buscar notificações do usuário 1 (médico)
        notificacoes = obter_notificacoes_por_usuario(1, "medico")
        count = contar_notificacoes_nao_lidas(1, "medico")
        
        print(f"✅ Encontradas {len(notificacoes)} notificações")
        print(f"✅ {count} notificações não lidas")
        
        if notificacoes:
            primeira = notificacoes[0]
            print(f"   Primeira: {primeira.titulo} - {primeira.mensagem}")
        
        return len(notificacoes) > 0
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def testar_marcar_como_lida():
    """Testa marcar notificação como lida"""
    print("\n📖 Testando marcar como lida...")
    
    try:
        from data.repo.notificacao_repo import obter_notificacoes_por_usuario, marcar_notificacao_como_lida
        
        # Buscar uma notificação não lida
        notificacoes = obter_notificacoes_por_usuario(1, "medico")
        
        if notificacoes:
            notification = notificacoes[0]
            sucesso = marcar_notificacao_como_lida(notification.idNotificacao, 1, "medico")
            
            if sucesso:
                print(f"✅ Notificação {notification.idNotificacao} marcada como lida")
                return True
            else:
                print("❌ Erro ao marcar como lida")
                return False
        else:
            print("ℹ️  Nenhuma notificação para marcar")
            return True
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def testar_notificacao_agendamento():
    """Testa criação de notificação de agendamento"""
    print("\n📅 Testando notificação de agendamento...")
    
    try:
        from data.repo.notificacao_repo import criar_notificacao_agendamento
        
        notification_id = criar_notificacao_agendamento(
            id_medico=1,
            nome_paciente="João Teste",
            data_consulta="2024-12-01",
            horario="14:30",
            agendamento_id=999
        )
        
        if notification_id:
            print(f"✅ Notificação de agendamento criada: ID {notification_id}")
            return True
        else:
            print("❌ Erro ao criar notificação de agendamento")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def testar_notificacao_confirmacao():
    """Testa criação de notificação de confirmação"""
    print("\n⏰ Testando notificação de confirmação...")
    
    try:
        from data.repo.notificacao_repo import criar_notificacao_confirmacao_consulta
        
        # Data/hora atual + 1 hora
        agora = datetime.now()
        uma_hora_depois = agora + timedelta(hours=1)
        data_consulta = uma_hora_depois.strftime("%Y-%m-%d")
        horario = uma_hora_depois.strftime("%H:%M")
        
        notification_id = criar_notificacao_confirmacao_consulta(
            id_paciente=2,
            nome_medico="Dr. João Teste",
            data_consulta=data_consulta,
            horario=horario,
            agendamento_id=999
        )
        
        if notification_id:
            print(f"✅ Notificação de confirmação criada: ID {notification_id}")
            return True
        else:
            print("❌ Erro ao criar notificação de confirmação")
            return False
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def testar_endpoints():
    """Testa se os endpoints estão corretos"""
    print("\n🌐 Verificando endpoints...")
    
    try:
        import inspect
        from routes.notifications_routes import (
            get_notifications,
            mark_notification_read,
            mark_all_notifications_read,
            confirm_presence
        )
        
        print("✅ Endpoint get_notifications encontrado")
        print("✅ Endpoint mark_notification_read encontrado")  
        print("✅ Endpoint mark_all_notifications_read encontrado")
        print("✅ Endpoint confirm_presence encontrado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar endpoints: {e}")
        return False


def executar_todos_testes():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO SISTEMA DE NOTIFICAÇÕES")
    print("=" * 60)
    
    testes = [
        testar_criacao_tabela,
        testar_inserir_notificacao,
        testar_buscar_notificacoes,
        testar_marcar_como_lida,
        testar_notificacao_agendamento,
        testar_notificacao_confirmacao,
        testar_endpoints
    ]
    
    resultados = []
    
    for teste in testes:
        resultado = teste()
        resultados.append(resultado)
    
    print("\n" + "=" * 60)
    print("📊 RESULTADOS DOS TESTES")
    print("=" * 60)
    
    passaram = sum(resultados)
    total = len(resultados)
    
    print(f"✅ Testes passaram: {passaram}/{total}")
    print(f"❌ Testes falharam: {total - passaram}/{total}")
    
    if passaram == total:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("💡 O sistema de notificações está funcionando corretamente!")
    else:
        print(f"\n⚠️  {total - passaram} teste(s) falharam")
        print("💡 Revise a implementação dos componentes que falharam")
    
    return passaram == total


def mostrar_instrucoes():
    """Mostra instruções de como usar o sistema"""
    print("\n" + "=" * 60)
    print("📖 COMO USAR O SISTEMA DE NOTIFICAÇÕES")
    print("=" * 60)
    
    print("""
🔧 PARA DESENVOLVEDORES:

1. Iniciar o servidor principal:
   python main.py

2. Iniciar o serviço de notificações automáticas (em outro terminal):
   python notification_service.py

3. Testar notificação manual:
   python notification_service.py --test

🖥️  PARA USUÁRIOS:

1. Médicos:
   - Recebem notificação quando paciente agenda consulta
   - Veem resposta de confirmação do paciente
   - Clicam no sininho na navbar para ver notificações

2. Pacientes:
   - Recebem notificação quando consulta é iniciada
   - Recebem pergunta de confirmação 1h antes da consulta
   - Podem responder "Sim" ou "Não" na notificação

🛠️  ENDPOINTS API:

• GET /api/notifications/{user_type}/{user_id}
  Buscar notificações do usuário

• POST /api/notifications/{notification_id}/read
  Marcar notificação como lida

• POST /api/notifications/{user_type}/{user_id}/mark-all-read
  Marcar todas como lidas

• POST /api/confirm-presence
  Confirmar presença em consulta
  
📁 ARQUIVOS IMPORTANTES:

• static/js/notification_system.js - Sistema principal
• static/css/notifications.css - Estilos
• data/repo/notificacao_repo.py - Banco de dados
• routes/notifications_routes.py - API
• notification_service.py - Serviço automático
""")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        mostrar_instrucoes()
    else:
        sucesso = executar_todos_testes()
        
        if sucesso:
            mostrar_instrucoes()
        
        print(f"\n{'🎉' if sucesso else '⚠️'} Script de teste finalizado!")