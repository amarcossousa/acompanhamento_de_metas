import unicodedata

def normalizar(texto):
    texto = str(texto)
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.lower().strip()

def achar_coluna(df, palavras_chave):
    """
    Localiza a coluna cujo nome contém todas as palavras-chave normalizadas.
    Retorna o nome exato da coluna encontrada.
    
    Exemplo:
    >>> achar_coluna(df, ["nome", "tecnico"])
    'DADOS DE EXECUÇÃO > Nome do(a) técnico(a) responsável'
    """
    # Normaliza as palavras-chave
    palavras_chave = [normalizar(p) for p in palavras_chave]

    # Percorre todas as colunas do DataFrame
    for col in df.columns:
        col_norm = normalizar(col)
        # Verifica se todas as palavras-chave estão presentes no nome da coluna
        if all(p in col_norm for p in palavras_chave):
            return col

    # Se nenhuma coluna corresponde, levanta erro
    raise ValueError(f"❌ Coluna não encontrada para palavras-chave: {palavras_chave}")

