import os
import calendar
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from dotenv import load_dotenv
from scripts.ingestao.coletum_client import ColetumClient

load_dotenv()

ENDPOINT = os.getenv("COLETUM_ENDPOINT")
TOKEN = os.getenv("COLETUM_TOKEN")


class RelatorioPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(
            0,
            10,
            f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Página {self.page_no()}",
            align="R"
        )


QUERY_VISITAS = """
{answer(formId:32933){
  answer{
    dadosDeExecucao800970{
      dataDaRealizacaoDaAtividade800974
    }
  }
  metaData{
    userName
  }
}}
"""


QUERY_COLETIVAS = """
{answer(formId:31179){
  answer{
    dadosDeExecucao484334{
      data484336
    }
    atividadePre_fixada484342{
      atividades484343
    }
  }
  metaData{
    userName
  }
}}
"""


def _extrair_visitas(resposta):
    lista = resposta["data"]["answer"]
    linhas = []

    for item in lista:
        data_atividade = item["answer"]["dadosDeExecucao800970"]["dataDaRealizacaoDaAtividade800974"]
        tecnico = item["metaData"]["userName"]

        linhas.append({
            "tecnico": tecnico,
            "data_atividade": data_atividade,
            "tipo": "visita",
            "atividade": ""
        })

    return pd.DataFrame(linhas)


def _extrair_coletivas(resposta):
    lista = resposta["data"]["answer"]
    linhas = []

    for item in lista:
        data_atividade = item["answer"]["dadosDeExecucao484334"]["data484336"]
        tecnico = item["metaData"]["userName"]

        atividades = item["answer"]["atividadePre_fixada484342"]["atividades484343"]

        linhas.append({
            "tecnico": tecnico,
            "data_atividade": data_atividade,
            "tipo": "coletiva",
            "atividade": atividades
        })

    return pd.DataFrame(linhas)


def buscar_visitas_api(mes: int, ano: int):
    """
    Retorna um DataFrame com visitas + coletivas do mês/ano.
    """
    client = ColetumClient(ENDPOINT, TOKEN)

    resp_visitas = client.executar_query(QUERY_VISITAS)
    df_visitas = _extrair_visitas(resp_visitas)

    resp_coletivas = client.executar_query(QUERY_COLETIVAS)
    df_coletivas = _extrair_coletivas(resp_coletivas)

    df = pd.concat([df_visitas, df_coletivas], ignore_index=True)

    df["data_atividade"] = pd.to_datetime(df["data_atividade"], errors="coerce")
    df = df[(df["data_atividade"].dt.month == mes) & (df["data_atividade"].dt.year == ano)]

    return df

def buscar_visitas_api_df(mes, ano):
    client = ColetumClient(ENDPOINT, TOKEN)

    resp_visitas = client.executar_query(QUERY_VISITAS)
    df_visitas = _extrair_visitas(resp_visitas)

    resp_coletivas = client.executar_query(QUERY_COLETIVAS)
    df_coletivas = _extrair_coletivas(resp_coletivas)

    df = pd.concat([df_visitas, df_coletivas], ignore_index=True)

    df["data_atividade"] = pd.to_datetime(df["data_atividade"], errors="coerce")
    df = df[(df["data_atividade"].dt.month == mes) & (df["data_atividade"].dt.year == ano)]

    return df


