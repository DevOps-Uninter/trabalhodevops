"""Rotas relacionadas aos clientes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/produtos", tags=["Produtos"])


def get_db():
    """Cria e fecha a sessão com o banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# cadastrar um produto
@router.post("/criar", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo produto.

    Args:
        produto (ProdutoCreate): Dados do produto.
        db (Session): Sessão do banco de dados.

    Returns:
        Produto criado.
    """
    return crud.criar_produto(db, produto)


# listar todos os produtos cadastrados/retorna um JSON vazio, caso não haja nenhum
@router.get("/", response_model=list[schemas.Produto])
def listar_produtos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
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


#  buscar um produto pelo id
@router.get("/{produto_id}", response_model=schemas.Produto)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Obtém um produto pelo ID.

    Args:
        produto_id (int): ID do produto.
        db (Session): Sessão do banco de dados.

    Returns:
        Produto correspondente ao ID.
    """
    produto = crud.obter_produto(db, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


#  atualizar um produto
@router.put("/atualizar/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(
    produto_id: int, produto: schemas.ProdutoCreate, db: Session = Depends(get_db)
):
    """
    Atualiza um produto existente.

    Args:
        produto_id (int): O ID do produto a ser atualizado.
        produto (ProdutoCreate): Os novos dados do produto.
        db (Session): A sessão do banco de dados.

    Returns:
        O produto atualizado.

    Raises:
        HTTPException: 404 Not Found se o produto não for encontrado.
    """
    produto_atualizado = crud.atualizar_produto(db, produto_id, produto)
    if not produto_atualizado:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto_atualizado


#  deletar um produto
@router.delete("/deletar/{produto_id}", status_code=status.HTTP_200_OK)
def deletar_produto(produto_id: int, db: Session = Depends(get_db)):
    """
    Deleta um produto pelo ID.

    Args:
        produto_id (int): O ID do produto a ser deletado.
        db (Session): A sessão do banco de dados.

    Returns:
        Uma mensagem de sucesso.

    Raises:
        HTTPException: 404 Not Found se o produto não for encontrado.
    """
    produto_deletado = crud.deletar_produto(db, produto_id)
    if not produto_deletado:
        raise HTTPException(
            status_code=404, detail="Não foi possível deletar o produto"
        )

    return {"message": "Produto deletado com sucesso."}
