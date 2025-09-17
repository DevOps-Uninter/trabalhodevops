"""Esquemas Pydantic para validação de dados da API."""

from pydantic import BaseModel
from datetime import datetime


class PedidoBase(BaseModel):
    """Schema base para pedidos."""

    descricao: str


class PedidoCreate(PedidoBase):
    """Schema de criação de pedidos."""

    pass


class Pedido(PedidoBase):
    """Schema de leitura de pedidos."""

    id: int
    cliente_id: int

    class Config:
        """Configurações do Pydantic."""

        orm_mode = True


class ClienteBase(BaseModel):
    """Schema base para clientes."""

    nome: str
    email: str


class ClienteCreate(ClienteBase):
    """Schema de criação de clientes."""

    pass


class Cliente(ClienteBase):
    """Schema de leitura de clientes."""

    id: int
    pedidos: list[Pedido] = []

    class Config:
        """Configurações do Pydantic."""

        orm_mode = True


class RelatorioPedidosCliente(BaseModel):
    """Schema para relatório de pedidos por cliente."""

    cliente_id: int
    nome_cliente: str
    total_pedidos: int


class ProdutoBase(BaseModel):
    """Schema base para produtos."""

    nome: str
    preco: float
    categoria: str
    qtdEstoque: int


class ProdutoCreate(ProdutoBase):
    """Schema de criação de produtos."""

    pass


class Produto(ProdutoBase):
    """Schema de leitura de produtos."""

    id: int

    class Config:
        """Configurações do Pydantic."""

        orm_mode = True


class EntregaBase(BaseModel):
    """Schema base para entregas."""

    endereco: str
    status: str
    data_entrega: datetime


class EntregaCreate(EntregaBase):
    """Schema de criação de entregas."""
    pedido_id: int


class Entrega(EntregaBase):
    """Schema de leitura de entregas."""

    id: int
    pedido_id: int

    class Config:
        """Configurações do Pydantic."""

        orm_mode = True
