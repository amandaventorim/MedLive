from fastapi import APIRouter, Request, Form, Depends, Body, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo.agendamento_repo import inserir_agendamento
from data.repo.paciente_repo import obter_id_paciente_por_usuario
from data.repo.medico_repo import obter_medico_por_id
from data.repo.disponibilidade_medico_repo import obter_disponibilidades_por_medico
from data.model.agendamento_model import Agendamento
from datetime import datetime, timedelta
from typing import Optional, List
import re

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def validar_data_agendamento(data_str: str) -> tuple[bool, str, datetime]:
    """
    Valida se a data de agendamento é válida
    
    Returns:
        (is_valid, error_message, parsed_date)
    """
    try:
        # Tentar parsear a data
        data_agendamento = datetime.strptime(data_str, "%Y-%m-%d")
        hoje = datetime.now()
        
        # Verificar se não é no passado
        if data_agendamento.date() < hoje.date():
            return False, "Não é possível agendar consultas para datas passadas.", None
        
        # Verificar se não é muito longe no futuro (6 meses)
        limite_futuro = hoje + timedelta(days=180)
        if data_agendamento > limite_futuro:
            return False, "Não é possível agendar consultas com mais de 6 meses de antecedência.", None
        
        # Verificar se não é domingo (dia 6 = domingo)
        if data_agendamento.weekday() == 6:
            return False, "Não é possível agendar consultas aos domingos.", None
            
        return True, "", data_agendamento
        
    except ValueError:
        return False, "Formato de data inválido.", None


def validar_horario_agendamento(horario_str: str) -> tuple[bool, str]:
    """
    Valida se o horário de agendamento é válido
    
    Returns:
        (is_valid, error_message)
    """
    # Padrão de horário válido (HH:MM)
    if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', horario_str):
        return False, "Formato de horário inválido. Use o formato HH:MM."
    
    # Converter para objeto time para validação
    try:
        hora, minuto = map(int, horario_str.split(':'))
        
        # Horários de funcionamento: 08:00 às 18:00
        if hora < 8 or hora >= 18:
            return False, "Horário deve estar entre 08:00 e 17:59."
        
        # Apenas horários de 30 em 30 minutos
        if minuto not in [0, 30]:
            return False, "Horários disponíveis apenas de 30 em 30 minutos (ex: 08:00, 08:30)."
        
        # Horário de almoço: 12:00 às 14:00
        if 12 <= hora < 14:
            return False, "Horário de almoço (12:00 às 13:59) não disponível para consultas."
            
        return True, ""
        
    except ValueError:
        return False, "Horário inválido."


def validar_medico(id_medico: int) -> tuple[bool, str]:
    """
    Valida se o médico existe e está ativo
    
    Returns:
        (is_valid, error_message)
    """
    try:
        medico = obter_medico_por_id(id_medico)
        if not medico:
            return False, "Médico não encontrado."
        
        # Verificar se o médico está ativo (assumindo que statusProfissional indica isso)
        if hasattr(medico, 'statusProfissional') and medico.statusProfissional == 'inativo':
            return False, "Médico não está disponível para consultas."
            
        return True, ""
        
    except Exception as e:
        print(f"Erro ao validar médico {id_medico}: {e}")
        return False, "Erro ao verificar dados do médico."




def obter_agendamentos_existentes(id_medico: int, data_agendamento: str) -> List[str]:
    """
    Obtém lista de horários já agendados para um médico em uma data específica
    
    Returns:
        Lista de horários ocupados no formato 'HH:MM'
    """
    try:
        from data.repo.agendamento_repo import obter_todos_agendamentos
        agendamentos = obter_todos_agendamentos()
        
        horarios_ocupados = []
        for agendamento in agendamentos:
            if (agendamento.idMedico == id_medico and 
                agendamento.dataAgendamento == data_agendamento and
                agendamento.status in ['agendado', 'confirmado']):
                horarios_ocupados.append(agendamento.horario)
        
        return horarios_ocupados
    except Exception as e:
        print(f"Erro ao obter agendamentos existentes: {e}")
        return []


