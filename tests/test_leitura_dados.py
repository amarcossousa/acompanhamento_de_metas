import pandas as pd
from pathlib import Path
import pytest


@pytest.mark.parametrize("encoding", ["utf-8-sig", "latin1"])
def test_csv_pode_ser_lido_com_varios_encodings(encoding):
    """
    Garante que o CSV pode ser lido com diferentes encodings comuns.
    Isso evita falhas caso o arquivo venha de fontes variadas.
    """
    caminho = Path("data/visitas.csv")
    assert caminho.exists(), "❌ O arquivo de dados não foi encontrado"

    try:
        df = pd.read_csv(
            caminho,
            encoding=encoding,
            sep=None,              # pandas detecta o separador
            engine="python",       # parser mais tolerante
            quoting=3,             # ignora aspas mal formadas
            on_bad_lines="skip"    # ignora linhas quebradas
        )
    except Exception as e:
        pytest.fail(f"❌ Falha ao ler CSV com encoding {encoding}: {e}")

    # Validações adicionais
    assert isinstance(df, pd.DataFrame), "❌ O resultado não é um DataFrame"
    assert not df.empty, "❌ DataFrame está vazio após leitura"
    assert len(df.columns) >= 5, f"❌ Número inesperado de colunas: {len(df.columns)}"
    assert df.shape