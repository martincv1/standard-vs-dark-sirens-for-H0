import numpy as np
import pytest

from sirenas.catalogs.uniforme import VERSION_GENERADOR, catalogo_uniforme

Z_MIN, Z_MAX = 0.01, 0.05


def test_misma_semilla_mismo_catalogo():
    a = catalogo_uniforme(123, 50, Z_MIN, Z_MAX)
    b = catalogo_uniforme(123, 50, Z_MIN, Z_MAX)
    np.testing.assert_array_equal(a.z, b.z)


def test_semillas_distintas_catalogos_distintos():
    a = catalogo_uniforme(1, 50, Z_MIN, Z_MAX)
    b = catalogo_uniforme(2, 50, Z_MIN, Z_MAX)
    assert not np.array_equal(a.z, b.z)


def test_cantidad_y_rango():
    cat = catalogo_uniforme(0, 1000, Z_MIN, Z_MAX)
    assert cat.z.shape == (1000,)
    assert cat.z.min() >= Z_MIN
    assert cat.z.max() < Z_MAX


def test_una_sola_galaxia():
    assert catalogo_uniforme(0, 1, Z_MIN, Z_MAX).z.shape == (1,)


def test_media_y_varianza_de_una_uniforme():
    # Respuesta analítica: media (a+b)/2, varianza (b-a)^2/12. Tolerancia: 5 errores estándar.
    n = 200_000
    z = catalogo_uniforme(42, n, Z_MIN, Z_MAX).z
    media, var = (Z_MIN + Z_MAX) / 2, (Z_MAX - Z_MIN) ** 2 / 12
    assert abs(z.mean() - media) < 5 * np.sqrt(var / n)
    # Para una uniforme (curtosis 9/5): sd(s^2) = sigma^2 * sqrt(4 / (5 n)).
    assert abs(z.var() - var) < 5 * var * np.sqrt(4 / (5 * n))


def test_procedencia_registra_lo_necesario():
    cat = catalogo_uniforme(7, 10, Z_MIN, Z_MAX)
    p = cat.procedencia
    assert p["semilla"] == 7
    assert p["config"] == {"n_gal": 10, "z_min": Z_MIN, "z_max": Z_MAX, "distribucion": "uniforme en z"}
    assert p["version_generador"] == VERSION_GENERADOR


@pytest.mark.parametrize(
    "n_gal, z_min, z_max",
    [(0, Z_MIN, Z_MAX), (-3, Z_MIN, Z_MAX), (10, 0.05, 0.01), (10, 0.02, 0.02), (10, -0.1, 0.05)],
)
def test_entradas_invalidas_fallan(n_gal, z_min, z_max):
    with pytest.raises(ValueError):
        catalogo_uniforme(0, n_gal, z_min, z_max)


# --- catalogo_con_host (spec.md §3, paso 6) ---
from sirenas.catalogs.uniforme import catalogo_con_host  # noqa: E402

Z_HOST = 3017 / 299792.458  # la velocidad de Hubble de NGC 4993, solo como valor de prueba dentro del rango


def test_con_una_galaxia_es_solo_el_host():
    # Límite obligatorio: N_gal = 1 es el caso brillante.
    cat = catalogo_con_host(0, 1, Z_HOST, Z_MIN, Z_MAX)
    np.testing.assert_array_equal(cat.z, [Z_HOST])
    assert cat.indice_host == 0


@pytest.mark.parametrize("n_gal", [2, 3, 10, 100])
def test_el_host_esta_donde_dice_indice_host(n_gal):
    cat = catalogo_con_host(5, n_gal, Z_HOST, Z_MIN, Z_MAX)
    assert cat.z.shape == (n_gal,)
    assert cat.z[cat.indice_host] == Z_HOST
    assert np.all((cat.z >= Z_MIN) & (cat.z < Z_MAX))


def test_con_host_misma_semilla_mismo_catalogo():
    a = catalogo_con_host(9, 10, Z_HOST, Z_MIN, Z_MAX)
    b = catalogo_con_host(9, 10, Z_HOST, Z_MIN, Z_MAX)
    np.testing.assert_array_equal(a.z, b.z)
    assert a.indice_host == b.indice_host


def test_interlopers_son_uniformes():
    # Las N_gal - 1 galaxias que no son el host: media (a+b)/2 y varianza (b-a)^2/12, a 5 errores estándar.
    cat = catalogo_con_host(42, 200_001, Z_HOST, Z_MIN, Z_MAX)
    z = np.delete(cat.z, cat.indice_host)
    n = z.size
    media, var = (Z_MIN + Z_MAX) / 2, (Z_MAX - Z_MIN) ** 2 / 12
    assert abs(z.mean() - media) < 5 * np.sqrt(var / n)
    assert abs(z.var() - var) < 5 * var * np.sqrt(4 / (5 * n))


def test_posicion_del_host_es_uniforme():
    # Con N_gal = 5 y 20 000 semillas, cada posición recibe 1/5 de las veces; tolerancia de 5σ binomial.
    n_gal, n = 5, 20_000
    cuentas = np.bincount([catalogo_con_host(s, n_gal, Z_HOST, Z_MIN, Z_MAX).indice_host for s in range(n)],
                          minlength=n_gal)
    p = 1 / n_gal
    assert np.all(np.abs(cuentas - n * p) < 5 * np.sqrt(n * p * (1 - p)))


def test_con_host_procedencia():
    p = catalogo_con_host(7, 10, Z_HOST, Z_MIN, Z_MAX).procedencia
    assert p["semilla"] == 7
    assert p["config"]["z_host"] == Z_HOST and p["config"]["n_gal"] == 10
    assert p["version_generador"] == VERSION_GENERADOR


@pytest.mark.parametrize(
    "n_gal, z_host, z_min, z_max",
    [(0, Z_HOST, Z_MIN, Z_MAX), (5, Z_MAX, Z_MIN, Z_MAX), (5, 0.001, Z_MIN, Z_MAX), (5, Z_HOST, 0.05, 0.01)],
)
def test_con_host_entradas_invalidas_fallan(n_gal, z_host, z_min, z_max):
    with pytest.raises(ValueError):
        catalogo_con_host(0, n_gal, z_host, z_min, z_max)
