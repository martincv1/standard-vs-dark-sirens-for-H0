from pathlib import Path

import numpy as np
import pytest
from scipy import integrate, stats

from sirenas.core.grilla import grilla_h0, normalizar, prior_uniforme
from sirenas.data import gw170817 as g
from sirenas.data.comparacion import distancia_ks, hpd_grilla, map_grilla

HDF5 = Path(__file__).resolve().parents[1] / "data" / "raw" / "GW170817_GWTC-1.hdf5"


@pytest.mark.parametrize("x", [0.0, 1500.0, 3017.0, 3500.0, 4500.0, 9000.0])
def test_integral_en_vp_contra_cuadratura(x):
    # Respuesta esperada: la integral numérica directa del integrando de la ec. 9 en v_p.
    lo, hi = g.V_P_PRIOR

    def integrando(vp):
        return (stats.norm.pdf(g.V_R, vp + x, g.SIGMA_V_R) * stats.norm.pdf(g.V_P_MEDIDA, vp, g.SIGMA_V_P)
                / (hi - lo))

    # epsabs=0: con la tolerancia absoluta por defecto (1,5e-8) quad no resuelve valores de ~1e-24 (x = 4500).
    numerica, _ = integrate.quad(integrando, lo, hi, points=[g.V_R - x, g.V_P_MEDIDA], limit=200,
                                 epsabs=0, epsrel=1e-10)
    assert g.likelihood_velocidad(np.array(x)) == pytest.approx(numerica, rel=1e-6, abs=1e-30)


def test_lejos_del_borde_es_gaussiana_en_la_velocidad_de_hubble():
    # Sin truncamiento efectivo: N(V_R - x; <v_p>, sqrt(72² + 150²)) / 2000, con máximo en x = 3327 - 310 = 3017.
    # El truncamiento es despreciable si la media de la gaussiana en v_p, m = 0,8127·(V_R - x) + 58,05, queda
    # a más de 6τ (τ = 64,9) de ±1000, es decir x ∈ [2648, 4149]. Fuera de ahí, el prior de v_p recorta.
    x = np.linspace(2700, 4100, 1401)
    s = np.hypot(g.SIGMA_V_R, g.SIGMA_V_P)
    np.testing.assert_allclose(g.likelihood_velocidad(x), stats.norm.pdf(g.V_R - x, g.V_P_MEDIDA, s) / 2000,
                               rtol=1e-9)
    assert x[np.argmax(g.likelihood_velocidad(x))] == 3017.0


def test_distancia_fija_da_map_en_vh_sobre_d():
    # Límite: si todas las muestras valen d0 y el prior es uniforme, el MAP es 3017/d0 (a la resolución de la grilla).
    h0 = grilla_h0()
    d = np.full(50, 40.0)
    p = normalizar(g.likelihood_h0(h0, d, np.ones_like(d)) * prior_uniforme(h0), h0)
    assert map_grilla(h0, p) == pytest.approx(3017 / 40, abs=0.1)


def test_likelihood_invariante_al_orden_de_las_muestras_y_a_escalar_pesos():
    h0 = grilla_h0()
    rng = np.random.default_rng(0)
    d = rng.uniform(20, 60, 300)
    w = rng.uniform(0.5, 2, 300)
    base = g.likelihood_h0(h0, d, w)
    orden = rng.permutation(300)
    np.testing.assert_allclose(g.likelihood_h0(h0, d[orden], w[orden]), base, rtol=1e-12)
    np.testing.assert_allclose(g.likelihood_h0(h0, d, 7 * w), base, rtol=1e-12)


def test_reweighting_d2_sobre_d2_da_pesos_constantes():
    # Control de spec.md §4: dividir por π_PE ∝ d² y multiplicar por el p(d) ∝ d² del paper no cambia nada.
    d = np.array([10.0, 25.0, 40.0, 70.0])
    w = g.pesos_reweighting(d, lambda x: x**2, lambda x: x**2)
    np.testing.assert_allclose(w, 1.0)
    assert g.n_efectivo(w) == pytest.approx(4)


def test_n_efectivo_de_pesos_conocidos():
    assert g.n_efectivo(np.array([1.0, 1.0, 0.0, 0.0])) == pytest.approx(2)
    assert g.n_efectivo(np.array([1.0, 0.0, 0.0])) == pytest.approx(1)


def test_hpd_de_una_gaussiana():
    # Respuesta analítica: el HPD al 68,3 % de N(100, 10) es ≈ [90, 110], con medida ≈ 20.
    h0 = grilla_h0()
    p = normalizar(stats.norm.pdf(h0, 100, 10), h0)
    lo, hi, medida = hpd_grilla(h0, p)
    assert lo == pytest.approx(90, abs=0.2)
    assert hi == pytest.approx(110, abs=0.2)
    assert medida == pytest.approx(20, abs=0.3)


def test_hpd_bimodal_no_cuenta_el_valle():
    # Dos gaussianas iguales y separadas: la medida del HPD es ≈ 2 veces la de una sola, mucho menor que hi - lo.
    h0 = grilla_h0()
    p = normalizar(stats.norm.pdf(h0, 60, 3) + stats.norm.pdf(h0, 160, 3), h0)
    lo, hi, medida = hpd_grilla(h0, p)
    assert medida == pytest.approx(2 * 2 * 3, abs=0.3)
    assert hi - lo > 100


def test_distancia_ks():
    h0 = grilla_h0()
    p = normalizar(stats.norm.pdf(h0, 100, 10), h0)
    muestras = np.random.default_rng(1).normal(100, 10, 100_000)
    # Misma distribución: la KS típica es ~1/sqrt(n) ≈ 0,003.
    assert distancia_ks(h0, p, muestras) < 0.01
    # Corrida en 5 (medio σ): la KS analítica es 2Φ(0,25) − 1 ≈ 0,197.
    assert distancia_ks(h0, p, muestras + 5) == pytest.approx(0.197, abs=0.01)


@pytest.mark.skipif(not HDF5.exists(), reason="data/raw no está: correr scripts/descargar_datos.py")
def test_lectura_de_distancias_reales():
    # provenance/GW170817_GWTC-1.hdf5.md: 8078 muestras lowSpin, mediana 40,0 Mpc.
    d = g.leer_distancias(HDF5)
    assert d.size == 8078
    assert np.median(d) == pytest.approx(40.0, abs=0.05)
