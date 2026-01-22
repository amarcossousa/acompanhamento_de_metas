import pytest
import pandas as pd

def test_data_atualizacao_maior_ou_igual_a_data_criacao():
    """
    Garante que a data de atualização seja sempre maior ou igual à data de criação.
    """
    df = pd.DataFrame({
        "Criado em": ["2024-05-10 14:32", "2025-01-22 09:15"],
        "Atualizado em": ["2024-05-11 10:00", "2025-01-22 09:15"]
    })

    # Converte para datetime
    df["Criado em"] = pd.to_datetime(df["Criado em"], errors="raise")
    df["Atualizado em"] = pd.to_datetime(df["Atualizado em"], errors="raise")

    # Verifica consistência
    assert (df["Atualizado em"] >= df["Criado em"]).all(), "❌ Há registros com atualização anterior à criação"
