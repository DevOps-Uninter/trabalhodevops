"""Modelos de dados do sistema EasyOrder."""

# External libraries
from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship

# Own libraries
from app.database import Base


class Cliente(Base):
    """Modelo para clientes."""

    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    pedidos = relationship("Pedido", back_populates="cliente")


class Pedido(Base):
    """Modelo para pedidos."""

    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    descricao = Column(String, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))

    cliente = relationship("Cliente", back_populates="pedidos")
    pagamentos = relationship("Pagamento", back_populates="pedido")


class Produto(Base):
    """Modelo para produtos."""

    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True, nullable=False)
    preco = Column(Integer, nullable=False)
    categoria = Column(String, index=True, nullable=False)
    qtdEstoque = Column(Integer, nullable=False)


# Pagamento
class Pagamento(Base):
    """Representa um pagamento associado a um pedido."""

    __tablename__ = "pagamentos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    valor = Column(Float, nullable=False)
    status = Column(String, default="pendente")  # 'pendente', 'pago', 'cancelado'
    forma_pagamento = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    pedido = relationship("Pedido", back_populates="pagamentos")
