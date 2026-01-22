import pandas as pd
from pathlib import Path
import pytest


def test_arquivo_de_dados_existe():
    caminho = Path("data/acompanhamento.csv")
    assert caminho.exists(), "❌ O arquivo de dados não foi encontrado"


def test_csv_pode_ser_lido_com_configuracao_tolerante():
    """
    Garante que o CSV real pode ser lido usando uma estratégia robusta,
    mesmo com aspas quebradas e separadores inconsistentes.
    """
    caminho = Path("data/acompanhamento.csv")

    try:
        df = pd.read_csv(
            caminho,
            encoding="latin1",     # encoding real mais comum nesses casos
            sep=None,              # pandas detecta o separador
            engine="python",       # parser mais tolerante
            quoting=3,             # ignora aspas mal formadas
            on_bad_lines="skip"    # ignora linhas quebradas
        )
    except Exception as e:
        pytest.fail(f"❌ Falha ao ler CSV mesmo em modo tolerante: {e}")

    assert not df.empty, "❌ DataFrame está vazio após leitura tolerante"
    assert len(df.columns) >= 5, "❌ Número inesperado de colunas"
