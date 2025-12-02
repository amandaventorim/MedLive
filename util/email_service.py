import os
import resend
from typing import Optional

class EmailService:
    def __init__(self):
        # Carregar variáveis de ambiente
        from dotenv import load_dotenv
        load_dotenv()
        
        self.api_key = os.getenv('RESEND_API_KEY')
        self.from_email = os.getenv('RESEND_FROM_EMAIL', 'noreply@seudominio.com')
        self.from_name = os.getenv('RESEND_FROM_NAME', 'MedLive Sistema')
        self.debug = os.getenv('EMAIL_DEBUG', 'true').lower() == 'true'

        # Configura a API key do Resend
        if self.api_key:
            resend.api_key = self.api_key
            if self.debug:
                print(f"✅ Resend configurado com sucesso")
                print(f"   API Key: {self.api_key[:10]}...")
                print(f"   From: {self.from_name} <{self.from_email}>")
        else:
            print("❌ RESEND_API_KEY não encontrada!")
            print("💡 Configure no arquivo .env: RESEND_API_KEY=sua_chave_aqui")
            print("💡 Obtenha sua chave em: https://resend.com/api-keys")

    def enviar_email(
        self,
        para_email: str,
        para_nome: str,
        assunto: str,
        html: str,
        texto: Optional[str] = None
    ) -> bool:
        """Envia e-mail via Resend.com"""
        if self.debug:
            print(f"\n📧 Tentando enviar email:")
            print(f"   Para: {para_email}")
            print(f"   Assunto: {assunto}")
            print(f"   From: {self.from_name} <{self.from_email}>")
        
        if not self.api_key:
            print("❌ RESEND_API_KEY não configurada")
            print("💡 Configure sua chave do Resend no arquivo .env")
            return False

        params = {
            "from": f"{self.from_name} <{self.from_email}>",
            "to": [para_email],
            "subject": assunto,
            "html": html
        }
        
        if self.debug:
            print(f"📤 Enviando via Resend API...")

        try:
            email = resend.Emails.send(params)  # type: ignore[arg-type]
            email_id = email.get('id', 'N/A')
            print(f"✅ Email enviado com sucesso!")
            print(f"   ID: {email_id}")
            print(f"   Para: {para_email}")
            return True
        except Exception as e:
            print(f"❌ Erro ao enviar email:")
            print(f"   Erro: {str(e)}")
            print(f"   Tipo: {type(e).__name__}")
            if 'unauthorized' in str(e).lower():
                print("💡 Verifique se sua RESEND_API_KEY está correta")
            elif 'domain' in str(e).lower():
                print(f"💡 Verifique se o domínio '{self.from_email.split('@')[1]}' está verificado no Resend")
            return False

    def enviar_recuperacao_senha(self, para_email: str, para_nome: str, token: str) -> bool:
        """Envia e-mail de recuperação de senha"""
        url_recuperacao = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/redefinir-senha?token={token}"

        html = f"""
        <html>
        <body>
            <h2>Recuperação de Senha</h2>
            <p>Olá {para_nome},</p>
            <p>Você solicitou a recuperação de senha.</p>
            <p>Clique no link abaixo para redefinir sua senha:</p>
            <a href="{url_recuperacao}">Redefinir Senha</a>
            <p>Este link expira em 1 hora.</p>
            <p>Se você não solicitou esta recuperação, ignore este e-mail.</p>
        </body>
        </html>
        """

        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Recuperação de Senha",
            html=html
        )

    def enviar_boas_vindas(self, para_email: str, para_nome: str) -> bool:
        """Envia e-mail de boas-vindas"""
        html = f"""
        <html>
        <body>
            <h2>Bem-vindo(a)!</h2>
            <p>Olá {para_nome},</p>
            <p>Seu cadastro foi realizado com sucesso!</p>
            <p>Agora você pode acessar o sistema com seu e-mail e senha.</p>
        </body>
        </html>
        """

        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Bem-vindo ao Sistema",
            html=html
        )

    def enviar_codigo_verificacao(self, para_email: str, para_nome: str, codigo: str) -> bool:
        """Envia e-mail com código de verificação de 6 dígitos"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background: linear-gradient(135deg, #001942 0%, #003366 100%);
                    padding: 30px;
                    border-radius: 10px;
                    color: white;
                    text-align: center;
                }}
                .code-box {{
                    background-color: white;
                    color: #001942;
                    padding: 20px;
                    border-radius: 8px;
                    margin: 20px 0;
                    font-size: 32px;
                    font-weight: bold;
                    letter-spacing: 8px;
                }}
                .footer {{
                    margin-top: 20px;
                    font-size: 14px;
                    color: #f0f0f0;
                }}
                .logo {{
                    font-size: 28px;
                    font-weight: bold;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">🏥 MedLive</div>
                <h2>Verificação de Email</h2>
                <p>Olá, {para_nome}!</p>
                <p>Use o código abaixo para verificar seu email e concluir seu cadastro:</p>
                
                <div class="code-box">
                    {codigo}
                </div>
                
                <p>Este código é válido por <strong>5 minutos</strong>.</p>
                
                <div class="footer">
                    <p>Se você não solicitou este código, ignore este email.</p>
                    <p>© 2025 MedLive - Sistema de Gestão Médica</p>
                </div>
            </div>
        </body>
        </html>
        """

        return self.enviar_email(
            para_email=para_email,
            para_nome=para_nome,
            assunto="Código de Verificação - MedLive",
            html=html
        )

# Instância global
email_service = EmailService()