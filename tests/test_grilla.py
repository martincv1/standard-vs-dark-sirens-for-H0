import numpy as np
import pytest

from sirenas.core.grilla import H0_MAX, H0_MIN, grilla_h0, normalizar, prior_inverso, prior_uniforme


def test_grilla_de_spec():
    # spec.md §2.1: [20, 250] con paso 0,1 → 2301 puntos.
    h0 = grilla_h0()
    assert h0.size == 2301
    assert h0[0] == H0_MIN == 20.0
    assert h0[-1] == H0_MAX == 250.0
    np.testing.assert_allclose(np.diff(h0), 0.1, rtol=1e-9)


def test_priors_integran_uno():
    h0 = grilla_h0()
    assert np.trapezoid(prior_uniforme(h0), h0) == pytest.approx(1.0, abs=1e-12)
    assert np.trapezoid(prior_inverso(h0), h0) == pytest.approx(1.0, abs=1e-12)


def test_prior_uniforme_vale_uno_sobre_el_ancho():
    h0 = grilla_h0()
    np.testing.assert_allclose(prior_uniforme(h0), 1 / 230)


def test_prior_inverso_contra_forma_cerrada():
    # Respuesta analítica: la normalización continua de 1/H0 en [a, b] es 1/ln(b/a).
    # El trapecio con paso 0,1 la aproxima con error relativo ~1e-6.
    h0 = grilla_h0()
    np.testing.assert_allclose(prior_inverso(h0), 1 / (h0 * np.log(250 / 20)), rtol=1e-5)


def test_normalizar_rechaza_integral_nula():
    h0 = grilla_h0()
    with pytest.raises(ValueError):
        normalizar(np.zeros_like(h0), h0)
