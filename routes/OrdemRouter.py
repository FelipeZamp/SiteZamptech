from io import BytesIO
import os
from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Path,
    Request,
    UploadFile,
    status,
)
from fastapi.templating import Jinja2Templates
from models.Ordem import Ordem
from models.Usuario import Usuario
from repositories.OrdemRepo import OrdemRepo
from util.imagem import transformar_em_quadrada
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado
from PIL import Image

router = APIRouter(prefix="/ordem")
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
    
    ordens = OrdemRepo.obter_todos()
    
    return templates.TemplateResponse(
        "ordem/index.html",
        {"request": request, "usuario": usuario, "ordens": ordens},
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
        "ordem/inserir.html",
        {"request": request, "usuario": usuario},
    )

@router.post("/inserir")
async def post_inserir(
    cliente: str = Form(...),
    servico: str = Form(...),
    status: str = Form(...),
    desc: str = Form(...),
    arquivoImagem: UploadFile = File(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ordem = Ordem(cliente=cliente,servico=servico,status=status,desc=desc)  
    ordem = OrdemRepo.inserir(ordem)

    if arquivoImagem.filename:
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/ordens/{ordem.id:04d}.jpg", "JPEG")

    response = redirecionar_com_mensagem("/ordem", "Ordem inserida com sucesso!")
    return response

@router.get("/excluir/{id_ordem:int}")
async def get_excluir(
    request: Request,
    id_ordem: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ordem = OrdemRepo.obter_por_id(id_ordem)

    return templates.TemplateResponse(
        "ordem/excluir.html",
        {"request": request, "usuario": usuario, "ordem": ordem},
    )

@router.post("/excluir/{id_ordem:int}")
async def post_excluir(
    id_ordem: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    OrdemRepo.excluir(id_ordem)

    caminho_imagem = f"static/img/ordens/{id_ordem:04d}.jpg"
    if os.path.exists(caminho_imagem):
        os.remove(caminho_imagem)

    response = redirecionar_com_mensagem("/ordem", "Ordem excluída com sucesso!")
    return response

@router.get("/alterar/{id_ordem:int}")
async def get_alterar(
    request: Request,
    id_ordem: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ordem = OrdemRepo.obter_por_id(id_ordem)

    return templates.TemplateResponse(
        "ordem/alterar.html",
        {"request": request, "usuario": usuario, "ordem": ordem},
    )

@router.post("/alterar/{id_ordem:int}")
async def post_alterar(
    id_ordem: int = Path(),
    cliente: str = Form(...),
    servico: str = Form(...),
    status: str = Form(...),
    desc: str = Form(...),
    arquivoImagem: UploadFile = File(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    OrdemRepo.alterar(Ordem(id_ordem,cliente,servico,status,desc))

    if arquivoImagem.filename:
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/ordens/{id_ordem:04d}.jpg", "JPEG")

    response = redirecionar_com_mensagem("/ordem", "Ordem alterada com sucesso!")
    return response