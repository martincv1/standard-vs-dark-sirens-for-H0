"""Carga las configs de configs/ y las expande en celdas con semilla (spec.md §2.5 y §5). Dueño: Datos.

Una config de experimento (barrido.yaml, piloto.yaml) apunta a generativo.yaml por nombre; al cargarla
se inserta el contenido. Cada celda es un dict autocontenido, pensado para guardarse tal cual en
procedencia["config"] (core/resultado.py).

Semillas: celda i → semilla_base + i, en orden (eps, después n_gal). Realizaciones de una celda →
SeedSequence(semilla_celda).spawn(n): la realización k no cambia si se agregan realizaciones.
"""

from itertools import product
from pathlib import Path

import numpy as np
import yaml

CONFIGS = Path(__file__).resolve().parents[3] / "configs"
CLAVES_GENERATIVO = ("h0_true", "v_min", "v_max", "sigma_v", "d_ref")
CLAVES_EXPERIMENTO = ("experimento", "estado", "generativo", "eps", "n_gal", "n_max", "realizaciones", "semilla_base")


def cargar(ruta: Path) -> dict:
    """Lee una config de experimento, le inserta el generativo y la valida."""
    ruta = Path(ruta)
    cfg = yaml.safe_load(ruta.read_text(encoding="utf-8"))
    faltan = [k for k in CLAVES_EXPERIMENTO if k not in cfg]
    if faltan:
        raise ValueError(f"{ruta.name}: faltan claves {faltan}")
    if isinstance(cfg["generativo"], str):
        cfg["generativo"] = yaml.safe_load((ruta.parent / cfg["generativo"]).read_text(encoding="utf-8"))
    validar(cfg)
    return cfg


def validar(cfg: dict) -> None:
    g = cfg["generativo"]
    faltan = [k for k in CLAVES_GENERATIVO if k not in g]
    if faltan:
        raise ValueError(f"generativo: faltan claves {faltan}")
    if not 0 < g["v_min"] < g["v_max"]:
        raise ValueError(f"se pide 0 < v_min < v_max, no {g['v_min']}, {g['v_max']}")
    if not (g["h0_true"] > 0 and g["sigma_v"] > 0 and g["d_ref"] > 0):
        raise ValueError("h0_true, sigma_v y d_ref tienen que ser positivos")
    for clave in ("eps", "n_gal"):
        valores = cfg[clave]
        if not valores or len(set(valores)) != len(valores):
            raise ValueError(f"{clave} tiene que ser una lista no vacía y sin repetidos: {valores}")
    if not all(e > 0 for e in cfg["eps"]):
        raise ValueError(f"eps tiene que ser positivo: {cfg['eps']}")
    if not all(isinstance(n, int) and n >= 1 for n in cfg["n_gal"]):
        raise ValueError(f"n_gal tiene que tener enteros >= 1: {cfg['n_gal']}")
    for clave in ("n_max", "realizaciones", "semilla_base"):
        if not (isinstance(cfg[clave], int) and cfg[clave] >= (0 if clave == "semilla_base" else 1)):
            raise ValueError(f"{clave} inválido: {cfg[clave]}")


def celdas(cfg: dict) -> list[dict]:
    """Una entrada por combinación (eps, n_gal), con nombre, índice y semilla."""
    salida = []
    for i, (eps, n_gal) in enumerate(product(cfg["eps"], cfg["n_gal"])):
        salida.append({
            "experimento": cfg["experimento"],
            "estado": cfg["estado"],
            "nombre": f"eps{eps:.2f}_ngal{n_gal}",
            "indice": i,
            "semilla": cfg["semilla_base"] + i,
            "eps": eps,
            "n_gal": n_gal,
            "n_max": cfg["n_max"],
            "realizaciones": cfg["realizaciones"],
            "generativo": dict(cfg["generativo"]),
        })
    return salida


def semillas_realizaciones(semilla_celda: int, n: int) -> list[np.random.SeedSequence]:
    """Semillas independientes para las n realizaciones de una celda."""
    return np.random.SeedSequence(semilla_celda).spawn(n)
