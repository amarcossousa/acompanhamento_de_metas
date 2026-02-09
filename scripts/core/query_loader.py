import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

QUERIES_PATH = os.path.join(BASE_DIR, "graphql", "queries")


def carregar_query(nome_arquivo: str) -> str:
    caminho = os.path.join(QUERIES_PATH, nome_arquivo)

    with open(caminho, "r", encoding="utf-8") as f:
        return f.read()
