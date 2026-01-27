import sys
from datetime import datetime
from scripts.ingestao.visitas_api_calendario import gerar_relatorio_visitas

def main():
    mes = 1
    ano = 2026

    if len(sys.argv) >= 3:
        mes = int(sys.argv[1])
        ano = int(sys.argv[2])

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = f"reports/relatorio_visitas_api_{mes:02d}{ano}_{timestamp}.pdf"

    print(f"📊 Gerando relatório para {mes:02d}/{ano}")
    gerar_relatorio_visitas(mes, ano, pdf_path)

if __name__ == "__main__":
    main()
