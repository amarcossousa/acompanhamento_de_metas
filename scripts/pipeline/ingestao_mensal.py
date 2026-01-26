from scripts.ingestao.coletum_client import ColetumClient
from scripts.ingestao.visitas_api import buscar_visitas
from scripts.ingestao.coletivas_api import buscar_coletivas
from scripts.normalizacao.normalizar import (
    normalizar_visitas,
    normalizar_coletivas
)


def executar_ingestao_mensal(token, mes, ano):
    client = ColetumClient(token)

    visitas_raw = buscar_visitas(client, mes, ano)
    coletivas_raw = buscar_coletivas(client, mes, ano)

    df_visitas = normalizar_visitas(visitas_raw)
    df_coletivas = normalizar_coletivas(coletivas_raw)

    return df_visitas, df_coletivas
