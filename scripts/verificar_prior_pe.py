"""Verifica empíricamente el prior de PE de GW170817 con las muestras de prior del propio HDF5.

Uso:  uv run python scripts/verificar_prior_pe.py

El notebook oficial (GWTC-1_sample_release.ipynb) documenta columnas y unidades, pero no la
forma del prior de distancia. El HDF5 trae un dataset con muestras del prior, así que se
contrasta contra las hipótesis p(D_L) ∝ D_L^k (k = 1, 2, 3) y cos(theta_jn) ~ U(-1, 1).

Límite del método: los bordes del prior se toman de min/max de las muestras, no del
archivo de configuración del análisis, que no está publicado acá.
"""

import sys
from pathlib import Path

import h5py
import numpy as np
from scipy import stats

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
HDF5 = RAW / "GW170817_GWTC-1.hdf5"
FIG1 = RAW / "Figure1.csv"
ANALISIS = "IMRPhenomPv2NRT_lowSpin"


def main() -> int:
    # Imprime caracteres fuera de ASCII (∝, ±, tildes); una consola Windows en cp1252/cp437 no los codifica.
    sys.stdout.reconfigure(encoding="utf-8")
    with h5py.File(HDF5, "r") as f:
        prior = f[f"{ANALISIS}_prior"][()]
        post = f[f"{ANALISIS}_posterior"][()]

    d = prior["luminosity_distance_Mpc"]
    lo, hi = d.min(), d.max()
    print(f"Análisis: {ANALISIS}")
    print(f"Prior D_L: n={d.size}, min={lo:.2f} Mpc, max={hi:.2f} Mpc")
    for k in (1, 2, 3):
        # Si p(d) ∝ d^k en [lo, hi], la CDF (d^(k+1) - lo^(k+1)) / (hi^(k+1) - lo^(k+1)) es U(0, 1).
        u = (d ** (k + 1) - lo ** (k + 1)) / (hi ** (k + 1) - lo ** (k + 1))
        print(f"  KS contra p(d) ∝ d^{k}: p-valor = {stats.kstest(u, 'uniform').pvalue:.3g}")
    ks = np.linspace(0, 4, 401)
    loglik = [k * np.log(d).sum() - d.size * np.log((hi ** (k + 1) - lo ** (k + 1)) / (k + 1)) for k in ks]
    print(f"  Exponente de máxima verosimilitud: k = {ks[int(np.argmax(loglik))]:.2f}")

    c = prior["costheta_jn"]
    p_c = stats.kstest((c + 1) / 2, "uniform").pvalue
    print(f"Prior cos(theta_jn): min={c.min():.3f}, max={c.max():.3f}, KS contra U(-1, 1): p = {p_c:.3g}")

    for nombre, a in (("prior", prior), ("posterior", post)):
        print(f"Cielo en el {nombre}: std(RA) = {a['right_ascension'].std():.1e} rad, "
              f"std(dec) = {a['declination'].std():.1e} rad")

    dp = post["luminosity_distance_Mpc"]
    q = np.percentile(dp, [16, 50, 84])
    print(f"Posterior D_L: n={dp.size}, mediana {q[1]:.1f} Mpc, 16-84 % [{q[0]:.1f}, {q[2]:.1f}]")

    h0 = np.loadtxt(FIG1, skiprows=1)
    qh = np.percentile(h0, [16, 50, 84])
    print(f"Figure1.csv: {h0.size} muestras de H0, rango [{h0.min():.1f}, {h0.max():.1f}], "
          f"mediana {qh[1]:.1f}, 16-84 % [{qh[0]:.1f}, {qh[2]:.1f}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
