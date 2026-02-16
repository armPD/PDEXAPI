# PDEXAPI Client lib

Libreria para interactuar con la API de datos exógenos nativa de Polydata (PDEXAPI). Esta libreria es la envoltura del lado del **Cliente**. Provee acceso mediante autenticación a variables de clima históricas, predicciones, inflación, población y más.

## Adopción

### Instalación con solo pip

```bash
pip install git+https://github.com/armPD/PDEXAPI.git
```
> Opcional instalar una versión específica (recomendado para producción):

```bash
pip install git+https://github.com/armPD/PDEXAPI.git@v0.1.0
```

### Instalación con uv

Dado los estándares de manejo de paqueterias, es recomendable hacer la instalación utilizando **uv**. Es necesario crear ambiente virtual antes de ejecutar el comando.

```bash
uv pip install git+https://github.com/armPD/PDEXAPI.git
```

### Uso rápido

```python
from pdexapi  import PDEXClient

cli = PDEXClient(
    base_url="http://api.pdexapi.com", # Nota: sin la s en http
    username="tu_usuario",
    password="tu_password",
)
```
La autenticación es manejada automáticamente cuando el cliente es creado y validado con las credenciales.

## Contextualización del clima

Actualmente se manejan dos servicios de proveedor de datos climatológicos: **WeatherAPI** y **Copernicus**. 
- El primero es una API de suscripción completamente optimizada para el usuario final, con ella se hace una actualización diaria para la geografía de interés. Es una caja negra y no se sabe certeramente como funciona.
- El segundo es un servicio mucho más técnico y científico, con el cual se tienen que hacer diversos preprocesamientos para llegar a un esquema similar de manejo de datos. 

Variables históricas de clima:

```python
WeatherAPI = 
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

Copernicus =
[
    "maxtemp_c",
    "mintemp_c",
    "avgtemp_c",
    "totalprecip_mm",
]
```

Variables predictivas de clima:

```python
WeatherAPI = 
[
    "maxtemp_c",
    "mintemp_c",
    "avgtemp_c",
    "maxwind_kph",
    "avghumidity",
    "heatindex_c",
    "feelslike_c"
]

Copernicus =
[
    "maxtemp_c",
    "mintemp_c",
    "avgtemp_c",
    "totalprecip_mm",
]
```

Variables nativas de Copernicus y su análogo:

```python
{
    "mx2t": "maxtemp_c",
    "mn2t": "mintemp_c",
    "2t": "avgtemp_c",
    "tp": "totalprecip_mm",
}
```

## Métodos disponibles

| Método | Ruta                          | Descripción                                                                                                                                               | Referencia |
| ------ | ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ---- |
| `POST` | `/token`                      | Genera token JWT (OAuth2 Password Flow)                                                                                                                   | ⚠️   |
| `GET`  | `/tables`                     | Listado de tablas disponibles en DB                                                                                                                       | ✅   |
| `GET`  | `/inflacion`                  | Histórico de inflación                                                                                                                                    | ✅   |
| `GET`  | `/inflacion_prediccion`       | Predicción de inflación                                                                                                                                   | ✅   |
| `GET`  | `/poblacion`                  | Dato de población por ciudad estado                                                                                                                       |  ✅  |
| `GET`  | `/clima_historico`            | (WeatherAPI) Histórico de variables de clima                                                                                                                           |  ✅  |
| `GET`  | `/clima_historico_nacional`   | (WeatherAPI) Histórico de clima agregado diario nacional                                                                                                               |  ✅  |
| `GET`  | `/clima_historico_estado_mes` | (WeatherAPI) Histórico de clima mensual a nivel estado                                                                                                                 |  ✅  |
| `GET`  | `/fc_clima_mes`               | (WeatherAPI) Pronóstico **mensual** ARIMA por ciudad                                                                                                                   |  ✅  |
| `GET`  | `/fc_clima_mes_estado`        | (WeatherAPI) Pronóstico **mensual** ARIMA por estado                                                                                                                   |  ✅  |
| `GET`  | `/fc_clima_diario`            | (WeatherAPI) Pronóstico **diario** ARIMA por ciudad                                                                                                                    |  ✅  |
| `GET`  | `/turismo`                    | Dato de turismo mensual por estado                                                                                                                        | ✅   |
| `GET`  | `/dias_festivos`              | Carta de días festivos nacionales                                                                                                                         | ✅   |
| `GET`  | `/cov_matrix`                 | **Matriz de covarianza** (h×h) de pronósticos SARIMA                                                                                                      | ✅   |
| `GET`  | `/clima_pasado_futuro`        | **Serie mensual** que concatena pasado y futuro alrededor de `fecha_modelo` hasta `fecha_fin`                                                             | ✅   |
| `GET`  | `/copernicus_hourly_grib`     | **historia a nivel hora**,se obtiene en su nivel mas desagregado y se procesa directamente de los archivos .grib                                          | ✅   |
| `GET`  | `/copernicus_historical`      | **historia en diario (D) o mensual (M)**, al elegir nivel = 'estado' o 'ciudad' se hace la agrupación deseada en la temporalidad dada                      | ✅   |
| `GET`  | `/copernicus_forecast`        | Forecast Copernicus basado en **anomalías** primeros 6 meses son las predichas, después el promedio histórico de las anomalías en su máxima desagregación, al elegir nivel = 'estado' o 'ciudad' se hace la agrupación deseada | ✅   |
| `GET`  | `/copernicus_historical_latam` | **historia en diario (D) o mensual (M) para LATAM**, al elegir nivel = 'departamento' o 'municipio' se hace la agrupación deseada en la temporalidad dada | ✅   |
| `GET`  | `/copernicus_forecast_latam`   | Forecast Copernicus basado en **anomalías** para LATAM, primeros 6 meses son las predichas, después el promedio histórico de las anomalías | ✅   |

