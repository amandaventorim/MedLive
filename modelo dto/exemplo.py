

@router.get("/cadastrar")
@requer_autenticacao(["admin"])
async def get_cadastrar(request: Request, usuario_logado: dict = None):
    response = templates.TemplateResponse("cadastrar.html", {"request": request})
    return response


@router.post("/cadastrar")
@requer_autenticacao(["admin"])
async def post_cadastrar(
    request: Request, 
    nome: str = Form(...),
    usuario_logado: dict = None):
    # guarda os dados originais do formulário
    dados_formulario = {
        "nome": nome
    }
    try:
        # Validar dados com Pydantic
        dados = CriarCategoriaDTO(nome=nome)
        # Criar objeto Categoria
        nova_categoria = Categoria(id=0, nome=dados.nome)
        # Processar cadastro
        categoria_repo.inserir(nova_categoria)
        # Sucesso - Redirecionar com mensagem flash
        informar_sucesso(request, f"Categoria cadastrada com sucesso!")
        return RedirectResponse("/admin/categorias", status_code=303)
    except ValidationError as e:
        # Extrair mensagens de erro do Pydantic
        erros = []
        for erro in e.errors():
            # Pegar apenas a mensagem customizada, removendo prefixos do Pydantic
            mensagem = erro['msg']
            # Se a mensagem começa com "Value error, ", remove esse prefixo
            if mensagem.startswith("Value error, "):
                mensagem = mensagem.replace("Value error, ", "")
            erros.append(mensagem)
        erro_msg = " | ".join(erros)
        # logger.warning(f"Erro de validação no cadastro: {erro_msg}")
        # Retornar template com dados preservados e erro
        informar_erro(request, "Há erros no formulário.")
        return templates.TemplateResponse("cadastrar.html", {
            "request": request,
            "erro": erro_msg,
            "dados": dados_formulario  # Preservar dados digitados
        })
    except Exception as e:
        # logger.error(f"Erro ao processar cadastro: {e}")
        return templates.TemplateResponse("cadastrar.html", {
            "request": request,
            "erro": "Erro ao processar cadastro. Tente novamente.",
            "dados": dados_formulario
        })
