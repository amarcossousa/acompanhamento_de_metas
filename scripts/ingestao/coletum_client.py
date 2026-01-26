import os
import requests
from dotenv import load_dotenv
from pathlib import Path


# Garante que o .env da raiz do projeto seja carregado
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")


class ColetumClient:
    def __init__(
        self,
        endpoint: str | None = None,
        token: str | None = None,
        timeout: int = 30
    ):
        self.endpoint = endpoint or os.getenv("COLETUM_ENDPOINT")
        self.token = token or os.getenv("COLETUM_TOKEN")
        self.timeout = timeout

        if not self.endpoint:
            raise ValueError("COLETUM_ENDPOINT não configurado")

        if not self.token:
            raise ValueError("COLETUM_TOKEN não configurado")

    def executar_query(self, query: str, variables: dict | None = None) -> dict:
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        payload = {
            "query": query,
            "variables": variables or {},
        }

        response = requests.post(
            self.endpoint,
            json=payload,
            headers=headers,
            timeout=self.timeout,
        )

        response.raise_for_status()

        data = response.json()

        if "errors" in data:
            raise RuntimeError(f"Erro GraphQL: {data['errors']}")

        return data
