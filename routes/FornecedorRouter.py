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
from models.Fornecedor import Fornecedor
from models.Usuario import Usuario
from repositories.FornecedorRepo import FornecedorRepo
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado

router = APIRouter(prefix="/fornecedor")
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
    
    fornecedores = FornecedorRepo.obter_todos()
    
    return templates.TemplateResponse(
        "fornecedor/index.html",
        {"request": request, "usuario": usuario, "fornecedores": fornecedores},
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
        "fornecedor/inserir.html",
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

    fornecedor = Fornecedor(nome=nome,endereco=endereco,telefone=telefone,email=email)  
    fornecedor = FornecedorRepo.inserir(fornecedor)

    response = redirecionar_com_mensagem("/fornecedor", "Fornecedor inserido com sucesso!")
    return response

@router.get("/excluir/{id_fornecedor:int}")
async def get_excluir(
    request: Request,
    id_fornecedor: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    fornecedor = FornecedorRepo.obter_por_id(id_fornecedor)

    return templates.TemplateResponse(
        "fornecedor/excluir.html",
        {"request": request, "usuario": usuario, "fornecedor": fornecedor},
    )

@router.post("/excluir/{id_fornecedor:int}")
async def post_excluir(
    id_fornecedor: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    FornecedorRepo.excluir(id_fornecedor)

    response = redirecionar_com_mensagem("/fornecedor", "Fornecedor excluído com sucesso!")
    return response

@router.get("/alterar/{id_fornecedor:int}")
async def get_alterar(
    request: Request,
    id_fornecedor: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    fornecedor = FornecedorRepo.obter_por_id(id_fornecedor)

    return templates.TemplateResponse(
        "fornecedor/alterar.html",
        {"request": request, "usuario": usuario, "fornecedor": fornecedor},
    )

@router.post("/alterar/{id_fornecedor:int}")
async def post_alterar(
    id_fornecedor: int = Path(),
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

    FornecedorRepo.alterar(Fornecedor(id_fornecedor,nome,endereco,telefone,email))

    response = redirecionar_com_mensagem("/fornecedor", "Fornecedor alterado com sucesso!")
    return response