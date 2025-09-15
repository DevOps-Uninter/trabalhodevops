"""Rotas relacionadas aos pagamentos."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


def get_db():
    """Cria e fecha a sessão com o banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Pagamento, status_code=status.HTTP_201_CREATED)
def criar_pagamento(pagamento: schemas.PagamentoCreate, db: Session = Depends(get_db)):
    """
    Cria um novo pagamento associado a um pedido.

    Args:
        pagamento (PagamentoCreate): Dados do pagamento.
        db (Session): Sessão do banco de dados.

    Returns:
        Pagamento criado.
    """
    return crud.criar_pagamento(db, pagamento)


@router.get("/", response_model=list[schemas.Pagamento])
def listar_pagamentos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista todos os pagamentos cadastrados com paginação.

    Args:
        skip (int): Quantidade de registros a pular.
        limit (int): Quantidade máxima de registros a retornar.
        db (Session): Sessão do banco de dados.

    Returns:
        Lista de pagamentos.
    """
    return crud.listar_pagamentos(db, skip=skip, limit=limit)


@router.get("/{pagamento_id}", response_model=schemas.Pagamento)
def obter_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    """
    Obtém um pagamento pelo ID.

    Args:
        pagamento_id (int): ID do pagamento.
        db (Session): Sessão do banco de dados.

    Returns:
        Pagamento correspondente ao ID.

    Raises:
        HTTPException: 404 se o pagamento não for encontrado.
    """
    pagamento = crud.obter_pagamento(db, pagamento_id)
    if not pagamento:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento


@router.put("/{pagamento_id}", response_model=schemas.Pagamento)
def atualizar_pagamento(
    pagamento_id: int, pagamento: schemas.PagamentoUpdate, db: Session = Depends(get_db)
):
    """Atualiza os dados de um pagamento existente."""
    pagamento_atualizado = crud.atualizar_pagamento(db, pagamento_id, pagamento)
    if not pagamento_atualizado:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    return pagamento_atualizado


@router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    """
    Deleta um pagamento pelo ID.

    Args:
        pagamento_id (int): ID do pagamento a ser deletado.
        db (Session): Sessão do banco de dados.

    Raises:
        HTTPException: 404 se o pagamento não for encontrado.
    """
    sucesso = crud.deletar_pagamento(db, pagamento_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Pagamento não encontrado")
