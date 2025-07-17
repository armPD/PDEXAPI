# ======================================================================================
# Script:  conn_test.py
# Purpose: ejemplo de uso del cliente PDEXClient para conectarse a la API de Polydata Exógenos
# Author:  Fernando Figueroa  |  Equipo Polydata
# Created: 2025‑07‑06  |  Last Updated: 2025‑07‑10  |  Version: 1.1-debugging
# ======================================================================================
import sys
from pdexapi.PDExAPI_Client import PDEXClient

cli = PDEXClient("url_api_PDEXAPI", "user_dummy", "password_dummy")
sys.exit()
tabla_df = cli.list_tables()

print(tabla_df)

df_fc = cli.fc_clima_mes(
    estado="Jalisco",             # clave del estado (ej. Nuevo León)
    ciudad="Zapopan",      # nombre usado al entrenar el modelo
    variable="maxtemp_c",    # variable climática (coincide con la entrenada)
    fecha_inicio="2025-08-01",
    fecha_fin="2025-12-01",
    as_frame=True,           # ← devuelve pandas.DataFrame
)

print(df_fc.head())

df_fc = cli.fc_clima_diario(
    estado="Jalisco",             # clave del estado (ej. Nuevo León)
    ciudad="Zapopan",      # nombre usado al entrenar el modelo
    variable="maxtemp_c",    # variable climática (coincide con la entrenada)
    fecha_inicio="2025-08-01",
    fecha_fin="2025-09-01",
    as_frame=True,           # ← devuelve pandas.DataFrame
)
