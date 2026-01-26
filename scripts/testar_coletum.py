from scripts.ingestao.coletum_client import ColetumClient
from scripts.ingestao.visitas_api import buscar_visitas

client = ColetumClient()

visitas = buscar_visitas(client)

print(f"Total de visitas: {len(visitas)}")
print(visitas[:1])
