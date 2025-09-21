"""Script para popular o banco de dados EasyOrder com dados iniciais."""

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import models


Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

db.query(models.Pagamento).delete()
db.query(models.Entrega).delete()
db.query(models.Produto).delete()
db.query(models.Pedido).delete()
db.query(models.Cliente).delete()
db.commit()


clientes = [
    models.Cliente(nome="Alice Souza", email="alice@example.com"),
    models.Cliente(nome="Bruno Lima", email="bruno@example.com"),
    models.Cliente(nome="Carla Mendes", email="carla@example.com"),
]
db.add_all(clientes)
db.commit()


produtos = [
    models.Produto(nome="Notebook", preco=3500.00, categoria="Eletrônicos", qtd_estoque=10),
    models.Produto(nome="Mouse Gamer", preco=150.00, categoria="Acessórios", qtd_estoque=30),
    models.Produto(nome="Teclado Mecânico", preco=400.00, categoria="Acessórios", qtd_estoque=20),
]
db.add_all(produtos)
db.commit()


pedido1 = models.Pedido(descricao="Compra Notebook e Mouse", cliente_id=clientes[0].id)
pedido2 = models.Pedido(descricao="Compra Teclado", cliente_id=clientes[1].id)

db.add_all([pedido1, pedido2])
db.commit()


pagamentos = [
    models.Pagamento(
        pedido_id=pedido1.id,
        valor=3650.00,
        status="pago",
        forma_pagamento="cartão",
        created_at=datetime.now(timezone.utc),
    ),
    models.Pagamento(
        pedido_id=pedido2.id,
        valor=400.00,
        status="pendente",
        forma_pagamento="boleto",
        created_at=datetime.now(timezone.utc),
    ),
]
db.add_all(pagamentos)
db.commit()

entregas = [
    models.Entrega(
        endereco="Rua das Flores, 123",
        status="entregue",
        data_entrega=datetime.now(timezone.utc) - timedelta(days=2),
        pedido_id=pedido1.id,
    ),
    models.Entrega(
        endereco="Av. Paulista, 500",
        status="em transporte",
        data_entrega=datetime.now(timezone.utc) + timedelta(days=3),
        pedido_id=pedido2.id,
    ),
]
db.add_all(entregas)
db.commit()

db.close()

print("✅ Banco de dados populado com sucesso!")
