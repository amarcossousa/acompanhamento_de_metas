import pytest
import pandas as pd
from scripts.utils import normalizar

@pytest.mark.parametrize("coluna,valores_normalizados", [
    ("DADOS DE EXECUÇÃO > Território", ["territorio norte", "territorio sul"]),
    ("DADOS DE EXECUÇÃO > Município", ["monte santo", "euclides da cunha"]),
    ("DADOS DE EXECUÇÃO > Comunidade", ["comunidade a", "comunidade b"])
])
def test_colunas_de_territorio_municipio_comunidade_sao_strings(coluna, valores_normalizados):
    """
    Garante que as colunas de território, município e comunidade são strings e podem ser normalizadas.
    """
    df = pd.DataFrame({coluna: ["Território Norte", "Território Sul"]}) if "Território" in coluna else \
         pd.DataFrame({coluna: ["Monte Santo", "Euclides da Cunha"]}) if "Município" in coluna else \
         pd.DataFrame({coluna: ["Comunidade A", "Comunidade B"]})

    # Verifica se os valores são strings
    assert pd.api.types.is_string_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato string"

    # Normaliza os valores
    normalizados = df[coluna].apply(normalizar).tolist()

    # Confere se os valores esperados aparecem
    for esperado in valores_normalizados:
        assert esperado in normalizados, f"❌ Valor esperado '{esperado}' não encontrado na coluna {coluna}"
