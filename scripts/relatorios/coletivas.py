import pandas as pd

def carregar_coletivas(arquivo_csv_coletivas: str, mes: int, ano: int):
    df = pd.read_csv(arquivo_csv_coletivas, sep=";", encoding="utf-8")

    df["DataColetiva"] = pd.to_datetime(
        df["Dados de Execução > Data"], dayfirst=True, errors="coerce"
    )

    df = df[(df["DataColetiva"].dt.month == mes) & (df["DataColetiva"].dt.year == ano)]

    coletivas = (
        df.groupby(["Criado por", df["DataColetiva"].dt.day, "ATIVIDADE PRÉ-FIXADA > ATIVIDADES"])
        .size()
        .reset_index(name="qtd")
    )

    return coletivas
