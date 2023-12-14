from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    Path,
    Request,
    status,
)
from fastapi.templating import Jinja2Templates
from models.Cliente import Cliente
from models.Usuario import Usuario
from repositories.ClienteRepo import ClienteRepo
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado

router = APIRouter(prefix="/cliente")
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_index(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    clientes = ClienteRepo.obter_todos()
    
    return templates.TemplateResponse(
        "cliente/index.html",
        {"request": request, "usuario": usuario, "clientes": clientes},
    )

@router.get("/inserir")
async def get_inserir(
    request: Request,
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    return templates.TemplateResponse(
        "cliente/inserir.html",
        {"request": request, "usuario": usuario},
    )

@router.post("/inserir")
async def post_inserir(
    nome: str = Form(...),
    endereco: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(...),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    cliente = Cliente(nome=nome,endereco=endereco,telefone=telefone,email=email)  
    cliente = ClienteRepo.inserir(cliente)

    response = redirecionar_com_mensagem("/cliente", "Cliente inserido com sucesso!")
    return response

@router.get("/excluir/{id_cliente:int}")
async def get_excluir(
    request: Request,
    id_cliente: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    cliente = ClienteRepo.obter_por_id(id_cliente)

    return templates.TemplateResponse(
        "cliente/excluir.html",
        {"request": request, "usuario": usuario, "cliente": cliente},
    )

@router.post("/excluir/{id_cliente:int}")
async def post_excluir(
    id_cliente: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ClienteRepo.excluir(id_cliente)

    response = redirecionar_com_mensagem("/cliente", "Cliente excluído com sucesso!")
    return response

@router.get("/alterar/{id_cliente:int}")
async def get_alterar(
    request: Request,
    id_cliente: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    cliente = ClienteRepo.obter_por_id(id_cliente)

    return templates.TemplateResponse(
        "cliente/alterar.html",
        {"request": request, "usuario": usuario, "cliente": cliente},
    )

@router.post("/alterar/{id_cliente:int}")
async def post_alterar(
    id_cliente: int = Path(),
    nome: str = Form(...),
    endereco: str = Form(...),
    telefone: str = Form(...),
    email: str = Form(...),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ClienteRepo.alterar(Cliente(id_cliente,nome,endereco,telefone,email))

    response = redirecionar_com_mensagem("/cliente", "Cliente alterado com sucesso!")
    return response