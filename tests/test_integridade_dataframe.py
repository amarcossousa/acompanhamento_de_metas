def test_dataframe_tem_colunas_obrigatorias(df_exemplo):
    colunas_esperadas = [
        "Criado por",
        "Atualizado por",
        "DADOS DE EXECUÇÃO > Município",
        "Relato > Relato geral do acompanhamento"
    ]

    for col in colunas_esperadas:
        assert col in df_exemplo.columns, f"❌ Coluna obrigatória {col} não encontrada"
