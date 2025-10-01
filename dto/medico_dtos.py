"""
DTOs relacionados a médicos.
Agrupa todas as validações e estruturas de dados para operações com médicos.
"""

from pydantic import Field, field_validator
from typing import Optional
from enum import Enum
from dto.usuario_dtos import CriarUsuarioDTO, AtualizarUsuarioDTO, PerfilEnum
from dto.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio
)


class StatusProfissionalEnum(str, Enum):
    """Enum para status profissional do médico"""
    ATIVO = "ativo"
    INATIVO = "inativo"
    LICENCA = "licenca"
    AFASTADO = "afastado"


class CriarMedicoDTO(CriarUsuarioDTO):
    """
    DTO para cadastro de novo médico.
    Herda validações básicas de usuário e adiciona campos específicos.
    """

    # Sobrescrever perfil para ser sempre médico
    perfil: PerfilEnum = Field(
        default=PerfilEnum.MEDICO,
        description="Perfil fixo como médico"
    )
    
    crm: str = Field(
        ...,
        min_length=4,
        max_length=20,
        description="Número do CRM do médico"
    )
    
    statusProfissional: StatusProfissionalEnum = Field(
        default=StatusProfissionalEnum.ATIVO,
        description="Status profissional do médico"
    )

    @field_validator('crm')
    @classmethod
    def validar_crm(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=4, max_chars=20
            ),
            "CRM"
        )
        crm_limpo = validador(v)
        
        # Validação adicional: CRM deve conter apenas números e letras
        import re
        if not re.match(r'^[A-Z0-9\-\/]+$', crm_limpo.upper()):
            raise ValueError("CRM deve conter apenas números, letras e traços")
        
        return crm_limpo.upper()

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "Dr. Carlos Ferreira Silva",
            "cpf": "123.456.789-01",
            "email": "dr.carlos@clinica.com",
            "senha": "senha123",
            "genero": "masculino",
            "dataNascimento": "1980-03-20",
            "perfil": "medico",
            "crm": "CRM/SP-123456",
            "statusProfissional": "ativo"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarMedicoDTO(AtualizarUsuarioDTO):
    """
    DTO para atualização de dados do médico.
    Permite atualizar campos específicos do médico.
    """

    crm: Optional[str] = Field(
        None,
        min_length=4,
        max_length=20,
        description="Número do CRM do médico"
    )
    
    statusProfissional: Optional[StatusProfissionalEnum] = Field(
        None,
        description="Status profissional do médico"
    )

    @field_validator('crm')
    @classmethod
    def validar_crm(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
            
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=4, max_chars=20
            ),
            "CRM"
        )
        crm_limpo = validador(v)
        
        # Validação adicional: CRM deve conter apenas números e letras
        import re
        if not re.match(r'^[A-Z0-9\-\/]+$', crm_limpo.upper()):
            raise ValueError("CRM deve conter apenas números, letras e traços")
        
        return crm_limpo.upper()


class MedicoFiltroDTO(BaseDTO):
    """
    DTO para filtros de listagem de médicos.
    Usado em buscas e paginação.
    """

    nome_busca: Optional[str] = Field(
        None,
        max_length=100,
        description="Busca por nome do médico"
    )
    
    crm_busca: Optional[str] = Field(
        None,
        max_length=20,
        description="Busca por CRM"
    )
    
    statusProfissional: Optional[StatusProfissionalEnum] = Field(
        None,
        description="Filtrar por status profissional"
    )
    
    especialidade_id: Optional[int] = Field(
        None,
        gt=0,
        description="Filtrar por especialidade"
    )

    # Paginação
    pagina: int = Field(
        default=1,
        ge=1,
        description="Número da página"
    )
    
    tamanho_pagina: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Itens por página"
    )

    @field_validator('nome_busca')
    @classmethod
    def validar_nome_busca(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return v.strip()

    @field_validator('crm_busca')
    @classmethod
    def validar_crm_busca(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return v.strip().upper()


# Configurar exemplos JSON nos model_config
CriarMedicoDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarMedicoDTO.criar_exemplo_json()
    }
})