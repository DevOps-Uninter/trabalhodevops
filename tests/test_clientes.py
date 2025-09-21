"""Testes para o router de clientes."""

from fastapi.testclient import TestClient


def test_listar_clientes_vazio(test_client: TestClient):
    """
    Testa se a listagem de clientes retorna uma lista vazia quando o banco
    de dados está limpo.
    """
    response = test_client.get("/clientes")
    assert response.status_code == 200
    assert response.json() == []


def test_criar_e_obter_cliente(test_client: TestClient):
    """
    Testa a criação de um novo cliente e verifica se ele pode ser
    obtido na listagem e individualmente.
    """
    # 1. Cria um cliente
    cliente_data = {"nome": "Cliente de Teste", "email": "teste@exemplo.com"}
    response_create = test_client.post("/clientes/", json=cliente_data)

    assert response_create.status_code == 200
    created_data = response_create.json()
    assert created_data["nome"] == cliente_data["nome"]
    assert "id" in created_data
    cliente_id = created_data["id"]

    # 2. Verifica se o cliente aparece na listagem geral
    response_list = test_client.get("/clientes/")
    assert response_list.status_code == 200
    assert len(response_list.json()) == 1
    assert response_list.json()[0]["nome"] == cliente_data["nome"]

    # 3. Verifica se o cliente pode ser obtido pelo seu ID
    response_get = test_client.get(f"/clientes/{cliente_id}")
    assert response_get.status_code == 200
    assert response_get.json()["email"] == cliente_data["email"]