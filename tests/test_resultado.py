import json
import re

import numpy as np
import pytest
from scipy import stats

from sirenas.core.grilla import grilla_h0, normalizar
from sirenas.core.resultado import (CAMPOS_EVENTO, CLAVES_PROCEDENCIA, guardar_celda, leer_celda,
                                    procedencia, validar)

R, E = 3, 4  # realizaciones, eventos


def celda():
    h0 = grilla_h0()
    rng = np.random.default_rng(0)
    L = np.stack([[normalizar(stats.norm.pdf(h0, rng.uniform(60, 80), 10), h0) for _ in range(E)] for _ in range(R)])
    campos = {"a_obs": rng.uniform(0.01, 0.03, (R, E)), "cos_iota_true": rng.uniform(-1, 1, (R, E)),
              "v_true": rng.uniform(2000, 4000, (R, E)), "detectado": np.ones((R, E), dtype=bool)}
    proc = procedencia("tests.test_resultado", 42, {"eps": 0.1, "n_gal": 10}, "1")
    return h0, L, campos, proc


def test_ida_y_vuelta_exacta(tmp_path):
    h0, L, campos, proc = celda()
    guardar_celda(tmp_path / "c", h0, L, campos, proc)
    h0b, Lb, camposb, procb = leer_celda(tmp_path / "c")
    np.testing.assert_array_equal(h0b, h0)
    np.testing.assert_array_equal(Lb, L)
    for c in CAMPOS_EVENTO:
        np.testing.assert_array_equal(camposb[c], campos[c])
    assert procb == proc


def test_procedencia_tiene_todo():
    proc = procedencia("x", 7, {"a": 1}, "2")
    assert set(CLAVES_PROCEDENCIA) <= set(proc)
    assert re.fullmatch(r"[0-9a-f]{40}", proc["git_commit"])
    assert isinstance(proc["git_dirty"], bool)
    assert proc["semilla"] == 7 and proc["config"] == {"a": 1} and proc["version_generador"] == "2"
    json.dumps(proc)


def test_config_no_serializable_falla_al_armar_la_procedencia():
    with pytest.raises(TypeError):
        procedencia("x", 0, {"arr": np.zeros(2)}, "1")


def test_no_sobrescribe_sin_pedirlo(tmp_path):
    h0, L, campos, proc = celda()
    guardar_celda(tmp_path / "c", h0, L, campos, proc)
    with pytest.raises(FileExistsError):
        guardar_celda(tmp_path / "c", h0, L, campos, proc)
    guardar_celda(tmp_path / "c", h0, 2 * L / 2, campos, proc, sobrescribir=True)


def test_rechaza_L_sin_normalizar():
    h0, L, campos, proc = celda()
    with pytest.raises(ValueError, match="normalizada"):
        validar(h0, 1.01 * L, campos, proc)


def test_rechaza_forma_de_L_equivocada():
    h0, L, campos, proc = celda()
    with pytest.raises(ValueError, match="forma"):
        validar(h0, L[0], campos, proc)
    with pytest.raises(ValueError, match="forma"):
        validar(h0[:-1], L, campos, proc)


@pytest.mark.parametrize("malo", [np.nan, -1e-3])
def test_rechaza_valores_invalidos(malo):
    h0, L, campos, proc = celda()
    L[0, 0, 100] = malo
    with pytest.raises(ValueError, match="negativos o no finitos"):
        validar(h0, L, campos, proc)


def test_rechaza_campos_faltantes_o_de_forma_equivocada():
    h0, L, campos, proc = celda()
    sin = {k: v for k, v in campos.items() if k != "v_true"}
    with pytest.raises(ValueError, match="faltan campos"):
        validar(h0, L, sin, proc)
    campos["a_obs"] = campos["a_obs"][:, :-1]
    with pytest.raises(ValueError, match="a_obs"):
        validar(h0, L, campos, proc)


def test_rechaza_procedencia_incompleta():
    h0, L, campos, proc = celda()
    del proc["git_commit"]
    with pytest.raises(ValueError, match="git_commit"):
        validar(h0, L, campos, proc)


def test_leer_valida_lo_que_hay_en_disco(tmp_path):
    # Si alguien edita el .npz a mano y rompe la normalización, leer_celda lo detecta.
    h0, L, campos, proc = celda()
    guardar_celda(tmp_path / "c", h0, L, campos, proc)
    np.savez(tmp_path / "c" / "likelihoods.npz", h0=h0, L=3 * L, **campos)
    with pytest.raises(ValueError, match="normalizada"):
        leer_celda(tmp_path / "c")
