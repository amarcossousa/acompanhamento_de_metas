import pandas as pd


def consolidar_visitas_mensal_por_tecnico(
    df_visitas: pd.DataFrame,
    mes: int,
    ano: int
) -> pd.DataFrame:
    """
    Consolida visitas por técnico em um mês/ano específico.

    Espera um DataFrame com as colunas:
    - tecnico
    - ano
    - mes

    Retorna:
    - tecnico
    - total_visitas
    """

    if df_visitas.empty:
        return pd.DataFrame(columns=["tecnico", "total_visitas"])

    df_filtrado = df_visitas[
        (df_visitas["mes"] == mes) &
        (df_visitas["ano"] == ano)
    ]

    if df_filtrado.empty:
        return pd.DataFrame(columns=["tecnico", "total_visitas"])

    consolidado = (
        df_filtrado
        .groupby("tecnico")
        .size()
        .reset_index(name="total_visitas")
        .sort_values("tecnico")
        .reset_index(drop=True)
    )

    return consolidado
