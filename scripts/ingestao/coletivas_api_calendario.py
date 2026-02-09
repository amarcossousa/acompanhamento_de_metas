import os
import pandas as pd
import requests
from datetime import datetime
from dotenv import load_dotenv

from scripts.core.query_loader import carregar_query

QUERY_VISITAS = carregar_query("answer_form_32933.graphql")
QUERY_COLETIVAS = carregar_query("answer_form_31179.graphql")

load_dotenv()

ENDPOINT = os.getenv("COLETUM_ENDPOINT")
TOKEN = os.getenv("COLETUM_TOKEN")


def buscar_coletivas_api(mes: int, ano: int) -> pd.DataFrame:
    query = carregar_query("answer_form_31179.graphql")


    url = f"{ENDPOINT}?query={query}&token={TOKEN}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()

    itens = data["data"]["answer"]["answer"]

    rows = []
    for item in itens:
        data_str = item["dadosDeExecucao484334"]["data484336"]
        nome = item["atividadePre_fixada484342"]["atividades484343"]
        user = item["metaData"]["userName"]

        # converter data
        data_dt = datetime.strptime(data_str, "%Y-%m-%d")

        rows.append({
            "data_coletiva": data_dt,
            "nome_coletiva": nome,
            "userName": user
        })

    df = pd.DataFrame(rows)

    # filtrar por mês/ano
    df = df[
        (df["data_coletiva"].dt.month == mes) &
        (df["data_coletiva"].dt.year == ano)
    ]

    return df
