import numpy as np
import pytest
import yaml

from sirenas.core.resultado import procedencia
from sirenas.data.configuracion import CONFIGS, cargar, celdas, semillas_realizaciones


def test_generativo_coincide_con_spec():
    # Respuesta esperada: spec.md §3.
    g = cargar(CONFIGS / "barrido.yaml")["generativo"]
    assert g == {"h0_true": 70.0, "v_min": 2000.0, "v_max": 4000.0, "sigma_v": 166.0, "d_ref": 40.0}
    # 166 = sqrt(150² + 72²) redondeado (Abbott et al. 2017, Methods).
    assert g["sigma_v"] == pytest.approx(np.hypot(150, 72), abs=0.5)


def test_barrido_coincide_con_spec():
    # Respuesta esperada: spec.md §5.
    cfg = cargar(CONFIGS / "barrido.yaml")
    assert cfg["eps"] == [0.03, 0.10, 0.30]
    assert cfg["n_gal"] == [3, 10, 100]
    assert cfg["n_max"] == 200 and cfg["realizaciones"] == 200 and cfg["semilla_base"] == 20260925


def test_celdas_del_barrido():
    c = celdas(cargar(CONFIGS / "barrido.yaml"))
    assert len(c) == 9
    assert [x["semilla"] for x in c] == list(range(20260925, 20260934))
    assert len({x["nombre"] for x in c}) == 9
    # Orden: eps primero, después n_gal.
    assert [(x["eps"], x["n_gal"]) for x in c[:4]] == [(0.03, 3), (0.03, 10), (0.03, 100), (0.10, 3)]
    assert c[0]["nombre"] == "eps0.03_ngal3"


def test_piloto_es_una_celda_del_barrido_con_semillas_propias():
    piloto = celdas(cargar(CONFIGS / "piloto.yaml"))
    barrido = celdas(cargar(CONFIGS / "barrido.yaml"))
    assert len(piloto) == 1
    assert (piloto[0]["eps"], piloto[0]["n_gal"]) in {(x["eps"], x["n_gal"]) for x in barrido}
    assert piloto[0]["generativo"] == barrido[0]["generativo"]
    assert piloto[0]["semilla"] not in {x["semilla"] for x in barrido}


def test_celda_se_puede_guardar_como_procedencia():
    # Cada celda va entera a procedencia["config"]: tiene que ser serializable.
    celda = celdas(cargar(CONFIGS / "barrido.yaml"))[4]
    assert procedencia("test", celda["semilla"], celda, "1")["config"] == celda


def test_semillas_realizaciones_reproducibles_e_independientes():
    a = [np.random.default_rng(s).random() for s in semillas_realizaciones(123, 10)]
    b = [np.random.default_rng(s).random() for s in semillas_realizaciones(123, 10)]
    assert a == b
    assert len(set(a)) == 10


def test_agregar_realizaciones_no_cambia_las_anteriores():
    # Si el piloto pide más realizaciones, las primeras tienen que dar lo mismo.
    pocas = [np.random.default_rng(s).random() for s in semillas_realizaciones(7, 5)]
    muchas = [np.random.default_rng(s).random() for s in semillas_realizaciones(7, 50)]
    assert muchas[:5] == pocas


@pytest.mark.parametrize("cambio", [
    {"eps": []}, {"eps": [0.1, 0.1]}, {"eps": [-0.1]}, {"n_gal": [0]}, {"n_gal": [2.5]},
    {"realizaciones": 0}, {"n_max": 0},
])
def test_config_invalida_falla(tmp_path, cambio):
    cfg = yaml.safe_load((CONFIGS / "barrido.yaml").read_text(encoding="utf-8"))
    cfg.update(cambio)
    (tmp_path / "generativo.yaml").write_text((CONFIGS / "generativo.yaml").read_text(encoding="utf-8"),
                                              encoding="utf-8")
    (tmp_path / "x.yaml").write_text(yaml.safe_dump(cfg), encoding="utf-8")
    with pytest.raises(ValueError):
        cargar(tmp_path / "x.yaml")


def test_generativo_invalido_falla(tmp_path):
    (tmp_path / "generativo.yaml").write_text("h0_true: 70.0\nv_min: 4000.0\nv_max: 2000.0\n"
                                              "sigma_v: 166.0\nd_ref: 40.0\n", encoding="utf-8")
    (tmp_path / "x.yaml").write_text((CONFIGS / "piloto.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    with pytest.raises(ValueError, match="v_min"):
        cargar(tmp_path / "x.yaml")
