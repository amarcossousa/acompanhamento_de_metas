import pandas as pd
import calendar
from fpdf import FPDF


def gerar_relatorio_pdf(arquivo_csv: str, mes: int, ano: int, saida_pdf: str):
    """
    Gera um relatório em PDF com calendário mensal de visitas por técnico,
    usando os dados exportados do Coletum.
    """

    # 1. Carregar dados
    df = pd.read_csv(arquivo_csv, sep=";")

    # 2. Converter coluna de data
    df["Criado em"] = pd.to_datetime(df["Criado em"], errors="coerce")

    # 3. Filtrar mês/ano
    df = df[(df["Criado em"].dt.month == mes) & (df["Criado em"].dt.year == ano)]

    # 4. Agrupar visitas por técnico e dia
    visitas = (
        df.groupby(["Criado por", df["Criado em"].dt.day])
        .size()
        .reset_index(name="Visitas")
    )

    # 5. Criar PDF
    pdf = FPDF()
    tecnicos = visitas["Criado por"].unique()

    for tecnico in tecnicos:
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, f"Relatório de {tecnico} - {calendar.month_name[mes]} {ano}", ln=True, align="C")

        # Criar calendário do mês
        cal = calendar.monthcalendar(ano, mes)
        for semana in cal:
            linha = ""
            for dia in semana:
                if dia == 0:
                    linha += "    "
                else:
                    v = visitas[(visitas["Criado por"] == tecnico) & (visitas["Criado em"] == dia)]
                    qtd = int(v["Visitas"].values[0]) if not v.empty else 0
                    linha += f"{dia}({qtd}) "
            pdf.cell(200, 10, linha, ln=True)

    # 6. Exportar PDF
    pdf.output(saida_pdf)
