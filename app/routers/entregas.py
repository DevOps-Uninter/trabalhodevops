"""Rotas relacionadas às entregas."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/entregas", tags=["Entregas"])


def get_db():
    """Cria e fecha a sessão com o banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# cadastrar uma entrega
@router.post("/criar", response_model=schemas.Entrega)
def criar_entrega(
    entrega: schemas.EntregaCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo entrega.

    Args:
        entrega (EntregaCreate): Dados do entrega.
        db (Session): Sessão do banco de dados.

    Returns:
        Entrega criada.
    """
    return crud.criar_entrega(db, entrega)


# listar todas as entregas
@router.get("/", response_model=list[schemas.Entrega])
def listar_entregas(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Lista as entregas cadastradas.

    Args:
        skip (int): Quantidade de registros a pular.
        limit (int): Quantidade máxima de registros a retornar.
        db (Session): Sessão do banco de dados.

    Returns:
        Lista de entregas.
    """
    return crud.listar_entregas(db, skip=skip, limit=limit)


# obter uma entrega pelo id
@router.get("/{entrega_id}", response_model=schemas.Entrega)
def obter_entrega(entrega_id: int, db: Session = Depends(get_db)):
    """
    Obtém uma entrega pelo ID.

    Args:
        entrega_id (int): ID da entrega.
        db (Session): Sessão do banco de dados.

    Returns:
        Entrega encontrada.
    """
    db_entrega = crud.obter_entrega(db, entrega_id)
    if db_entrega is None:
        raise HTTPException(status_code=404, detail="Entrega não encontrada")
    return db_entrega
