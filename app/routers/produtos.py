"""Rotas relacionadas aos produtos."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/produtos", tags=["Produtos"])


# cadastrar um produto
@router.post("/criar", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate):
    """
    Cria um novo produto.

    Args:
        produto (ProdutoCreate): Dados do produto.

    Returns:
        Produto criado.
    """
    db: Session = SessionLocal()
    try:
        return crud.criar_produto(db, produto)
    finally:
        db.close()


# listar todos os produtos cadastrados
@router.get("/", response_model=list[schemas.Produto])
def listar_produtos(skip: int = 0, limit: int = 10):
    """
    Lista os produtos cadastrados.

    Args:
        skip (int): Quantidade de registros a pular.
        limit (int): Quantidade máxima de registros a retornar.

    Returns:
        Lista de produtos.
    """
    db: Session = SessionLocal()
    try:
        return crud.listar_produtos(db, skip=skip, limit=limit)
    finally:
        db.close()


# buscar um produto pelo id
@router.get("/{produto_id}", response_model=schemas.Produto)
def obter_produto(produto_id: int):
    """
    Obtém um produto pelo ID.

    Args:
        produto_id (int): ID do produto.

    Returns:
        Produto correspondente ao ID.
    """
    db: Session = SessionLocal()
    try:
        produto = crud.obter_produto(db, produto_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return produto
    finally:
        db.close()


# atualizar um produto
@router.put("/atualizar/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(produto_id: int, produto: schemas.ProdutoCreate):
    """
    Atualiza um produto existente.

    Args:
        produto_id (int): O ID do produto a ser atualizado.
        produto (ProdutoCreate): Os novos dados do produto.

    Returns:
        O produto atualizado.

    Raises:
        HTTPException: 404 Not Found se o produto não for encontrado.
    """
    db: Session = SessionLocal()
    try:
        produto_atualizado = crud.atualizar_produto(db, produto_id, produto)
        if not produto_atualizado:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        return produto_atualizado
    finally:
        db.close()


# deletar um produto
@router.delete("/deletar/{produto_id}", status_code=status.HTTP_200_OK)
def deletar_produto(produto_id: int):
    """
    Deleta um produto pelo ID.

    Args:
        produto_id (int): O ID do produto a ser deletado.

    Returns:
        Uma mensagem de sucesso.

    Raises:
        HTTPException: 404 Not Found se o produto não for encontrado.
    """
    db: Session = SessionLocal()
    try:
        produto_deletado = crud.deletar_produto(db, produto_id)
        if not produto_deletado:
            raise HTTPException(
                status_code=404, detail="Não foi possível deletar o produto"
            )
        return {"message": "Produto deletado com sucesso."}
    finally:
        db.close()
