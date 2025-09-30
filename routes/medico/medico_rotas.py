from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List, Optional
from datetime import datetime
from util.auth_decorator import requer_autenticacao
from data.repo.disponibilidade_medico_repo import *
from data.model.disponibilidade_medico_model import DisponibilidadeMedico

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard_medico")
@requer_autenticacao(["medico"])
async def get_dashboard_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/dashboard_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/agenda_medico")
@requer_autenticacao(["medico"])
async def get_agenda_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/agenda_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/consultas_medico")
@requer_autenticacao(["medico"])
async def get_consultas_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/consultas_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/pacientes_medico")
@requer_autenticacao(["medico"])
async def get_pacientes_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/pacientes_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/perfil_medico")
@requer_autenticacao(["medico"])
async def get_perfil_medico(request: Request, usuario_logado: dict = None):
    # Buscar disponibilidades do médico
    disponibilidades = obter_disponibilidades_por_medico(usuario_logado["idUsuario"])
    
    return templates.TemplateResponse("/medico/perfil_medico.html", {
        "request": request,
        "usuario": usuario_logado,
        "disponibilidades": disponibilidades
    })

@router.get("/planos_medico")
@requer_autenticacao(["medico"])
async def get_planos_medico(request: Request, usuario_logado: dict = None):
    return templates.TemplateResponse("/medico/planos_medico.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.get("/cadastro_medico")
async def get_cadastro_medico(request: Request):
    # Rota de cadastro deve ser pública
    return templates.TemplateResponse("/medico/cadastro_medico.html", {
        "request": request
    })

@router.get("/pagamento_plano")
async def get_pagamento_plano(request: Request):
    # Rota de pagamento pode ser pública para permitir cadastro
    return templates.TemplateResponse("/medico/pagamento_plano.html", {
        "request": request
    })

@router.get("/sala_consulta")
@requer_autenticacao(["medico", "paciente"])
async def get_sala_consulta(request: Request, usuario_logado: dict = None):
    # Sala de consulta acessível para médicos e pacientes
    return templates.TemplateResponse("/sala_consulta.html", {
        "request": request,
        "usuario": usuario_logado
    })

@router.post("/salvar_disponibilidade")
@requer_autenticacao(["medico"])
async def salvar_disponibilidade(request: Request, usuario_logado: dict = None):
    """Salvar disponibilidade do médico usando JSON"""
    try:
        # Receber dados JSON
        try:
            dados_json = await request.json()
        except Exception as json_error:
            return JSONResponse(content={
                "success": False, 
                "message": f"Erro ao processar dados: {str(json_error)}"
            }, status_code=422)
        
        # Deletar todas as disponibilidades existentes do médico
        deletar_todas_disponibilidades_medico(usuario_logado["idUsuario"])
        
        # Processar as disponibilidades dos dias da semana
        dias_semana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta', 'sabado', 'domingo']
        disponibilidades_inseridas = 0
        erros = []
        
        for i, dia in enumerate(dias_semana, 1):  # 1 = Segunda, 7 = Domingo
            dia_ativo_key = f"{dia}_ativo"
            dia_ativo = dados_json.get(dia_ativo_key) == "on"
            
            if dia_ativo:
                hora_inicio = dados_json.get(f"{dia}_inicio", "08:00")
                hora_fim = dados_json.get(f"{dia}_fim", "18:00")
                
                # Validar horários
                if not hora_inicio or not hora_fim:
                    erros.append(f"Horários não informados para {dia}")
                    continue
                
                if hora_inicio >= hora_fim:
                    erros.append(f"Horário de início deve ser menor que o fim para {dia}")
                    continue
                
                # Criar nova disponibilidade
                disponibilidade = DisponibilidadeMedico(
                    idDisponibilidade=0,
                    idMedico=usuario_logado["idUsuario"],
                    diaSemana=i,  # 1-7 (Segunda a Domingo)
                    horaInicio=hora_inicio,
                    horaFim=hora_fim,
                    ativo=True
                )
                
                resultado = inserir_disponibilidade_medico(disponibilidade)
                if resultado:
                    disponibilidades_inseridas += 1
                else:
                    erros.append(f"Erro ao inserir disponibilidade para {dia}")
        
        if erros:
            return JSONResponse(content={
                "success": False, 
                "message": f"Alguns erros ocorreram: {'; '.join(erros)}"
            }, status_code=400)
        
        if disponibilidades_inseridas == 0:
            return JSONResponse(content={
                "success": False, 
                "message": "Nenhuma disponibilidade foi configurada. Selecione pelo menos um dia."
            }, status_code=400)
        
        return JSONResponse(content={
            "success": True, 
            "message": f"Disponibilidade salva com sucesso! {disponibilidades_inseridas} dias configurados."
        })
        
    except Exception as e:
        return JSONResponse(content={
            "success": False, 
            "message": f"Erro interno do servidor: {str(e)}"
        }, status_code=500)

@router.get("/obter_disponibilidades")
@requer_autenticacao(["medico"])
async def obter_disponibilidades(request: Request, usuario_logado: dict = None):
    try:
        disponibilidades = obter_disponibilidades_por_medico(usuario_logado["idUsuario"])
        
        # Organizar disponibilidades por dia da semana
        disponibilidades_dict = {}
        for disp in disponibilidades:
            if disp.ativo:
                disponibilidades_dict[disp.diaSemana] = {
                    "horaInicio": disp.horaInicio,
                    "horaFim": disp.horaFim,
                    "ativo": disp.ativo
                }
        
        return JSONResponse(content={"success": True, "disponibilidades": disponibilidades_dict})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "message": f"Erro ao obter disponibilidades: {str(e)}"}, status_code=500)

@router.get("/obter_disponibilidades_medico/{idMedico}")
async def obter_disponibilidades_medico(idMedico: int):
    try:
        disponibilidades = obter_disponibilidades_por_medico(idMedico)
        
        # Organizar disponibilidades por dia da semana
        disponibilidades_dict = {}
        for disp in disponibilidades:
            if disp.ativo:
                disponibilidades_dict[disp.diaSemana] = {
                    "horaInicio": disp.horaInicio,
                    "horaFim": disp.horaFim,
                    "ativo": disp.ativo
                }
        
        return JSONResponse(content={"success": True, "disponibilidades": disponibilidades_dict})
        
    except Exception as e:
        return JSONResponse(content={"success": False, "message": "Erro ao obter disponibilidades"}, status_code=500)
