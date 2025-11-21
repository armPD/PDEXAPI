# ======================================================================================
# Script:  pdexapi_client.py
# Purpose: funciones para conectarse e interactuar con la API de Polydata Exógenos
#          (PDExAPI) de manera sencilla y eficiente.
# Author:  Fernando Figueroa  |  Equipo Polydata
# Created: 2025‑07‑06  |  Last Updated: 2025‑07‑10  |  Version: 1.1-debugging
# ======================================================================================
"""Resumen
-----------
Funciones y clases auxiliares para:
• Inicialización de la clase core PDEXClient
• funciones completas de la API
-----------
"""
# --------------------------------------------------------------------------------------
# Librerias
# --------------------------------------------------------------------------------------
import os
import sys
import time
import requests
import numpy as np
import pandas as pd

from pathlib import Path
from typing import Any, Dict, List, Optional, Literal, overload


class PDEXClient:
    """
    Cliente ligero para la API de Polydata Exógenos.

    Ejemplo rápido
    --------------
    >>> cli = PDEXClient("http://localhost:8000", "demo", "tu_password")
    >>> cli.list_tables()
    ['inflacion', 'precipitacion_mensual', ...]
    >>> df = cli.fc_clima_mes(
    ...     estado="NL", ciudad="Monterrey", variable="maxtemp_c",
    ...     fecha_inicio="2025-08-01", fecha_fin="2025-12-01",
    ...     as_frame=True
    ... )
    """

    # ------------------------------------------------------------------ #
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        *,
        timeout: int | float = 10,
    ):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        self.timeout = timeout

        self._token: str | None = None
        self._exp_ts: float | None = None  # timestamp UNIX (segundos)

        # Autentica inmediatamente
        self._login()

    # ------------------------------------------------------------------ #
    # Helpers privados
    # ------------------------------------------------------------------ #
    def _login(self) -> None:
        """Obtiene y guarda el token de acceso."""
        url = f"{self.base_url}/token"
        data = {"username": self.username, "password": self.password}
        r = requests.post(url, data=data, timeout=self.timeout)
        r.raise_for_status()
        payload = r.json()
        self._token = payload["access_token"]
        # decode payload["access_token"]? → si fuera JWT podríamos saber exp.
        # Como es Fernet, usamos TTL de .env (p.ej. 60 min) como aproximación.
        self._exp_ts = time.time() + 55 * 60  # refrescaremos a los 55 min

    def _headers(self) -> Dict[str, str]:
        """Cabeceras con token; renueva si está a punto de expirar."""
        if self._exp_ts and time.time() > self._exp_ts:
            self._login()
        return {"Authorization": f"Bearer {self._token}"}

    def _get(self, path: str, params: Dict[str, Any] | None = None):
        url = f"{self.base_url}{path}"
        r = requests.get(url, params=params, headers=self._headers(), timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    # ------------------------------------------------------------------ #
    # Endpoints públicos
    # ------------------------------------------------------------------ #
    def list_tables(self) -> List[str]:
        """Lista todas las tablas disponibles en la BD."""
        return self._get("/tables")


    def inflacion(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        fecha_proceso: str | None = None,
        *,
        as_frame: bool = False,
    ):
        params: Dict[str, Any] = {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
        if fecha_proceso:
            params["fecha_proceso"] = fecha_proceso
        data = self._get("/inflacion", params=params)
        return pd.DataFrame(data) if as_frame else data
    

    def inflacion_prediccion(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        fecha_proceso: str | None = None,
        *,
        as_frame: bool = False,
    ):
        params: Dict[str, Any] = {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
        if fecha_proceso:
            params["fecha_proceso"] = fecha_proceso
        data = self._get("/inflacion_prediccion", params=params)
        return pd.DataFrame(data) if as_frame else data


    def fc_clima_mes(
        self,
        *,
        estado: str,
        ciudad: str,
        variable: str,
        fecha_inicio: str,
        fecha_fin: str,
        as_frame: bool = False,
    ):
        params = {
            "estado": estado,
            "ciudad": ciudad,
            "variable": variable,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
        data = self._get("/fc_clima_mes", params=params)
        return pd.DataFrame(data) if as_frame else data
    

    def fc_clima_diario(
        self,
        *,
        estado: str,
        ciudad: str,
        variable: str,
        fecha_inicio: str,
        fecha_fin: str,
        as_frame: bool = False,
    ):
        params = {
            "estado": estado,
            "ciudad": ciudad,
            "variable": variable,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
        data = self._get("/fc_clima_diario", params=params)
        return pd.DataFrame(data) if as_frame else data


    def clima_historico(
        self,
        *,
        estado: str,
        ciudad: str,
        fecha_inicio: str,
        fecha_fin: str,
        variable: str | None = None,   # ← opcional
        mes: bool = False, 
        as_frame: bool = False,
    ):
        """
        Devuelve clima diario histórico entre dos fechas.

        • Si `variable` se omite, regresa todas las variables climáticas.
        • Siempre incluye columnas: fecha, estado, ciudad.

        Parámetros
        ----------
        estado, ciudad : str
        fecha_inicio, fecha_fin : 'YYYY-MM-DD'
        variable : str | None
            Ej. 'maxtemp_c', 'totalprecip_mm', etc.
        """
        params = {
            "estado": estado,
            "ciudad": ciudad,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "mes": mes,
        }
        if variable:
            params["variable"] = variable

        data = self._get("/clima_historico", params=params)
        return pd.DataFrame(data) if as_frame else data


    def clima_historico_nacional(
        self,
        *,
        fecha_inicio: str,
        fecha_fin: str,
        variable: str | None = None,   # ← opcional
        mes: bool = False,
        as_frame: bool = False,
    ):
        """
        Clima histórico de TODO el país entre `fecha_inicio` y `fecha_fin`
        (incluye todas las variables meteorológicas).

        Parámetros
        ----------
        fecha_inicio, fecha_fin : 'YYYY-MM-DD'
        as_frame : bool, opcional
            Si True, devuelve `pandas.DataFrame`; si False, lista de dicts.
        """
        params = {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "mes": mes,
        }
        if variable:
            params["variable"] = variable

        data = self._get("/clima_historico_nacional", params=params)
        return pd.DataFrame(data) if as_frame else data


    def clima_historico_estado_mes(
            self, 
            *, 
            estado: str, 
            fecha_inicio: str, 
            fecha_fin: str, 
            variable: str | None = None, 
            as_frame: bool = False
        ):
        params = {
            "estado": estado,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }
        if variable:
            params["variable"] = variable
        data = self._get("/clima_historico_estado_mes", params=params)
        return pd.DataFrame(data) if as_frame else data
    

    def fc_clima_mes_estado(
        self,
        *,
        estado: str,
        variable: str,
        fecha_inicio: str,
        fecha_fin: str,
        as_frame: bool = False,
    ):
        """
        Pronóstico mensual de variable climática entre dos fechas para un estado.

        Parámetros
        ----------
        estado : str
            Nombre del estado (ej. "Jalisco")
        variable : str
            Nombre de la variable climática (ej. "avgtemp_c")
        fecha_inicio : str
            Fecha inicial (ej. "2025-01-01")
        fecha_fin : str
            Fecha final (ej. "2025-06-01")
        as_frame : bool, opcional
            Si True, devuelve `pandas.DataFrame`; si False, lista de dicts.
        """
        params = {
            "estado": estado,
            "variable": variable,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

        data = self._get("/fc_clima_mes_estado", params=params)
        return pd.DataFrame(data) if as_frame else data

    def cov_matrix(
        self,
        *,
        fecha_modelo: str,
        forecast_horizon: int,
        variable: str,
        estado: Optional[str] = None,
        as_array: bool = False,
        as_frame: bool = False,
    ):
        """
        Matriz de covarianza de pronóstico SARIMA (h x h).

        Parámetros
        ----------
        fecha_modelo : str
            Iteración del modelo (ej. "2025-06-01").
        forecast_horizon : int
            Horizonte de pronóstico (h).
        variable : str
            Variable climática (ej. "avgtemp_c").
        estado : str, opcional
            Estado (ej. "Jalisco"). Si no se especifica, usa "Nacional".
        as_array : bool, opcional
            Si True, devuelve `numpy.ndarray` (h x h).
        as_frame : bool, opcional
            Si True, devuelve `pandas.DataFrame` con índices/columnas 1..h.

        Returns
        -------
        list[list[float]] | np.ndarray | pd.DataFrame
        """
        params: Dict[str, Any] = {
            "fecha_modelo": fecha_modelo,
            "forecast_horizon": forecast_horizon,
            "variable": variable,
        }
        if estado:
            params["estado"] = estado

        data: List[List[float]] = self._get("/cov_matrix", params=params)

        if as_array:
            return np.asarray(data)

        if as_frame:
            h = len(data)
            idx = range(1, h + 1)
            return pd.DataFrame(data, index=idx, columns=idx)

        return data


    def copernicus_historical(
        self,
        *,
        estado: str | None,
        ciudad: str | None,
        fecha_inicio: str,
        fecha_fin: str,
        variable=None,
        freq: str = "D",
        as_frame: bool = False,
    ):
        """
        Consulta datos históricos Copernicus.

        Parámetros
        ----------
        estado : str | None
        ciudad : str | None
        fecha_inicio, fecha_fin : 'YYYY-MM-DD'
        variable : str | list[str] | None
            Si None → todas las variables de copernicus_variables.
        freq : {'H', 'D', 'M'}
        as_frame : bool
            True → DataFrame, False → lista de dicts.
        """
        # Normalizar variable en formato list[str]
        if variable is None:
            pass  # API devolverá todo
        elif isinstance(variable, str):
            variable = [variable]
        elif isinstance(variable, list):
            pass
        else:
            raise ValueError("variable debe ser string, lista o None")

        params = {
            "estado": estado,
            "ciudad": ciudad,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "freq": freq,
        }

        if variable is not None:
            # FastAPI acepta múltiples ?variable=a&variable=b
            params["variable"] = variable

        data = self._get("/copernicus_historical", params=params)
        return pd.DataFrame(data) if as_frame else data


    # ------------------------------------------------------------------ #
    # Copernicus Forecast
    # ------------------------------------------------------------------ #
    def copernicus_forecast(
        self,
        *,
        estado: str | None,
        ciudad: str | None,
        fecha_entrenamiento: str,
        fh: int,
        variable=None,
        as_frame: bool = False,
    ):
        """
        Forecast climático Copernicus basado en anomalías mensuales.

        Parámetros
        ----------
        estado : str | None
        ciudad : str | None
        fecha_entrenamiento : 'YYYY-MM-DD'
        fh : int
            Horizonte de pronóstico (meses).
        variable : str | list[str] | None
            Si None → todas las variables.
        as_frame : bool
            True → DataFrame, False → lista de dicts.
        """

        # Normalizar variable en formato lista
        if variable is None:
            pass
        elif isinstance(variable, str):
            variable = [variable]
        elif isinstance(variable, list):
            pass
        else:
            raise ValueError("variable debe ser string, lista o None")

        params = {
            "estado": estado,
            "ciudad": ciudad,
            "fecha_entrenamiento": fecha_entrenamiento,
            "fh": fh,
        }

        if variable is not None:
            params["variable"] = variable

        data = self._get("/copernicus_forecast", params=params)
        return pd.DataFrame(data) if as_frame else data


    def copernicus_forecast(
        self,
        *,
        estado: str | None,
        ciudad: str | None,
        fecha_entrenamiento: str,
        fh: int,
        variable=None,
        as_frame: bool = False,
    ):
        """
        Forecast climático Copernicus basado en anomalías.

        Parámetros
        ----------
        estado : str | None
        ciudad : str | None
        fecha_entrenamiento : 'YYYY-MM-DD'
        fh : int
            Horizon de forecast (meses)
        variable : str | list[str] | None
            Si None → todas las variables disponibles
        as_frame : bool
            Si True → pandas.DataFrame

        """
        params = {
            "estado": estado,
            "ciudad": ciudad,
            "fecha_entrenamiento": fecha_entrenamiento,
            "fh": fh,
            "variable": variable,
        }

        data = self._get("/copernicus_forecast", params=params)
        return pd.DataFrame(data) if as_frame else data


    def poblacion(
        self,
        *,
        estado: str,
        ciudad: str | None = None,
        fecha_proceso: str | None = None,
        as_frame: bool = False,
    ):
        """
        Devuelve población.

        • Si `ciudad` es None se agrupa por todo el estado (SUM).
        • Si `fecha_proceso` se omite, usa la fecha más reciente disponible.
        """
        params: Dict[str, Any] = {"estado": estado}
        if ciudad:
            params["ciudad"] = ciudad
        if fecha_proceso:
            params["fecha_proceso"] = fecha_proceso

        data = self._get("/poblacion", params=params)
        return pd.DataFrame(data) if as_frame else data 
    

    def turismo(
        self,
        *,
        estado: str,
        fecha_inicio: str,
        fecha_fin: str,
        as_frame: bool = False,
    ):
        """
        Devuelve datos de turismo para un estado entre dos fechas (por `fecha_periodo`).

        • Siempre usa la fecha más reciente de `fecha_proceso` disponible.

        Parámetros
        ----------
        estado : str
        fecha_inicio, fecha_fin : 'YYYY-MM-DD'
        as_frame : bool, opcional
            Si True, devuelve `pandas.DataFrame`; si False, lista de dicts.
        """
        params = {
            "estado": estado,
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
        }

        data = self._get("/turismo", params=params)
        return pd.DataFrame(data) if as_frame else data
    

    def dias_festivos(
        self,
        *,
        as_frame: bool = False,
    ):
        """
        Devuelve la carta completa de dias festivos
        Parámetros
        ----------
        as_frame : bool, opcional
            Si True, devuelve `pandas.DataFrame`; si False, lista de dicts.
        """
        params = {}

        data = self._get("/dias_festivos", params=params)
        return pd.DataFrame(data) if as_frame else data