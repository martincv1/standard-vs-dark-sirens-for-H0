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
