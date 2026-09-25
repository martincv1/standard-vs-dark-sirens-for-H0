"""Formato de resultado y procedencia (spec.md §2.5). Convención de Datos en core/; revisa Modelo.

Una celda del barrido se guarda en results/<experimento>/<celda>/ como:
- likelihoods.npz: h0 (grilla), L [realización, evento, h0] y los campos por evento de CAMPOS_EVENTO,
  cada uno con forma [realización, evento];
- procedencia.json: origen, semilla, config, versión del generador, commit, dirty, versiones, fecha UTC.

Cada L[r, e, :] tiene que estar normalizada sobre h0 (trapecio). Se valida al guardar y al leer.
Una celda existente no se sobrescribe salvo que se pida explícitamente.
"""

import json
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import scipy

CAMPOS_EVENTO = ("a_obs", "cos_iota_true", "v_true", "detectado")  # spec.md §2.5
CLAVES_PROCEDENCIA = ("origen", "semilla", "config", "version_generador",
                      "git_commit", "git_dirty", "versiones", "fecha_utc")
TOL_NORMA = 1e-6
RAIZ = Path(__file__).resolve().parents[3]


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=RAIZ, capture_output=True, text=True).stdout.strip()


def procedencia(origen: str, semilla: int, config: dict, version_generador: str) -> dict:
    """Arma la procedencia de una celda. `config` es la config de la celda tal como se leyó del YAML."""
    json.dumps(config)  # falla acá, y no al guardar, si la config no es serializable
    return {
        "origen": origen,
        "semilla": semilla,
        "config": config,
        "version_generador": version_generador,
        "git_commit": _git("rev-parse", "HEAD"),
        "git_dirty": bool(_git("status", "--porcelain", "--untracked-files=no")),
        "versiones": {"python": platform.python_version(), "numpy": np.__version__, "scipy": scipy.__version__},
        "fecha_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def validar(h0: np.ndarray, L: np.ndarray, campos: dict, proc: dict) -> None:
    """Levanta ValueError si la celda no cumple el formato."""
    if L.ndim != 3 or L.shape[2] != h0.size:
        raise ValueError(f"L tiene que tener forma [realización, evento, {h0.size}], no {L.shape}")
    if not np.all(np.isfinite(L)) or np.any(L < 0):
        raise ValueError("L tiene valores negativos o no finitos")
    normas = np.trapezoid(L, h0, axis=2)
    if np.max(np.abs(normas - 1)) > TOL_NORMA:
        raise ValueError(f"L no está normalizada sobre h0: máx |∫L − 1| = {np.max(np.abs(normas - 1)):.2e}")
    faltan = [c for c in CAMPOS_EVENTO if c not in campos]
    if faltan:
        raise ValueError(f"faltan campos por evento: {faltan}")
    for c in CAMPOS_EVENTO:
        if np.shape(campos[c]) != L.shape[:2]:
            raise ValueError(f"el campo {c} tiene forma {np.shape(campos[c])}, se esperaba {L.shape[:2]}")
    faltan = [k for k in CLAVES_PROCEDENCIA if k not in proc]
    if faltan:
        raise ValueError(f"faltan claves de procedencia: {faltan}")


def guardar_celda(directorio: Path, h0: np.ndarray, L: np.ndarray, campos: dict, proc: dict,
                  sobrescribir: bool = False) -> None:
    directorio = Path(directorio)
    validar(h0, L, campos, proc)
    if (directorio / "likelihoods.npz").exists() and not sobrescribir:
        raise FileExistsError(f"{directorio} ya tiene resultados; pasar sobrescribir=True para reemplazarlos")
    directorio.mkdir(parents=True, exist_ok=True)
    np.savez(directorio / "likelihoods.npz", h0=h0, L=L, **{c: np.asarray(campos[c]) for c in CAMPOS_EVENTO})
    (directorio / "procedencia.json").write_text(json.dumps(proc, indent=2, ensure_ascii=False), encoding="utf-8")


def leer_celda(directorio: Path) -> tuple[np.ndarray, np.ndarray, dict, dict]:
    """Devuelve (h0, L, campos por evento, procedencia), validados."""
    directorio = Path(directorio)
    with np.load(directorio / "likelihoods.npz") as f:
        h0, L = f["h0"], f["L"]
        campos = {c: f[c] for c in CAMPOS_EVENTO if c in f}
    proc = json.loads((directorio / "procedencia.json").read_text(encoding="utf-8"))
    validar(h0, L, campos, proc)
    return h0, L, campos, proc
