import pytest
import pandas as pd
from scripts.utils import normalizar

def test_objetivos_do_acompanhamento_eh_string_normalizada():
    """
    Garante que a coluna de objetivos do acompanhamento é string e pode ser normalizada.
    """
    coluna = "OBJETIVOS DO ACOMPANHAMENTO > Objetivos do acompanhamento"
    df = pd.DataFrame({coluna: ["Melhorar produção agrícola", "Aumentar renda familiar"]})

    assert pd.api.types.is_string_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato string"

    normalizados = df[coluna].apply(normalizar).tolist()
    assert "melhorar producao agricola" in normalizados
    assert "aumentar renda familiar" in normalizados


def test_relato_geral_do_acompanhamento_eh_string_normalizada():
    """
    Garante que a coluna de relato geral do acompanhamento é string e pode ser normalizada.
    """
    coluna = "Relato > Relato geral do acompanhamento"
    df = pd.DataFrame({coluna: ["Visita realizada com sucesso", "Necessidade de ajustes técnicos"]})

    assert pd.api.types.is_string_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato string"

    normalizados = df[coluna].apply(normalizar).tolist()
    assert "visita realizada com sucesso" in normalizados
    assert "necessidade de ajustes tecnicos" in normalizados
