#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from electrocampos_api import DatosGovClient


def main() -> None:
    parser = argparse.ArgumentParser(description="Descarga mediciones desde datos.gov.co")
    parser.add_argument("--token", required=True, help="Valor para header X-App-Token")
    parser.add_argument("--limit", type=int, default=5000, help="Cantidad de registros")
    parser.add_argument("--offset", type=int, default=0, help="Desplazamiento")
    parser.add_argument("--output", default="data/mediciones.csv", help="Ruta de salida CSV")
    args = parser.parse_args()

    client = DatosGovClient(app_token=args.token)
    df = client.fetch_dataframe(limit=args.limit, offset=args.offset)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    print(f"Se guardaron {len(df)} registros en {output}")


if __name__ == "__main__":
    main()