def gerar_horarios_disponiveis(id_medico: int, data_selecionada: datetime) -> List[str]:
    """
    Gera lista de horários disponíveis baseado na disponibilidade do médico
    e agendamentos existentes
    
    Returns:
        Lista de horários disponíveis no formato 'HH:MM'
    """
    try:
        print(f"🔍 GERAR DEBUG: Iniciando para médico {id_medico} na data {data_selecionada}")
        
        # Obter disponibilidades do médico
        disponibilidades = obter_disponibilidades_por_medico(id_medico)
        print(f"🔍 GERAR DEBUG: Encontradas {len(disponibilidades)} disponibilidades")
        
        for disp in disponibilidades:
            print(f"🔍 GERAR DEBUG: Disponibilidade - Dia: {disp.diaSemana}, Horário: {disp.horaInicio}-{disp.horaFim}, Ativo: {disp.ativo}")
        
        # Filtrar apenas disponibilidades ativas para o dia da semana
        # Python: Monday=0, Sunday=6 / Banco: Monday=1, Sunday=7
        dia_semana_banco = data_selecionada.weekday() + 1
        print(f"🔍 GERAR DEBUG: Dia da semana Python: {data_selecionada.weekday()}, Banco: {dia_semana_banco}")
        
        disponibilidades_dia = [
            d for d in disponibilidades 
            if d.diaSemana == dia_semana_banco and d.ativo
        ]
        
        print(f"🔍 GERAR DEBUG: Disponibilidades para este dia: {len(disponibilidades_dia)}")
        
        if not disponibilidades_dia:
            print(f"🔍 GERAR DEBUG: Médico não trabalha no dia {dia_semana_banco}")
            return []  # Médico não trabalha neste dia
        
        # Gerar horários de 30 em 30 minutos dentro das disponibilidades
        horarios_disponiveis = []
        for disponibilidade in disponibilidades_dia:
            hora_inicio = datetime.strptime(disponibilidade.horaInicio, "%H:%M")
            hora_fim = datetime.strptime(disponibilidade.horaFim, "%H:%M")
            
            current_time = hora_inicio
            while current_time < hora_fim:
                horario_str = current_time.strftime("%H:%M")
                horarios_disponiveis.append(horario_str)
                current_time += timedelta(minutes=30)
        
        # Remover horários já agendados
        data_str = data_selecionada.strftime("%Y-%m-%d")
        horarios_ocupados = obter_agendamentos_existentes(id_medico, data_str)
        
        horarios_livres = [
            h for h in horarios_disponiveis 
            if h not in horarios_ocupados
        ]
        
        return sorted(list(set(horarios_livres)))  # Remove duplicatas e ordena
        
    except Exception as e:
        print(f"Erro ao gerar horários disponíveis: {e}")
        return []


def validar_queixa(queixa: str) -> tuple[bool, str]:
    """
    Valida a queixa/motivo da consulta
    
    Returns:
        (is_valid, error_message)
    """
    if not queixa or not queixa.strip():
        return False, "Motivo da consulta é obrigatório."
    
    if len(queixa.strip()) < 10:
        return False, "Motivo da consulta deve ter pelo menos 10 caracteres."
    
    if len(queixa.strip()) > 500:
        return False, "Motivo da consulta deve ter no máximo 500 caracteres."
        
    return True, ""

@router.get("/agendar_consulta")
@requer_autenticacao(["paciente"])
async def agendar_consulta_form(request: Request, idMedico: Optional[int] = Query(None), usuario_logado: dict = None):
    # Renderiza o formulário de agendamento
    return templates.TemplateResponse("/paciente/agendar_consulta.html", {
        "request": request,
        "usuario": usuario_logado,
        "idMedico": idMedico
    })

@router.get("/api/horarios-disponiveis")
async def api_horarios_disponiveis(
    idMedico: int = Query(...),
    data: str = Query(...)
):
    """
    API para obter horários disponíveis de um médico em uma data específica
    """
    try:
        print(f"🔍 API DEBUG: idMedico={idMedico}, data={data}")
        
        # Validar data
        data_selecionada = datetime.strptime(data, "%Y-%m-%d")
        print(f"🔍 API DEBUG: Data parsed: {data_selecionada}")
        
        # Validar se data não é no passado
        hoje = datetime.now().date()
        if data_selecionada.date() < hoje:
            return JSONResponse(
                content={"success": False, "message": "Não é possível buscar horários para datas passadas"}
            )
        
        # Obter horários disponíveis (removendo validação de médico por ora)
        print(f"🔍 API DEBUG: Chamando gerar_horarios_disponiveis")
        horarios = gerar_horarios_disponiveis(idMedico, data_selecionada)
        print(f"🔍 API DEBUG: Horários retornados: {horarios}")
        
        if horarios:
            return JSONResponse(content={
                "success": True,
                "horarios": horarios,
                "medico": f"Médico {idMedico}",
                "data": data,
                "message": f"{len(horarios)} horários disponíveis"
            })
        else:
            return JSONResponse(content={
                "success": True,
                "horarios": [],
                "medico": f"Médico {idMedico}",
                "data": data,
                "message": "Nenhum horário disponível para esta data"
            })
        
    except ValueError as e:
        print(f"🔍 API DEBUG: Erro ValueError: {e}")
        return JSONResponse(
            content={"success": False, "message": "Formato de data inválido. Use YYYY-MM-DD"},
            status_code=400
        )
    except Exception as e:
        print(f"🔍 API DEBUG: Erro Exception: {e}")
        return JSONResponse(
            content={"success": False, "message": "Erro interno do servidor"},
            status_code=500
        )
