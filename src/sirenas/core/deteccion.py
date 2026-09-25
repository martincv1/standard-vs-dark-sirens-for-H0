"""Regla generativa de detección y α(H0) (spec.md §2.4). Convención de Datos en core/; revisa Modelo.

Un evento se detecta si a_obs ≥ A_TH, con A_TH = 1/(190 Mpc): la amplitud de un evento face-on
(A = 1) en el horizonte BNS de ≈190 Mpc de Abbott et al. 2017 (Methods). Tomarlo face-on es un
supuesto (decisiones/2026-09-25-UC-deteccion-y-seleccion.md). Esta es la ÚNICA regla de detección
del repo: todos los escenarios, bright y dark, la importan de acá.

    α(H0) = ∫ dv p0(v) ∫ dcosι/2  P(a_obs ≥ A_TH | media A(ι)·H0/v, σ_a),   p0(v) = U[v_min, v_max]

A(ι) se recibe como argumento (`amplitud`, función de cosι) para no duplicar la de L_GW, que es de Modelo.
"""

import numpy as np
from scipy import stats

HORIZONTE_MPC = 190.0  # Abbott et al. 2017, Methods (efectos de selección)
A_TH = 1.0 / HORIZONTE_MPC  # Mpc^-1


def detectado(a_obs):
    """True si la amplitud observada supera el umbral (a_obs ≥ A_TH). Vectorizada."""
    return np.asarray(a_obs) >= A_TH


def prob_deteccion(a_media, sigma_a: float):
    """P(a_obs ≥ A_TH) con a_obs ~ N(a_media, sigma_a)."""
    return stats.norm.sf(A_TH, loc=a_media, scale=sigma_a)


def alfa(h0: np.ndarray, sigma_a: float, amplitud, v_min: float, v_max: float,
         n_v: int = 401, n_cos: int = 201) -> np.ndarray:
    """α(H0) sobre los puntos de h0: fracción de eventos detectados, con v ~ U[v_min, v_max] y cosι ~ U[-1, 1].

    Integral doble por trapecio en una grilla (v, cosι); su convergencia está testeada.
    """
    v = np.linspace(v_min, v_max, n_v)
    cos_i = np.linspace(-1.0, 1.0, n_cos)
    A = amplitud(cos_i)
    salida = np.empty(np.size(h0))
    for k, h in enumerate(np.atleast_1d(h0)):
        p = prob_deteccion(A[None, :] * h / v[:, None], sigma_a)  # [v, cosι]
        salida[k] = np.trapezoid(np.trapezoid(p, cos_i, axis=1) / 2, v) / (v_max - v_min)
    return salida
