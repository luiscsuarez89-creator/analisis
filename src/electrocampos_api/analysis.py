from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")


def coerce_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        out[col] = pd.to_numeric(out[col], errors="ignore")
    return out


def choose_columns(df: pd.DataFrame) -> tuple[str | None, str | None]:
    categorical_candidates = [
        c
        for c in df.columns
        if not pd.api.types.is_numeric_dtype(df[c]) and 1 < df[c].nunique(dropna=True) <= 12
    ]
    numeric_candidates = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]

    cat_col = categorical_candidates[0] if categorical_candidates else None
    num_col = numeric_candidates[0] if numeric_candidates else None
    return cat_col, num_col


def generate_charts(df: pd.DataFrame, output_dir: str = "outputs") -> list[Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    df = coerce_numeric_columns(df)
    cat_col, num_col = choose_columns(df)
    generated: list[Path] = []

    if cat_col:
        counts = df[cat_col].fillna("Sin dato").value_counts().head(10)

        fig, ax = plt.subplots(figsize=(10, 6))
        counts.plot(kind="bar", ax=ax, color="#1f77b4")
        ax.set_title(f"Top categorías en {cat_col}")
        ax.set_xlabel(cat_col)
        ax.set_ylabel("Frecuencia")
        plt.xticks(rotation=45, ha="right")
        bar_path = output / "grafico_barras.png"
        fig.tight_layout()
        fig.savefig(bar_path, dpi=150)
        plt.close(fig)
        generated.append(bar_path)

        fig, ax = plt.subplots(figsize=(8, 8))
        counts.plot(kind="pie", ax=ax, autopct="%1.1f%%", startangle=120)
        ax.set_ylabel("")
        ax.set_title(f"Distribución porcentual de {cat_col}")
        pie_path = output / "grafico_pie.png"
        fig.tight_layout()
        fig.savefig(pie_path, dpi=150)
        plt.close(fig)
        generated.append(pie_path)

    if num_col:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x=df[num_col].dropna(), ax=ax, color="#ff7f0e")
        ax.set_title(f"Caja y bigotes de {num_col}")
        box_path = output / "grafico_boxplot.png"
        fig.tight_layout()
        fig.savefig(box_path, dpi=150)
        plt.close(fig)
        generated.append(box_path)

    return generated
