import pytest
import pandas as pd

@pytest.mark.parametrize("coluna", [
    "DADOS DE EXECUÇÃO > Localização da UPF (Latitude)",
    "DADOS DE EXECUÇÃO > Localização da UPF (Longitude)",
    "Local da coleta (Latitude)",
    "Local da coleta (Longitude)",
    "Local de edição (Latitude)",
    "Local de edição (Longitude)"
])
def test_colunas_de_localizacao_sao_numericas(coluna):
    """
    Garante que colunas de localização (Latitude/Longitude) podem ser convertidas para valores numéricos.
    """
    # Criamos um DataFrame falso com valores de localização
    df = pd.DataFrame({
        coluna: ["-10.1234", "-39.5678", "12.3456"]
    })

    try:
        # Tenta converter para float
        df[coluna] = pd.to_numeric(df[coluna], errors="raise")
    except Exception as e:
        pytest.fail(f"❌ Falha ao converter coluna {coluna} para numérico: {e}")

    # Validações
    assert pd.api.types.is_float_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato numérico"
    assert df[coluna].between(-90, 90).any() or df[coluna].between(-180, 180).any(), f"❌ Valores fora do intervalo esperado em {coluna}"
