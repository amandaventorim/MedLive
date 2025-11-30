# Sistema de Notificações - MedLive

## Visão Geral

O sistema de notificações do MedLive foi projetado para manter médicos e pacientes informados sobre eventos importantes do sistema através de notificações em tempo real e persistentes.

## Funcionalidades Implementadas

### 1. Interface Visual

#### Ícone de Notificação na Navbar
- **Localização**: Lado direito da navbar, entre o perfil do usuário
- **Badge**: Mostra o número de notificações não lidas
- **Dropdown**: Lista interativa de notificações ao clicar

#### Dropdown de Notificações
- **Header**: Título e botão "Marcar todas como lida"
- **Lista**: Notificações organizadas por data (mais recentes primeiro)
- **Footer**: Link para "Ver todas" (futuro)
- **Ações**: Botões específicos para cada tipo de notificação

### 2. Tipos de Notificação

#### Para Médicos
1. **Nova Consulta Agendada**
   - Disparada quando paciente agenda consulta
   - Mostra: nome do paciente, data e horário
   - Ação: Redireciona para agenda

2. **Resposta de Confirmação**
   - Disparada quando paciente confirma/recusa presença
   - Mostra: status da confirmação (verde/vermelho)
   - Ação: Informativa

#### Para Pacientes
1. **Consulta Iniciada**
   - Disparada quando médico inicia consulta
   - Mostra: nome do médico e botão para entrar
   - Ação: Botão "Entrar na Consulta"

2. **Confirmação de Presença**
   - Disparada 24 horas antes da consulta
   - Mostra: dados da consulta e questão de confirmação
   - Ações: Botões "Sim, vou comparecer" / "Não posso comparecer"
   - Expira em 2 horas se não respondida

### 3. Sistema de Persistência

#### Banco de Dados
- **Tabela**: `notificacoes`
- **Campos**: ID, usuário, tipo, título, mensagem, lida, dados extras, etc.
- **Índices**: Otimizado para consultas rápidas

#### Funcionalidades
- Notificações salvas no banco
- Estado de lida/não lida
- Dados extras em JSON
- Expiração automática
- Limpeza de notificações antigas

### 4. Sistema de Tempo Real

#### WebSocket Integration
- Notificações enviadas em tempo real
- Integração com sistema existente
- Fallback para polling

#### Notificações Browser
- Permissão solicitada automaticamente
- Notificações mesmo com aba fechada
- Som de notificação opcional

## Como Usar

### Para Desenvolvedores

#### Enviar Notificação Simples
```python
from util.websocket_manager import manager

# Notificação em tempo real (não persistente)
await manager.send_notification(
    user_id="123",
    user_type="paciente",
    message={
        "type": "info",
        "message": "Mensagem de teste"
    }
)
```

#### Enviar Notificação Persistente
```python
# Notificação que será salva no banco
await manager.send_persistent_notification(
    user_id="123",
    user_type="medico",
    notification_data={
        "type": "custom",
        "titulo": "Título",
        "mensagem": "Mensagem",
        "dados_extras": {"key": "value"},
        "acao_requerida": False
    }
)
```

#### Criar Notificação Específica
```python
from data.repo.notificacao_repo import criar_notificacao_agendamento

# Notificação de agendamento para médico
notification_id = criar_notificacao_agendamento(
    id_medico=medico_id,
    nome_paciente="João Silva",
    data_consulta="2024-01-15",
    horario="14:30",
    agendamento_id=123
)
```

### Para Usuários Finais

#### Médicos
1. **Ver Notificações**: Clicar no ícone do sino na navbar
2. **Nova Consulta**: Recebe notificação automática quando paciente agenda
3. **Confirmação**: Recebe resposta do paciente sobre presença

#### Pacientes
1. **Consulta Iniciada**: Recebe notificação quando médico inicia consulta
2. **Confirmação**: Recebe pergunta 24 horas antes da consulta
3. **Responder**: Clicar em "Sim" ou "Não" na notificação

## Serviço Automático

### Notificações de Confirmação

#### Como Executar
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar serviço
python notification_service.py

# Testar manualmente
python notification_service.py --test
```

#### Configuração
- **Frequência**: Verificação a cada 5 minutos
- **Antecedência**: 24 horas antes da consulta
- **Janela**: ±30 minutos de tolerância

#### Logs
- Consultas encontradas para notificar
- Status de envio das notificações
- Erros e problemas

## API Endpoints

### GET /api/notifications/{user_type}/{user_id}
Obtém todas as notificações do usuário
- **Parâmetros**: user_type (medico/paciente), user_id
- **Retorna**: Lista de notificações e contagem de não lidas

### POST /api/notifications/{notification_id}/read
Marca notificação como lida
- **Body**: user_id, user_type

### POST /api/notifications/{user_type}/{user_id}/mark-all-read
Marca todas as notificações como lidas

### POST /api/confirm-presence
Confirma presença em consulta
- **Body**: notification_id, confirmed (boolean)

## Estrutura de Arquivos

```
/data
  /model/notificacao_model.py      # Modelo de dados
  /sql/notificacao_sql.py          # Queries SQL
  /repo/notificacao_repo.py        # Repositório de dados

/routes
  /notifications_routes.py         # Endpoints API

/static/js
  /notification_system.js          # Sistema principal
  /paciente_notifications.js       # Cliente paciente
  /medico_consultas.js            # Cliente médico

/static/css
  /notifications.css               # Estilos

/util
  /websocket_manager.py           # WebSocket atualizado

/templates
  /base_medico.html               # Base com notificações
  /base_paciente.html             # Base com notificações

notification_service.py           # Serviço automático
```

## Configuração de Produção

### 1. Banco de Dados
A tabela de notificações é criada automaticamente na primeira execução.

### 2. Serviço Background
Configure o `notification_service.py` para executar como serviço:

**Linux/systemd**:
```ini
[Unit]
Description=MedLive Notification Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/medlive
ExecStart=/path/to/python notification_service.py
Restart=always

[Install]
WantedBy=multi-user.target
```

**Windows**:
Use NSSM ou Task Scheduler para executar como serviço.

### 3. Monitoramento
- Logs do serviço de notificação
- Verificação de conectividade WebSocket
- Performance das consultas ao banco

## Troubleshooting

### Problemas Comuns

1. **Notificações não aparecem**
   - Verificar permissões do browser
   - Checar conexão WebSocket
   - Validar sessão do usuário

2. **Badge não atualiza**
   - Verificar JavaScript errors
   - Testar endpoints API
   - Limpar cache do browser

3. **Confirmação não funciona**
   - Verificar se serviço está rodando
   - Checar logs de erro
   - Validar dados do agendamento

### Logs Úteis

```bash
# Ver logs do serviço
tail -f notification_service.log

# Testar WebSocket
python test_websocket.py

# Verificar banco
sqlite3 database.db "SELECT * FROM notificacoes ORDER BY dataInclusao DESC LIMIT 10;"
```

## Extensões Futuras

- [ ] Notificações por email/SMS
- [ ] Templates customizáveis
- [ ] Agendamento de notificações
- [ ] Dashboard de estatísticas
- [ ] Integração com calendários externos
- [ ] Notificações push mobile