"""
Pacote de DTOs do sistema MedLive.

Este módulo centraliza todos os DTOs (Data Transfer Objects) organizados por funcionalidade:
- BaseDTO: Classe base com configurações comuns
- usuario_dtos: DTOs relacionados a usuários
- medico_dtos: DTOs relacionados a médicos
- paciente_dtos: DTOs relacionados a pacientes

Imports facilitados para os DTOs mais comuns:
"""

# Base
from .base_dto import BaseDTO

# Usuário
from .usuario_dtos import (
    CriarUsuarioDTO,
    LoginUsuarioDTO,
    AtualizarUsuarioDTO,
    AlterarSenhaDTO,
    GeneroEnum,
    PerfilEnum
)

# Médico
from .medico_dtos import (
    CriarMedicoDTO,
    AtualizarMedicoDTO,
    MedicoFiltroDTO,
    StatusProfissionalEnum
)

# Paciente
from .paciente_dtos import (
    CriarPacienteDTO,
    AtualizarPacienteDTO,
    PacienteFiltroDTO,
    AgendarConsultaDTO
)

__all__ = [
    # Base
    'BaseDTO',

    # Usuário
    'CriarUsuarioDTO',
    'LoginUsuarioDTO',
    'AtualizarUsuarioDTO',
    'AlterarSenhaDTO',
    'GeneroEnum',
    'PerfilEnum',

    # Médico
    'CriarMedicoDTO',
    'AtualizarMedicoDTO',
    'MedicoFiltroDTO',
    'StatusProfissionalEnum',

    # Paciente
    'CriarPacienteDTO',
    'AtualizarPacienteDTO',
    'PacienteFiltroDTO',
    'AgendarConsultaDTO',
]