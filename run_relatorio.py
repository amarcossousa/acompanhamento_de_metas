import pandas as pd
from scripts.relatorios.calendario_pdf import RelatorioPDF, gerar_relatorio_pdf
from scripts.relatorios.consolidado import gerar_relatorio_consolidado

def main():
    arquivo_visitas = "data/visitas.csv"
    mes = 1   # exemplo: Janeiro
    ano = 2026
    saida_pdf = "reports/relatorio.pdf"

    pdf = RelatorioPDF()

    # Relatório calendário
    gerar_relatorio_pdf(arquivo_visitas, mes, ano, saida_pdf, pdf)

    # Carregar dados
    visitas_df = pd.read_csv(arquivo_visitas, sep=";", encoding="utf-8")
    metas_df = pd.read_csv("data/metas.csv", sep=";", encoding="utf-8")

    # Consolidado (agora passando mes e ano também)
    gerar_relatorio_consolidado(visitas_df, metas_df, pdf, mes, ano)

    # Salvar PDF final
    pdf.output(saida_pdf)


if __name__ == "__main__":
    main()
