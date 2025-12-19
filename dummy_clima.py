import os

from pdexapi  import PDEXClient

from dotenv import load_dotenv

from typing import Any, Dict

def _load_env() -> Dict[str, Any]:
    """Carga variables de entorno y valida su presencia."""
    load_dotenv()
    keys = [
        "pdexapi",
        "user",
        "password",
    ]
    env = {k: os.getenv(k) for k in keys}
    missing = [k for k, v in env.items() if v is None]
    if missing:
        raise EnvironmentError(f"Faltan variables de entorno: {', '.join(missing)}")
    return env

env = _load_env()

cli = PDEXClient(
    base_url=env["pdexapi"], # Nota: sin la s en http
    username=env["user"],
    password=env["password"],
)

# --------------------------------------- HISTORICO -------------------------------------------#
# Hora
df = cli.copernicus_historical(
    estado="Jalisco",
    ciudad="Guadalajara",
    fecha_inicio="2023-01-01",
    fecha_fin="2023-01-05",
    variable=["avgtemp_c", "totalprecip_mm"],
    freq="H",
    as_frame=True
)

# dia ciudad
df_ciudad_dia = cli.copernicus_historical(
        nivel = 'ciudad', # nivel estado o ciudad
        freq = 'D', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado=None, # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad=None,
        as_frame=True
    )

# dia estado
df_estado_dia = cli.copernicus_historical(
        nivel = 'estado', # nivel estado o ciudad
        freq = 'D', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado='Jalisco', # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad=None,
        as_frame=True
    )

# dia todo (estados + nacional)
df_completo_dia = cli.copernicus_historical(
        nivel = 'estado', # nivel estado o ciudad
        freq = 'D', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado=None, # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad=None,
        as_frame=True
    )

# mes ciudad
df_ciudad_mes = cli.copernicus_historical(
        nivel = 'ciudad', # nivel estado o ciudad
        freq = 'M', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado='Jalisco', # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad='Zapopan',
        as_frame=True
    )

# mes estado
df_estado_mes = cli.copernicus_historical(
        nivel = 'estado', # nivel estado o ciudad
        freq = 'M', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado='Jalisco', # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad=None,
        as_frame=True
    )

# mes estado
df_completo_mes = cli.copernicus_historical(
        nivel = 'estado', # nivel estado o ciudad
        freq = 'M', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado=None, # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad=None,
        as_frame=True
    )

# Cualquier temporalidad solo nacional
df_nacional_diario = cli.copernicus_historical(
        nivel = 'estado', # nivel estado o ciudad
        freq = 'D', # freq mensual (M) o diaria (D)
        variable = "maxtemp_c",
        fecha_inicio = '2025-01-01',
        fecha_fin = '2025-11-01',
        estado='Nacional', # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
        ciudad=None,
        as_frame=True
    )

# --------------------------------------- FORECAST -------------------------------------------#

# ciudad mes
fc_df = cli.copernicus_forecast(
            nivel = 'ciudad', # nivel estado o ciudad
            fecha_entrenamiento = '2024-12-20',
            variable = ["maxtemp_c", "avgtemp_c"],
            fh = 12,
            estado = "Jalisco", # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
            ciudad = "Zapopan",
            as_frame=True
         )

# estado mes
fc_df = cli.copernicus_forecast(
            nivel = 'estado', # nivel estado o ciudad
            fecha_entrenamiento = '2025-11-01',
            variable = ["maxtemp_c", "avgtemp_c"],
            fh = 12,
            estado = "Jalisco", # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
            ciudad = None,
            as_frame=True
         )

# completo mes
fc_df = cli.copernicus_forecast(
            nivel = 'estado', # nivel estado o ciudad
            fecha_entrenamiento = '2025-11-01',
            variable = "maxtemp_c",
            fh = 12,
            estado = None, # si se coloca None en ciudad y estado, la api devuelve todos los estados y ciudades y nacional
            ciudad = None,
            as_frame=True
         )
