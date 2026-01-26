import pytest
import pandas as pd
import pytest
from scripts.ingestao.coletum_client import ColetumClient


@pytest.fixture
def mock_client(client):
    """
    Alias exigido por alguns testes.
    """
    return client


@pytest.fixture
def df_exemplo():
    """
    DataFrame de exemplo com colunas obrigatórias.
    Pode ser usado em vários testes.
    """
    return pd.DataFrame(columns=[
        "Criado por",
        "Atualizado por",
        "DADOS DE EXECUÇÃO > Município",
        "Relato > Relato geral do acompanhamento"
    ])

