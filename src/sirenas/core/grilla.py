"""Grilla y prior de H0 compartidos (spec.md §2.1). Dueño: Modelo; escrito por Datos a pedido, revisa Modelo.

Grilla: H0 en [20, 250] km/s/Mpc, paso 0,1 (2301 puntos, extremos incluidos).
Priors: uniforme (escenarios sintéticos) y ∝ 1/H0 (solo validación con GW170817).
Todas las integrales sobre la grilla son por trapecio.
"""

import numpy as np

H0_MIN = 20.0
H0_MAX = 250.0
DH0 = 0.1


def grilla_h0(h0_min: float = H0_MIN, h0_max: float = H0_MAX, dh0: float = DH0) -> np.ndarray:
    """Puntos de la grilla de H0 [km/s/Mpc], extremos incluidos. Los argumentos solo se cambian en tests de convergencia."""
    n = int(round((h0_max - h0_min) / dh0)) + 1
    return np.linspace(h0_min, h0_max, n)


def normalizar(p: np.ndarray, h0: np.ndarray) -> np.ndarray:
    """Devuelve p / ∫ p dH0 (trapecio sobre la grilla)."""
    integral = np.trapezoid(p, h0)
    if not integral > 0:
        raise ValueError(f"no se puede normalizar: la integral es {integral}")
    return p / integral


def prior_uniforme(h0: np.ndarray) -> np.ndarray:
    """π(H0) uniforme sobre la grilla, normalizado."""
    return normalizar(np.ones_like(h0), h0)


def prior_inverso(h0: np.ndarray) -> np.ndarray:
    """π(H0) ∝ 1/H0 sobre la grilla, normalizado. Solo para la validación con GW170817 (Abbott et al. 2017, Methods)."""
    return normalizar(1.0 / h0, h0)
