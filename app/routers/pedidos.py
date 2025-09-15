"""Rotas relacionadas aos pedidos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])


def get_db():
    """Cria e fecha a sessão com o banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Pedido)
def criar_pedido(
    cliente_id: int, pedido: schemas.PedidoCreate, db: Session = Depends(get_db)
):
    """
    Cria um novo pedido associado a um cliente.

    Args:
        cliente_id (int): ID do cliente.
        pedido (PedidoCreate): Dados do pedido.
        db (Session): Sessão do banco de dados.

    Returns:
        Pedido criado.
    """
    return crud.criar_pedido(db, pedido, cliente_id)


@router.get("/", response_model=list[schemas.Pedido])
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista os pedidos cadastrados.

    Args:
        skip (int): Quantidade de registros a pular.
        limit (int): Quantidade máxima de registros a retornar.
        db (Session): Sessão do banco de dados.

    Returns:
        Lista de pedidos.
    """
    return crud.listar_pedidos(db, skip=skip, limit=limit)


@router.get("/{pedido_id}", response_model=schemas.Pedido)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    """
    Obtém um pedido pelo ID.

    Args:
        pedido_id (int): ID do pedido.
        db (Session): Sessão do banco de dados.

    Returns:
        Pedido correspondente ao ID.
    """
    pedido = crud.obter_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido
