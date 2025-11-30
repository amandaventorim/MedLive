import sqlite3
from typing import List, Optional
from data.model.notificacao_model import Notificacao
from data.sql.notificacao_sql import *
from data.util import get_connection
import json
from datetime import datetime, timedelta


def criar_tabela_notificacoes():
    """Cria a tabela de notificações se ela não existir"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(CREATE_TABLE_NOTIFICACOES)
            
            # Executar comandos de criação de índices separadamente
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_usuario_tipo ON notificacoes (idUsuario, tipoUsuario);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_lida ON notificacoes (lida);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_data_inclusao ON notificacoes (dataInclusao);")
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao criar tabela de notificações: {e}")
        return False


def inserir_notificacao(notificacao: Notificacao) -> Optional[int]:
    """Insere uma nova notificação no banco de dados"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(INSERT_NOTIFICACAO, (
                notificacao.idUsuario,
                notificacao.tipoUsuario,
                notificacao.tipo,
                notificacao.titulo,
                notificacao.mensagem,
                int(notificacao.lida),
                notificacao.dadosAdicionais,
                int(notificacao.acaoRequerida),
                notificacao.expiresAt
            ))
            conn.commit()
            return cursor.lastrowid
    except Exception as e:
        print(f"Erro ao inserir notificação: {e}")
        return None


def obter_notificacoes_por_usuario(id_usuario: int, tipo_usuario: str, limite: int = 20, offset: int = 0) -> List[Notificacao]:
    """Obtém todas as notificações de um usuário com paginação"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SELECT_NOTIFICACOES_POR_USUARIO, (id_usuario, tipo_usuario, limite, offset))
            rows = cursor.fetchall()
            
            notificacoes = []
            for row in rows:
                notificacao = Notificacao(
                    idNotificacao=row[0],
                    idUsuario=row[1],
                    tipoUsuario=row[2],
                    tipo=row[3],
                    titulo=row[4],
                    mensagem=row[5],
                    lida=bool(row[6]),
                    dataInclusao=row[7],
                    dadosAdicionais=row[8],
                    acaoRequerida=bool(row[9]),
                    expiresAt=row[10]
                )
                notificacoes.append(notificacao)
            
            return notificacoes
    except Exception as e:
        print(f"Erro ao obter notificações: {e}")
        return []


def obter_notificacoes_nao_lidas(id_usuario: int, tipo_usuario: str) -> List[Notificacao]:
    """Obtém todas as notificações não lidas de um usuário"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SELECT_NOTIFICACOES_NAO_LIDAS, (id_usuario, tipo_usuario))
            rows = cursor.fetchall()
            
            notificacoes = []
            for row in rows:
                notificacao = Notificacao(
                    idNotificacao=row[0],
                    idUsuario=row[1],
                    tipoUsuario=row[2],
                    tipo=row[3],
                    titulo=row[4],
                    mensagem=row[5],
                    lida=bool(row[6]),
                    dataInclusao=row[7],
                    dadosAdicionais=row[8],
                    acaoRequerida=bool(row[9]),
                    expiresAt=row[10]
                )
                notificacoes.append(notificacao)
            
            return notificacoes
    except Exception as e:
        print(f"Erro ao obter notificações não lidas: {e}")
        return []


def contar_notificacoes_nao_lidas(id_usuario: int, tipo_usuario: str) -> int:
    """Conta quantas notificações não lidas um usuário tem"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(COUNT_NOTIFICACOES_NAO_LIDAS, (id_usuario, tipo_usuario))
            result = cursor.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Erro ao contar notificações não lidas: {e}")
        return 0


def marcar_notificacao_como_lida(id_notificacao: int, id_usuario: int, tipo_usuario: str) -> bool:
    """Marca uma notificação específica como lida"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_NOTIFICACAO_LIDA, (id_notificacao, id_usuario, tipo_usuario))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao marcar notificação como lida: {e}")
        return False


def marcar_todas_notificacoes_como_lidas(id_usuario: int, tipo_usuario: str) -> bool:
    """Marca todas as notificações não lidas de um usuário como lidas"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(UPDATE_TODAS_NOTIFICACOES_LIDAS, (id_usuario, tipo_usuario))
            conn.commit()
            return True
    except Exception as e:
        print(f"Erro ao marcar todas as notificações como lidas: {e}")
        return False


def deletar_notificacao(id_notificacao: int, id_usuario: int, tipo_usuario: str) -> bool:
    """Deleta uma notificação específica"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETE_NOTIFICACAO, (id_notificacao, id_usuario, tipo_usuario))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        print(f"Erro ao deletar notificação: {e}")
        return False


