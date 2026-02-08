import sys
import os
import pandas as pd
from datetime import datetime

from scripts.relatorios.consolidado_visitas import RelatorioPDF, gerar_relatorio_pdf
from scripts.relatorios.consolidado import gerar_relatorio_consolidado


def main():
    arquivo_visitas = "data/visitas.csv"
    arquivo_coletivas = "data/coletivas.csv"
    arquivo_metas = "data/metas.csv"

    # valores padrão
    mes = 1
    ano = 2026

    # parâmetros do .bat
    if len(sys.argv) >= 3:
        mes = int(sys.argv[1])
        ano = int(sys.argv[2])

    print(f"📊 Gerando relatório para {mes:02d}/{ano}")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saida_pdf_temp = f"reports/temp_relatorio_{timestamp}.pdf"
    saida_pdf_final = f"reports/relatorio_{mes:02d}_{ano}_{timestamp}.pdf"

    os.makedirs("reports", exist_ok=True)

    pdf = RelatorioPDF()

    # Calendário (já existente)
    gerar_relatorio_pdf(arquivo_visitas, mes, ano, pdf)

    # Carrega dados
    visitas_df = pd.read_csv(arquivo_visitas, sep=";", encoding="utf-8")
    metas_df = pd.read_csv(arquivo_metas, sep=";", encoding="utf-8")

    coletivas_df = pd.read_csv(
        arquivo_coletivas,
        sep=";",
        encoding="utf-8"
    )

    # Consolidado + Coletivas
    gerar_relatorio_consolidado(
        visitas_df,
        metas_df,
        pdf,
        mes,
        ano,
        coletivas_df
    )

    pdf.output(saida_pdf_temp)
    os.rename(saida_pdf_temp, saida_pdf_final)

    print(f"✅ Relatório gerado em: {saida_pdf_final}")


if __name__ == "__main__":
    main()
