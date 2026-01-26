# scripts/testar_ping.py
from scripts.ingestao.coletum_client import ColetumClient

client = ColetumClient()

query = """
query {
  __typename
}
"""

print(client.executar_query(query))
