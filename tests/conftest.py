import pytest
import pandas as pd

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
