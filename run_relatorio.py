import pandas as pd
from scripts.relatorios.calendario_pdf import RelatorioPDF, gerar_relatorio_pdf
from scripts.relatorios.consolidado import gerar_relatorio_consolidado
from datetime import datetime
import os

def main():
    arquivo_visitas = "data/visitas.csv"
    mes = 1  # exemplo: Janeiro
    ano = 2026

    # nome temporário
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saida_pdf_temp = f"reports/temp_relatorio_{timestamp}.pdf"
    saida_pdf_final = f"reports/relatorio_{timestamp}.pdf"

    pdf = RelatorioPDF()

    # Relatório calendário
    gerar_relatorio_pdf(arquivo_visitas, mes, ano, pdf)

    # Carregar dados
    visitas_df = pd.read_csv(arquivo_visitas, sep=";", encoding="utf-8")
    metas_df = pd.read_csv("data/metas.csv", sep=";", encoding="utf-8")

    # Consolidado
    gerar_relatorio_consolidado(visitas_df, metas_df, pdf, mes, ano)

    # SALVA O PDF TEMPORÁRIO
    pdf.output(saida_pdf_temp)

    # RENOMEIA PARA FINAL
    os.rename(saida_pdf_temp, saida_pdf_final)

if __name__ == "__main__":
    main()