def limpar_notificacoes_expiradas() -> bool:
    """Remove notificações expiradas do banco"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(DELETE_NOTIFICACOES_EXPIRADAS)
            conn.commit()
            print(f"Removidas {cursor.rowcount} notificações expiradas")
            return True
    except Exception as e:
        print(f"Erro ao limpar notificações expiradas: {e}")
        return False


def obter_notificacao_por_id(id_notificacao: int, id_usuario: int, tipo_usuario: str) -> Optional[Notificacao]:
    """Obtém uma notificação específica pelo ID"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(SELECT_NOTIFICACAO_POR_ID, (id_notificacao, id_usuario, tipo_usuario))
            row = cursor.fetchone()
            
            if row:
                return Notificacao(
                    idNotificacao=row[0],
                    idUsuario=row[1],
                    tipoUsuario=row[2],
                    tipo=row[3],
                    titulo=row[4],
                    mensagem=row[5],
                    lida=bool(row[6]),
                    dataInclusao=row[7],
                    dadosAdicionais=row[8],
                    acaoRequerida=bool(row[9]),
                    expiresAt=row[10]
                )
            return None
    except Exception as e:
        print(f"Erro ao obter notificação por ID: {e}")
        return None


def criar_notificacao_agendamento(id_medico: int, nome_paciente: str, data_consulta: str, horario: str, agendamento_id: int) -> Optional[int]:
    """Cria uma notificação para o médico quando um paciente agenda uma consulta"""
    dados_adicionais = json.dumps({
        "agendamento_id": agendamento_id,
        "nome_paciente": nome_paciente,
        "data_consulta": data_consulta,
        "horario": horario
    })
    
    notificacao = Notificacao(
        idNotificacao=None,
        idUsuario=id_medico,
        tipoUsuario="medico",
        tipo="novo_agendamento",
        titulo="Nova Consulta Agendada",
        mensagem=f"{nome_paciente} agendou uma consulta para {data_consulta} às {horario}",
        lida=False,
        dadosAdicionais=dados_adicionais,
        acaoRequerida=False
    )
    
    return inserir_notificacao(notificacao)


def criar_notificacao_confirmacao_consulta(id_paciente: int, nome_medico: str, data_consulta: str, horario: str, agendamento_id: int) -> Optional[int]:
    """Cria uma notificação de confirmação de consulta (24 horas antes)"""
    # Expira em 2 horas (tempo suficiente para responder)
    expires_at = datetime.now() + timedelta(hours=2)
    
    dados_adicionais = json.dumps({
        "agendamento_id": agendamento_id,
        "nome_medico": nome_medico,
        "data_consulta": data_consulta,
        "horario": horario
    })
    
    notificacao = Notificacao(
        idNotificacao=None,
        idUsuario=id_paciente,
        tipoUsuario="paciente",
        tipo="confirmacao_consulta",
        titulo="Confirme sua Presença",
        mensagem=f"Sua consulta com Dr(a). {nome_medico} está marcada para amanhã ({horario}). Você confirmará presença?",
        lida=False,
        dadosAdicionais=dados_adicionais,
        acaoRequerida=True,
        expiresAt=expires_at.isoformat()
    )
    
    return inserir_notificacao(notificacao)


def criar_notificacao_resposta_confirmacao(id_medico: int, nome_paciente: str, confirmou: bool, data_consulta: str, horario: str, agendamento_id: int) -> Optional[int]:
    """Cria uma notificação para o médico com a resposta do paciente sobre confirmação"""
    status_texto = "CONFIRMOU" if confirmou else "NÃO CONFIRMOU"
    cor = "success" if confirmou else "warning"
    
    dados_adicionais = json.dumps({
        "agendamento_id": agendamento_id,
        "nome_paciente": nome_paciente,
        "confirmou": confirmou,
        "data_consulta": data_consulta,
        "horario": horario,
        "cor": cor
    })
    
    notificacao = Notificacao(
        idNotificacao=None,
        idUsuario=id_medico,
        tipoUsuario="medico",
        tipo="resposta_confirmacao",
        titulo=f"Paciente {status_texto} Presença",
        mensagem=f"{nome_paciente} {status_texto.lower()} presença para consulta de {data_consulta} às {horario}",
        lida=False,
        dadosAdicionais=dados_adicionais,
        acaoRequerida=False
    )
    
    return inserir_notificacao(notificacao)


# Inicializar tabela ao importar o módulo
criar_tabela_notificacoes()