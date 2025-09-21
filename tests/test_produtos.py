"""Testes para o router de produtos."""

from fastapi.testclient import TestClient


def test_criar_produto(test_client: TestClient):
    """Testa a criação de um novo produto."""
    produto_data = {
        "nome": "Notebook Gamer",
        "preco": 5500.50,
        "categoria": "Eletrônicos",
        "qtd_estoque": 15,
    }
    response = test_client.post("/produtos/criar", json=produto_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == produto_data["nome"]
    assert data["preco"] == produto_data["preco"]
    assert "id" in data


def test_listar_produtos(test_client: TestClient):
    """Testa a listagem de todos os produtos."""
    # Primeiro, cria um produto para garantir que a lista não esteja vazia
    produto_data = {
        "nome": "Mouse sem Fio",
        "preco": 120.00,
        "categoria": "Acessórios",
        "qtd_estoque": 50,
    }
    test_client.post("/produtos/criar", json=produto_data)

    response = test_client.get("/produtos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["nome"] == produto_data["nome"]


def test_atualizar_produto(test_client: TestClient):
    """Testa a atualização de um produto existente."""
    # Cria o produto inicial
    produto_data = {
        "nome": "Teclado Mecânico",
        "preco": 350.00,
        "categoria": "Acessórios",
        "qtd_estoque": 20,
    }
    response_create = test_client.post("/produtos/criar", json=produto_data)
    produto_id = response_create.json()["id"]

    # Atualiza o produto
    update_data = {
        "nome": "Teclado Mecânico RGB",
        "preco": 450.00,
        "categoria": "Acessórios",
        "qtd_estoque": 18,
    }
    response_update = test_client.put(
        f"/produtos/atualizar/{produto_id}", json=update_data
    )
    assert response_update.status_code == 200
    data = response_update.json()
    assert data["nome"] == update_data["nome"]
    assert data["preco"] == update_data["preco"]
    assert data["qtd_estoque"] == 18


def test_deletar_produto(test_client: TestClient):
    """Testa a exclusão de um produto."""
    # Cria um produto para deletar
    produto_data = {
        "nome": "Monitor Ultrawide",
        "preco": 1800.00,
        "categoria": "Monitores",
        "qtd_estoque": 10,
    }
    response_create = test_client.post("/produtos/criar", json=produto_data)
    produto_id = response_create.json()["id"]

    # Deleta o produto
    response_delete = test_client.delete(f"/produtos/deletar/{produto_id}")
    assert response_delete.status_code == 200
    assert response_delete.json()["message"] == "Produto deletado com sucesso."

    # Verifica se o produto não é mais encontrado
    response_get = test_client.get(f"/produtos/{produto_id}")
    assert response_get.status_code == 404
