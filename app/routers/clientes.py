"""Rotas relacionadas aos clientes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(tags=["Clientes"])


@router.post("/", response_model=schemas.Cliente)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(database.get_db)):
    """
    Cria um novo cliente.

    Args:
        cliente (ClienteCreate): Dados do cliente.
        db (Session): Sessão do banco de dados.

    Returns:
        Cliente criado.
    """
    return crud.criar_cliente(db, cliente)


@router.get("/", response_model=list[schemas.Cliente])
def listar_clientes(
    skip: int = 0, limit:
    int = 10,
    db: Session = Depends(database.get_db)
):
    """
    Lista os clientes cadastrados.

    Args:
        skip (int): Quantidade de registros a pular.
        limit (int): Quantidade máxima de registros a retornar.
        db (Session): Sessão do banco de dados.

    Returns:
        Lista de clientes.
    """
    return crud.listar_clientes(db, skip=skip, limit=limit)


@router.get("/{cliente_id}", response_model=schemas.Cliente)
def obter_cliente(cliente_id: int, db: Session = Depends(database.get_db)):
    """
    Obtém um cliente pelo ID.

    Args:
        cliente_id (int): ID do cliente.
        db (Session): Sessão do banco de dados.

    Returns:
        Cliente correspondente ao ID.
    """
    cliente = crud.obter_cliente(db, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente
