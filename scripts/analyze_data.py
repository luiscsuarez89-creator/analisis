#!/usr/bin/env python3
from __future__ import annotations

import argparse

import pandas as pd

from electrocampos_api.analysis import generate_charts


def main() -> None:
    parser = argparse.ArgumentParser(description="Genera análisis y gráficos del dataset")
    parser.add_argument("--input", default="data/mediciones.csv", help="CSV de entrada")
    parser.add_argument("--output-dir", default="outputs", help="Directorio para gráficos")
    args = parser.parse_args()

    df = pd.read_csv(args.input)
    charts = generate_charts(df, output_dir=args.output_dir)

    if charts:
        print("Gráficos generados:")
        for chart in charts:
            print(f" - {chart}")
    else:
        print("No fue posible generar gráficos; faltan columnas compatibles.")


if __name__ == "__main__":
    main()
