import os
from dotenv import load_dotenv
from scripts.ingestao.coletum_client import ColetumClient
from scripts.core.query_loader import carregar_query

QUERY_VISITAS = carregar_query("answer_form_32933.graphql")
QUERY_COLETIVAS = carregar_query("answer_form_31179.graphql")

# ===============================
# CONFIGURAÇÃO
# ===============================

load_dotenv()

COLETUM_ENDPOINT = os.getenv("COLETUM_ENDPOINT")
COLETUM_TOKEN = os.getenv("COLETUM_TOKEN")

if not COLETUM_ENDPOINT or not COLETUM_TOKEN:
    raise EnvironmentError("COLETUM_ENDPOINT ou COLETUM_TOKEN não configurados")


# ===============================
# QUERY VISITAS (FORM 32933)
# ===============================



# ===============================
# INGESTÃO
# ===============================

def buscar_visitas_api() -> list:
    """
    Busca todas as visitas no Coletum (formulário 32933).

    Retorna:
    - Lista bruta de registros (answer)
    - NÃO filtra por data
    - NÃO salva em disco
    """

    client = ColetumClient(
        endpoint=COLETUM_ENDPOINT,
        token=COLETUM_TOKEN
    )

    resposta = client.executar_query(QUERY_VISITAS)

    dados = resposta.get("data", {}).get("answer", [])

    if not isinstance(dados, list):
        return []

    return dados
