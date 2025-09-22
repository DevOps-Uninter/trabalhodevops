"""Rotas relacionadas aos pedidos."""

import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Own libraries
from app import crud, schemas, database
from app.main import sqs_client, SQS_QUEUE_URL


router = APIRouter(tags=["Pedidos"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=schemas.Pedido)
def criar_pedido(
    cliente_id: int, pedido: schemas.PedidoCreate, db: Session = Depends(database.get_db)
):
    """Cria um novo pedido associado a um cliente e envia para a fila SQS.

    Args:
        cliente_id (int): ID do cliente.
        pedido (PedidoCreate): Dados do pedido.
        db (Session): Sessão do banco de dados.

    Returns:
        Pedido criado.
    """
    novo_pedido = crud.criar_pedido(db, pedido, cliente_id)

    # Envia para fila SQS
    if SQS_QUEUE_URL:
        try:
            sqs_client.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(
                    {
                        "pedido_id": novo_pedido.id,
                        "cliente_id": cliente_id,
                        "valor_total": str(novo_pedido.valor_total),
                    }
                ),
            )
            logger.info(f"📩 Pedido {novo_pedido.id} enviado para SQS com sucesso.")
        except Exception as e:
            logger.error(f"⚠️ Erro ao enviar pedido {novo_pedido.id} para SQS: {e}")

    return novo_pedido


@router.get("/", response_model=list[schemas.Pedido])
def listar_pedidos(
    skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)
):
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
def obter_pedido(pedido_id: int, db: Session = Depends(database.get_db)):
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


@router.put("/{pedido_id}", response_model=schemas.Pedido)
def atualizar_pedido(
    pedido_id: int, pedido: schemas.PedidoUpdate, db: Session = Depends(database.get_db)
):
    """
    Atualiza um pedido existente.

    Args:
        pedido_id (int): ID do pedido.
        pedido (PedidoUpdate): Dados atualizados do pedido.
        db (Session): Sessão do banco de dados.

    Returns:
        Pedido atualizado.
    """
    pedido_atualizado = crud.atualizar_pedido(db, pedido_id, pedido)
    if not pedido_atualizado:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return pedido_atualizado


@router.delete("/{pedido_id}", response_model=dict)
def deletar_pedido(pedido_id: int, db: Session = Depends(database.get_db)):
    """
    Remove um pedido pelo ID.

    Args:
        pedido_id (int): ID do pedido.
        db (Session): Sessão do banco de dados.

    Returns:
        Mensagem de sucesso.
    """
    sucesso = crud.deletar_pedido(db, pedido_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return {"mensagem": "Pedido removido com sucesso"}
