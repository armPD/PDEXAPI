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
    base_url="https://api.pdexapi.com",
    username="tu_usuario",
    password="tu_password",
)

```

## Métodos disponibles

Variables históricas de clima:
```python
[
    "maxtemp_c", 
    "mintemp_c", 
    "avgtemp_c", 
    "maxwind_kph", 
    "totalprecip_mm",
    "daily_chance_of_rain",
    "chance_of_rain",
    "avghumidity", 
    "heatindex_c", 
    "feelslike_c",
    "uv",
]
```


Variables predictivas de clima:
```python
[
    "maxtemp_c", 
    "mintemp_c", 
    "avgtemp_c", 
    "maxwind_kph", 
    "avghumidity", 
    "heatindex_c", 
    "feelslike_c"
]
```


| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| `POST` | `/token` | Genera token JWT (OAuth2 Password Flow) | ❌ |
| `GET`  | `/tables` | Listado de tablas disponibles en DB | ✅ |
| `GET`  | `/inflacion` | Histórico de inflación | ✅ |
| `GET`  | `/inflacion_prediccion` | Predicción de inflación | ✅ |
| `GET`  | `/poblacion` | Dato de población por ciudad estado | ✅ |
| `GET`  | `/clima_historico` | Histórico de variables de clima | ✅ |
| `GET`  | `/clima_historico_nacional` | Histórico de variables de clima agregado diario nacional | ✅ |
| `GET`  | `/fc_clima_mes` | Pronóstico **mensual** ARIMA | ✅ |
| `GET`  | `/fc_clima_diario` | Pronóstico **diario** ARIMA | ✅ |


## Ejemplos de uso de la librería

A continuación se muestran ejemplos de cómo utilizar cada uno de los métodos disponibles en la clase `PDEXClient`, con sus parámetros y argumentos.

Copiar el codigo PDExAPI_Client.py al folder de la libreria local. Poner usuario y contraseña.

```python
from lib_local.PDExAPI_Client import PDEXClient

cli = PDEXClient(
    base_url="https://api.pdexapi.com",
    username="tu_usuario",
    password="tu_password",
)

```

### list_tables
Lista las tablas reflejadas en la base de datos.

```python
# Obtiene la lista de tablas
tablas = client.list_tables()
print(tablas)  # Ejemplo de salida: ['inflacion', 'fc_clima_mes', ...]
```

### inflacion
Obtiene la inflación diaria en un rango de fechas.

```python
infl = client.inflacion(
    fecha_inicio="2025-01-01",  # Fecha de inicio (YYYY-MM-DD)
    fecha_fin="2025-01-31",     # Fecha de fin (YYYY-MM-DD)
    fecha_proceso="2025-02-01", # (Opcional) Fecha de proceso
    limit=50,                   # (Opcional) Límite de registros a retornar
    as_frame=True               # Devuelve un pandas.DataFrame en lugar de lista de dicts
)
print(infl.head())
```

### fc_clima_mes
Pronóstico mensual climático para una variable específica.

```python
fc_mes = client.fc_clima_mes(
    estado="Jalisco",           # Nombre del estado
    ciudad="Guadalajara",       # Nombre de la ciudad
    variable="temperature",     # Variable a consultar (e.g. 'temperature', 'precipitation')
    fecha_inicio="2025-07-01",  # Fecha de inicio (YYYY-MM-DD)
    fecha_fin="2025-12-31",     # Fecha de fin (YYYY-MM-DD)
    as_frame=False              # Retorna lista de dicts
)
print(fc_mes)
```

### fc_clima_diario
Pronóstico diario climático para una variable específica.

```python
fc_diario = client.fc_clima_diario(
    estado="Ciudad de México",  # Nombre del estado
    ciudad="Coyoacán",          # Nombre de la ciudad
    variable="humidity",        # Variable a consultar (e.g. 'humidity', 'wind_speed')
    fecha_inicio="2025-07-15",  # Fecha de inicio (YYYY-MM-DD)
    fecha_fin="2025-07-22",     # Fecha de fin (YYYY-MM-DD)
    as_frame=True               # Devuelve un DataFrame
)
print(fc_diario.tail())
```

### clima_historico
Recupera clima observado diario histórico entre dos fechas.

```python
clima_hist = client.clima_historico(
    estado="Nuevo León",             # Nombre del estado
    ciudad="Monterrey",              # Nombre de la ciudad
    fecha_inicio="2024-01-01",       # Fecha de inicio (YYYY-MM-DD)
    fecha_fin="2024-12-31",          # Fecha de fin (YYYY-MM-DD)
    variable="totalprecip_mm",       # (Opcional) Nombre de la variable (e.g. 'maxtemp_c', 'totalprecip_mm')
    as_frame=False                   # Devuelve lista de dicts
)
print(clima_hist[:3])
```

### poblacion
Obtiene la población de una ciudad o estado en una fecha de proceso.

```python
# Población por estado (suma ciudades)
pob_estado = client.poblacion(
    estado="Puebla",                  # Nombre del estado
    ciudad=None,                      # None agrupa por todo el estado
    fecha_proceso="2025-01-01",       # (Opcional) Fecha de proceso
    as_frame=True                     # Devuelve DataFrame
)
print(pob_estado)

# Población por ciudad
pob_ciudad = client.poblacion(
    estado="Puebla",
    ciudad="Puebla de Zaragoza",      # Nombre de la ciudad
    as_frame=False                    # Lista de dicts con la fecha más reciente
)
print(pob_ciudad)
```

### Turismo
Obtiene la población turística de un estado en el periodo dado

```python

df_turismo = cli.turismo(
    estado="Yucatán",
    fecha_inicio="2023-01-01",
    fecha_fin="2023-12-01",
    as_frame=True
)
print(df_turismo.head())

```

### Días festivos
Obtiene los días festivos previstos

```python

df = cli.dias_festivos(
    as_frame=True
)
print(df_turismo.head())

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

* Python ≥3.11
* `requests`
* `pandas`

© 2025 Equipo Polydata — Uso interno.
