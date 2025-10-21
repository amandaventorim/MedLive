# 🎯 Guia Rápido - Verificação de Email

## Como Funciona na Demonstração

### Passo 1: Cadastro Inicial
```
┌─────────────────────────────────┐
│  📝 Cadastro de Paciente       │
├─────────────────────────────────┤
│ Nome: [João Silva]              │
│ CPF: [123.456.789-09]           │
│ Email: [joao@email.com]         │
│ Senha: [******]                 │
│                                 │
│        [  Continuar  ]          │
└─────────────────────────────────┘
```

### Passo 2: Verificação de Email
```
┌─────────────────────────────────────────┐
│  📧 Verifique seu email                │
│                                         │
│  Enviamos um código para:              │
│  joao@email.com                        │
├─────────────────────────────────────────┤
│                                         │
│  Código: [ 1 2 3 4 5 6 ]               │
│                                         │
│  ⚠️  MODO DEMONSTRAÇÃO:                │
│  Seu código é: 123456  [📋 Copiar]    │
│                                         │
├─────────────────────────────────────────┤
│ [Alterar email] [Reenviar] [Verificar] │
└─────────────────────────────────────────┘
```

### Passo 3: Validação
```
✅ Código CORRETO
   → Avança para próxima etapa

❌ Código ERRADO
   → "Código incorreto. Você tem 4 tentativa(s) restante(s)"

⏰ Código EXPIRADO (após 10 min)
   → "Código expirado. Solicite um novo código"

🚫 Muitas tentativas (5+)
   → "Número máximo de tentativas excedido"
```

## Recursos Implementados

| Recurso | Descrição |
|---------|-----------|
| 🎲 **Geração de Código** | Código aleatório de 6 dígitos (100000-999999) |
| ⏱️ **Expiração** | 10 minutos após geração |
| 🔢 **Tentativas** | Máximo de 5 tentativas incorretas |
| 🔄 **Reenvio** | Cooldown de 30 segundos entre reenvios |
| 📋 **Copiar** | Botão para copiar e colar automaticamente |
| ✏️ **Alterar Email** | Voltar e corrigir o email digitado |

## Endpoints da API

### Gerar Código
```http
POST /gerar_codigo_verificacao
Content-Type: application/json

{
  "email": "usuario@email.com"
}

Response (200):
{
  "success": true,
  "message": "Código gerado com sucesso",
  "demo_code": "123456"  // APENAS EM DEMO
}
```

### Verificar Código
```http
POST /verificar_codigo
Content-Type: application/json

{
  "email": "usuario@email.com",
  "codigo": "123456"
}

Response (200):
{
  "success": true,
  "message": "Email verificado com sucesso!"
}

Response (400 - erro):
{
  "success": false,
  "message": "Código incorreto. Você tem 4 tentativa(s) restante(s)"
}
```

## Fluxo de Estados

```
┌──────────────┐
│  Etapa 1:    │
│ Dados Básicos│
└──────┬───────┘
       │ Validação OK
       ↓
┌──────────────┐
│  Etapa 1.5:  │
│ Verificação  │◄────┐
│   de Email   │     │ Reenviar
└──────┬───────┘     │
       │             │
       │ Código OK   │
       ↓             │
┌──────────────┐     │
│  Etapa 2:    │     │
│   Gênero e   │     │
│    Data      │     │
└──────┬───────┘     │
       │             │
       ↓             │
┌──────────────┐     │
│  Etapa 3:    │     │
│  Endereço e  │     │
│   Convênio   │     │
└──────────────┘     │
                     │
       [Alterar]─────┘
```

## Dados Armazenados (Temporário)

```python
verification_codes = {
    "joao@email.com": {
        "codigo": "123456",           # Código gerado
        "expiracao": datetime(...),   # 10 minutos à frente
        "tentativas": 0               # Contador de erros
    }
}
```

## Console de Debug

Durante a execução, você verá no terminal:

```
[DEMO] Código de verificação gerado para joao@email.com: 123456
```

## Customização Rápida

### Alterar tempo de expiração:
```python
# Em cadastro_paciente.py
expiracao = datetime.now() + timedelta(minutes=10)  # Mude 10 para o valor desejado
```

### Alterar máximo de tentativas:
```python
# Em cadastro_paciente.py
if dados_verificacao["tentativas"] >= 5:  # Mude 5 para o valor desejado
```

### Alterar cooldown de reenvio:
```javascript
// Em cadastro_paciente.js
setTimeout(() => { ... }, 30000);  // 30000ms = 30s
```

## Teste Rápido

### Teste 1: Fluxo Normal ✅
1. Cadastro → Continuar
2. Ver código na tela
3. Copiar código
4. Verificar → Sucesso

### Teste 2: Código Errado ❌
1. Digite código incorreto (ex: 000000)
2. Veja mensagem de erro com tentativas restantes
3. Tente novamente com código correto

### Teste 3: Reenvio 🔄
1. Clique em "Reenviar"
2. Veja botão ficar desabilitado por 30s
3. Novo código é gerado

### Teste 4: Alterar Email ✏️
1. Clique em "Alterar email"
2. Volta para Etapa 1
3. Modifique o email
4. Continue novamente

---

**🎓 Dica para Apresentação:**
Durante a demo, mencione que:
- O código aparece na tela "para facilitar a demonstração"
- Em produção, seria enviado por email usando SendGrid/Gmail
- Sistema tem segurança: expiração, limite de tentativas, etc.
