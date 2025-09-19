"""Rotas relacionadas às entregas."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter(prefix="/entregas", tags=["Entregas"])


@router.post("/criar", response_model=schemas.Entrega)
def criar_entrega(entrega: schemas.EntregaCreate, db: Session = Depends(database.get_db)):
    """Cria uma nova entrega."""
    return crud.criar_entrega(db, entrega)


@router.get("/", response_model=list[schemas.Entrega])
def listar_entregas(
    skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    """Lista todas as entregas cadastradas."""
    return crud.listar_entregas(db, skip=skip, limit=limit)


@router.get("/{entrega_id}", response_model=schemas.Entrega)
def obter_entrega(entrega_id: int, db: Session = Depends(database.get_db)):
    """Obtém uma entrega pelo ID."""
    db_entrega = crud.obter_entrega(db, entrega_id)
    if db_entrega is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return db_entrega


# Atualizar entrega pelo ID
@router.put("/{entrega_id}", response_model=schemas.Entrega)
def atualizar_entrega(
    entrega_id: int, entrega: schemas.EntregaCreate,
     db: Session = Depends(database.get_db)):
    """Atualiza uma entrega pelo ID."""
    db_entrega = crud.obter_entrega(db, entrega_id)
    if db_entrega is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return crud.atualizar_entrega(db, entrega_id, entrega)


# Deletar entrega pelo ID
@router.delete("/{entrega_id}")
def deletar_entrega(entrega_id: int, db: Session = Depends(database.get_db)):
    """Deleta uma entrega pelo ID."""
    db_entrega = crud.obter_entrega(db, entrega_id)
    if db_entrega is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    crud.deletar_entrega(db, entrega_id)
    return {"message": "Entrega deletada com sucesso"}
