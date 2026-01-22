import pytest
from scripts.utils import normalizar

@pytest.mark.parametrize("entrada, esperado", [
    ("Árvore", "arvore"),
    ("CÃO", "cao"),
    ("  teste  ", "teste"),
    ("João da Silva", "joao da silva"),
    (123, "123"),
    (None, "none"),
])
def test_funcao_normalizar(entrada, esperado):
    """
    Garante que a função normalizar remove acentos, 
    converte para minúsculas e elimina espaços extras.
    """
    try:
        resultado = normalizar(entrada)
    except Exception as e:
        pytest.fail(f"❌ Falha ao executar normalizar: {e}")

    assert resultado == esperado, f"❌ Resultado inesperado: {resultado} (esperado: {esperado})"
