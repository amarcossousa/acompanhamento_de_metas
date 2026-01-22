import pytest
import pandas as pd
from scripts.utils import normalizar

def test_coluna_visita_numero_eh_inteiro():
    """
    Garante que a coluna 'Visita n°' contém números inteiros válidos.
    """
    coluna = "DADOS DE EXECUÇÃO > RESULTADO DAS RECOMENDAÇÕES TÉCNICAS ANTERIORES > Visita n°"
    df = pd.DataFrame({coluna: ["1", "2", "3"]})

    try:
        df[coluna] = pd.to_numeric(df[coluna], downcast="integer", errors="raise")
    except Exception as e:
        pytest.fail(f"❌ Falha ao converter coluna {coluna} para inteiro: {e}")

    assert pd.api.types.is_integer_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato inteiro"


def test_coluna_data_visita_anterior_eh_datetime():
    """
    Garante que a coluna 'Data da Visita Anterior' pode ser convertida para datetime.
    """
    coluna = "DADOS DE EXECUÇÃO > RESULTADO DAS RECOMENDAÇÕES TÉCNICAS ANTERIORES > Data da Visita Anterior"
    df = pd.DataFrame({coluna: ["2024-04-10", "2025-01-15", "2023-12-01"]})

    try:
        df[coluna] = pd.to_datetime(df[coluna], errors="raise")
    except Exception as e:
        pytest.fail(f"❌ Falha ao converter coluna {coluna} para datetime: {e}")

    assert pd.api.types.is_datetime64_any_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato datetime"


def test_coluna_resultado_recomendacoes_eh_string_normalizavel():
    """
    Garante que a coluna de resultado das recomendações técnicas anteriores é string e pode ser normalizada.
    """
    coluna = "DADOS DE EXECUÇÃO > RESULTADO DAS RECOMENDAÇÕES TÉCNICAS ANTERIORES > RESULTADO DAS RECOMENDAÇÕES TÉCNICAS ANTERIORES"
    df = pd.DataFrame({coluna: ["Recomendação atendida", "Não atendida", "Parcialmente atendida"]})

    assert pd.api.types.is_string_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato string"

    normalizados = df[coluna].apply(normalizar).tolist()
    assert "recomendacao atendida" in normalizados
    assert "nao atendida" in normalizados
    assert "parcialmente atendida" in normalizados