def gerar_relatorio_visitas(mes: int, ano: int, pdf_path: str = "reports/relatorio_visitas_api.pdf"):
    """
    Mantém compatibilidade com seu código antigo:
    gera o PDF diretamente (sem retornar DF).
    """
    df = buscar_visitas_api(mes, ano)

    if df.empty:
        print("❌ Nenhuma atividade encontrada na API.")
        return

    pdf = RelatorioPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    tecnicos = df["tecnico"].unique()

    for tecnico in tecnicos:
        df_tec = df[df["tecnico"] == tecnico]

        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório de Atividades", ln=True, align="C")
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Técnico: {tecnico}", ln=True, align="L")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Mês: {calendar.month_name[mes]} {ano}", ln=True, align="L")
        pdf.ln(10)

        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        page_width = pdf.w - 2 * pdf.l_margin
        cell_w = page_width / 7
        cell_h = 20

        pdf.set_font("Arial", "B", 10)
        for dia in dias_semana:
            pdf.cell(cell_w, 10, dia, border=1, align="C")
        pdf.ln()

        cal = calendar.monthcalendar(ano, mes)

        for semana in cal:
            for dia in semana:
                x = pdf.get_x()
                y = pdf.get_y()

                if dia == 0:
                    pdf.set_fill_color(230, 230, 230)
                    pdf.cell(cell_w, cell_h, "", border=1, fill=True)
                    continue

                data_atual = datetime(ano, mes, dia)
                v = df_tec[df_tec["data_atividade"].dt.date == data_atual.date()]

                visitas = v[v["tipo"] == "visita"].shape[0]
                coletivas = v[v["tipo"] == "coletiva"].shape[0]

                if visitas > 0 and coletivas > 0:
                    pdf.set_fill_color(255, 180, 180)
                elif visitas > 0:
                    pdf.set_fill_color(180, 255, 180)
                elif coletivas > 0:
                    pdf.set_fill_color(180, 200, 255)
                else:
                    pdf.set_fill_color(240, 240, 240)

                pdf.rect(x, y, cell_w, cell_h, style="F")
                pdf.rect(x, y, cell_w, cell_h)

                pdf.set_xy(x, y)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(cell_w, cell_h / 2, str(dia), align="C")

                texto = ""

                # VISITAS
                if visitas == 1:
                    texto += "1 visita"
                elif visitas > 1:
                    texto += f"{visitas} visitas"

                # COLETIVAS
                if coletivas > 0:
                    if texto != "":
                        texto += "\n"

                    atividades = v[v["tipo"] == "coletiva"]["atividade"].tolist()
                    atividades_texto = "\n".join([f"{a}" for a in atividades])

                    if coletivas == 1:
                        texto += f"1 {atividades_texto}"
                    else:
                        texto += f"{coletivas} coletivas\n{atividades_texto}"

                pdf.set_xy(x, y + 6)
                pdf.set_font("Arial", "", 8)
                pdf.multi_cell(cell_w, 4, texto, align="C")

                pdf.set_xy(x + cell_w, y)

            pdf.ln(cell_h)

    pdf.output(pdf_path)
    print(f"✅ PDF gerado: {pdf_path}")
    
def gerar_calendario_no_pdf(df_api, mes, ano, pdf: RelatorioPDF):
    """
    Desenha o calendário no PDF, usando o dataframe já filtrado.
    Não salva o PDF (isso é feito no script principal).
    """

    pdf.set_auto_page_break(auto=True, margin=15)

    tecnicos = df_api["tecnico"].unique()

    for tecnico in tecnicos:
        df_tec = df_api[df_api["tecnico"] == tecnico]

        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório de Atividades", ln=True, align="C")
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Técnico: {tecnico}", ln=True, align="L")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Mês: {calendar.month_name[mes]} {ano}", ln=True, align="L")
        pdf.ln(10)

        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        page_width = pdf.w - 2 * pdf.l_margin
        cell_w = page_width / 7
        cell_h = 20

        pdf.set_font("Arial", "B", 10)
        for dia in dias_semana:
            pdf.cell(cell_w, 10, dia, border=1, align="C")
        pdf.ln()

        cal = calendar.monthcalendar(ano, mes)

        for semana in cal:
            for dia in semana:
                x = pdf.get_x()
                y = pdf.get_y()

                if dia == 0:
                    pdf.set_fill_color(230, 230, 230)
                    pdf.cell(cell_w, cell_h, "", border=1, fill=True)
                    continue

                data_atual = datetime(ano, mes, dia)
                v = df_tec[df_tec["data_atividade"].dt.date == data_atual.date()]

                visitas = v[v["tipo"] == "visita"].shape[0]
                coletivas = v[v["tipo"] == "coletiva"].shape[0]

                if visitas > 0 and coletivas > 0:
                    pdf.set_fill_color(255, 180, 180)
                elif visitas > 0:
                    pdf.set_fill_color(180, 255, 180)
                elif coletivas > 0:
                    pdf.set_fill_color(180, 200, 255)
                else:
                    pdf.set_fill_color(240, 240, 240)

                pdf.rect(x, y, cell_w, cell_h, style="F")
                pdf.rect(x, y, cell_w, cell_h)

                pdf.set_xy(x, y)
                pdf.set_font("Arial", "B", 10)
                pdf.cell(cell_w, cell_h / 2, str(dia), align="C")

                texto = ""

                if visitas == 1:
                    texto += "1 visita"
                elif visitas > 1:
                    texto += f"{visitas} visitas"

                if coletivas > 0:
                    if texto != "":
                        texto += "\n"

                    atividades = v[v["tipo"] == "coletiva"]["atividade"].tolist()
                    atividades_texto = "\n".join([f"{a}" for a in atividades])

                    if coletivas == 1:
                        texto += f"1 {atividades_texto}"
                    else:
                        texto += f"{coletivas} coletivas\n{atividades_texto}"

                pdf.set_xy(x, y + 6)
                pdf.set_font("Arial", "", 8)
                pdf.multi_cell(cell_w, 4, texto, align="C")

                pdf.set_xy(x + cell_w, y)

            pdf.ln(cell_h)
