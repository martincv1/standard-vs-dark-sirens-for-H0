"""Posterior de H0 de GW170817 a partir de las muestras públicas de D_L (spec.md §4). Dueño: Datos.

Ecuación 9 de Abbott et al. 2017 (Nature 551, 85; arXiv:1710.05835v1, Methods):

    p(H0 | datos) ∝ p(H0) ∫ dd dv_p dcosι  p(x_GW | d, cosι) p(d) p(cosι)
                     × N(v_r; v_p + H0 d, σ_vr) × N(<v_p>; v_p, σ_vp) × p(v_p)

Las muestras de PE representan p(x_GW | d, cosι) π_PE(d) π_PE(cosι). Como π_PE(d) ∝ d² es el mismo
p(d) del paper, el peso de cada muestra es w_i = p(d_i) / π_PE(d_i) = 1 (spec.md §4). cosι no aparece
en el factor de velocidad, así que se marginaliza solo al ignorar esa columna.

La integral en v_p es analítica: el producto de las dos gaussianas es
N(v_r - H0 d; <v_p>, s) × N(v_p; m, τ), con s² = σ_vr² + σ_vp², y la gaussiana en v_p se integra sobre
el prior uniforme [-1000, 1000] con la CDF normal.
"""

from pathlib import Path

import h5py
import numpy as np
from scipy import stats

# Abbott et al. 2017, Methods, ecs. 5–6 y el párrafo siguiente a la ec. 7. Leídos del paper, no de memoria.
V_R = 3327.0  # km/s, velocidad de recesión del grupo de NGC 4993 en el sistema de la CMB
SIGMA_V_R = 72.0  # km/s
V_P_MEDIDA = 310.0  # km/s, velocidad peculiar medida <v_p>
SIGMA_V_P = 150.0  # km/s
V_P_PRIOR = (-1000.0, 1000.0)  # km/s, prior uniforme de v_p

DATASET = "IMRPhenomPv2NRT_lowSpin_posterior"  # spec.md §4
COLUMNA_D = "luminosity_distance_Mpc"


def leer_distancias(hdf5: Path, dataset: str = DATASET) -> np.ndarray:
    """Muestras posteriores de D_L [Mpc] del HDF5 de GWTC-1."""
    with h5py.File(hdf5, "r") as f:
        return np.asarray(f[dataset][COLUMNA_D], dtype=float)


def pesos_reweighting(d: np.ndarray, prior_nuevo, prior_pe) -> np.ndarray:
    """w_i = prior_nuevo(d_i) / prior_pe(d_i). Con los dos ∝ d² da pesos constantes."""
    return prior_nuevo(d) / prior_pe(d)


def n_efectivo(w: np.ndarray) -> float:
    """Tamaño de muestra efectivo (Σw)² / Σw²."""
    return float(w.sum() ** 2 / (w**2).sum())


def likelihood_velocidad(x: np.ndarray) -> np.ndarray:
    """∫ dv_p N(V_R; v_p + x, σ_vr) N(<v_p>; v_p, σ_vp) U(v_p; V_P_PRIOR), con x = H0·d [km/s]."""
    s2 = SIGMA_V_R**2 + SIGMA_V_P**2
    tau = np.sqrt(SIGMA_V_R**2 * SIGMA_V_P**2 / s2)
    y = V_R - x  # la v_p que pide la medición de v_r
    m = tau**2 * (y / SIGMA_V_R**2 + V_P_MEDIDA / SIGMA_V_P**2)
    lo, hi = V_P_PRIOR
    masa = stats.norm.cdf((hi - m) / tau) - stats.norm.cdf((lo - m) / tau)
    return stats.norm.pdf(y, V_P_MEDIDA, np.sqrt(s2)) * masa / (hi - lo)


def likelihood_h0(h0: np.ndarray, d: np.ndarray, w: np.ndarray, bloque: int = 100) -> np.ndarray:
    """L(H0) = Σ_i w_i · likelihood_velocidad(H0 · d_i) / Σ_i w_i, sin normalizar. Se calcula por bloques de H0."""
    L = np.empty_like(h0)
    for i in range(0, h0.size, bloque):
        x = h0[i : i + bloque, None] * d[None, :]
        L[i : i + bloque] = likelihood_velocidad(x) @ w / w.sum()
    return L
