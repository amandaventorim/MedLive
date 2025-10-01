# 📋 Implementação de DTOs - MedLive

## 🎯 Resumo da Implementação

DTOs (Data Transfer Objects) implementados para o sistema MedLive seguindo o padrão descrito no `modelo dto/DTO.md`.

### 📁 Estrutura Criada

```
dto/
├── __init__.py              # Imports centralizados
├── base_dto.py              # Classe base (já existia)
├── usuario_dtos.py          # DTOs de usuários
├── medico_dtos.py           # DTOs de médicos
└── paciente_dtos.py         # DTOs de pacientes
```

## 📝 DTOs Implementados

### 👤 **Usuário** (`usuario_dtos.py`)

- **`CriarUsuarioDTO`** - Cadastro base de usuário
  - Validações: nome (2-100 chars), CPF, email, senha (6+ chars), gênero, data nascimento (18+ anos)
  - Enums: `GeneroEnum`, `PerfilEnum`

- **`LoginUsuarioDTO`** - Autenticação
  - Validações: email, senha obrigatória

- **`AtualizarUsuarioDTO`** - Atualização de dados
  - Campos opcionais: nome, gênero

- **`AlterarSenhaDTO`** - Mudança de senha
  - Validações: senha atual, nova senha, confirmação

### 👨‍⚕️ **Médico** (`medico_dtos.py`)

- **`CriarMedicoDTO`** - Herda `CriarUsuarioDTO`
  - Campos extras: CRM (4-20 chars), status profissional
  - Enum: `StatusProfissionalEnum` (ativo, inativo, licença, afastado)
  - Validação CRM: apenas números, letras e traços

- **`AtualizarMedicoDTO`** - Atualização específica
- **`MedicoFiltroDTO`** - Filtros para listagem com paginação

### 👥 **Paciente** (`paciente_dtos.py`)

- **`CriarPacienteDTO`** - Herda `CriarUsuarioDTO`
  - Campos extras: endereço (10-200 chars), convênio (2-100 chars)

- **`AtualizarPacienteDTO`** - Atualização específica
- **`PacienteFiltroDTO`** - Filtros para listagem
- **`AgendarConsultaDTO`** - Agendamento de consultas
  - Validações: data futura, horário comercial (8h-18h)

## 🔧 Rotas Atualizadas

### ✅ **Implementadas com DTOs**

1. **`/cadastro_paciente`** (`routes/paciente/cadastro_paciente.py`)
   - ✅ Validação automática com `CriarPacienteDTO`
   - ✅ Tratamento de erros de validação
   - ✅ Preservação de dados em caso de erro

2. **`/cadastro_medico`** (`routes/medico/cadastro_medico.py`)
   - ✅ Validação automática com `CriarMedicoDTO`
   - ✅ Tratamento de erros de validação
   - ✅ Preservação de dados em caso de erro

3. **`/login`** (`routes/auth_routes.py`)
   - ✅ Validação automática com `LoginUsuarioDTO`
   - ✅ Tratamento de erros de validação

### 🔄 **Próximas Rotas a Atualizar**

- Rotas de atualização de perfil (usar `AtualizarUsuarioDTO`, `AtualizarMedicoDTO`, `AtualizarPacienteDTO`)
- Rotas de alteração de senha (usar `AlterarSenhaDTO`)
- Rotas de listagem com filtros (usar DTOs de filtro)
- Rotas de agendamento (usar `AgendarConsultaDTO`)

## 🎯 Benefícios Alcançados

### 🛡️ **Segurança**
- ✅ Validação automática de CPF
- ✅ Validação de formato de email
- ✅ Validação de data de nascimento (idade mínima)
- ✅ Sanitização de dados de entrada
- ✅ Prevenção de mass assignment

### 🔧 **Manutenibilidade**
- ✅ Validações centralizadas em `util/validacoes_dto.py`
- ✅ DTOs organizados por domínio
- ✅ Reutilização de código através de herança
- ✅ Tratamento consistente de erros

### 📚 **Documentação**
- ✅ Schemas automáticos para API
- ✅ Exemplos JSON para cada DTO
- ✅ Mensagens de erro amigáveis

## 🚀 Como Usar

### **1. Importar DTOs**

```python
from dto import CriarPacienteDTO, CriarMedicoDTO, LoginUsuarioDTO
```

### **2. Validar Dados em Rotas**

```python
@router.post("/endpoint")
async def endpoint(request: Request, dados: dict):
    try:
        # Validação automática
        dto = CriarPacienteDTO(**dados)
        
        # Usar dados validados
        usuario = Usuario(
            nome=dto.nome,
            email=dto.email,
            # ... outros campos
        )
        
    except ValidationError as e:
        # Tratar erros de validação
        erros = [erro['msg'] for erro in e.errors()]
        return {"erro": " | ".join(erros)}
```

### **3. Preservar Dados em Templates**

```python
return templates.TemplateResponse("form.html", {
    "request": request,
    "erro": erro_msg,
    "dados": dados_formulario  # Preservar dados digitados
})
```

## 📋 Checklist de Migração

### ✅ **Concluído**
- [x] Estrutura de DTOs criada
- [x] DTOs básicos implementados
- [x] Rotas principais atualizadas
- [x] Tratamento de erros implementado

### 🔄 **Próximos Passos**
- [ ] Atualizar rotas de atualização de perfil
- [ ] Implementar DTOs para agendamento
- [ ] Adicionar DTOs para consultas médicas
- [ ] Implementar filtros de listagem
- [ ] Adicionar validações específicas do negócio
- [ ] Criar testes unitários para DTOs

## 🐛 Troubleshooting

### **Erro: "Field required"**
- **Causa:** Campo obrigatório não enviado
- **Solução:** Verificar se todos os campos obrigatórios estão sendo enviados do formulário

### **Erro: "Value error, CPF inválido"**
- **Causa:** CPF não passou na validação dos dígitos verificadores
- **Solução:** Verificar se CPF está correto

### **Erro: "ImportError: cannot import name"**
- **Causa:** Erro de importação
- **Solução:** Verificar se o arquivo `dto/__init__.py` está correto

## 📚 Recursos

- **Documentação completa:** `modelo dto/DTO.md`
- **Validações disponíveis:** `util/validacoes_dto.py`
- **Classe base:** `dto/base_dto.py`