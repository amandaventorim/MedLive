"""
DTOs relacionados a usuários.
Agrupa todas as validações e estruturas de dados para operações com usuários.
"""

from pydantic import EmailStr, Field, field_validator
from typing import Optional
from enum import Enum
from dto.base_dto import BaseDTO
from util.validacoes_dto import (
    validar_texto_obrigatorio, validar_cpf, validar_nome_pessoa,
    validar_data_nascimento, validar_senha
)


class GeneroEnum(str, Enum):
    """Enum para gêneros disponíveis"""
    MASCULINO = "masculino"
    FEMININO = "feminino"
    OUTROS = "outros"


class PerfilEnum(str, Enum):
    """Enum para perfis de usuário"""
    ADMIN = "admin"
    MEDICO = "medico"
    PACIENTE = "paciente"


class CriarUsuarioDTO(BaseDTO):
    """
    DTO para criação de novo usuário.
    Usado em formulários de registro base.
    """

    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nome completo do usuário"
    )
    cpf: str = Field(
        ...,
        description="CPF do usuário (com ou sem máscara)"
    )
    email: EmailStr = Field(
        ...,
        description="E-mail válido do usuário"
    )
    senha: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Senha do usuário"
    )
    genero: GeneroEnum = Field(
        ...,
        description="Gênero do usuário"
    )
    dataNascimento: str = Field(
        ...,
        description="Data de nascimento no formato YYYY-MM-DD"
    )
    perfil: PerfilEnum = Field(
        default=PerfilEnum.PACIENTE,
        description="Perfil do usuário no sistema"
    )

    @field_validator('genero', mode='before')
    @classmethod
    def normalizar_genero(cls, v):
        """Normaliza o gênero para lowercase para aceitar diferentes casos"""
        if isinstance(v, str):
            return v.lower()
        return v

    @field_validator('perfil', mode='before')
    @classmethod
    def normalizar_perfil(cls, v):
        """Normaliza o perfil para lowercase para aceitar diferentes casos"""
        if isinstance(v, str):
            return v.lower()
        return v

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor, min_chars=2, max_chars=100),
            "Nome"
        )
        return validador(v)

    @field_validator('cpf')
    @classmethod
    def validar_cpf_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_cpf(valor),
            "CPF"
        )
        return validador(v)

    @field_validator('senha')
    @classmethod
    def validar_senha_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=6, max_chars=128),
            "Senha"
        )
        return validador(v)

    @field_validator('dataNascimento')
    @classmethod
    def validar_data_nascimento_campo(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_data_nascimento(valor, idade_minima=16),
            "Data de Nascimento"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        """Exemplo de dados para documentação da API"""
        exemplo = {
            "nome": "João Silva Santos",
            "cpf": "123.456.789-01",
            "email": "joao.silva@email.com",
            "senha": "minhasenha123",
            "genero": "masculino",
            "dataNascimento": "1990-05-15",
            "perfil": "paciente"
        }
        exemplo.update(overrides)
        return exemplo


class LoginUsuarioDTO(BaseDTO):
    """
    DTO para login de usuário.
    Usado na autenticação.
    """

    email: str
    senha: str

    @field_validator('email')
    @classmethod
    def validar_email(cls, v: str) -> str:
        if not v:
            raise ValueError('Email é obrigatório')
        if not '@' in v:
            raise ValueError('Email deve conter "@"')
        if not "." in v.split('@')[-1]:
            raise ValueError('Email deve conter domínio válido após "@"')
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_texto_obrigatorio(valor, campo, min_chars=5, max_chars=100),
            "Email"
        )
        return validador(v)
    
    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v: str) -> str:
        if not v:
            raise ValueError('Senha é obrigatória')
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=6, max_chars=128),
            "Senha"
        )
        return validador(v)

    @classmethod
    def criar_exemplo_json(cls, **overrides) -> dict:
        exemplo = {
            "email": "usuario@email.com",
            "senha": "minhasenha123"
        }
        exemplo.update(overrides)
        return exemplo


class AtualizarUsuarioDTO(BaseDTO):
    """
    DTO para atualização de dados do usuário.
    Campos opcionais para atualização parcial.
    """

    nome: Optional[str] = Field(
        None,
        min_length=2,
        max_length=100,
        description="Nome completo"
    )
    genero: Optional[GeneroEnum] = Field(
        None,
        description="Gênero do usuário"
    )

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_nome_pessoa(valor, min_chars=2, max_chars=100),
            "Nome"
        )
        return validador(v)


class AlterarSenhaDTO(BaseDTO):
    """
    DTO para alteração de senha.
    """

    senha_atual: str = Field(
        ...,
        min_length=1,
        description="Senha atual do usuário"
    )
    nova_senha: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Nova senha"
    )
    confirmar_senha: str = Field(
        ...,
        min_length=6,
        max_length=128,
        description="Confirmação da nova senha"
    )

    @field_validator('nova_senha')
    @classmethod
    def validar_nova_senha(cls, v: str) -> str:
        validador = cls.validar_campo_wrapper(
            lambda valor, campo: validar_senha(valor, min_chars=6, max_chars=128),
            "Nova Senha"
        )
        return validador(v)

    @field_validator('confirmar_senha')
    @classmethod
    def senhas_devem_coincidir(cls, v: str, info) -> str:
        if hasattr(info, 'data') and 'nova_senha' in info.data and v != info.data['nova_senha']:
            raise ValueError('Senhas não coincidem')
        return v


# Configurar exemplos JSON nos model_config
CriarUsuarioDTO.model_config.update({
    "json_schema_extra": {
        "example": CriarUsuarioDTO.criar_exemplo_json()
    }
})

LoginUsuarioDTO.model_config.update({
    "json_schema_extra": {
        "example": LoginUsuarioDTO.criar_exemplo_json()
    }
})