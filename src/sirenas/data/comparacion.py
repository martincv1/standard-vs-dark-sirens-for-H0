"""Comparación del posterior de GW170817 con Abbott et al. 2017 y Figure1.csv (spec.md §4). Dueño: Datos.

La tolerancia se escribió antes de comparar (decisiones/2026-09-25-UC-validacion-gw170817.md).
MAP y HPD de este archivo son solo para la validación. Cuando Modelo publique las métricas en core/,
el HPD de la validación pasa a importarse de ahí, con un test de que las dos dan lo mismo.
"""

import numpy as np
from scipy.ndimage import gaussian_filter1d

# Abbott et al. 2017, Methods (después de la ec. 9): MAP y HPD 68,3 % = 70,0 +12,0 −8,0 km/s/Mpc.
MAP_PUBLICADO = 70.0
HPD_PUBLICADO = (62.0, 82.0)
NIVEL = 0.683

# Tolerancias (spec.md §4)
TOL_MAP = 3.0
TOL_BORDES = 3.0
TOL_KS = 0.05


def map_grilla(h0: np.ndarray, p: np.ndarray) -> float:
    return float(h0[np.argmax(p)])


def hpd_grilla(h0: np.ndarray, p: np.ndarray, nivel: float = NIVEL) -> tuple[float, float, float]:
    """Conjunto de máxima densidad con masa `nivel`. Devuelve (borde inferior, borde superior, medida).

    Grilla equiespaciada: masa de cada punto ≈ p·ΔH0. Si el conjunto es disjunto, la medida es menor que
    (superior - inferior).
    """
    dh = h0[1] - h0[0]
    masa = p * dh / np.sum(p * dh)
    orden = np.argsort(masa)[::-1]
    k = np.searchsorted(np.cumsum(masa[orden]), nivel) + 1
    dentro = np.sort(h0[orden[:k]])
    return float(dentro[0]), float(dentro[-1]), float(k * dh)


def densidad_histograma(muestras: np.ndarray, h0: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Densidad de muestras: histograma de 1 km/s/Mpc sobre el rango de la grilla, suavizado con σ = 2 bins."""
    bordes = np.arange(h0[0], h0[-1] + 1e-9, 1.0)
    cuentas, _ = np.histogram(muestras, bins=bordes, density=True)
    return (bordes[1:] + bordes[:-1]) / 2, gaussian_filter1d(cuentas, 2)


def distancia_ks(h0: np.ndarray, p: np.ndarray, muestras: np.ndarray) -> float:
    """Máxima |CDF de p sobre la grilla − CDF empírica de las muestras|, evaluada en los puntos de la grilla."""
    cdf = np.concatenate([[0.0], np.cumsum((p[1:] + p[:-1]) / 2 * np.diff(h0))])
    cdf /= cdf[-1]
    empirica = np.searchsorted(np.sort(muestras), h0, side="right") / muestras.size
    return float(np.max(np.abs(cdf - empirica)))


def chequeos(h0: np.ndarray, p: np.ndarray, muestras: np.ndarray) -> dict:
    """Los tres números de la tolerancia y si cada uno cae dentro. Si el control pasa lo decide un humano."""
    mapa = map_grilla(h0, p)
    lo, hi, medida = hpd_grilla(h0, p)
    ks = distancia_ks(h0, p, muestras)
    return {
        "map": mapa,
        "hpd": [lo, hi],
        "hpd_medida": medida,
        "ks": ks,
        "map_dentro": abs(mapa - MAP_PUBLICADO) <= TOL_MAP,
        "hpd_dentro": abs(lo - HPD_PUBLICADO[0]) <= TOL_BORDES and abs(hi - HPD_PUBLICADO[1]) <= TOL_BORDES,
        "ks_dentro": ks <= TOL_KS,
    }
