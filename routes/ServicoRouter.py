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
from models.Servico import Servico
from models.Usuario import Usuario
from repositories.ServicoRepo import ServicoRepo
from util.imagem import transformar_em_quadrada
from util.mensagem import redirecionar_com_mensagem
from util.seguranca import obter_usuario_logado
from PIL import Image

router = APIRouter(prefix="/servico")
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
    
    servicos = ServicoRepo.obter_todos()
    
    return templates.TemplateResponse(
        "servico/index.html",
        {"request": request, "usuario": usuario, "servicos": servicos},
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
        "servico/inserir.html",
        {"request": request, "usuario": usuario},
    )

@router.post("/inserir")
async def post_inserir(
    nome: str = Form(...),
    desc: str = Form(...),
    valor: float = Form(...),
    arquivoImagem: UploadFile = File(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    servico = Servico(nome=nome,desc=desc,valor=valor)  
    servico = ServicoRepo.inserir(servico)

    if arquivoImagem.filename:
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/servicos/{servico.id:04d}.jpg", "JPEG")

    response = redirecionar_com_mensagem("/servico", "Serviço inserido com sucesso!")
    return response

@router.get("/excluir/{id_servico:int}")
async def get_excluir(
    request: Request,
    id_servico: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    servico = ServicoRepo.obter_por_id(id_servico)

    return templates.TemplateResponse(
        "servico/excluir.html",
        {"request": request, "usuario": usuario, "servico": servico},
    )

@router.post("/excluir/{id_servico:int}")
async def post_excluir(
    id_servico: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ServicoRepo.excluir(id_servico)

    caminho_imagem = f"static/img/servicos/{id_servico:04d}.jpg"
    if os.path.exists(caminho_imagem):
        os.remove(caminho_imagem)

    response = redirecionar_com_mensagem("/servico", "Serviço excluído com sucesso!")
    return response

@router.get("/alterar/{id_servico:int}")
async def get_alterar(
    request: Request,
    id_servico: int = Path(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    servico = ServicoRepo.obter_por_id(id_servico)

    return templates.TemplateResponse(
        "servico/alterar.html",
        {"request": request, "usuario": usuario, "servico": servico},
    )

@router.post("/alterar/{id_servico:int}")
async def post_alterar(
    id_servico: int = Path(),
    nome: str = Form(...),
    desc: str = Form(...),
    valor: float = Form(...),
    arquivoImagem: UploadFile = File(),
    usuario: Usuario = Depends(obter_usuario_logado),
):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    ServicoRepo.alterar(Servico(id_servico,nome,desc,valor))

    if arquivoImagem.filename:
        conteudo_arquivo = await arquivoImagem.read()
        imagem = Image.open(BytesIO(conteudo_arquivo))
        imagem_quadrada = transformar_em_quadrada(imagem)
        imagem_quadrada.save(f"static/img/servicos/{id_servico:04d}.jpg", "JPEG")

    response = redirecionar_com_mensagem("/servico", "Serviço alterado com sucesso!")
    return response