import os
import secrets
from fastapi import APIRouter, Request, UploadFile, File, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from util.auth_decorator import requer_autenticacao
from data.repo.usuario_repo import atualizar_foto_usuario
from util.auth_decorator import criar_sessao

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.post("/perfil/alterar-foto")
@requer_autenticacao()
async def alterar_foto(
    request: Request,
    foto: UploadFile = File(...),
    usuario_logado: dict = None
):
    """
    Rota para upload e alteração da foto de perfil do usuário.
    Suporta pacientes e médicos.
    """
    
    # 1. Validar tipo de arquivo
    tipos_permitidos = ["image/jpeg", "image/png", "image/jpg", "image/webp"]
    if foto.content_type not in tipos_permitidos:
        # Redirecionar para a página de perfil apropriada com erro
        if usuario_logado.get('perfil') == 'paciente':
            return RedirectResponse("/perfil_paciente?erro=tipo_invalido", status_code=status.HTTP_303_SEE_OTHER)
        elif usuario_logado.get('perfil') == 'medico':
            return RedirectResponse("/perfil_medico?erro=tipo_invalido", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse("/?erro=tipo_invalido", status_code=status.HTTP_303_SEE_OTHER)

    # 2. Validar tamanho do arquivo (máximo 5MB)
    MAX_SIZE = 5 * 1024 * 1024  # 5MB em bytes
    conteudo = await foto.read()
    if len(conteudo) > MAX_SIZE:
        if usuario_logado.get('perfil') == 'paciente':
            return RedirectResponse("/perfil_paciente?erro=arquivo_muito_grande", status_code=status.HTTP_303_SEE_OTHER)
        elif usuario_logado.get('perfil') == 'medico':
            return RedirectResponse("/perfil_medico?erro=arquivo_muito_grande", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse("/?erro=arquivo_muito_grande", status_code=status.HTTP_303_SEE_OTHER)

    # 3. Criar diretório se não existir
    upload_dir = "static/uploads/usuarios"
    os.makedirs(upload_dir, exist_ok=True)

    # 4. Gerar nome único para evitar conflitos
    extensao = foto.filename.split(".")[-1]
    nome_arquivo = f"{usuario_logado['idUsuario']}_{secrets.token_hex(8)}.{extensao}"
    caminho_arquivo = os.path.join(upload_dir, nome_arquivo)

    # 5. Salvar arquivo no sistema
    try:
        with open(caminho_arquivo, "wb") as f:
            f.write(conteudo)

        # 6. Salvar caminho no banco de dados
        caminho_relativo = f"/static/uploads/usuarios/{nome_arquivo}"
        sucesso = atualizar_foto_usuario(usuario_logado['idUsuario'], caminho_relativo)
        
        if not sucesso:
            # Se falhou ao salvar no banco, remove o arquivo físico
            if os.path.exists(caminho_arquivo):
                os.remove(caminho_arquivo)
            raise Exception("Falha ao atualizar banco de dados")

        # 7. Atualizar sessão do usuário
        usuario_logado['foto'] = caminho_relativo
        criar_sessao(request, usuario_logado)

        # 8. Redirecionar com sucesso
        if usuario_logado.get('perfil') == 'paciente':
            return RedirectResponse("/perfil_paciente?foto_sucesso=1", status_code=status.HTTP_303_SEE_OTHER)
        elif usuario_logado.get('perfil') == 'medico':
            return RedirectResponse("/perfil_medico?foto_sucesso=1", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse("/?foto_sucesso=1", status_code=status.HTTP_303_SEE_OTHER)

    except Exception as e:
        # Em caso de erro, limpar arquivo se foi criado
        if os.path.exists(caminho_arquivo):
            try:
                os.remove(caminho_arquivo)
            except:
                pass
        
        print(f"Erro ao alterar foto: {e}")
        
        # Redirecionar com erro
        if usuario_logado.get('perfil') == 'paciente':
            return RedirectResponse("/perfil_paciente?erro=upload_falhou", status_code=status.HTTP_303_SEE_OTHER)
        elif usuario_logado.get('perfil') == 'medico':
            return RedirectResponse("/perfil_medico?erro=upload_falhou", status_code=status.HTTP_303_SEE_OTHER)
        else:
            return RedirectResponse("/?erro=upload_falhou", status_code=status.HTTP_303_SEE_OTHER)
