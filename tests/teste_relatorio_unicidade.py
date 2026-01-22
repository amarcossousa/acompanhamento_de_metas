import pytest
import pandas as pd

def test_cpf_responsavel_unico_por_titular():
    """
    Garante que não existam CPFs duplicados para o mesmo titular.
    Se houver, lista quais são e quantas vezes aparecem.
    """
    coluna_cpf = "CPF Responsável para identificação do grupo familiar > CPF do Titular 1 do Grupo Familiar"
    coluna_nome = "CPF Responsável para identificação do grupo familiar > Nome:"

    df = pd.DataFrame({
        coluna_cpf: ["01234567890", "98765432100", "01234567890"],
        coluna_nome: ["João da Silva", "Maria Souza", "João da Silva"]
    })

    # Conta duplicados
    duplicados = df.groupby([coluna_cpf, coluna_nome]).size().reset_index(name="quantidade")
    duplicados = duplicados[duplicados["quantidade"] > 1]

    # Se houver duplicados, falha mostrando quais são
    assert duplicados.empty, f"❌ Existem CPFs duplicados:\n{duplicados}"
