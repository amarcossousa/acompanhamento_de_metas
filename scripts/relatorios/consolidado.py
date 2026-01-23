import pandas as pd
from fpdf import FPDF

def gerar_relatorio_consolidado(visitas_df, metas_df, pdf: FPDF, mes: int, ano: int):
    # Converter a coluna de datas
    visitas_df["DataExecucao"] = pd.to_datetime(
        visitas_df["DADOS DE EXECUÇÃO > Data da realização da atividade"],
        dayfirst=True,
        errors="coerce"
    )

    # Filtrar apenas o mês/ano desejado
    visitas_mes = visitas_df[
        (visitas_df["DataExecucao"].dt.month == mes) &
        (visitas_df["DataExecucao"].dt.year == ano)
    ]

    # Agrupar visitas por técnico
    resumo = visitas_mes.groupby("Criado por").size().reset_index(name="Executado")

    # Juntar com metas
    resumo = resumo.merge(metas_df, left_on="Criado por", right_on="Tecnico", how="left")

    # Calcular percentual de cumprimento
    resumo["Cumprimento (%)"] = (resumo["Executado"] / resumo["Meta"] * 100).round(1)

    # Ordenar por cumprimento
    resumo = resumo.sort_values(by="Cumprimento (%)", ascending=False)

    # Adicionar nova página no PDF
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, f"Resumo Consolidado - {mes}/{ano}", ln=True, align="C")

    # Cabeçalho da tabela
    pdf.set_font("Arial", "B", 12)
    pdf.cell(50, 10, "Técnico", 1)
    pdf.cell(30, 10, "Meta", 1)
    pdf.cell(30, 10, "Executado", 1)
    pdf.cell(50, 10, "Cumprimento (%)", 1)
    pdf.ln()

    # Linhas da tabela
    pdf.set_font("Arial", "", 12)
    for _, row in resumo.iterrows():
        pdf.cell(50, 10, str(row["Criado por"]), 1)
        pdf.cell(30, 10, str(row["Meta"]), 1)
        pdf.cell(30, 10, str(row["Executado"]), 1)
        pdf.cell(50, 10, f"{row['Cumprimento (%)']}%", 1)
        pdf.ln()