**Leyenda**
- ✅ - Endpoint validado y actualizado hasta la versión de última actualización reportada.
- ⚠️ - Método propio de la API, omitir su uso.


### Ejemplos de uso de la librería

A continuación se muestran ejemplos de cómo utilizar cada uno de los métodos disponibles en la clase `PDEXClient`, con sus parámetros y argumentos.

```python
from pdexapi  import PDEXClient

cli = PDEXClient(
    base_url="http://api.pdexapi.com",
    username="tu_usuario",
    password="tu_password",
)
```

## Endpoints
### inflacion

Obtiene la inflación diaria en un rango de fechas. Proveedor: gobierno de México.

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

Predicción de inflación futura. Proveedor: gobierno de México.

```python
pred = cli.inflacion_prediccion(
    fecha_inicio="2025-07-01",
    fecha_fin="2025-12-01",
    as_frame=True
)
print(pred)
```

### fc_clima_mes

Pronóstico mensual climático para una ciudad. Proveedor: WeatherAPI + Polydata.

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

Pronóstico mensual climático para un estado completo. Proveedor: WeatherAPI + Polydata.

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

Pronóstico diario climático para una ciudad. Proveedor: WeatherAPI + Polydata.

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

Clima diario histórico entre dos fechas. Proveedor: WeatherAPI.

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

Clima histórico agregado a nivel nacional (todas las ciudades). Proveedor: WeatherAPI.

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

Clima mensual histórico para un estado. Proveedor: WeatherAPI.

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

### cov_matrix

Matriz de covarianza de pronóstico SARIMA de tamaño `h × h`. Proveedor: Polydata.

```python
# Como DataFrame (índices/columnas 1..h)
S_df = cli.cov_matrix(
    fecha_modelo="2025-06-01",
    forecast_horizon=12,
    variable="avgtemp_c",
    estado="Jalisco",
    as_frame=True,
)
print(S_df)

# Como lista de listas (JSON nativo)
S_list = cli.cov_matrix(
    fecha_modelo="2025-06-01",
    forecast_horizon=12,
    variable="avgtemp_c",
)
print(len(S_list), "x", len(S_list[0]))

# Como numpy.ndarray (requiere `numpy`)
S_np = cli.cov_matrix(
    fecha_modelo="2025-06-01",
    forecast_horizon=12,
    variable="avgtemp_c",
    as_array=True,
)
print(S_np.shape)
```

### clima_pasado_futuro

Serie mensual que concatena pasado y futuro alrededor de `fecha_modelo` hasta `fecha_fin`, para una variable y estado dados. Devuelve lista de diccionarios o `DataFrame`. Proveedor: Polydata.

```python
# Como lista de dicts
fc = cli.clima_pasado_futuro(
    fecha_modelo="2025-01-01",
    fecha_fin="2025-06-01",
    variable="avgtemp_c",
    estado="Jalisco",
)
print(fc[:3])

# Como DataFrame
fc_df = cli.clima_pasado_futuro(
    fecha_modelo="2025-01-01",
    fecha_fin="2025-06-01",
    variable="avgtemp_c",
    estado="Jalisco",
    as_frame=True,
)
print(fc_df.head())
```

### **Copernicus Historical** 

#### temporalidad hora (H) 
En este endpoint se encuentra la mayor desagregación de clima en la base, en la cual se consultan los archivos GRIB directamente (archivos binarios optimizados para meteorología) los cuales tienen la data por horas. Si se desea usar es recomendable consultar día por día, ya que un rango de fechas amplio podría botar el timeout del sistema.

```python
df = cli.copernicus_historical(
    estado="Jalisco",
    ciudad="Guadalajara",
    fecha_inicio="2023-01-01",
    fecha_fin="2023-01-05",
    variable=["avgtemp_c", "totalprecip_mm"],
    freq="H",
    as_frame=True
)
```

#### temporalidad diaria (D)
En este endpoint se consulta la información ya depurada de los archivos GRIB en su agregación por día.

```python
df_estado = cli.copernicus_historical(
        nivel = 'estado', # nivel estado o ciudad
        freq = 'D', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado='Jalisco', # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad='Zapopan',
        as_frame=True
    )
```

