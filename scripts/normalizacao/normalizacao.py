import pandas as pd
import re
import unicodedata


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

def normalizar_visitas_com_tecnico(registros: list) -> pd.DataFrame:
    """
    Normaliza os registros da API de visitas incluindo o técnico responsável.
    Usa normalizar_visitas como base, preservando o contrato atual.
    """

    # Reaproveita a normalização mínima já existente
    df = normalizar_visitas(registros)

    tecnicos = []
    for item in registros:
        # Ajuste a chave abaixo se o nome real for diferente na API
        tecnico = (
            item.get("responsavel")
            or item.get("tecnico")
            or item.get("usuario")
            or "Não informado"
        )
        tecnicos.append(tecnico)

    df["tecnico"] = tecnicos
    return df


def normalizar_chave(texto):

    if not texto:
        return ""

    texto = texto.lower()

    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')

    texto = re.sub(r'\(.*?\)', '', texto)
    texto = re.sub(r'[^a-z0-9 ]', '', texto)

    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto


