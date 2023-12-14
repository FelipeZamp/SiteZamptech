from fastapi import APIRouter, Depends, Form, Query, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.Usuario import Usuario
from repositories.UsuarioRepo import UsuarioRepo
from util.mensagem import adicionar_cookie_mensagem, redirecionar_com_mensagem
from util.seguranca import adicionar_cookie_autenticacao, conferir_senha, excluir_cookie_autenticacao, gerar_token, obter_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_root(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    return templates.TemplateResponse(
        "root/index.html",
        {"request": request, "usuario": usuario},
    )

@router.get("/login", response_class=HTMLResponse)
async def get_login(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
):
    return templates.TemplateResponse(
        "root/login.html",
        {"request": request, "usuario": usuario},
    )

@router.post("/login", response_class=RedirectResponse)
async def post_login(
    email: str = Form(...),
    senha: str = Form(...),
    return_url: str = Query("/"),
):
    hash_senha_bd = UsuarioRepo.obter_senha_por_email(email)
    if conferir_senha(senha, hash_senha_bd):
        token = gerar_token()
        UsuarioRepo.alterar_token_por_email(token, email)
        response = RedirectResponse(return_url, status.HTTP_302_FOUND)
        adicionar_cookie_autenticacao(response, token)
        adicionar_cookie_mensagem(response, "Login realizado com sucesso.")
    else:
        response = redirecionar_com_mensagem(
            "/login",
            "Credenciais inválidas. Tente novamente.",
        )
    return response

@router.get("/logout")
async def get_logout(usuario: Usuario = Depends(obter_usuario_logado)):
    if usuario:
        UsuarioRepo.alterar_token_por_email("", usuario.email)
        response = RedirectResponse("/", status.HTTP_302_FOUND)
        excluir_cookie_autenticacao(response)
        adicionar_cookie_mensagem(response, "Saída realizada com sucesso.")
        return response
    
@router.get("/servicos", response_class=HTMLResponse)
async def getServicos(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    return templates.TemplateResponse("root/servicos.html", {"request": request, "usuario": usuario})

@router.get("/contato", response_class=HTMLResponse)
def getContato(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    return templates.TemplateResponse("root/contato.html", {"request": request, "usuario": usuario})

@router.get("/sobrenos", response_class=HTMLResponse)
def getSobrenos(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    return templates.TemplateResponse("root/sobrenos.html", {"request": request, "usuario": usuario})

