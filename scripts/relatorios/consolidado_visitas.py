import pandas as pd


def consolidar_visitas_mensal_por_tecnico(df_visitas: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida visitas mensalmente por técnico.
    Espera um DataFrame já normalizado com:
    - municipio
    - data_realizacao
    - tecnico
    """

    if df_visitas.empty:
        return pd.DataFrame()

    df = df_visitas.copy()

    # Garante que a data está no formato datetime
    df["data_realizacao"] = pd.to_datetime(
        df["data_realizacao"], errors="coerce"
    )

    # Remove registros sem data válida
    df = df.dropna(subset=["data_realizacao"])

    # Cria coluna de referência mensal (YYYY-MM)
    df["mes"] = df["data_realizacao"].dt.to_period("M").astype(str)

    # Consolidação
    consolidado = (
        df.groupby(["tecnico", "mes"])
        .size()
        .reset_index(name="total_visitas")
        .sort_values(["mes", "tecnico"])
    )

    return consolidado