@requer_autenticacao(["paciente"])
async def agendar_consulta(
    request: Request,
    date: str = Form(...),
    time: str = Form(...),
    queixa: str = Form(...),
    idMedico: int = Form(...),
    usuario_logado: dict = None
):
    """
    Rota para processar agendamento de consulta com validações completas
    """
    try:
        # ===== VALIDAÇÕES DE ENTRADA =====
        
        # 1. Validar data
        data_valida, erro_data, data_parsed = validar_data_agendamento(date)
        if not data_valida:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "idMedico": idMedico,
                "erro": erro_data
            })
        
        # 2. Validar horário
        horario_valido, erro_horario = validar_horario_agendamento(time)
        if not horario_valido:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "idMedico": idMedico,
                "erro": erro_horario
            })
        
        # 3. Validar médico
        medico_valido, erro_medico = validar_medico(idMedico)
        if not medico_valido:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "erro": erro_medico
            })
        
        # 4. Validar queixa
        queixa_valida, erro_queixa = validar_queixa(queixa)
        if not queixa_valida:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "idMedico": idMedico,
                "erro": erro_queixa
            })
        
        # 5. Validar disponibilidade do médico para data/horário selecionados
        data_obj = datetime.strptime(date, "%Y-%m-%d")
        horarios_disponiveis = gerar_horarios_disponiveis(idMedico, data_obj)
        
        if time not in horarios_disponiveis:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "idMedico": idMedico,
                "erro": f"Horário {time} não está disponível para este médico na data selecionada."
            })
        
        # 6. Validar queixa
        queixa_valida, erro_queixa = validar_queixa(queixa)
        if not queixa_valida:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "idMedico": idMedico,
                "erro": erro_queixa
            })
        
        # ===== OBTENÇÃO DO ID PACIENTE =====
        
        # Tentar obter idPaciente da sessão (otimização)
        id_paciente = usuario_logado.get("idPaciente")
        
        # Se não estiver na sessão, buscar no banco (fallback)
        if not id_paciente:
            id_usuario = usuario_logado.get("idUsuario")
            if not id_usuario:
                return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                    "request": request,
                    "usuario": usuario_logado,
                    "erro": "Erro de sessão: dados do usuário não encontrados."
                })
            
            id_paciente = obter_id_paciente_por_usuario(id_usuario)
        
        if not id_paciente:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "erro": "Erro: Usuário não possui cadastro de paciente. Entre em contato com o administrador."
            })
        
        # ===== CRIAÇÃO DO AGENDAMENTO =====
        
        status = "agendado"
        agendamento = Agendamento(
            idAgendamento=None,
            idPaciente=id_paciente,
            idMedico=idMedico,
            dataAgendamento=date,
            horario=time,
            status=status,
            queixa=queixa.strip(),  # Remover espaços extras
            preco=0.0  # Valor padrão, pode ser alterado futuramente
        )
        
        # ===== INSERÇÃO NO BANCO =====
        
        agendamento_id = inserir_agendamento(agendamento)
        if agendamento_id:
            print(f"Agendamento criado com sucesso: ID {agendamento_id}")  # Log de sucesso
            return RedirectResponse("/paciente/minhas_consultas", status_code=303)
        else:
            return templates.TemplateResponse("/paciente/agendar_consulta.html", {
                "request": request,
                "usuario": usuario_logado,
                "idMedico": idMedico,
                "erro": "Erro ao inserir agendamento no banco de dados. Tente novamente."
            })
            
    except ValueError as ve:
        # Erros de validação de entrada (datas, números, etc.)
        print(f"Erro de validação no agendamento: {ve}")
        return templates.TemplateResponse("/paciente/agendar_consulta.html", {
            "request": request,
            "usuario": usuario_logado,
            "idMedico": idMedico if 'idMedico' in locals() else None,
            "erro": f"Dados inválidos: {str(ve)}"
        })
        
    except KeyError as ke:
        # Erros de campos obrigatórios ausentes
        print(f"Campo obrigatório ausente no agendamento: {ke}")
        return templates.TemplateResponse("/paciente/agendar_consulta.html", {
            "request": request,
            "usuario": usuario_logado,
            "erro": "Dados do formulário incompletos. Verifique todos os campos."
        })
        
    except Exception as e:
        # Erros gerais (banco de dados, etc.)
        print(f"Erro interno no agendamento: {e}")
        return templates.TemplateResponse("/paciente/agendar_consulta.html", {
            "request": request,
            "usuario": usuario_logado,
            "idMedico": idMedico if 'idMedico' in locals() else None,
            "erro": "Erro interno no sistema. Tente novamente mais tarde ou entre em contato com o suporte."
        })
