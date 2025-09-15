"""Rotas relacionadas aos relatórios."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter(prefix="/relatorios", tags=["Relatórios"])


def get_db():
    """Cria e fecha a sessão com o banco de dados."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get(
    "/pedidos-por-cliente", response_model=list[schemas.RelatorioPedidosCliente]
)
def relatorio_pedidos_cliente(db: Session = Depends(get_db)):
    """Retorna relatório com o total de pedidos por cliente."""
    return crud.relatorio_pedidos_por_cliente(db)
