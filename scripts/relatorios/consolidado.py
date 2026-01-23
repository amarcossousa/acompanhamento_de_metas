import pandas as pd
from datetime import datetime
from fpdf import FPDF

def gerar_relatorio_consolidado(visitas_df, metas_df, pdf: FPDF, mes: int, ano: int):
    # filtra mês e ano
    visitas_df["DataExecucao"] = pd.to_datetime(
        visitas_df["DADOS DE EXECUÇÃO > Data da realização da atividade"],
        dayfirst=True,
        errors="coerce"
    )
    visitas_df = visitas_df[
        (visitas_df["DataExecucao"].dt.month == mes) &
        (visitas_df["DataExecucao"].dt.year == ano)
    ]

    # agrupa por técnico
    resumo = visitas_df.groupby("Criado por").size().reset_index(name="Visitas")

    # cria página do consolidado
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório Consolidado", ln=True, align="C")
    pdf.ln(10)

    # tabela
    pdf.set_font("Arial", "B", 12)
    pdf.cell(60, 10, "Técnico", border=1)
    pdf.cell(60, 10, "Visitas", border=1)
    pdf.cell(60, 10, "Meta", border=1)
    pdf.ln()

    for _, row in resumo.iterrows():
        tecnico = row["Criado por"]
        visitas = row["Visitas"]
        meta = metas_df.loc[metas_df["Tecnico"] == tecnico, "Meta"].values
        meta = int(meta[0]) if len(meta) > 0 else 0

        pdf.set_font("Arial", "", 12)
        pdf.cell(60, 10, str(tecnico), border=1)
        pdf.cell(60, 10, str(visitas), border=1)
        pdf.cell(60, 10, str(meta), border=1)
        pdf.ln()
