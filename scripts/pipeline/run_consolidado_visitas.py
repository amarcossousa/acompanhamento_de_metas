from scripts.ingestao.visitas_api_ingestao import ingestir_visitas
from scripts.servicos.consolidado_visitas_service import consolidar_visitas_mensal_por_tecnico
import pandas as pd

def main():
    parquet = ingestir_visitas("2026-01")
    df = pd.read_parquet(parquet)

    consolidado = consolidar_visitas_mensal_por_tecnico(df)
    gerar_pdf_visitas_mensal(consolidado)
