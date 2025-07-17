# PDEX API Python Client

Ligera envoltura (*wrapper*) para interactuar con la **API Polydata Exógenos** (PDExAPI).

## Instalación

```bash
pip install pandas requests
# copia `pdexapi_client.py` a tu proyecto
```

## Uso rápido

```python
from pdexapi_client import PDEXClient

cli = PDEXClient(
    base_url="https://api.polydata.mx",
    username="tu_usuario",
    password="tu_password",
)

print(cli.list_tables())
```

## Métodos disponibles

| Método | Descripción |
|--------|-------------|
| `list_tables()` | Lista las tablas reflejadas en la BD |
| `inflacion()` | Inflación diaria |
| `fc_clima_mes()` | Pronóstico mensual climático |
| `fc_clima_diario()` | Pronóstico diario |
| `clima_historico()` | Clima observado diario |
| `poblacion()` | Población por ciudad/estado |

Todos aceptan `as_frame=True` para `pandas.DataFrame`.

## Ejemplos

```python
df_infl = cli.inflacion("2025-01-01", "2025-03-31", as_frame=True)
df_fc   = cli.fc_clima_mes(estado="NL", ciudad="Monterrey",
                           variable="maxtemp_c",
                           fecha_inicio="2025-08-01",
                           fecha_fin="2025-12-01",
                           as_frame=True)
```

## Manejo de errores

Se propagan como `requests.HTTPError`.  
```python
try:
    cli.inflacion("2020-01-01", "2020-01-05")
except requests.HTTPError as e:
    print(e.response.text)
```

## Requisitos

* Python ≥3.8
* `requests`
* `pandas`

© 2025 Equipo Polydata — Uso interno.
