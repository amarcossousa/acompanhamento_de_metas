import requests

class ColetumClient:
    def __init__(self, endpoint: str, token: str):
        self.endpoint = endpoint
        self.token = token

    def executar_query(self, query: str):
        params = {
            "query": query,
            "token": self.token
        }

        response = requests.get(self.endpoint, params=params)
        response.raise_for_status()
        return response.json()
