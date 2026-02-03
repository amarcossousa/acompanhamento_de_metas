from scripts.relatorios.consolidado_visitas import gerar_consolidados_visitas
import pandas as pd


# ===============================
# DADOS FAKES (SIMULANDO A API)
# ===============================

respostas_api_mock = [
    {
        "metaData": {
            "userName": "Tecnico A"
        },
        "answer": {
            "dadosDeExecucao800970": {
                "dataDaRealizacaoDaAtividade800974": "2024-01-15"
            }
        }
    },
    {
        "metaData": {
            "userName": "Tecnico A"
        },
        "answer": {
            "dadosDeExecucao800970": {
                "dataDaRealizacaoDaAtividade800974": "2024-01-20"
            }
        }
    },
    {
        "metaData": {
            "userName": "Tecnico B"
        },
        "answer": {
            "dadosDeExecucao800970": {
                "dataDaRealizacaoDaAtividade800974": "2024-02-10"
            }
        }
    },
    {
        "metaData": {
            "userName": "Tecnico B"
        },
        "answer": {
            "dadosDeExecucao800970": {
                "dataDaRealizacaoDaAtividade800974": "2023-12-05"
            }
        }
    },
]


# ===============================
# EXECUÇÃO DO TESTE
# ===============================

def main():
    print("🚀 Iniciando teste do consolidado de visitas...\n")

    paths = gerar_consolidados_visitas(respostas_api_mock)

    print("✅ Arquivos gerados com sucesso:\n")
    for nome, path in paths.items():
        print(f"- {nome}: {path}")

    print("\n📊 Preview dos consolidados:\n")

    print("🔹 Consolidado Geral")
    print(pd.read_parquet(paths["geral"]))
    print()

    print("🔹 Por Técnico (Anual)")
    print(pd.read_parquet(paths["por_tecnico"]))
    print()

    print("🔹 Por Técnico (Mensal)")
    print(pd.read_parquet(paths["por_tecnico_mes"]))
    print()


if __name__ == "__main__":
    main()
