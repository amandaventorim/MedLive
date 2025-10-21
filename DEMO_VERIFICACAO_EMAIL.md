# Verificação de Email - Modo Demonstração

## 📧 Funcionalidade Implementada

Durante o cadastro de paciente, após preencher os dados da **Etapa 1** (nome, CPF, email e senha), o sistema agora:

1. **Gera um código de verificação** de 6 dígitos
2. **Exibe o código na tela** (modo demonstração - em produção seria enviado por email)
3. **Valida o código** digitado pelo usuário
4. **Permite reenvio** do código caso necessário

## 🎯 Como Funciona (Demonstração)

### Fluxo do Usuário:

1. Preenche os dados básicos no cadastro
2. Clica em "Continuar"
3. É direcionado para tela de verificação de email
4. **Um alerta amarelo aparece mostrando o código** (ex: "123456")
5. Pode copiar o código clicando no botão "Copiar" ou digitar manualmente
6. Clica em "Verificar"
7. Se correto, avança para próxima etapa

### Recursos de Segurança:

- ✅ Código expira em **10 minutos**
- ✅ Máximo de **5 tentativas** por código
- ✅ Botão de reenvio com **cooldown de 30 segundos**
- ✅ Validação de 6 dígitos obrigatória

## 🔧 Implementação Técnica

### Backend (FastAPI)

**Arquivo:** `routes/paciente/cadastro_paciente.py`

**Novos Endpoints:**

```python
POST /gerar_codigo_verificacao
- Gera código aleatório de 6 dígitos
- Armazena em memória com timestamp de expiração
- Retorna código para demonstração (em produção, enviaria email)

POST /verificar_codigo
- Valida o código digitado
- Verifica expiração e número de tentativas
- Retorna sucesso/erro
```

**Armazenamento Temporário:**
```python
verification_codes = {
    "email@exemplo.com": {
        "codigo": "123456",
        "expiracao": datetime,
        "tentativas": 0
    }
}
```

### Frontend (JavaScript)

**Arquivo:** `static/js/cadastro_paciente.js`

**Funções Implementadas:**

- `enviarCodigoVerificacao(email)` - Chama endpoint para gerar código
- `mostrarCodigoDemo(codigo)` - Exibe alerta com código na tela
- `copiarCodigo(codigo)` - Copia e cola automaticamente no campo
- `verifyEmailCode()` - Valida código com backend
- `resendEmailCode()` - Reenvia código com cooldown

### Estilos (CSS)

**Arquivo:** `static/css/cadastro_paciente.css`

- Animações suaves (fadeIn, fadeInDown)
- Destaque visual para o código
- Feedback visual de sucesso/erro

## 🚀 Para Produção

Para usar em produção com envio real de email, você precisaria:

### 1. Escolher um Serviço de Email

**Opção A: Gmail SMTP**
```python
import smtplib
from email.mime.text import MIMEText

def enviar_email(destinatario, codigo):
    msg = MIMEText(f"Seu código de verificação é: {codigo}")
    msg['Subject'] = 'Código de Verificação - MedLive'
    msg['From'] = 'seu-email@gmail.com'
    msg['To'] = destinatario
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('seu-email@gmail.com', 'sua-senha-app')
        smtp.send_message(msg)
```

**Opção B: SendGrid (Recomendado)**
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def enviar_email(destinatario, codigo):
    message = Mail(
        from_email='noreply@medlive.com',
        to_emails=destinatario,
        subject='Código de Verificação - MedLive',
        html_content=f'<strong>Seu código é: {codigo}</strong>'
    )
    sg = SendGridAPIClient('SUA_API_KEY')
    sg.send(message)
```

**Opção C: AWS SES, Mailgun, etc.**

### 2. Modificar o Endpoint

```python
@router.post("/gerar_codigo_verificacao")
async def gerar_codigo_verificacao(request: Request):
    # ... código existente ...
    
    # Em produção, remover isso:
    # "demo_code": codigo
    
    # E adicionar:
    # enviar_email(email, codigo)
    
    return JSONResponse({
        "success": True,
        "message": "Código enviado para seu email"
        # NÃO retornar o código!
    })
```

### 3. Usar Banco de Dados

Em vez de `verification_codes = {}` em memória, usar Redis ou tabela no banco:

```python
# Redis
import redis
r = redis.Redis(host='localhost', port=6379, db=0)
r.setex(f"verification:{email}", 600, codigo)  # 600s = 10min

# Ou tabela SQL
CREATE TABLE verification_codes (
    email VARCHAR(255) PRIMARY KEY,
    codigo VARCHAR(6),
    expiracao TIMESTAMP,
    tentativas INT
);
```

## 📝 Notas

- **Demonstração:** O código é exibido na tela para facilitar testes
- **Produção:** Remover `demo_code` do response e implementar envio real
- **Segurança:** Códigos em memória são perdidos ao reiniciar servidor (usar Redis/banco)
- **Logs:** Sistema registra códigos gerados no console para debug

## 🎨 Interface

A tela de verificação mostra:
- 📧 Ícone de envelope
- Email para onde o código "foi enviado"
- Campo para digitar código (6 dígitos)
- Alerta amarelo com o código (APENAS DEMO)
- Botões: Alterar email | Reenviar | Verificar

## 🧪 Como Testar

1. Acesse: http://127.0.0.1:8000/cadastro_paciente
2. Preencha os dados da etapa 1
3. Clique em "Continuar"
4. Veja o código aparecer em alerta amarelo
5. Digite ou copie o código
6. Clique em "Verificar"
7. Teste também:
   - Código errado (mostra tentativas restantes)
   - Reenvio (gera novo código)
   - Expiração (aguarde 10 minutos - ou reduza tempo no código)

---

**Desenvolvido para fins de demonstração do projeto MedLive**
