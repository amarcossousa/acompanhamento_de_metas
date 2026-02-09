import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF

from scripts.ingestao.coletum_client import ColetumClient

from scripts.core.query_loader import carregar_query

QUERY_VISITAS = carregar_query("answer_form_32933.graphql")
QUERY_COLETIVAS = carregar_query("answer_form_31179.graphql")

load_dotenv()

ENDPOINT = os.getenv("COLETUM_ENDPOINT")
TOKEN = os.getenv("COLETUM_TOKEN")

def normalizar_nome(nome):
    if not nome:
        return ""
    return str(nome).strip().split()[0].title()


def normalizar_atividade(nome):
    if not nome:
        return "NÃO INFORMADO"
    return str(nome).strip().title()


class PDFTabela(FPDF):

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "", 8)
        texto = f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Fonte: Coletum API"
        self.cell(0, 5, texto, align="R")


def buscar_visitas(mes, ano):
    client = ColetumClient(ENDPOINT, TOKEN)
    resp = client.executar_query(QUERY_VISITAS)

    linhas = []
    for item in resp["data"]["answer"]:
        dados = item["answer"]["dadosDeExecucao800970"]
        data = dados.get("dataDaRealizacaoDaAtividade800974")
        tecnico = normalizar_nome(dados.get("nomeDoaTecnicoaResponsavel800972"))
        if data:
            linhas.append({"tecnico": tecnico, "data": data})

    df = pd.DataFrame(linhas)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df[(df["data"].dt.month == mes) & (df["data"].dt.year == ano)]
    return df


def buscar_coletivas(mes, ano):
    client = ColetumClient(ENDPOINT, TOKEN)
    resp = client.executar_query(QUERY_COLETIVAS)

    linhas = []
    for item in resp["data"]["answer"]:
        dados = item["answer"]["dadosDeExecucao484334"]
        atividade = normalizar_atividade(
            item["answer"]["atividadePre_fixada484342"]["atividades484343"]
        )

        data = dados.get("data484336")
        tecnico = normalizar_nome(dados.get("nomeDoaTecnicoa484337"))
        comunidade = dados.get("comunidade484341") or "NÃO PREENCHIDO"

        if data:
            linhas.append({
                "atividade": atividade,
                "tecnico": tecnico,
                "data": data,
                "comunidade": comunidade
            })

    df = pd.DataFrame(linhas)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df[(df["data"].dt.month == mes) & (df["data"].dt.year == ano)]
    return df.sort_values(["atividade", "data"])


def gerar_pdf(mes, ano):

    df_visitas = buscar_visitas(mes, ano)
    df_coletivas = buscar_coletivas(mes, ano)

    tecnicos = sorted(set(df_visitas["tecnico"].unique()).union(df_coletivas["tecnico"].unique()))

    pdf = PDFTabela(orientation="L")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"RELATÓRIO MENSAL - {mes}/{ano}", ln=True)

    largura_atividade = 70
    largura_tecnico = 30
    largura_soma = 25
    altura_linha = 10

    # Cabeçalho
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Helvetica", "B", 9)

    pdf.cell(largura_atividade, altura_linha, "Atividade", border=1, align="C", fill=True)
    for t in tecnicos:
        pdf.cell(largura_tecnico, altura_linha, t, border=1, align="C", fill=True)
    pdf.cell(largura_soma, altura_linha, "Somatório", border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)

    # Linha Visitas Técnicas
    visitas_count = df_visitas.groupby("tecnico").size()
    total_geral_visitas = visitas_count.sum()

    pdf.set_fill_color(210, 225, 245)
    pdf.cell(largura_atividade, altura_linha, "Visitas Técnicas", border=1, fill=True)

    for t in tecnicos:
        total = visitas_count.get(t, "")
        pdf.cell(largura_tecnico, altura_linha, str(total) if total != "" else "", border=1, align="C", fill=True)

    pdf.cell(largura_soma, altura_linha, str(total_geral_visitas), border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_fill_color(255, 255, 255)

    # Coletivas agrupadas
    for atividade, df_ativ in df_coletivas.groupby("atividade"):

        ocorrencias_por_tecnico = {}

        for t in tecnicos:
            df_t = df_ativ[df_ativ["tecnico"] == t].sort_values("data")
            ocorrencias_por_tecnico[t] = [
                f"{row['data'].day}-{row['comunidade']}"
                for _, row in df_t.iterrows()
            ]

        max_linhas = max((len(v) for v in ocorrencias_por_tecnico.values()), default=0)

        for i in range(max_linhas):

            pdf.cell(largura_atividade, altura_linha, atividade, border=1)

            total_linha = 0

            for t in tecnicos:
                lista = ocorrencias_por_tecnico[t]
                texto = lista[i] if i < len(lista) else ""
                if texto:
                    total_linha += 1
                pdf.cell(largura_tecnico, altura_linha, texto, border=1)

            pdf.cell(largura_soma, altura_linha, str(total_linha) if total_linha else "", border=1, align="C")
            pdf.ln()

    output = f"reports/relatorio_mensal_integrado_{mes}_{ano}.pdf"
    pdf.output(output)

    print("PDF gerado:", output)


if __name__ == "__main__":
    gerar_pdf(2, 2026)
