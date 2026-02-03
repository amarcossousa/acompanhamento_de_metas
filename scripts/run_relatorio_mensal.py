from pathlib import Path
import sys

from scripts.servicos.consolidado_visitas_service import (
    consolidar_visitas_mensal_por_tecnico
)
from scripts.relatorios.pdf_consolidado_visitas import (
    gerar_pdf_visitas_mensal_por_tecnico
)
from scripts.ingestao.visitas_api_ingestao import (
    buscar_visitas_api  # ajuste se o nome for outro
)
from scripts.normalizacao.visitas import (
    normalizar_visitas_com_tecnico  # a nova função
)


def main(mes: int, ano: int):
    """
    Script executável para gerar relatório mensal de visitas por técnico.
    """

    print("🔎 Buscando dados da API...")
    respostas_api = buscar_visitas_api()

    print("🧹 Normalizando dados...")
    df_visitas = normalizar_visitas_com_tecnico(respostas_api)

    print("📊 Gerando consolidado mensal...")
    df_consolidado = consolidar_visitas_mensal_por_tecnico(
        df_visitas=df_visitas,
        mes=mes,
        ano=ano
    )

    if df_consolidado.empty:
        print("⚠️ Nenhum dado encontrado para o período informado.")
        return

    print("📄 Gerando PDF...")
    pdf_path = gerar_pdf_visitas_mensal_por_tecnico(
        df_consolidado=df_consolidado,
        mes=mes,
        ano=ano,
        output_dir=Path("scripts/relatorios/saidas")
    )

    print(f"✅ Relatório gerado com sucesso: {pdf_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso:")
        print("  python scripts/run_relatorio_mensal.py <mes> <ano>")
        print("Exemplo:")
        print("  python scripts/run_relatorio_mensal.py 1 2025")
        sys.exit(1)

    mes = int(sys.argv[1])
    ano = int(sys.argv[2])

    main(mes, ano)
