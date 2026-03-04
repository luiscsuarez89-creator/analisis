from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import pandas as pd


@dataclass
class DatosGovClient:
    """Cliente mínimo para consultar datasets de datos.gov.co vía endpoint query.json."""

    base_url: str = "https://www.datos.gov.co/api/v3/views/vhn3-kbc6/query.json"
    app_token: str | None = None

    def run_query(self, query: str) -> dict[str, Any]:
        params = urlencode({"query": query})
        url = f"{self.base_url}?{params}"
        headers = {"Accept": "application/json"}
        if self.app_token:
            headers["X-App-Token"] = self.app_token

        request = Request(url, headers=headers)
        with urlopen(request, timeout=60) as response:
            payload = json.loads(response.read().decode("utf-8"))
        return payload

    def fetch_dataframe(self, limit: int = 5000, offset: int = 0) -> pd.DataFrame:
        payload = self.run_query(f"SELECT * LIMIT {limit} OFFSET {offset}")
        return normalize_records(payload)


def normalize_records(payload: dict[str, Any]) -> pd.DataFrame:
    """Convierte distintas formas de respuesta JSON de Socrata a DataFrame."""

    rows = payload.get("results") or payload.get("data") or []
    if not rows:
        return pd.DataFrame()

    first = rows[0]
    if isinstance(first, dict):
        return pd.DataFrame(rows)

    if isinstance(first, list):
        columns = payload.get("columns")
        if isinstance(columns, list) and columns:
            names = [col.get("fieldName") or col.get("name") or f"col_{idx}" for idx, col in enumerate(columns)]
            return pd.DataFrame(rows, columns=names)

        meta_cols = payload.get("meta", {}).get("view", {}).get("columns", [])
        if meta_cols:
            names = [col.get("fieldName") or col.get("name") or f"col_{idx}" for idx, col in enumerate(meta_cols)]
            return pd.DataFrame(rows, columns=names)

        return pd.DataFrame(rows)

    return pd.DataFrame(rows)
