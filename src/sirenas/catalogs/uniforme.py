"""Catálogo sintético 1D en z, con galaxias uniformes en z. Dueño: Datos.

Cada galaxia es un redshift z ~ U(z_min, z_max), sorteado de forma independiente.
El catálogo no lleva p_g(z) ni pesos w_g: esos los pone la mezcla oscura (Modelo).
"""

from dataclasses import dataclass, field

import numpy as np

VERSION_GENERADOR = "1"


@dataclass(frozen=True)
class Catalogo:
    z: np.ndarray
    procedencia: dict = field(default_factory=dict)
    indice_host: int | None = None  # posición del host verdadero en z; None si el catálogo no tiene host


def catalogo_uniforme(semilla: int, n_gal: int, z_min: float, z_max: float) -> Catalogo:
    """Devuelve n_gal redshifts uniformes en [z_min, z_max), reproducibles desde `semilla`."""
    if n_gal < 1:
        raise ValueError(f"n_gal tiene que ser >= 1, no {n_gal}")
    if not 0 <= z_min < z_max:
        raise ValueError(f"se pide 0 <= z_min < z_max, no z_min={z_min}, z_max={z_max}")

    rng = np.random.default_rng(semilla)
    z = rng.uniform(z_min, z_max, size=n_gal)

    procedencia = {
        "origen": "sirenas.catalogs.uniforme.catalogo_uniforme",
        "semilla": semilla,
        "config": {"n_gal": n_gal, "z_min": z_min, "z_max": z_max, "distribucion": "uniforme en z"},
        "version_generador": VERSION_GENERADOR,
        "numpy": np.__version__,
    }
    return Catalogo(z=z, procedencia=procedencia)


def catalogo_con_host(semilla: int, n_gal: int, z_host: float, z_min: float, z_max: float) -> Catalogo:
    """Catálogo de spec.md §3 (paso 6): el host verdadero más n_gal - 1 galaxias uniformes en [z_min, z_max), barajadas.

    Con n_gal = 1 el catálogo es solo el host: el caso brillante. `indice_host` dice dónde quedó el host.
    Los redshifts son los verdaderos; el ruido de medición y p_g(z) los pone quien usa el catálogo.
    """
    if n_gal < 1:
        raise ValueError(f"n_gal tiene que ser >= 1, no {n_gal}")
    if not 0 <= z_min < z_max:
        raise ValueError(f"se pide 0 <= z_min < z_max, no z_min={z_min}, z_max={z_max}")
    if not z_min <= z_host < z_max:
        raise ValueError(f"el host tiene que estar en [z_min, z_max): z_host={z_host}")

    rng = np.random.default_rng(semilla)
    z = np.concatenate([[z_host], rng.uniform(z_min, z_max, size=n_gal - 1)])
    orden = rng.permutation(n_gal)
    z = z[orden]
    indice_host = int(np.flatnonzero(orden == 0)[0])

    procedencia = {
        "origen": "sirenas.catalogs.uniforme.catalogo_con_host",
        "semilla": semilla,
        "config": {"n_gal": n_gal, "z_host": z_host, "z_min": z_min, "z_max": z_max,
                   "distribucion": "host + uniforme en z, barajado"},
        "version_generador": VERSION_GENERADOR,
        "numpy": np.__version__,
    }
    return Catalogo(z=z, procedencia=procedencia, indice_host=indice_host)
