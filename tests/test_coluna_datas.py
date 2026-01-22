import pytest
import pandas as pd
from scripts.utils import normalizar, achar_coluna

@pytest.mark.parametrize("coluna", [
    "DADOS DE EXECUÇÃO > Data da realização da atividade",
    "DADOS DE EXECUÇÃO > RESULTADO DAS RECOMENDAÇÕES TÉCNICAS ANTERIORES > Data da Visita Anterior"
])
def test_colunas_de_datas_sao_convertidas_para_datetime(coluna):
    """
    Garante que colunas de datas podem ser convertidas corretamente para datetime.
    """
    # Criamos um DataFrame falso com a coluna de interesse
    df = pd.DataFrame({
        coluna: ["2024-05-10", "2025-01-22", "2023-12-31"]
    })

    try:
        # Tenta converter para datetime
        df[coluna] = pd.to_datetime(df[coluna], errors="raise", dayfirst=False)
    except Exception as e:
        pytest.fail(f"❌ Falha ao converter coluna {coluna} para datetime: {e}")

    # Validações
    assert pd.api.types.is_datetime64_any_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato datetime"
    assert df[coluna].dt.year.min() >= 2020, "❌ Datas inesperadas (antes de 2020)"
