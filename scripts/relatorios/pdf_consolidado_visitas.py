from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from pathlib import Path


def gerar_pdf_visitas_mensal_por_tecnico(
    df_consolidado,
    mes: int,
    ano: int,
    output_dir: Path
):
    """
    Gera relatório PDF mensal de visitas por técnico.

    Espera DataFrame com colunas:
    - tecnico
    - total_visitas
    """

    if df_consolidado.empty:
        raise ValueError("Não há dados para gerar o relatório")

    output_dir.mkdir(parents=True, exist_ok=True)

    arquivo_pdf = output_dir / f"relatorio_visitas_{ano}_{mes:02d}.pdf"

    doc = SimpleDocTemplate(
        str(arquivo_pdf),
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo = Paragraph(
        f"<b>Relatório Mensal de Visitas por Técnico</b><br/>{mes:02d}/{ano}",
        styles["Title"]
    )
    elementos.append(titulo)

    # Tabela
    dados_tabela = [["Técnico", "Total de Visitas"]]

    for _, row in df_consolidado.iterrows():
        dados_tabela.append([
            row["tecnico"],
            str(row["total_visitas"])
        ])

    tabela = Table(dados_tabela, colWidths=[300, 150])

    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 10),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
    ]))

    elementos.append(tabela)

    doc.build(elementos)

    return arquivo_pdf
