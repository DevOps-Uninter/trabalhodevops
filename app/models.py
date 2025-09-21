"""Modelos de dados do sistema EasyOrder."""

# External libraries
from sqlalchemy import (
    Column, Integer, Float, String, ForeignKey, DateTime, Numeric
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

# Own libraries
from app.database import Base


class Cliente(Base):
    """Modelo para clientes."""

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)

    pedidos = relationship("Pedido", back_populates="cliente")


class Pedido(Base):
    """Modelo para pedidos."""

    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String(255), index=True, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    cliente = relationship("Cliente", back_populates="pedidos")
    pagamentos = relationship(
        "Pagamento", back_populates="pedido", cascade="all, delete-orphan"
    )


class Produto(Base):
    """Modelo para produtos."""

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), index=True, nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    categoria = Column(String(255), index=True, nullable=False)
    qtd_estoque = Column(Integer, nullable=False)


class Entrega(Base):
    """Modelo para entregas."""

    __tablename__ = "entregas"

    id = Column(Integer, primary_key=True, index=True)
    endereco = Column(String(255), index=True, nullable=False)
    status = Column(String(50), index=True, nullable=False)
    data_entrega = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)


class Pagamento(Base):
    """Representa um pagamento associado a um pedido."""

    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    valor = Column(Float, nullable=False)
    status = Column(
        String(50), default="pendente", nullable=False
    )  # 'pendente', 'pago', 'cancelado'
    forma_pagamento = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    pedido = relationship("Pedido", back_populates="pagamentos")
