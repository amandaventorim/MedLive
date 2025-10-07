# CPFs Válidos para Teste

Para testar o sistema de cadastro, use um dos CPFs válidos abaixo:

## CPFs Numéricos (sem máscara)
- `12345678909`
- `98765432100` 
- `45678912364`
- `78912345664`
- `32165498791`

## CPFs Formatados (com máscara)
- `123.456.789-09`
- `987.654.321-00`
- `456.789.123-64`
- `789.123.456-64`
- `321.654.987-91`

## Outros Requisitos

### Endereço
- **Mínimo**: 10 caracteres
- **Exemplos válidos**:
  - `Rua A, 123`
  - `Avenida Paulista, 1000`
  - `Rua das Flores, 456 - Centro`

### Nome
- **Formato**: Nome e sobrenome (sem títulos como "Dr.")
- **Exemplos válidos**:
  - `João Silva Santos`
  - `Maria Oliveira`
  - `Carlos Ferreira Silva`

### Data de Nascimento
- **Idade mínima**: 16 anos
- **Formato**: YYYY-MM-DD
- **Exemplo**: `1990-05-15`

### Gênero
- `masculino`
- `feminino` 
- `outros`

### Status Profissional (apenas médicos)
- `ativo`
- `inativo`
- `licenca`
- `afastado`

## Exemplo de Cadastro Completo

### Paciente
```
Nome: Maria Santos Silva
CPF: 123.456.789-09
Email: maria@teste.com
Senha: senha123
Gênero: feminino
Data de Nascimento: 1995-03-20
Endereço: Rua das Flores, 456 - Centro - Rio de Janeiro - RJ
Convênio: Unimed
```

### Médico
```
Nome: Carlos Silva Santos
CPF: 987.654.321-00
Email: carlos@teste.com
Senha: senha123
Gênero: masculino
Data de Nascimento: 1980-05-15
CRM: CRM123456-SP
Status Profissional: ativo
```