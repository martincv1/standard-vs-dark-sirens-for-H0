import numpy as np
import pytest

from sirenas.core.deteccion import A_TH, alfa, detectado, prob_deteccion

# A(ι) de spec.md §2.2, escrita acá solo como entrada de test: la de producción es la de L_GW (Modelo).
def amplitud(c):
    return (1 + c**2) / 2


V_MIN, V_MAX = 2000.0, 4000.0  # spec.md §3
D_REF = 40.0


def test_umbral_de_spec():
    assert A_TH == pytest.approx(1 / 190)


def test_detectado_en_el_borde_y_vectorizado():
    assert detectado(A_TH)
    assert not detectado(np.nextafter(A_TH, 0))
    np.testing.assert_array_equal(detectado(np.array([0.0, A_TH, 1.0])), [False, True, True])


def test_prob_deteccion_limites():
    assert prob_deteccion(A_TH, 1e-3) == pytest.approx(0.5)
    assert prob_deteccion(A_TH + 10 * 1e-3, 1e-3) == pytest.approx(1.0, abs=1e-12)
    assert prob_deteccion(A_TH - 10 * 1e-3, 1e-3) == pytest.approx(0.0, abs=1e-12)


def test_alfa_sin_ruido_contra_forma_cerrada():
    # σ_a → 0: se detecta si v ≤ 190·A(ι)·H0. Con v ~ U[2000, 4000]:
    #   α(H0) = E_cosι[ clip((190·A·H0 − 2000)/2000, 0, 1) ],
    # que vale 1 para H0 ≥ 4000/(0,5·190) = 42,1. La esperanza en cosι se hace con 10⁶ puntos.
    h0 = np.array([25.0, 30.0, 35.0, 42.2, 70.0, 250.0])
    c = np.linspace(-1, 1, 1_000_001)
    esperado = [np.clip((190 * amplitud(c) * h - V_MIN) / (V_MAX - V_MIN), 0, 1).mean() for h in h0]
    # El escalón de σ_a → 0 es el peor caso del trapecio: tolerancia de discretización 5e-3.
    np.testing.assert_allclose(alfa(h0, 1e-9, amplitud, V_MIN, V_MAX, n_v=2001, n_cos=1001), esperado, atol=5e-3)
    np.testing.assert_allclose(alfa(h0[3:], 1e-9, amplitud, V_MIN, V_MAX), 1.0, atol=1e-12)


@pytest.mark.parametrize("eps", [0.03, 0.10, 0.30])
def test_alfa_contra_simulacion_del_proceso_generativo(eps):
    # Respuesta esperada: la fracción de eventos que pasan `detectado` al simular spec.md §3 paso a paso.
    sigma_a = eps / D_REF
    rng = np.random.default_rng(20260925)
    n = 400_000
    h0 = np.array([20.0, 30.0, 45.0, 70.0])
    esperado = []
    for h in h0:
        v = rng.uniform(V_MIN, V_MAX, n)
        c = rng.uniform(-1, 1, n)
        a_obs = rng.normal(amplitud(c) * h / v, sigma_a)
        esperado.append(detectado(a_obs).mean())
    esperado = np.array(esperado)
    tol = 5 * np.sqrt(esperado * (1 - esperado) / n) + 1e-4
    assert np.all(np.abs(alfa(h0, sigma_a, amplitud, V_MIN, V_MAX) - esperado) <= tol)


@pytest.mark.parametrize("eps", [0.03, 0.30])
def test_alfa_converge_con_la_resolucion(eps):
    h0 = np.array([20.0, 25.0, 30.0, 40.0, 70.0])
    base = alfa(h0, eps / D_REF, amplitud, V_MIN, V_MAX)
    fina = alfa(h0, eps / D_REF, amplitud, V_MIN, V_MAX, n_v=801, n_cos=401)
    np.testing.assert_allclose(base, fina, atol=1e-4)


def test_alfa_crece_con_h0_y_esta_en_cero_uno():
    # Más H0 ⇒ misma v a menor distancia ⇒ más amplitud ⇒ más detecciones.
    h0 = np.linspace(20, 250, 47)
    a = alfa(h0, 0.3 / D_REF, amplitud, V_MIN, V_MAX)
    assert np.all((a >= 0) & (a <= 1))
    assert np.all(np.diff(a) >= -1e-12)
