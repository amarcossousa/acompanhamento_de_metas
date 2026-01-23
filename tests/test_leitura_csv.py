import pandas as pd

def test_leitura_csv():
    df = pd.read_csv("data/acompanhamento.csv", sep=";", encoding="utf-8")
    assert not df.empty, "❌ O CSV não foi carregado corretamente"
    assert "Criado por" in df.columns, "❌ Coluna 'Criado por' não encontrada"
    assert "Criado em" in df.columns, "❌ Coluna 'Criado em' não encontrada"
