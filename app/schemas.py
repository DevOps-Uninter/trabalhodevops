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

        from_attributes = True


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

        from_attributes = True


class RelatorioPedidosCliente(BaseModel):
    """Schema para relatório de pedidos por cliente."""

    cliente_id: int
    nome_cliente: str
    total_pedidos: int


class RelatorioFaturamento(BaseModel):
    """Schema para relatório de faturamento."""

    total_faturado: float
    periodo: str


class RelatorioProdutoEstoqueBaixo(BaseModel):
    """Schema para relatório de produtos com estoque baixo."""

    id: int
    nome: str
    qtd_estoque: int


class ProdutoBase(BaseModel):
    """Schema base para produtos."""

    nome: str
    preco: float
    categoria: str
    qtd_estoque: int


class ProdutoCreate(ProdutoBase):
    """Schema de criação de produtos."""

    pass


class Produto(ProdutoBase):
    """Schema de leitura de produtos."""

    id: int

    class Config:
        """Configurações do Pydantic."""

        from_attributes = True


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

        from_attributes = True


class PagamentoBase(BaseModel):
    """Schema base para pagamentos."""

    pedido_id: int
    valor: float
    forma_pagamento: str


class PagamentoCreate(PagamentoBase):
    """Schema para criar novos pagamentos."""

    pass


class PagamentoUpdate(BaseModel):
    """Schema para atualizar o status de um pagamento."""

    status: str  # 'pendente', 'pago', 'cancelado'


class Pagamento(PagamentoBase):
    """Schema para leitura de pagamentos."""

    id: int
    status: str
    created_at: datetime

    class Config:
        """Configurações do Pydantic para o schema Pagamento."""

        from_attributes = True
