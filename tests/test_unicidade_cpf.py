import pytest
import pandas as pd

def test_cpf_responsavel_unico_por_titular():
    """
    Garante que não existam CPFs duplicados para o mesmo titular do grupo familiar.
    """
    coluna_cpf = "CPF Responsável para identificação do grupo familiar > CPF do Titular 1 do Grupo Familiar"
    coluna_nome = "CPF Responsável para identificação do grupo familiar > Nome:"

    df = pd.DataFrame({
        coluna_cpf: ["01234567890", "98765432100", "01234567890"],
        coluna_nome: ["João da Silva", "Maria Souza", "João da Silva"]
    })

    # Verifica duplicatas
    duplicados = df.duplicated(subset=[coluna_cpf, coluna_nome], keep=False)

    assert not duplicados.any(), "❌ Existem CPFs duplicados para o mesmo titular"
