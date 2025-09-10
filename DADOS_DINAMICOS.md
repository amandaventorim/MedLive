# Dados Dinâmicos - MedLive

## Alterações realizadas para tornar dados dinâmicos:

### 1. **Dashboard Paciente** ✅
- `templates/paciente/dashboard_paciente.html` linha 14: `{{ usuario.nome }}`
- `templates/base_paciente.html` navbar: `{{ usuario.nome }}`

### 2. **Dashboard Médico** ✅  
- `templates/medico/dashboard_medico.html` linha 14: `{{ usuario.nome }}`
- `templates/base_medico.html` navbar: `{{ usuario.nome }}`

### 3. **Dashboard Admin** ✅
- `templates/admin/dashboard_admin.html` linha 14: `{{ usuario.nome }}`

### 4. **Perfil Paciente** ✅
- Nome no cabeçalho: `{{ usuario.nome }}`
- Data nascimento: `{{ usuario.dataNascimento }}`
- Email: `{{ usuario.email }}`

### 5. **Perfil Médico** ✅
- Nome no cabeçalho: `{{ usuario.nome }}`
- Email: `{{ usuario.email }}`

### 6. **Prontuário** ✅
- Nome: `{{ usuario.nome }}`
- CPF: `{{ usuario.cpf }}`
- Data nascimento: `{{ usuario.dataNascimento }}`

## Dados que ainda precisam ser dinâmicos:

### **Sala de Consulta**
- `templates/sala_consulta.html`:
  - Linha 23: Nome do paciente na consulta
  - Linha 53: Nome do participante
  - Linha 61: Nome do médico
  - Linhas 130, 279, 335: Formulários com nomes

### **Dashboard Médico - Próximas consultas**
- `templates/medico/dashboard_medico.html`:
  - Linha 16: Nome do próximo paciente
  - Linha 119: Nome do paciente João Silva
  - Linha 173: Nome do paciente Maria Santos

### **Dashboard Paciente - Consultas**
- `templates/paciente/dashboard_paciente.html`:
  - Linha 100: Nome do médico Dr. Carlos Silva

### **Admin Dashboard - Listas**
- `templates/admin/dashboard_admin.html`:
  - Médicos: linhas 114, 168 (nomes dos médicos)
  - Pacientes: linhas 221, 248 (nomes dos pacientes)

### **Agendamento**
- `templates/paciente/agendar_consulta.html`:
  - Linhas 28, 121: Nome do médico selecionado

## Para implementar:

1. **Consultas**: Criar loop `{% for consulta in consultas %}` e usar `{{ consulta.paciente.nome }}`, `{{ consulta.medico.nome }}`

2. **Listas Admin**: Criar loops para médicos e pacientes do banco

3. **Sala Consulta**: Passar dados da consulta atual via context

4. **Agendamento**: Usar JavaScript para preencher dados do médico selecionado

## Estrutura do Context necessária:

```python
# Para consultas
context = {
    "request": request,
    "usuario": usuario_logado,
    "consultas": lista_consultas,
    "proxima_consulta": proxima_consulta
}

# Para listas admin  
context = {
    "request": request,
    "usuario": usuario_logado,
    "medicos": lista_medicos,
    "pacientes": lista_pacientes
}
```
