"""Testes para o router de pedidos."""

from fastapi.testclient import TestClient


def test_criar_e_listar_pedidos(test_client: TestClient):
    """Testa a criação de um pedido vinculado a um cliente."""
    # 1. Primeiro, cria um cliente para associar ao pedido
    cliente_data = {"nome": "Cliente para Pedidos", "email": "pedidos@exemplo.com"}
    response_cliente = test_client.post("/clientes/", json=cliente_data)
    assert response_cliente.status_code == 200
    cliente_id = response_cliente.json()["id"]

    # 2. Cria um pedido para este cliente
    pedido_data = {"descricao": "Pedido de teste"}
    response_pedido = test_client.post(
        f"/pedidos/?cliente_id={cliente_id}", json=pedido_data
    )

    assert response_pedido.status_code == 200
    data = response_pedido.json()
    assert data["descricao"] == pedido_data["descricao"]
    assert data["cliente_id"] == cliente_id
    pedido_id = data["id"]

    # 3. Verifica se o pedido aparece na listagem
    response_list = test_client.get("/pedidos/")
    assert response_list.status_code == 200
    assert len(response_list.json()) > 0

    # 4. Verifica se o pedido individual é retornado corretamente
    response_get = test_client.get(f"/pedidos/{pedido_id}")
    assert response_get.status_code == 200
    assert response_get.json()["id"] == pedido_id
