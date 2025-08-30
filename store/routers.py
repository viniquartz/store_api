from fastapi import APIRouter
from store.core.database import db

router = APIRouter(tags=["Products"])

@router.get("/")
async def listar_produtos():
    produtos = await db["products"].find().to_list(100)
    return produtos

@router.post("/")
async def criar_produto(produto: dict):
    resultado = await db["products"].insert_one(produto)
    return {"id": str(resultado.inserted_id), "message": "Produto criado com sucesso"}