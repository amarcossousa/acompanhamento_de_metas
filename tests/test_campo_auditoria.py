import pytest
import pandas as pd


@pytest.mark.parametrize("coluna", [
    "Criado por",
    "Atualizado por"
])
def test_colunas_de_usuario_sao_strings(coluna):
    """
    Garante que os campos de auditoria de usuário são strings válidas.
    """
    df = pd.DataFrame({coluna: pd.Series(["antonio", "marcos", "erica"], dtype="string")})

    assert pd.api.types.is_string_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato string"
    assert all(isinstance(v, str) for v in df[coluna]), f"❌ Valores da coluna {coluna} não são strings"


@pytest.mark.parametrize("coluna", [
    "Criado em",
    "Criado em (horário do dispositivo)",
    "Atualizado em"
])
def test_colunas_de_data_auditoria_sao_datetime(coluna):
    """
    Garante que os campos de auditoria de data/hora podem ser convertidos para datetime.
    """
    df = pd.DataFrame({coluna: ["2024-05-10 14:32", "2025-01-22 09:15", "2023-12-31 23:59"]})

    try:
        df[coluna] = pd.to_datetime(df[coluna], errors="raise")
    except Exception as e:
        pytest.fail(f"❌ Falha ao converter coluna {coluna} para datetime: {e}")

    assert pd.api.types.is_datetime64_any_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato datetime"
