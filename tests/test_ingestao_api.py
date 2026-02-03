import pandas as pd
import pytest
from unittest.mock import patch, Mock

# imports futuros da v1.1
from scripts.ingestao.coletum_client import ColetumClient
from scripts.ingestao.visitas_api import buscar_visitas
from scripts.ingestao.coletivas_api import buscar_coletivas
from scripts.normalizacao.normalizacao import normalizar_visitas, normalizar_coletivas


# ---------------------------
# Fixtures
# ---------------------------

@pytest.fixture
def client():
    return ColetumClient(
        base_url="https://coletum.com/api/graphql",
        token="fake-token"
    )


@pytest.fixture
def resposta_api_visitas():
    return {
        "data": {
            "answer": {
                "answer": [
                    {
                        "dadosDeExecucao800970": {
                            "municipio800977": "Santaluz",
                            "dataDaRealizacaoDaAtividade800974": "2026-01-15"
                        }
                    }
                ]
            }
        }
    }


@pytest.fixture
def resposta_api_coletivas():
    return {
        "data": {
            "answer": {
                "answer": [
                    {
                        "dadosDeExecucao484334": {
                            "municipio484340": "Santaluz",
                            "data484336": "2026-01-20"
                        }
                    }
                ]
            }
        }
    }


# ---------------------------
# Testes do client
# ---------------------------

@patch("scripts.requests.post")
def test_client_faz_requisicao_graphql(mock_post, client):
    mock_response = Mock()
    mock_response.json.return_value = {"data": {}}
    mock_response.raise_for_status.return_value = None
    mock_post.return_value = mock_response

    query = "{ test }"
    response = client.executar_query(query)

    assert response == {"data": {}}
    mock_post.assert_called_once()


# ---------------------------
# Testes de Visitas
# ---------------------------

@patch("scripts.ingestao.visitas_api.ColetumClient.executar_query")
def test_buscar_visitas(mock_query, client, resposta_api_visitas):
    mock_query.return_value = resposta_api_visitas

    dados = buscar_visitas(client, mes=1, ano=2026)

    assert dados is not None
    assert isinstance(dados, list)
    assert len(dados) == 1


def test_normalizar_visitas_gera_dataframe(resposta_api_visitas):
    registros = resposta_api_visitas["data"]["answer"]["answer"]

    df = normalizar_visitas(registros)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "municipio" in df.columns
    assert "data_realizacao" in df.columns


# ---------------------------
# Testes de Coletivas
# ---------------------------

@patch("scripts.ingestao.coletivas_api.ColetumClient.executar_query")
def test_buscar_coletivas(mock_query, client, resposta_api_coletivas):
    mock_query.return_value = resposta_api_coletivas

    dados = buscar_coletivas(client, mes=1, ano=2026)

    assert dados is not None
    assert isinstance(dados, list)
    assert len(dados) == 1


def test_normalizar_coletivas_gera_dataframe(resposta_api_coletivas):
    registros = resposta_api_coletivas["data"]["answer"]["answer"]

    df = normalizar_coletivas(registros)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert "municipio" in df.columns
    assert "data_realizacao" in df.columns


# ---------------------------
# Teste de compatibilidade com CSV
# ---------------------------

def test_dataframe_pode_ser_salvo_como_csv(tmp_path, resposta_api_visitas):
    registros = resposta_api_visitas["data"]["answer"]["answer"]
    df = normalizar_visitas(registros)

    arquivo = tmp_path / "visitas.csv"
    df.to_csv(arquivo, index=False, encoding="utf-8-sig")

    assert arquivo.exists()

    
def test_buscar_visitas_retorna_lista(mock_client, monkeypatch):
    def fake_executar_query(query):
        return {
            "data": {
                "visitas": [
                    {"id": 1, "data": "2026-01-10"},
                    {"id": 2, "data": "2026-01-15"},
                ]
            }
        }

    monkeypatch.setattr(
        mock_client,
        "executar_query",
        fake_executar_query
    )

    registros = buscar_visitas(mock_client, 1, 2026)

    assert isinstance(registros, list)
    assert len(registros) == 2

