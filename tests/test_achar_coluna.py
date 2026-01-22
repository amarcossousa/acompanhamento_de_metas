import pytest
import pandas as pd
from scripts.utils import normalizar

def achar_coluna(df, palavras_chave):
    palavras_chave = [normalizar(p) for p in palavras_chave]
    for col in df.columns:
        col_norm = normalizar(col)
        if all(p in col_norm for p in palavras_chave):
            return col
    raise ValueError(f"❌ Coluna não encontrada: {palavras_chave}")


def test_achar_coluna_nome_tecnico():
    """
    Garante que a função encontra a coluna 'DADOS DE EXECUÇÃO > Nome do(a) técnico(a) responsável'.
    """
    df = pd.DataFrame(columns=[
        'DADOS DE EXECUÇÃO > Nome do(a) técnico(a) responsável',
        'DADOS DE EXECUÇÃO > Data da realização da atividade',
        'DADOS DE EXECUÇÃO > Município',
        'DADOS DE EXECUÇÃO > Comunidade',
        'Relato > Relato geral do acompanhamento'
    ])
    resultado = achar_coluna(df, ["nome", "tecnico"])
    assert resultado == 'DADOS DE EXECUÇÃO > Nome do(a) técnico(a) responsável'


def test_achar_coluna_data_realizacao():
    """
    Garante que a função encontra a coluna 'DADOS DE EXECUÇÃO > Data da realização da atividade'.
    """
    df = pd.DataFrame(columns=[
        'DADOS DE EXECUÇÃO > Nome do(a) técnico(a) responsável',
        'DADOS DE EXECUÇÃO > Data da realização da atividade',
        'DADOS DE EXECUÇÃO > Município',
        'DADOS DE EXECUÇÃO > Comunidade',
        'Relato > Relato geral do acompanhamento'
    ])
    resultado = achar_coluna(df, ["data", "realizacao"])
    assert resultado == 'DADOS DE EXECUÇÃO > Data da realização da atividade'


def test_achar_coluna_relato():
    """
    Garante que a função encontra a coluna 'Relato > Relato geral do acompanhamento'.
    """
    df = pd.DataFrame(columns=[
        'DADOS DE EXECUÇÃO > Nome do(a) técnico(a) responsável',
        'DADOS DE EXECUÇÃO > Data da realização da atividade',
        'DADOS DE EXECUÇÃO > Município',
        'DADOS DE EXECUÇÃO > Comunidade',
        'Relato > Relato geral do acompanhamento'
    ])
    resultado = achar_coluna(df, ["relato"])
    assert resultado == 'Relato > Relato geral do acompanhamento'


def test_achar_coluna_inexistente():
    """
    Garante que a função levanta erro quando a coluna não existe.
    """
    df = pd.DataFrame(columns=[
        'DADOS DE EXECUÇÃO > Nome do(a) técnico(a) responsável',
        'DADOS DE EXECUÇÃO > Data da realização da atividade',
        'DADOS DE EXECUÇÃO > Município',
        'DADOS DE EXECUÇÃO > Comunidade',
        'Relato > Relato geral do acompanhamento'
    ])
    with pytest.raises(ValueError):
        achar_coluna(df, ["coluna_inexistente"])
