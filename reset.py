import sqlite3
from data.sql.usuario_sql import CRIAR_TABELA_USUARIO
from data.sql.paciente_sql import CRIAR_TABELA_PACIENTE
from data.sql.medico_sql import CRIAR_TABELA_MEDICO
from data.sql.medico_especialidade_sql import CRIAR_TABELA_MEDICO_ESPECIALIDADE
from data.sql.medicamento_sql import CRIAR_TABELA_MEDICAMENTO
from data.sql.item_receita_sql import CRIAR_TABELA_ITEM_RECEITA
from data.sql.especialidade_sql import CRIAR_TABELA_ESPECIALIDADE
from data.sql.entrada_prontuario_sql import CRIAR_TABELA_ENTRADA_PRONTUARIO
from data.sql.consulta_sql import CRIAR_TABELA_CONSULTA
from data.sql.agenda_sql import CRIAR_TABELA_AGENDA
from data.sql.agendamento_sql import CRIAR_TABELA_AGENDAMENTO
from data.sql.administrador_sql import CRIAR_TABELA_ADMINISTRADOR

def reset_db():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()

    tabelas = [
        "item_receita", "medico_especialidade", "entrada_prontuario", "agendamento", "agenda", "consulta", "medicamento", "especialidade", "administrador", "paciente", "medico", "usuario"
    ]
    for tabela in tabelas:
        cursor.execute(f"DROP TABLE IF EXISTS {tabela};")

    cursor.executescript(CRIAR_TABELA_USUARIO)
    cursor.executescript(CRIAR_TABELA_PACIENTE)
    cursor.executescript(CRIAR_TABELA_MEDICO)
    cursor.executescript(CRIAR_TABELA_MEDICO_ESPECIALIDADE)
    cursor.executescript(CRIAR_TABELA_MEDICAMENTO)
    cursor.executescript(CRIAR_TABELA_ITEM_RECEITA)
    cursor.executescript(CRIAR_TABELA_ESPECIALIDADE)
    cursor.executescript(CRIAR_TABELA_ENTRADA_PRONTUARIO)
    cursor.executescript(CRIAR_TABELA_CONSULTA)
    cursor.executescript(CRIAR_TABELA_AGENDA)
    cursor.executescript(CRIAR_TABELA_AGENDAMENTO)
    cursor.executescript(CRIAR_TABELA_ADMINISTRADOR)
    conn.commit()
    conn.close()

reset_db()
