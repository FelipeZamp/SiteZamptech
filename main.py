from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from util.seguranca import atualizar_cookie_autenticacao
from util.excecoes import configurar_paginas_de_erro
from repositories.UsuarioRepo    import UsuarioRepo
from repositories.OrdemRepo      import OrdemRepo
from repositories.ClienteRepo    import ClienteRepo
from repositories.ServicoRepo    import ServicoRepo
from repositories.ProdutoRepo    import ProdutoRepo
from repositories.FornecedorRepo import FornecedorRepo

from routes.RootRouter       import router as rootRouter
from routes.UsuarioRouter    import router as usuarioRouter
from routes.GestaoRouter     import router as gestaoRouter
from routes.OrdemRouter      import router as ordemRouter
from routes.ClienteRouter    import router as clienteRouter
from routes.ServicoRouter    import router as servicoRouter
from routes.ProdutoRouter    import router as produtoRouter
from routes.FornecedorRouter import router as fornecedorRouter


UsuarioRepo.criar_tabela()
UsuarioRepo.criar_administrador_padrao()
UsuarioRepo.criar_usuario_padrao()
OrdemRepo.criar_tabela()
ClienteRepo.criar_tabela()
ServicoRepo.criar_tabela()
ProdutoRepo.criar_tabela()
FornecedorRepo.criar_tabela()

app = FastAPI()
app.middleware("http")(atualizar_cookie_autenticacao)
configurar_paginas_de_erro(app)

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
app.include_router(rootRouter)
app.include_router(usuarioRouter)
app.include_router(gestaoRouter)
app.include_router(ordemRouter)
app.include_router(clienteRouter)
app.include_router(servicoRouter)
app.include_router(produtoRouter)
app.include_router(fornecedorRouter)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8001)
