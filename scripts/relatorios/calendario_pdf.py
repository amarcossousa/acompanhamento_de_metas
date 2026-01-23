import pandas as pd
import calendar
import os
from datetime import datetime
from fpdf import FPDF
from scripts.relatorios.coletivas import carregar_coletivas

class RelatorioPDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} - Página {self.page_no()}", align="R")

def gerar_relatorio_pdf(arquivo_csv_execucao: str, mes: int, ano: int, pdf: FPDF):
    df = pd.read_csv(arquivo_csv_execucao, sep=";", encoding="utf-8")
    df["DataExecucao"] = pd.to_datetime(
        df["DADOS DE EXECUÇÃO > Data da realização da atividade"],
        dayfirst=True,
        errors="coerce"
    )
    df = df[(df["DataExecucao"].dt.month == mes) & (df["DataExecucao"].dt.year == ano)]
    coletivas = carregar_coletivas("data/coletivas.csv", mes, ano)
    metas = pd.read_csv("data/metas.csv", sep=";", encoding="utf-8")

    visitas = (
        df.groupby(["Criado por", df["DataExecucao"].dt.day])
        .size()
        .reset_index(name="Visitas")
    )

    tecnicos = visitas["Criado por"].unique()

    for tecnico in tecnicos:
        visitas_tecnico = visitas[visitas["Criado por"] == tecnico]
        coletivas_tecnico = coletivas[coletivas["Criado por"] == tecnico]

        if visitas_tecnico.empty and coletivas_tecnico.empty:
            continue

        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório de Execução de Atividades", ln=True, align="C")
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Técnico: {tecnico}", ln=True, align="L")
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Mês: {calendar.month_name[mes]} {ano}", ln=True, align="L")
        pdf.ln(10)

        dias_semana = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
        page_width = pdf.w - 2*pdf.l_margin
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
                else:
                    v = visitas[(visitas["Criado por"] == tecnico) & (visitas["DataExecucao"] == dia)]
                    qtd_visitas = int(v["Visitas"].values[0]) if not v.empty else 0

                    c = coletivas[
                        (coletivas["Criado por"] == tecnico) &
                        (coletivas["DataColetiva"] == dia)
                    ]

                    if not c.empty:
                        textos_coletivas = [
                            f"{int(row['qtd'])} {row['ATIVIDADE PRÉ-FIXADA > ATIVIDADES']}"
                            for _, row in c.iterrows()
                        ]
                    else:
                        textos_coletivas = []

                    if qtd_visitas == 0 and not textos_coletivas:
                        pdf.set_fill_color(240, 240, 240)
                    elif qtd_visitas > 0 and not textos_coletivas:
                        pdf.set_fill_color(180, 255, 180)
                    else:
                        pdf.set_fill_color(255, 180, 180)

                    # DESENHA UMA ÚNICA VEZ
                    pdf.rect(x, y, cell_w, cell_h, style="F")
                    pdf.rect(x, y, cell_w, cell_h)

                    pdf.set_xy(x, y)
                    pdf.set_font("Arial", "B", 10)
                    pdf.cell(cell_w, cell_h/2, str(dia), align="C")

                    texto = ""
                    if qtd_visitas > 0:
                        texto += f"{qtd_visitas} visitas"
                    if textos_coletivas:
                        if texto != "":
                            texto += "\n"
                        texto += "\n".join(textos_coletivas)

                    pdf.set_xy(x, y + 6)
                    pdf.set_font("Arial", "", 8)
                    pdf.multi_cell(cell_w, 4, texto, align="C")

                    pdf.set_xy(x + cell_w, y)

            pdf.ln(cell_h)

        total = visitas[visitas["Criado por"] == tecnico]["Visitas"].sum()
        meta_tecnico = metas.loc[metas["Tecnico"] == tecnico, "Meta"].values
        meta_mensal = int(meta_tecnico[0]) if len(meta_tecnico) > 0 else 0
        percentual = (total / meta_mensal) * 100 if meta_mensal > 0 else 0

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, f"Meta do mês: {meta_mensal} visitas", ln=True, align="L")
        pdf.cell(0, 10, f"Executado: {total} visitas", ln=True, align="L")
        pdf.cell(0, 10, f"Cumprimento: {percentual:.1f}%", ln=True, align="L")

        # -------- GRÁFICO (COMENTADO) ----------
        # dados_tecnico = visitas[visitas["Criado por"] == tecnico].set_index("DataExecucao")["Visitas"]
        # plt.figure(figsize=(6,3))
        # dados_tecnico.plot(kind="bar", color="skyblue")
        # if meta_mensal > 0:
        #     plt.axhline(y=meta_mensal/len(cal), color="red", linestyle="--", label="Meta diária média")
        # plt.title(f"Visitas por dia - {tecnico}")
        # plt.xlabel("Dia")
        # plt.ylabel("Visitas")
        # plt.legend()
        #
        # grafico_path = f"reports/temp_{tecnico}.png"
        # plt.savefig(grafico_path, bbox_inches="tight")
        # plt.close()
        #
        # pdf.image(grafico_path, x=10, y=None, w=180)
        # ---------------------------------------

    # NÃO CHAME pdf.output() AQUI
    return
