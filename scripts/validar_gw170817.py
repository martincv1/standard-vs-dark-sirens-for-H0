"""Experimento 2: posterior de H0 de GW170817 contra Abbott et al. 2017 y Figure1.csv (spec.md §4).

Uso:  uv run python scripts/validar_gw170817.py

Escribe:
- results/validacion_gw170817/posterior.npz   (h0, posterior, likelihood)
- results/validacion_gw170817/procedencia.json (entradas con SHA-256, commit, versiones, chequeos)
- figures/validacion_gw170817.png y su .json de procedencia

Imprime los tres números de la tolerancia. Si el control pasa lo decide un humano, no este script.
"""

import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import scipy

from sirenas.core.grilla import grilla_h0, normalizar, prior_inverso
from sirenas.data import comparacion as c
from sirenas.data import gw170817 as g

RAIZ = Path(__file__).resolve().parents[1]
HDF5 = RAIZ / "data" / "raw" / "GW170817_GWTC-1.hdf5"
FIG1 = RAIZ / "data" / "raw" / "Figure1.csv"
SALIDA = RAIZ / "results" / "validacion_gw170817"
FIGURA = RAIZ / "figures" / "validacion_gw170817.png"


def sha256_de(ruta: Path) -> str:
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True).stdout.strip()


def main() -> int:
    d = g.leer_distancias(HDF5)
    # spec.md §4: p(d) del paper ∝ d² y π_PE ∝ d², así que los pesos son constantes (control, no atajo).
    w = g.pesos_reweighting(d, lambda x: x**2, lambda x: x**2)
    h0 = grilla_h0()
    L = g.likelihood_h0(h0, d, w)
    post = normalizar(L * prior_inverso(h0), h0)

    muestras = np.loadtxt(FIG1, skiprows=1)
    res = c.chequeos(h0, post, muestras)
    x_hist, p_hist = c.densidad_histograma(muestras, h0)
    lo_f, hi_f, _ = c.hpd_grilla(x_hist, p_hist)
    res["figure1_histograma"] = {"map": c.map_grilla(x_hist, p_hist), "hpd": [lo_f, hi_f]}
    res["n_muestras"] = int(d.size)
    res["n_efectivo"] = g.n_efectivo(w)
    res["media"] = float(np.trapezoid(h0 * post, h0))
    res["desvio"] = float(np.sqrt(np.trapezoid((h0 - res["media"]) ** 2 * post, h0)))

    SALIDA.mkdir(parents=True, exist_ok=True)
    np.savez(SALIDA / "posterior.npz", h0=h0, posterior=post, likelihood=L)
    procedencia = {
        "origen": "scripts/validar_gw170817.py",
        "entradas": {
            HDF5.name: {"sha256": sha256_de(HDF5), "dataset": g.DATASET, "columna": g.COLUMNA_D},
            FIG1.name: {"sha256": sha256_de(FIG1), "columna": "H0_samples"},
        },
        "constantes_abbott_2017": {"v_r": g.V_R, "sigma_v_r": g.SIGMA_V_R, "v_p": g.V_P_MEDIDA,
                                   "sigma_v_p": g.SIGMA_V_P, "prior_v_p": list(g.V_P_PRIOR),
                                   "prior_h0": "1/H0"},
        "tolerancia": {"map": [c.MAP_PUBLICADO, c.TOL_MAP], "hpd": [list(c.HPD_PUBLICADO), c.TOL_BORDES],
                       "ks": c.TOL_KS},
        "resultado": res,
        "git_commit": git("rev-parse", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "versiones": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    (SALIDA / "procedencia.json").write_text(json.dumps(procedencia, indent=2, ensure_ascii=False), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x_hist, p_hist, color="0.5", lw=2, label="Figure1.csv (Abbott et al. 2017), histograma suavizado")
    ax.plot(h0, post, color="C0", lw=1.5, label="Este trabajo (GWTC-1 lowSpin, ec. 9 de Abbott)")
    ax.axvspan(*res["hpd"], color="C0", alpha=0.15, label="HPD 68,3 % (este trabajo)")
    for b in c.HPD_PUBLICADO:
        ax.axvline(b, color="0.3", ls="--", lw=1)
    ax.set_xlim(40, 160)
    ax.set_xlabel(r"$H_0$ [km s$^{-1}$ Mpc$^{-1}$]")
    ax.set_ylabel("densidad posterior")
    ax.legend(fontsize=8)
    ax.set_title("Validación: posterior de $H_0$ de GW170817 (líneas: HPD publicado)", fontsize=10)
    fig.tight_layout()
    FIGURA.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURA, dpi=150)
    FIGURA.with_suffix(".json").write_text(json.dumps({
        "script": "scripts/validar_gw170817.py",
        "entradas": ["results/validacion_gw170817/posterior.npz", "data/raw/Figure1.csv"],
        "git_commit": procedencia["git_commit"], "git_dirty": procedencia["git_dirty"],
    }, indent=2), encoding="utf-8")

    print(f"Muestras: {d.size}, N_eff = {res['n_efectivo']:.0f}")
    print(f"MAP  = {res['map']:.1f}  (publicado {c.MAP_PUBLICADO} ± {c.TOL_MAP}) -> "
          f"{'dentro' if res['map_dentro'] else 'FUERA'}")
    print(f"HPD  = [{res['hpd'][0]:.1f}, {res['hpd'][1]:.1f}]  (publicado {list(c.HPD_PUBLICADO)} ± {c.TOL_BORDES}) -> "
          f"{'dentro' if res['hpd_dentro'] else 'FUERA'}")
    print(f"KS   = {res['ks']:.3f}  (tolerancia {c.TOL_KS}) -> {'dentro' if res['ks_dentro'] else 'FUERA'}")
    print(f"Media {res['media']:.1f}, desvío {res['desvio']:.1f}  (publicado: 78 y 15)")
    print(f"Figure1.csv por histograma: MAP {res['figure1_histograma']['map']:.1f}, "
          f"HPD [{lo_f:.1f}, {hi_f:.1f}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
