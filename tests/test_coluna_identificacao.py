import pytest
import pandas as pd
from scripts.utils import normalizar, achar_coluna


def test_coluna_cpf_eh_string():
    coluna = "CPF Responsável para identificação do grupo familiar > CPF do Titular 1 do Grupo Familiar"
    df = pd.DataFrame({coluna: pd.Series(["01234567890", "98765432100"], dtype="string")})

    # Verifica se os valores são strings
    assert pd.api.types.is_string_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato string"
    assert df[coluna].str.len().eq(11).all(), f"❌ CPF inválido na coluna {coluna}"



def test_coluna_nome_responsavel_normalizada():
    """
    Garante que a coluna de Nome do responsável pode ser normalizada corretamente.
    """
    coluna = "CPF Responsável para identificação do grupo familiar > Nome:"
    df = pd.DataFrame({coluna: ["João da Silva", "MARIA DE SOUZA", "Érica"]})

    # Normaliza os nomes
    nomes_normalizados = df[coluna].apply(normalizar)

    # Validações
    assert "joao da silva" in nomes_normalizados.values
    assert "maria de souza" in nomes_normalizados.values
    assert "erica" in nomes_normalizados.values
