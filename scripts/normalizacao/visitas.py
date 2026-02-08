import pandas as pd


def normalizar_visitas_api(respostas: list) -> pd.DataFrame:
    """
    Converte respostas da API do Coletum (visitas)
    em DataFrame mínimo para consolidados.
    """

    if not respostas:
        return pd.DataFrame()

    registros = []

    for item in respostas:
        answer = item.get("answer", {})
        meta = item.get("metaData", {})

        dados_execucao = answer.get("dadosDeExecucao800970", {})

        data_raw = dados_execucao.get("dataDaRealizacaoDaAtividade800974")

        if not data_raw:
            continue

        data_execucao = pd.to_datetime(data_raw, errors="coerce")

        registros.append({
            "tecnico": meta.get("userName"),
            "data_execucao": data_execucao,
            "ano": data_execucao.year if pd.notnull(data_execucao) else None,
            "mes": data_execucao.month if pd.notnull(data_execucao) else None,
        })

    df = pd.DataFrame(registros)

    return df.dropna(subset=["tecnico", "data_execucao"])

def normalizar_visitas_com_tecnico(registros: list) -> pd.DataFrame:
    """
    Normaliza visitas incluindo técnico e data.
    Usado exclusivamente para consolidados.
    NÃO afeta o fluxo atual de calendário.
    """

    linhas = []

    for item in registros:
        try:
            tecnico = item["metaData"]["userName"]
            dados = item["answer"]["dadosDeExecucao800970"]

            data = dados.get("dataDaRealizacaoDaAtividade800974")

            linhas.append({
                "tecnico": tecnico,
                "data_realizacao": data
            })

        except (KeyError, TypeError):
            continue

    df = pd.DataFrame(linhas)

    if not df.empty:
        df["data_realizacao"] = pd.to_datetime(
            df["data_realizacao"],
            errors="coerce"
        )
        df = df.dropna(subset=["data_realizacao"])

        df["ano"] = df["data_realizacao"].dt.year
        df["mes"] = df["data_realizacao"].dt.month

    return df

