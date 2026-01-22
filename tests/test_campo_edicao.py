import pytest
import pandas as pd

def test_latitude_edicao_convertida_para_float():
    coluna = "Local de edição (Latitude)"
    df = pd.DataFrame({coluna: ["-12.3456", "14.5678"]})

    df[coluna] = pd.to_numeric(df[coluna], errors="raise")
    assert pd.api.types.is_float_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato numérico"
    assert df[coluna].between(-90, 90).all(), f"❌ Valores fora do intervalo esperado em {coluna}"


def test_longitude_edicao_convertida_para_float():
    coluna = "Local de edição (Longitude)"
    df = pd.DataFrame({coluna: ["-40.1234", "55.6789"]})

    df[coluna] = pd.to_numeric(df[coluna], errors="raise")
    assert pd.api.types.is_float_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato numérico"
    assert df[coluna].between(-180, 180).all(), f"❌ Valores fora do intervalo esperado em {coluna}"


def test_criado_em_dispositivo_convertido_para_datetime():
    coluna = "Criado em (horário do dispositivo)"
    df = pd.DataFrame({coluna: ["2024-05-10 14:32", "2025-01-22 09:15"]})

    df[coluna] = pd.to_datetime(df[coluna], errors="raise")
    assert pd.api.types.is_datetime64_any_dtype(df[coluna]), f"❌ Coluna {coluna} não está em formato datetime"
