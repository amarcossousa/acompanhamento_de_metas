from scripts.ingestao.coletum_client import ColetumClient


QUERY_COLETIVAS = """
query BuscarColetivas {
  coletivas {
    id
    data
    municipio
    tema
  }
}
"""


def buscar_coletivas(
    client: ColetumClient,
    mes: int | None = None,
    ano: int | None = None
) -> list:
    """
    Contrato v1.0:
    - Sempre retorna uma lista
    - Não filtra por mes/ano ainda
    """
    resposta = client.executar_query(QUERY_COLETIVAS)

    data = resposta.get("data", {})
    coletivas = data.get("coletivas", [])

    if not isinstance(coletivas, list):
        return []

    return coletivas
