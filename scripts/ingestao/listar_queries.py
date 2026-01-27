from scripts.ingestao.coletum_client import ColetumClient

QUERY_SCHEMA = """
{
  __schema {
    queryType {
      fields {
        name
      }
    }
  }
}
"""

client = ColetumClient()
resposta = client.executar_query(QUERY_SCHEMA)

print(resposta)
