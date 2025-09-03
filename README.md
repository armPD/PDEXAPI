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
| `GET`  | `/clima_historico_nacional` | Histórico de clima agregado diario nacional | ✅ |
| `GET`  | `/clima_historico_estado_mes` | Histórico de clima mensual a nivel estado | ✅ |
| `GET`  | `/fc_clima_mes` | Pronóstico **mensual** ARIMA por ciudad | ✅ |
| `GET`  | `/fc_clima_mes_estado` | Pronóstico **mensual** ARIMA por estado | ✅ |
| `GET`  | `/fc_clima_diario` | Pronóstico **diario** ARIMA por ciudad | ✅ |
| `GET`  | `/turismo` | Dato de turismo mensual por estado | ✅ |
| `GET`  | `/dias_festivos` | Carta de días festivos nacionales | ✅ |


## Ejemplos de uso de la librería

A continuación se muestran ejemplos de cómo utilizar cada uno de los métodos disponibles en la clase `PDEXClient`, con sus parámetros y argumentos.

Copiar el código `PDExAPI_Client.py` al folder de la librería local. Poner usuario y contraseña.

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
tablas = cli.list_tables()
print(tablas)  # Ejemplo de salida: ['inflacion', 'fc_clima_mes', ...]
```

### inflacion
Obtiene la inflación diaria en un rango de fechas.

```python
infl = cli.inflacion(
    fecha_inicio="2025-01-01",
    fecha_fin="2025-01-31",
    fecha_proceso="2025-02-01",
    as_frame=True
)
print(infl.head())
```

### inflacion_prediccion
Predicción de inflación futura.

```python
pred = cli.inflacion_prediccion(
    fecha_inicio="2025-07-01",
    fecha_fin="2025-12-01",
    as_frame=True
)
print(pred)
```

### fc_clima_mes
Pronóstico mensual climático para una ciudad.

```python
fc_mes = cli.fc_clima_mes(
    estado="Jalisco",
    ciudad="Guadalajara",
    variable="avgtemp_c",
    fecha_inicio="2025-07-01",
    fecha_fin="2025-12-31",
    as_frame=True
)
print(fc_mes)
```

### fc_clima_mes_estado
Pronóstico mensual climático para un estado completo.

```python
fc_estado = cli.fc_clima_mes_estado(
    estado="Jalisco",
    variable="avgtemp_c",
    fecha_inicio="2025-07-01",
    fecha_fin="2025-12-31",
    as_frame=True
)
print(fc_estado)
```

### fc_clima_diario
Pronóstico diario climático para una ciudad.

```python
fc_diario = cli.fc_clima_diario(
    estado="Ciudad de México",
    ciudad="Coyoacán",
    variable="avghumidity",
    fecha_inicio="2025-07-15",
    fecha_fin="2025-07-22",
    as_frame=True
)
print(fc_diario.tail())
```

### clima_historico
Clima diario histórico entre dos fechas.

```python
clima_hist = cli.clima_historico(
    estado="Nuevo León",
    ciudad="Monterrey",
    fecha_inicio="2024-01-01",
    fecha_fin="2024-12-31",
    variable="totalprecip_mm",
    as_frame=True
)
print(clima_hist.head())
```

### clima_historico_nacional
Clima histórico agregado a nivel nacional (todas las ciudades).

```python
df_nacional = cli.clima_historico_nacional(
    fecha_inicio="2023-01-01",
    fecha_fin="2023-12-31",
    variable="avgtemp_c",
    mes=True,
    as_frame=True
)
print(df_nacional.head())
```

### clima_historico_estado_mes
Clima mensual histórico para un estado.

```python
df_estado = cli.clima_historico_estado_mes(
    estado="Puebla",
    fecha_inicio="2023-01-01",
    fecha_fin="2023-12-01",
    variable="avgtemp_c",
    as_frame=True
)
print(df_estado.head())
```

### poblacion
Consulta de población.

```python
# Población por estado
df = cli.poblacion(estado="Yucatán", as_frame=True)
print(df)

# Población por ciudad
df = cli.poblacion(estado="Yucatán", ciudad="Mérida", as_frame=True)
print(df)
```

### turismo
Consulta de turismo mensual por estado.

```python
df_turismo = cli.turismo(
    estado="Yucatán",
    fecha_inicio="2023-01-01",
    fecha_fin="2023-12-01",
    as_frame=True
)
print(df_turismo.head())
```

### dias_festivos
Carta nacional de días festivos.

```python
df_festivos = cli.dias_festivos(as_frame=True)
print(df_festivos.head())
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
