# 🩺 Guia de Cadastro - MedLive

## ❌ Problema Identificado

Você encontrou um erro silencioso no cadastro porque:

1. **Nome "paciente1"** - ❌ **Inválido**
   - A validação exige **nome completo** (pelo menos nome e sobrenome)
   - Exemplo válido: "João Silva", "Maria Santos", "Ana Paula Costa"

2. **CPF inválido** - ❌ **Números de exemplo não funcionam**
   - O sistema valida os dígitos verificadores do CPF
   - CPFs como "123.456.789-01" são matematicamente inválidos

## ✅ Como Corrigir

### 📝 **Nome Válido**
- ✅ **Correto:** "João Silva Santos"
- ✅ **Correto:** "Maria dos Santos"
- ✅ **Correto:** "Ana Paula Costa"
- ❌ **Errado:** "paciente1" (apenas uma palavra)
- ❌ **Errado:** "João" (apenas nome)

### 🆔 **CPF Válido para Teste**
Use um destes CPFs válidos para teste:
- ✅ **11144477735**
- ✅ **22233344456**
- ✅ **33322211167**
- ✅ **44455566678**
- ✅ **55566677789**

### 📧 **Email**
- ✅ **Correto:** "joao@email.com"
- ✅ **Correto:** "maria.silva@gmail.com"
- ❌ **Errado:** "email-sem-arroba"

### 🔒 **Senha**
- Mínimo de **6 caracteres**
- Exemplo: "senha123", "minhasenha"

### 📅 **Data de Nascimento**
- Formato: **YYYY-MM-DD** (ex: 1990-05-15)
- Idade mínima: **16 anos**
- ❌ **Errado:** 2020-01-01 (menor de idade)
- ✅ **Correto:** 1990-05-15

### 🏠 **Endereço**
- Mínimo de **10 caracteres**
- ✅ **Correto:** "Rua das Flores, 123 - Centro - São Paulo - SP"
- ❌ **Errado:** "Rua 123" (muito curto)

## 🔧 Melhorias Implementadas

1. **✅ Mensagens de erro agora aparecem** no topo do formulário
2. **✅ Dados digitados são preservados** em caso de erro
3. **✅ Mensagens mais claras** sobre o que está errado
4. **✅ Logs de debug** para identificar problemas

## 🧪 Exemplo de Teste Completo

```
Nome: João Silva Santos
CPF: 11144477735
Email: joao@teste.com
Senha: senha123
Gênero: masculino
Data de Nascimento: 1990-05-15
Endereço: Rua das Flores, 123 - Centro - São Paulo - SP
Convênio: Unimed Nacional
```

## 🚀 Como Testar Agora

1. **Acesse:** `/cadastro_paciente`
2. **Use dados válidos** (exemplo acima)
3. **Se houver erro:** A mensagem aparecerá no topo em vermelho
4. **Se houver sucesso:** Será redirecionado para `/login`

## 📊 Debug Console

Os logs agora mostram no console:
- ✅ "DEBUG: DTO criado com sucesso"
- ❌ "DEBUG: Erro de validação capturado"
- 📝 Detalhes específicos de cada erro

---

**Agora o sistema está funcionando corretamente com validações visíveis!** ✨