#### temporalidad mensual (M)
En este endpoint se consulta la información ya depurada de los archivos GRIB en su agregación mensual, su actualización se hace una vez que la tabla de datos diarios esté actualizada hasta el último día del mes.

```python
df_estado = cli.copernicus_historical(
        nivel = 'estado', # nivel estado o ciudad
        freq = 'M', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado=None, # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad=None,
        as_frame=True
    )
```

### **Copernicus Forecast**
Este endpoint es un trabajo de Polydata en el que se complementa la información de la API para poder generar escenarios futuros. Se toman las anomalías de las variables y se agregan al promedio histórico ponderado por población, dado que la actualización de anomalías de Copernicus es hasta 6 meses en el futuro, si se hace una consulta con fh mayor a 6, a partir del mes 7 regresará el promedio de las anomalías históricas agregado al promedio histórico.

```python
fc_df = cli.copernicus_forecast(
            nivel = 'estado', # nivel estado o ciudad
            fecha_entrenamiento = '2025-11-01',
            variable = ["maxtemp_c", "avgtemp_c"],
            fh = 24,
            velocity=False,  # incluir velocidad de cambio
            anomaly=True,    # incluir anomalías
            estado = "Jalisco", # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
            ciudad = "Zapopan",
            as_frame=True
         )
```

### **Copernicus Historical LATAM**

Endpoint para consultar datos históricos de clima de Copernicus para países de Latinoamérica. Funciona de manera similar a `copernicus_historical` pero con la estructura geográfica de LATAM (país → departamento → municipio).

#### temporalidad diaria (D)

```python
df = cli.copernicus_historical_latam(
    nivel='departamento',  # nivel departamento o municipio
    freq='D',  # freq mensual (M) o diaria (D)
    variable="maxtemp_c",
    fecha_inicio='2025-01-01',
    fecha_fin='2025-11-01',
    pais='Colombia',
    departamento='Antioquia',  # si se coloca None, la api devuelve todos los departamentos
    municipio=None,
    as_frame=True
)
print(df.head())
```

#### temporalidad mensual (M)

```python
df = cli.copernicus_historical_latam(
    nivel='municipio',
    freq='M',
    variable="avgtemp_c",
    fecha_inicio='2024-01-01',
    fecha_fin='2024-12-01',
    pais='Colombia',
    departamento='Cundinamarca',
    municipio='Bogotá',
    as_frame=True
)
print(df.head())
```

#### Consulta a nivel país (todos los departamentos/municipios)

```python
df = cli.copernicus_historical_latam(
    nivel='departamento',
    freq='M',
    variable="totalprecip_mm",
    fecha_inicio='2024-01-01',
    fecha_fin='2024-12-01',
    pais='Perú',
    departamento=None,  # None devuelve todos los departamentos
    municipio=None,
    as_frame=True
)
print(df.head())
```

### **Copernicus Forecast LATAM**

Endpoint de pronóstico climático para países de Latinoamérica basado en anomalías. Similar a `copernicus_forecast` pero adaptado a la estructura geográfica de LATAM. Incluye parámetros adicionales de `velocity` y `anomaly` para controlar el tipo de salida.

Al igual que en el forecast de México, si se hace una consulta con `fh` mayor a 6, a partir del mes 7 regresará el promedio de las anomalías históricas agregado al promedio histórico.

```python
fc_df = cli.copernicus_forecast_latam(
    nivel='departamento',  # nivel departamento o municipio
    fecha_entrenamiento='2025-11-01',
    variable=["maxtemp_c", "avgtemp_c"],
    fh=24,
    velocity=False,  # incluir velocidad de cambio
    anomaly=True,    # incluir anomalías
    pais='Colombia',
    departamento='Antioquia',  # si se coloca None, la api devuelve todos
    municipio=None,
    as_frame=True
)
print(fc_df.head())
```

#### Consulta a nivel municipio

```python
fc_df = cli.copernicus_forecast_latam(
    nivel='municipio',
    fecha_entrenamiento='2025-11-01',
    variable="avgtemp_c",
    fh=12,
    velocity=True,
    anomaly=True,
    pais='Chile',
    departamento='Metropolitana',
    municipio='Santiago',
    as_frame=True
)
print(fc_df.head())
```

**Parámetros específicos LATAM:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `pais` | `str` | País de Latinoamérica (ej: 'Colombia', 'Perú', 'Chile') |
| `departamento` | `str \| None` | División administrativa nivel 1 (opcional, None devuelve todos) |
| `municipio` | `str \| None` | División administrativa nivel 2 (opcional) |
| `velocity` | `bool` | Incluir velocidad de cambio en la respuesta |
| `anomaly` | `bool` | Incluir anomalías en la respuesta |

## Manejo de errores

Se propagan como `requests.HTTPError`.

```python
try:
    cli.inflacion("2020-01-01", "2020-01-05")
except requests.HTTPError as e:
    print(e.response.text)
```

## Requisitos

- Python ≥3.11
- `requests`
- `pandas`
- `numpy` (opcional, para `as_array=True`)

© 2025 Equipo Polydata — Uso interno.
