from scripts.ingestao.coletum_client import ColetumClient
from scripts.servicos.visitas_service import carregar_visitas_normalizadas


def main():
    print("🚀 Testando carregamento de visitas via API")

    client = ColetumClient()

    df = carregar_visitas_normalizadas(client)

    print("Total de registros:", len(df))
    print(df.head())
    print(df.dtypes)


if __name__ == "__main__":
    main()
