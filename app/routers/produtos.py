"""Rotas relacionadas aos produtos."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(tags=["Produtos"])


@router.post("/", response_model=schemas.Produto, status_code=status.HTTP_201_CREATED)
def criar_produto(
    produto: schemas.ProdutoCreate, db: Session = Depends(database.get_db)
):
    """
    Cria um novo produto.

    Args:
        produto (ProdutoCreate): Dados do produto.
        db (Session): Sessão do banco de dados.

    Returns:
        Produto criado.
    """
    return crud.criar_produto(db, produto)


@router.get("/", response_model=list[schemas.Produto])
def listar_produtos(
    skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
):
    """
    Lista os produtos cadastrados.

    Args:
        skip (int): Quantidade de registros a pular.
        limit (int): Quantidade máxima de registros a retornar.
        db (Session): Sessão do banco de dados.

    Returns:
        Lista de produtos.
    """
    return crud.listar_produtos(db, skip=skip, limit=limit)


@router.get("/{produto_id}", response_model=schemas.Produto)
def obter_produto(produto_id: int, db: Session = Depends(database.get_db)):
    """
    Obtém um produto pelo ID.

    Args:
        produto_id (int): ID do produto.
        db (Session): Sessão do banco de dados.

    Returns:
        Produto correspondente ao ID.

    Raises:
        HTTPException: 404 se o produto não for encontrado.
    """
    db_produto = crud.obter_produto(db, produto_id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto


@router.put("/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(
    produto_id: int,
    produto: schemas.ProdutoCreate,
    db: Session = Depends(database.get_db),
):
    """
    Atualiza um produto existente.

    Args:
        produto_id (int): O ID do produto a ser atualizado.
        produto (ProdutoCreate): Os novos dados do produto.
        db (Session): Sessão do banco de dados.

    Returns:
        O produto atualizado.

    Raises:
        HTTPException: 404 se o produto não for encontrado.
    """
    db_produto = crud.atualizar_produto(db, produto_id, produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto


@router.delete("/{produto_id}", status_code=status.HTTP_200_OK)
def deletar_produto(produto_id: int, db: Session = Depends(database.get_db)):
    """
    Deleta um produto pelo ID.

    Args:
        produto_id (int): O ID do produto a ser deletado.
        db (Session): Sessão do banco de dados.

    Returns:
        Uma mensagem de sucesso.

    Raises:
        HTTPException: 404 se o produto não for encontrado.
    """
    sucesso = crud.deletar_produto(db, produto_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"message": "Produto deletado com sucesso."}
