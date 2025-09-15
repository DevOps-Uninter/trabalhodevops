"""Funções CRUD para clientes, pedidos e relatórios."""

from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, schemas


# Clientes
def criar_cliente(db: Session, cliente: schemas.ClienteCreate) -> models.Cliente:
    """Cria um novo cliente no banco de dados."""
    db_cliente = models.Cliente(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente


def listar_clientes(db: Session, skip: int = 0, limit: int = 10) -> list:
    """Lista todos os clientes com paginação."""
    return db.query(models.Cliente).offset(skip).limit(limit).all()


def obter_cliente(db: Session, cliente_id: int) -> models.Cliente | None:
    """Obtém um cliente pelo ID."""
    return db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()


# Pedidos
def criar_pedido(
    db: Session, pedido: schemas.PedidoCreate, cliente_id: int
) -> models.Pedido:
    """Cria um novo pedido associado a um cliente."""
    db_pedido = models.Pedido(**pedido.model_dump(), cliente_id=cliente_id)
    db.add(db_pedido)
    db.commit()
    db.refresh(db_pedido)
    return db_pedido


def listar_pedidos(db: Session, skip: int = 0, limit: int = 10) -> list:
    """Lista todos os pedidos com paginação."""
    return db.query(models.Pedido).offset(skip).limit(limit).all()


def obter_pedido(db: Session, pedido_id: int) -> models.Pedido | None:
    """Obtém um pedido pelo ID."""
    return db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()


def relatorio_pedidos_por_cliente(db: Session) -> list[schemas.RelatorioPedidosCliente]:
    """Gera relatório de total de pedidos por cliente."""
    results = (
        db.query(
            models.Cliente.id.label("cliente_id"),
            models.Cliente.nome.label("nome_cliente"),
            func.count(models.Pedido.id).label("total_pedidos"),
        )
        .join(models.Pedido, models.Pedido.cliente_id == models.Cliente.id)
        .group_by(models.Cliente.id, models.Cliente.nome)
        .all()
    )

    return [
        schemas.RelatorioPedidosCliente(
            cliente_id=r.cliente_id,
            nome_cliente=r.nome_cliente,
            total_pedidos=r.total_pedidos,
        )
        for r in results
    ]


# Produtos
def criar_produto(db: Session, produto: schemas.ProdutoCreate) -> models.Produto:
    """Cria um novo produto no banco de dados."""
    db_produto = models.Produto(**produto.model_dump())
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


def listar_produtos(db: Session, skip: int = 0, limit: int = 10) -> list:
    """Lista todos os produtos com paginação."""
    return db.query(models.Produto).offset(skip).limit(limit).all()


def obter_produto(db: Session, produto_id: int) -> models.Produto | None:
    """Obtém um produto pelo ID."""
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()


def atualizar_produto(
    db: Session, produto_id: int, produto: schemas.ProdutoBase
) -> models.Produto | None:
    """Atualiza os dados de um produto existente."""
    db_produto = (
        db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    )
    if db_produto:
        for key, value in produto.model_dump().items():
            setattr(db_produto, key, value)
        db.commit()
        db.refresh(db_produto)
    return db_produto


def deletar_produto(db: Session, produto_id: int) -> bool:
    """Remove um produto do banco de dados."""
    db_produto = (
        db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    )
    if db_produto:
        db.delete(db_produto)
        db.commit()
        return True
    return False


# Pagamentos
def criar_pagamento(
    db: Session, pagamento: schemas.PagamentoCreate
) -> models.Pagamento:
    """
    Cria um novo pagamento no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        pagamento (PagamentoCreate): Dados do pagamento a ser criado.

    Returns:
        Pagamento: O pagamento criado.
    """
    db_pagamento = models.Pagamento(**pagamento.model_dump())
    db.add(db_pagamento)
    db.commit()
    db.refresh(db_pagamento)
    return db_pagamento


def listar_pagamentos(
    db: Session, skip: int = 0, limit: int = 10
) -> list[models.Pagamento]:
    """
    Lista os pagamentos existentes com paginação.

    Args:
        db (Session): Sessão do banco de dados.
        skip (int): Quantidade de registros a pular.
        limit (int): Quantidade máxima de registros a retornar.

    Returns:
        list[Pagamento]: Lista de pagamentos.
    """
    return db.query(models.Pagamento).offset(skip).limit(limit).all()


def obter_pagamento(
    db: Session, pagamento_id: int
) -> models.Pagamento | None:
    """
    Obtém um pagamento pelo ID.

    Args:
        db (Session): Sessão do banco de dados.
        pagamento_id (int): ID do pagamento.

    Returns:
        Pagamento | None: O pagamento correspondente, ou None se não existir.
    """
    return db.query(models.Pagamento).filter(models.Pagamento.id == pagamento_id).first()


def atualizar_pagamento(
    db: Session,
    pagamento_id: int,
    pagamento: schemas.PagamentoUpdate,
) -> models.Pagamento | None:
    """
    Atualiza o status de um pagamento existente.

    Args:
        db (Session): Sessão do banco de dados.
        pagamento_id (int): ID do pagamento a ser atualizado.
        pagamento (PagamentoUpdate): Novos dados do pagamento.

    Returns:
        Pagamento | None: O pagamento atualizado, ou None se não existir.
    """
    db_pagamento = (
        db.query(models.Pagamento)
        .filter(models.Pagamento.id == pagamento_id)
        .first()
    )

    if db_pagamento:
        for key, value in pagamento.model_dump().items():
            setattr(db_pagamento, key, value)
        db.commit()
        db.refresh(db_pagamento)

    return db_pagamento


def deletar_pagamento(db: Session, pagamento_id: int) -> bool:
    """
    Remove um pagamento do banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        pagamento_id (int): ID do pagamento a ser removido.

    Returns:
        bool: True se o pagamento foi deletado, False se não encontrado.
    """
    db_pagamento = (
        db.query(models.Pagamento)
        .filter(models.Pagamento.id == pagamento_id)
        .first()
    )

    if db_pagamento:
        db.delete(db_pagamento)
        db.commit()
        return True

    return False
