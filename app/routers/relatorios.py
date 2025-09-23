"""Rotas de relatórios extras do sistema EasyOrder."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas, database

router = APIRouter(tags=["Relatórios"])


@router.get("/pedidos-por-cliente", response_model=list[schemas.RelatorioPedidosCliente])
def relatorio_pedidos_por_cliente(db: Session = Depends(database.get_db)):
    """Retorna a quantidade total de pedidos por cliente."""
    clientes = db.query(models.Cliente).all()
    relatorio = []
    for cliente in clientes:
        relatorio.append(
            {
                "cliente_id": cliente.id,
                "nome_cliente": cliente.nome,
                "total_pedidos": len(cliente.pedidos),
            }
        )
    return relatorio


@router.get("/faturamento")
def relatorio_faturamento(
    inicio: str, fim: str, db: Session = Depends(database.get_db)
):
    """Retorna o total faturado em um período (considera apenas pagamentos pagos)."""
    inicio_dt = datetime.strptime(inicio, "%Y-%m-%d")
    fim_dt = datetime.strptime(fim, "%Y-%m-%d")

    total = (
        db.query(models.Pagamento)
        .filter(models.Pagamento.status == "pago")
        .filter(models.Pagamento.created_at >= inicio_dt)
        .filter(models.Pagamento.created_at <= fim_dt)
        .with_entities(models.Pagamento.valor)
        .all()
    )

    total_faturado = sum(v[0] for v in total)

    return {
        "total_faturado": total_faturado,
        "periodo": f"{inicio} a {fim}",
    }


@router.get("/produtos-estoque-baixo")
def relatorio_produtos_estoque_baixo(
    limite: int = 5, db: Session = Depends(database.get_db)
):
    """Lista produtos com estoque abaixo do limite informado (default = 5)."""
    produtos = (
        db.query(models.Produto)
        .filter(models.Produto.qtd_estoque < limite)
        .all()
    )

    return [
        {"id": p.id, "nome": p.nome, "qtd_estoque": p.qtd_estoque} for p in produtos
    ]
