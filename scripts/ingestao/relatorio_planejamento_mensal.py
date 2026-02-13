import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from scripts.ingestao.coletum_client import ColetumClient
from scripts.core.query_loader import carregar_query

# >>> IMPORTA O RESOLVEDOR DE VALORES (o mesmo que você já testou)
from scripts.core.financeiro import obter_valor_atividade

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

    def linha_quebra(pdf, altura_base, larguras, textos):
        x_inicio = pdf.get_x()
        y_inicio = pdf.get_y()

        alturas = []

        for largura, texto in zip(larguras, textos):
            linhas = pdf.multi_cell(
                largura,
                altura_base,
                texto,
                dry_run=True,
                output="LINES"
            )
            alturas.append(len(linhas) * altura_base)

        altura_max = max(alturas)
        x_atual = x_inicio

        for largura, texto in zip(larguras, textos):
            pdf.set_xy(x_atual, y_inicio)
            pdf.multi_cell(largura, altura_base, texto, border=0)
            pdf.rect(x_atual, y_inicio, largura, altura_max)
            x_atual += largura

        pdf.set_xy(x_inicio, y_inicio + altura_max)



    df_visitas = buscar_visitas(mes, ano)
    df_coletivas = buscar_coletivas(mes, ano)

    tecnicos = sorted(set(df_visitas["tecnico"].unique()).union(df_coletivas["tecnico"].unique()))

    pdf = PDFTabela(orientation="L")
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"RELATÓRIO MENSAL - {mes}/{ano}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    largura_atividade = 60
    largura_tecnico = 25
    largura_soma = 25
    largura_valor = 30
    altura_linha = 4  # reduzimos para permitir quebra

    # Cabeçalho
    pdf.set_fill_color(220, 220, 220)
    pdf.set_font("Helvetica", "B", 9)

    pdf.cell(largura_atividade, 10, "Atividade", border=1, align="C", fill=True)
    for t in tecnicos:
        pdf.cell(largura_tecnico, 10, t, border=1, align="C", fill=True)
    pdf.cell(largura_soma, 10, "Qtd.", border=1, align="C", fill=True)
    pdf.cell(largura_valor, 10, "R$", border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 8)

    total_financeiro = 0

    # ===== VISITAS =====
    visitas_count = df_visitas.groupby("tecnico").size()
    total_geral_visitas = visitas_count.sum()

    valor_visita_unit = obter_valor_atividade("Visita Técnica")
    valor_total_visitas = total_geral_visitas * valor_visita_unit
    total_financeiro += valor_total_visitas

    pdf.set_fill_color(210, 225, 245)
    pdf.cell(largura_atividade, 10, "Visitas Técnicas", border=1, fill=True)

    for t in tecnicos:
        total = visitas_count.get(t, "")
        pdf.cell(largura_tecnico, 10, str(total) if total != "" else "", border=1, align="C", fill=True)

    pdf.cell(largura_soma, 10, str(total_geral_visitas), border=1, align="C", fill=True)
    pdf.cell(largura_valor, 10, f"R$ {valor_total_visitas:,.2f}", border=1, align="R", fill=True)
    pdf.ln()

    pdf.set_fill_color(255, 255, 255)

    # ===== COLETIVAS (AGORA COM QUEBRA AUTOMÁTICA) =====
    for atividade, df_ativ in df_coletivas.groupby("atividade"):

        valor_unitario = obter_valor_atividade(atividade)

        ocorrencias_por_tecnico = {}

        for t in tecnicos:
            df_t = df_ativ[df_ativ["tecnico"] == t].sort_values("data")
            ocorrencias_por_tecnico[t] = [
                f"{row['data'].day}-{row['comunidade']}"
                for _, row in df_t.iterrows()
            ]

        max_linhas = max((len(v) for v in ocorrencias_por_tecnico.values()), default=0)

        for i in range(max_linhas):

            textos_linha = [atividade]

            total_linha = 0

            for t in tecnicos:
                lista = ocorrencias_por_tecnico[t]
                texto = lista[i] if i < len(lista) else ""
                if texto:
                    total_linha += 1
                textos_linha.append(texto)

            valor_linha = total_linha * valor_unitario
            total_financeiro += valor_linha

            textos_linha.append(str(total_linha) if total_linha else "")
            textos_linha.append(f"R$ {valor_linha:,.2f}" if total_linha else "")

            larguras = [largura_atividade] + [largura_tecnico]*len(tecnicos) + [largura_soma, largura_valor]

            linha_quebra(pdf, altura_linha, larguras, textos_linha)

    # ===== TOTAL FINAL =====
    pdf.set_font("Helvetica", "B", 10)

    pdf.cell(largura_atividade + len(tecnicos)*largura_tecnico, 10, "TOTAL FINANCEIRO", border=1)
    pdf.cell(largura_soma, 10, "", border=1)
    pdf.cell(largura_valor, 10, f"R$ {total_financeiro:,.2f}", border=1, align="R")

    pdf.ln(10)

    pdf.set_font("Helvetica", "I", 6)

    atividades_realizadas = set(df_coletivas["atividade"].unique())

    if total_geral_visitas > 0:
        atividades_realizadas.add("Visita Técnica")

    itens = []
    for atividade in sorted(atividades_realizadas):
        valor = obter_valor_atividade(atividade)
        itens.append(f"{atividade}: R$ {valor:,.2f}")

    linha_referencia = "Valores unitários de referência: " + "; ".join(itens)

    pdf.cell(0, 4, linha_referencia)

    os.makedirs("reports", exist_ok=True)
    output = f"reports/relatorio_mensal_integrado_{mes}_{ano}.pdf"
    pdf.output(output)

    print("PDF gerado:", output)



if __name__ == "__main__":
    gerar_pdf(11, 2025)
