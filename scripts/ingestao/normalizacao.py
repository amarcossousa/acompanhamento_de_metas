import pandas as pd


def normalizar_visitas(registros: list) -> pd.DataFrame:
    """
    Normaliza os registros da API de visitas para um DataFrame padronizado.
    """

    linhas = []
    for item in registros:
        dados = item.get("dadosDeExecucao800970", {})

        linhas.append({
            "municipio": dados.get("municipio800977", ""),
            "data_realizacao": dados.get("dataDaRealizacaoDaAtividade800974", "")
        })

    return pd.DataFrame(linhas)


def normalizar_coletivas(registros: list) -> pd.DataFrame:
    """
    Normaliza os registros da API de coletivas para um DataFrame padronizado.
    """

    linhas = []
    for item in registros:
        dados = item.get("dadosDeExecucao484334", {})

        linhas.append({
            "municipio": dados.get("municipio484340", ""),
            "data_realizacao": dados.get("data484336", "")
        })

    return pd.DataFrame(linhas)
