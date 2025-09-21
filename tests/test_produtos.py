"""Teste de integração para o ciclo de vida completo dos produtos."""

from fastapi.testclient import TestClient
from fastapi import status


def test_ciclo_de_vida_do_produto(test_client: TestClient):
    """
    Testa o ciclo completo de um produto:
    1. Criação (POST)
    2. Leitura (GET)
    3. Atualização (PUT)
    4. Remoção (DELETE)
    """
    produto_data_inicial = {
        "nome": "Teclado RGB",
        "preco": 350.75,
        "categoria": "Periféricos",
        "qtd_estoque": 50,
    }
    response_create = test_client.post("/produtos/", json=produto_data_inicial)
    assert (
        response_create.status_code == status.HTTP_201_CREATED
    ), "Falha ao criar o produto"

    data_criado = response_create.json()
    assert data_criado["nome"] == produto_data_inicial["nome"]
    assert "id" in data_criado
    produto_id = data_criado["id"]

    # 2. Leitura do produto criado (individual e na lista)
    response_get = test_client.get(f"/produtos/{produto_id}")
    assert (
        response_get.status_code == status.HTTP_200_OK
    ), "Falha ao obter o produto pelo ID"
    assert response_get.json()["categoria"] == "Periféricos"

    response_list = test_client.get("/produtos/")
    assert response_list.status_code == status.HTTP_200_OK, "Falha ao listar os produtos"
    assert len(response_list.json()) > 0, "A lista de produtos não deveria estar vazia"

    # 3. Atualização do produto (URL corrigida)
    produto_data_atualizado = {
        "nome": "Teclado Mecânico RGB",
        "preco": 499.90,
        "categoria": "Periféricos",
        "qtd_estoque": 45,
    }
    response_update = test_client.put(
        f"/produtos/{produto_id}", json=produto_data_atualizado
    )
    assert (
        response_update.status_code == status.HTTP_200_OK
    ), "Falha ao atualizar o produto"
    data_atualizado = response_update.json()
    assert data_atualizado["nome"] == "Teclado Mecânico RGB"
    assert data_atualizado["qtd_estoque"] == 45

    # 4. Remoção do produto (URL corrigida)
    response_delete = test_client.delete(f"/produtos/{produto_id}")
    assert response_delete.status_code == status.HTTP_200_OK, "Falha ao deletar produto"

    # Confirma que o produto foi realmente removido
    response_get_after_delete = test_client.get(f"/produtos/{produto_id}")
    assert (
        response_get_after_delete.status_code == status.HTTP_404_NOT_FOUND
    ), "Produto não foi removido corretamente"
