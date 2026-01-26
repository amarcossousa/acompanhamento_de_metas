import pandas as pd


def normalizar_registros(registros: list) -> pd.DataFrame:
    """
    Converte lista de dicionários em DataFrame.
    Sempre retorna DataFrame válido.
    """
    if not registros:
        return pd.DataFrame()

    return pd.json_normalize(registros)
