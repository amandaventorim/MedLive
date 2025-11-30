"""
DTOs relacionados a pacientes.
Agrupa todas as validações e estruturas de dados para operações com pacientes.
"""

from pydantic import Field, field_validator
from typing import Optional
from dto.usuario_dtos import CriarUsuarioDTO, AtualizarUsuarioDTO, PerfilEnum
from dto.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_texto_opcional
)


class CriarPacienteDTO(CriarUsuarioDTO):
    """
    DTO para cadastro de novo paciente.
    Herda validações básicas de usuário e adiciona campos específicos.
    """

    # Sobrescrever perfil para ser sempre paciente
    perfil: PerfilEnum = Field(
        default=PerfilEnum.PACIENTE,
        description="Perfil fixo como paciente"
    )
    
    endereco: str = Field(
        ...,
        min_length=10,
        max_length=200,
        description="Endereço completo do paciente"
    )
    
    convenio: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome do convênio médico"
    )

    @field_validator('endereco')
    @classmethod
    def validar_endereco(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=10, max_chars=200
            ),
            "Endereço"
        )
        return validador(v)

    @field_validator('convenio')
    @classmethod
    def validar_convenio(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Convênio"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "Maria Santos Silva",
            "cpf": "987.654.321-00",
            "email": "maria.santos@email.com",
            "senha": "senha123",
            "genero": "feminino",
            "dataNascimento": "1985-07-12",
            "perfil": "paciente",
            "endereco": "Rua das Flores, 123 - Centro - São Paulo - SP",
            "convenio": "Unimed Nacional"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarPacienteDTO(AtualizarUsuarioDTO):
    """
    DTO para atualização de dados do paciente.
    Permite atualizar campos específicos do paciente.
    """

    endereco: Optional[str] = Field(
        None,
        min_length=10,
        max_length=200,
        description="Endereço completo do paciente"
    )
    
    convenio: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nome do convênio médico"
    )

    @field_validator('endereco')
    @classmethod
    def validar_endereco(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=10, max_chars=200
            ),
            "Endereço"
        )
        return validador(v)

    @field_validator('convenio')
    @classmethod
    def validar_convenio(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(
                valor, campo, min_chars=2, max_chars=100
            ),
            "Convênio"
        )
        return validador(v)


class PacienteFiltroDTO(BaseDTO):
    """
    DTO para filtros de listagem de pacientes.
    Usado em buscas e paginação.
    """

    nome_busca: Optional[str] = Field(
        None,
        max_length=100,
        description="Busca por nome do paciente"
    )
    
    cpf_busca: Optional[str] = Field(
        None,
        max_length=14,
        description="Busca por CPF"
    )
    
    convenio_busca: Optional[str] = Field(
        None,
        max_length=100,
        description="Busca por convênio"
    )
    
    email_busca: Optional[str] = Field(
        None,
        max_length=100,
        description="Busca por email"
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

    @field_validator('cpf_busca')
    @classmethod
    def validar_cpf_busca(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        # Remover máscara para busca
        import re
        return re.sub(r'[^0-9]', '', v.strip())

    @field_validator('convenio_busca')
    @classmethod
    def validar_convenio_busca(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return v.strip()

    @field_validator('email_busca')
    @classmethod
    def validar_email_busca(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        return v.strip().lower()


class AgendarConsultaDTO(BaseDTO):
    """
    DTO para agendamento de consulta por parte do paciente.
    """
    
    medico_id: int = Field(
        ...,
        gt=0,
        description="ID do médico escolhido"
    )
    
    data_consulta: str = Field(
        ...,
        description="Data da consulta no formato YYYY-MM-DD"
    )
    
    horario_consulta: str = Field(
        ...,
        description="Horário da consulta no formato HH:MM"
    )
    
    observacoes: Optional[str] = Field(
        None,
        max_length=500,
        description="Observações adicionais sobre a consulta"
    )

    @field_validator('data_consulta')
    @classmethod
    def validar_data_consulta(cls, v: str) -> str:
        import re
        from datetime import datetime, date
        
        # Validar formato
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            raise ValueError('Data deve estar no formato YYYY-MM-DD')
        
        try:
            data_consulta = datetime.strptime(v, '%Y-%m-%d').date()
            hoje = date.today()
            
            if data_consulta <= hoje:
                raise ValueError('Data da consulta deve ser futura')
                
        except ValueError as e:
            if "time data" in str(e):
                raise ValueError('Data inválida')
            raise e
        
        return v

    @field_validator('horario_consulta')
    @classmethod
    def validar_horario_consulta(cls, v: str) -> str:
        import re
        from datetime import datetime
        
        # Validar formato HH:MM
        if not re.match(r'^\d{2}:\d{2}$', v):
            raise ValueError('Horário deve estar no formato HH:MM')
        
        try:
            # Validar se é um horário válido
            datetime.strptime(v, '%H:%M')
        except ValueError:
            raise ValueError('Horário inválido')
        
        return v

    @field_validator('observacoes')
    @classmethod
    def validar_observacoes(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = BaseDTO.validar_campo_wrapper(
            lambda valor, campo: validar_texto_opcional(valor, max_chars=500),
            "Observações"
        )
        return validador(v)


# Configurar exemplos JSON nos model_config
CriarPacienteDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarPacienteDTO.criar_exemplo_json()
    }
})