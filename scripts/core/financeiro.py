import os
import json
import re
import unicodedata
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from difflib import get_close_matches

from scripts.ingestao.coletum_client import ColetumClient
from scripts.core.query_loader import carregar_query

QUERY_VISITAS = carregar_query("answer_form_32933.graphql")
QUERY_COLETIVAS = carregar_query("answer_form_31179.graphql")

load_dotenv()

ENDPOINT = os.getenv("COLETUM_ENDPOINT")
TOKEN = os.getenv("COLETUM_TOKEN")

# ================= NORMALIZAÇÃO =================

def normalizar_nome(nome):
    if not nome:
        return ""
    return str(nome).strip().split()[0].title()

def normalizar_chave(texto):

    if not texto:
        return ""

    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ascii', 'ignore').decode('ascii')

    texto = re.sub(r'\(.*?\)', '', texto)
    texto = re.sub(r'[^a-z0-9 ]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

# ================= CARREGAR VALORES =================

def carregar_valores():

    with open("config/valores_atividades.json", encoding="utf-8") as f:
        return json.load(f)

VALORES_ATIVIDADES = carregar_valores()

def obter_valor_atividade(nome_api):

    chave = normalizar_chave(nome_api)

    if chave in VALORES_ATIVIDADES:
        return VALORES_ATIVIDADES[chave]

    candidatos = get_close_matches(chave, VALORES_ATIVIDADES.keys(), n=1, cutoff=0.75)

    if candidatos:
        return VALORES_ATIVIDADES[candidatos[0]]

    print("ATIVIDADE SEM VALOR CADASTRADO:", nome_api)
    return 0

# ================= PDF =================

class PDFTabela(FPDF):

    def footer(self):
        self.set_y(-10)
        self.set_font("Helvetica", "", 8)
        texto = f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}"
        self.cell(0, 5, texto, align="R")

# ================= BUSCA DADOS =================

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

        # PRINT ESTRATÉGICO PRA DESCOBRIR ID INTERNO
        print(item["answer"]["atividadePre_fixada484342"])

        dados = item["answer"]["dadosDeExecucao484334"]

        atividade = item["answer"]["atividadePre_fixada484342"]["atividades484343"]
        data = dados.get("data484336")
        tecnico = normalizar_nome(dados.get("nomeDoaTecnicoa484337"))

        if data:
            linhas.append({
                "atividade": atividade,
                "tecnico": tecnico,
                "data": data
            })

    df = pd.DataFrame(linhas)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df[(df["data"].dt.month == mes) & (df["data"].dt.year == ano)]

    return df

# ================= FINANCEIRO =================

def calcular_financeiro(df_coletivas, df_visitas):

    # Coletivas
    resumo_coletivas = (
        df_coletivas.groupby("atividade")
        .size()
        .reset_index(name="quantidade")
    )

    # Visitas viram uma atividade também
    qtd_visitas = len(df_visitas)

    if qtd_visitas > 0:
        resumo_visitas = pd.DataFrame([{
            "atividade": "Visita Técnica",
            "quantidade": qtd_visitas
        }])

        resumo = pd.concat([resumo_coletivas, resumo_visitas], ignore_index=True)
    else:
        resumo = resumo_coletivas

    resumo["valor_unitario"] = resumo["atividade"].apply(obter_valor_atividade)
    resumo["total"] = resumo["quantidade"] * resumo["valor_unitario"]

    total_geral = resumo["total"].sum()

    return resumo.sort_values("atividade"), total_geral


# ================= GERA PDF =================

def gerar_pdf(mes, ano):

    df_visitas = buscar_visitas(mes, ano)
    df_coletivas = buscar_coletivas(mes, ano)

    resumo_financeiro, total_geral = calcular_financeiro(df_coletivas, df_visitas)


    pdf = PDFTabela(orientation="L")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"RESUMO FINANCEIRO {mes}/{ano}", ln=True)

    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(120, 8, "Atividade", border=1)
    pdf.cell(30, 8, "Qtd", border=1)
    pdf.cell(40, 8, "Valor", border=1)
    pdf.cell(40, 8, "Total", border=1)
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)

    for _, row in resumo_financeiro.iterrows():
        pdf.cell(120, 8, row["atividade"], border=1)
        pdf.cell(30, 8, str(row["quantidade"]), border=1)
        pdf.cell(40, 8, f"R$ {row['valor_unitario']:,.2f}", border=1)
        pdf.cell(40, 8, f"R$ {row['total']:,.2f}", border=1)
        pdf.ln()

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(190, 10, "TOTAL GERAL", border=1)
    pdf.cell(40, 10, f"R$ {total_geral:,.2f}", border=1)

    os.makedirs("reports", exist_ok=True)
    output = f"reports/financeiro_{mes}_{ano}.pdf"
    pdf.output(output)

    print("PDF gerado:", output)

# ================= MAIN =================

if __name__ == "__main__":
    gerar_pdf(1, 2026)
