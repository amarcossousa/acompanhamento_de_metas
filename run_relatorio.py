from scripts.relatorios.calendario_pdf import gerar_relatorio_pdf

# Caminho para sua planilha exportada do Coletum
arquivo_csv = "data/visitas.csv"

# Mês e ano que você quer testar
mes = 1   # Janeiro
ano = 2026

# Saída do PDF
saida_pdf = "reports/visitas_tecnicos_jan2026.pdf"

# Executa a função
gerar_relatorio_pdf(arquivo_csv, mes, ano, saida_pdf)

print("✅ Relatório gerado com sucesso:", saida_pdf)
