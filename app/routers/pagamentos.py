"""Rotas relacionadas aos pagamentos."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


@router.post("/", response_model=schemas.Pagamento, status_code=status.HTTP_201_CREATED)
def criar_pagamento(pagamento: schemas.PagamentoCreate):
    """Cria um novo pagamento associado a um pedido."""
    db: Session = SessionLocal()
    try:
        return crud.criar_pagamento(db, pagamento)
    finally:
        db.close()


@router.get("/", response_model=list[schemas.Pagamento])
def listar_pagamentos(skip: int = 0, limit: int = 10):
    """Lista todos os pagamentos cadastrados com paginação."""
    db: Session = SessionLocal()
    try:
        return crud.listar_pagamentos(db, skip=skip, limit=limit)
    finally:
        db.close()


@router.get("/{pagamento_id}", response_model=schemas.Pagamento)
def obter_pagamento(pagamento_id: int):
    """Obtém um pagamento pelo ID."""
    db: Session = SessionLocal()
    try:
        pagamento = crud.obter_pagamento(db, pagamento_id)
        if not pagamento:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        return pagamento
    finally:
        db.close()


@router.put("/{pagamento_id}", response_model=schemas.Pagamento)
def atualizar_pagamento(pagamento_id: int, pagamento: schemas.PagamentoUpdate):
    """Atualiza os dados de um pagamento existente."""
    db: Session = SessionLocal()
    try:
        pagamento_atualizado = crud.atualizar_pagamento(db, pagamento_id, pagamento)
        if not pagamento_atualizado:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
        return pagamento_atualizado
    finally:
        db.close()


@router.delete("/{pagamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pagamento(pagamento_id: int):
    """Deleta um pagamento pelo ID."""
    db: Session = SessionLocal()
    try:
        sucesso = crud.deletar_pagamento(db, pagamento_id)
        if not sucesso:
            raise HTTPException(status_code=404, detail="Pagamento não encontrado")
    finally:
        db.close()
