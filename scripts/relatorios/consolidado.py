import pandas as pd
from fpdf import FPDF


def gerar_relatorio_consolidado(
    visitas_df: pd.DataFrame,
    metas_df: pd.DataFrame,
    pdf: FPDF,
    mes: int,
    ano: int,
    coletivas_df: pd.DataFrame | None = None
):
    # ==================================================
    # CONSOLIDADO DE VISITAS INDIVIDUAIS (INALTERADO)
    # ==================================================

    visitas_df["DataExecucao"] = pd.to_datetime(
        visitas_df["DADOS DE EXECUÇÃO > Data da realização da atividade"],
        dayfirst=True,
        errors="coerce"
    )

    visitas_df = visitas_df[
        (visitas_df["DataExecucao"].dt.month == mes) &
        (visitas_df["DataExecucao"].dt.year == ano)
    ]

    resumo = visitas_df.groupby("Criado por").size().reset_index(name="Visitas")
    resumo = resumo.sort_values(by="Visitas", ascending=False)

    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Relatório Consolidado - Visitas Individuais", ln=True, align="L")
    pdf.ln(8)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(70, 10, "Técnico", border=1)
    pdf.cell(40, 10, "Visitas", border=1)
    pdf.cell(40, 10, "Meta", border=1)
    pdf.ln()

    for _, row in resumo.iterrows():
        tecnico = row["Criado por"]
        visitas = row["Visitas"]

        meta = metas_df.loc[
            metas_df["Tecnico"] == tecnico,
            "Meta"
        ].values
        meta = int(meta[0]) if len(meta) > 0 else 0

        pdf.set_font("Arial", "", 12)
        pdf.cell(70, 10, str(tecnico), border=1)
        pdf.cell(40, 10, str(visitas), border=1)
        pdf.cell(40, 10, str(meta), border=1)
        pdf.ln()

    # ==================================================
    # NOVA FOLHA — ATIVIDADES COLETIVAS (SEM METAS)
    # ==================================================

    if coletivas_df is None or coletivas_df.empty:
        return

    # Validação defensiva
    colunas_necessarias = [
        "Dados de Execução > Data",
        "Dados de Execução > COMUNIDADE",
        "Dados de Execução > MUNICÍPIO",
        "ATIVIDADE PRÉ-FIXADA > ATIVIDADES",
        "Criado por"
    ]

    for col in colunas_necessarias:
        if col not in coletivas_df.columns:
            return

    coletivas_df["DataExecucao"] = pd.  to_datetime(
        coletivas_df["Dados de Execução > Data"],
        dayfirst=True,
        errors="coerce"
    )

    coletivas_df = coletivas_df[
        (coletivas_df["DataExecucao"].dt.month == mes) &
        (coletivas_df["DataExecucao"].dt.year == ano)
    
    ]
    coletivas_df = coletivas_df.sort_values(
        by=["DataExecucao", "Criado por"],
        ascending=[True, True]
    )

    if coletivas_df.empty:
        return

    pdf.ln(8)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Atividades Coletivas", ln=True, align="L")
    pdf.ln(6)

    pdf.set_font("Arial", "B", 10)
    pdf.cell(35, 8, "Data", border=1)
    pdf.cell(40, 8, "Técnico", border=1)
    pdf.cell(40, 8, "Comunidade", border=1)
    pdf.cell(40, 8, "Município", border=1)
    pdf.cell(35, 8, "Atividade", border=1)
    pdf.ln()

    pdf.set_font("Arial", "", 9)

    for _, row in coletivas_df.iterrows():
        data_fmt = row["DataExecucao"].strftime("%d/%m/%Y") if pd.notna(row["DataExecucao"]) else ""

        pdf.cell(35, 8, data_fmt, border=1)
        pdf.cell(40, 8, str(row["Criado por"])[:25], border=1)
        pdf.cell(40, 8, str(row["Dados de Execução > COMUNIDADE"])[:25], border=1)
        pdf.cell(40, 8, str(row["Dados de Execução > MUNICÍPIO"])[:25], border=1)
        pdf.cell(35, 8, str(row["ATIVIDADE PRÉ-FIXADA > ATIVIDADES"])[:25], border=1)
        pdf.ln()
