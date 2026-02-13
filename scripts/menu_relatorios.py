import subprocess
import sys

def pedir_int(msg, padrao=None):
    valor = input(msg).strip()
    if not valor and padrao is not None:
        return padrao
    try:
        return int(valor)
    except ValueError:
        print("Valor inválido.")
        return pedir_int(msg, padrao)

def rodar(modulo, *args):
    cmd = [sys.executable, "-m", modulo, *map(str, args)]
    subprocess.run(cmd, check=False)

while True:
    print("\n=== GERADOR DE RELATÓRIOS ===")
    print("1 - Relatório Mensal Integrado")
    print("2 - Relatório por Período (Consolidado)")
    print("3 - Relatório Somente Visitas")
    print("0 - Sair")

    op = input("Escolha uma opção: ").strip()

    if op == "1":
        mes = pedir_int("Mês (1-12): ")
        ano = pedir_int("Ano: ")
        rodar("scripts.ingestao.relatorio_planejamento_mensal", mes, ano)

    elif op == "2":
        mi = pedir_int("Mês inicial: ")
        mf = pedir_int("Mês final: ")
        ano = pedir_int("Ano: ")
        rodar("scripts.ingestao.relatorio_periodo", mi, mf, ano)

    elif op == "3":
        mes = pedir_int("Mês (1-12): ")
        ano = pedir_int("Ano: ")
        rodar("scripts.run_relatorio_visitas_api", mes, ano)

    elif op == "0":
        break
    else:
        print("Opção inválida.")
