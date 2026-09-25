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
