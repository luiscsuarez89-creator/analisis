# Proyecto de análisis: mediciones de exposición a campos electromagnéticos (datos.gov.co)

Este repositorio crea un flujo completo para:

1. **Consultar datos vía API** del dataset `vhn3-kbc6` usando `query.json`.
2. **Guardar datos en CSV** para análisis reproducible.
3. **Generar visualizaciones** (barras, pie, caja y bigotes) en archivos PNG.

Fuente de datos oficial:
- Página del dataset: https://www.datos.gov.co/Ciencia-Tecnolog-a-e-Innovaci-n/Mediciones-de-exposici-n-a-campos-electromagn-tico/vhn3-kbc6/about_data
- Endpoint de consulta: `https://www.datos.gov.co/api/v3/views/vhn3-kbc6/query.json`

## Estructura

- `src/electrocampos_api/client.py`: cliente API + normalización de respuesta JSON a DataFrame.
- `src/electrocampos_api/analysis.py`: selección de columnas y generación de gráficos.
- `scripts/download_data.py`: descarga datos desde API a CSV.
- `scripts/analyze_data.py`: lee CSV y exporta gráficos.
- `tests/test_client.py`: pruebas unitarias de normalización.

## Requisitos

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Uso rápido

### 1) Descargar datos desde API

```bash
PYTHONPATH=src python scripts/download_data.py \
  --token 'F5X1iif1iZrvHH3CvjP5Box2a' \
  --limit 5000 \
  --output data/mediciones.csv
```

### 2) Generar gráficos

```bash
PYTHONPATH=src python scripts/analyze_data.py \
  --input data/mediciones.csv \
  --output-dir outputs
```

Archivos esperados:
- `outputs/grafico_barras.png`
- `outputs/grafico_pie.png`
- `outputs/grafico_boxplot.png`

## Nota sobre conectividad

Si tu entorno bloquea la salida a `datos.gov.co`, ejecuta los scripts en una red con acceso externo o en tu máquina local.
