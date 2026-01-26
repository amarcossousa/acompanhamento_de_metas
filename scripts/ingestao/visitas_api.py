from scripts.ingestao.coletum_client import ColetumClient


QUERY_VISITAS = """
query BuscarVisitas {
  visitas {
    id
    data
    municipio
    tecnico
  }
}
"""


def buscar_visitas(
    client: ColetumClient,
    mes: int | None = None,
    ano: int | None = None
) -> list:
    """
    Contrato v1.0:
    - Sempre retorna uma lista
    - Não filtra por mes/ano ainda
    """
    resposta = client.executar_query(QUERY_VISITAS)

    data = resposta.get("data", {})
    visitas = data.get("visitas", [])

    if not isinstance(visitas, list):
        return []

    return visitas
