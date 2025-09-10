# criar_admin.py
from util.security import criar_hash_senha
from data.repo import administrador_repo, usuario_repo
from data.model.usuario_model import Usuario

def criar_admin_padrao():
    # Verificar se já existe admin
    admins = usuario_repo.obter_todos_usuarios_por_perfil("admin")
    if not admins:
        senha_hash = criar_hash_senha("admin123")
        admin = Usuario(
            idUsuario=0,
            nome="Administrador",
            cpf="00000000000",
            email="admin@admin.com",
            senha=senha_hash,
            genero="Outro",
            dataNascimento="1970-01-01",
            perfil="admin",
            foto=None,
            token_redefinicao=None,
            data_token=None,
            data_cadastro=None,
        )
        administrador_repo.inserir_administrador(admin)
        print("Admin criado: admin@admin.com / admin123")

if __name__ == "__main__":
    criar_admin_padrao()

