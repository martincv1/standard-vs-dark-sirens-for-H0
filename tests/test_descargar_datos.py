import hashlib
import importlib.util
from pathlib import Path

RUTA = Path(__file__).resolve().parents[1] / "scripts" / "descargar_datos.py"
spec = importlib.util.spec_from_file_location("descargar_datos", RUTA)
dd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dd)

# SHA-256 de b"abc": vector de prueba estándar (FIPS 180-2), no calculado con nuestro código.
SHA_ABC = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_sha256_de_vector_conocido(tmp_path):
    f = tmp_path / "abc.bin"
    f.write_bytes(b"abc")
    assert dd.sha256_de(f) == SHA_ABC


def test_sha256_de_archivo_mas_grande_que_un_bloque(tmp_path):
    datos = b"x" * ((1 << 20) * 2 + 123)
    f = tmp_path / "grande.bin"
    f.write_bytes(datos)
    assert dd.sha256_de(f) == hashlib.sha256(datos).hexdigest()


def test_procedencia_se_lee_de_vuelta(tmp_path):
    a = {"nombre": "x.csv", "url": "https://ejemplo.org/x.csv", "pagina": "p", "referencia": "r"}
    prov = tmp_path / "x.csv.md"
    dd.escribir_procedencia(a, prov, SHA_ABC, 3)
    assert dd.sha256_registrado(prov) == SHA_ABC
    assert dd.sha256_registrado(tmp_path / "no_existe.md") is None


def test_el_script_no_corre_con_urls_sin_verificar(monkeypatch, capsys):
    monkeypatch.setattr(dd, "ARCHIVOS", [{"nombre": "a", "url": None, "pagina": "", "referencia": ""}])
    monkeypatch.setattr("sys.argv", ["descargar_datos.py"])
    assert dd.main() == 1


def test_si_la_oficial_falla_usa_el_espejo_y_lo_registra(monkeypatch, tmp_path):
    a = {"nombre": "x.csv", "url": "https://oficial/x", "espejo": "https://espejo/x", "pagina": "p", "referencia": "r"}
    pedidas = []

    def bajar_falso(url, destino):
        pedidas.append(url)
        if url == a["url"]:
            raise OSError("timeout")
        destino.write_bytes(b"abc")

    monkeypatch.setattr(dd, "bajar", bajar_falso)
    usada = dd.bajar_con_espejo(a, tmp_path / "x.csv")
    assert usada == a["espejo"]
    assert pedidas == [a["url"], a["espejo"]]

    prov = tmp_path / "x.csv.md"
    dd.escribir_procedencia(a, prov, SHA_ABC, 3, usada)
    texto = prov.read_text(encoding="utf-8")
    assert "espejo" in texto and "PENDIENTE" in texto


def test_sin_espejo_el_error_de_la_oficial_no_se_esconde(monkeypatch, tmp_path):
    a = {"nombre": "x.csv", "url": "https://oficial/x", "pagina": "p", "referencia": "r"}

    def bajar_falso(url, destino):
        raise OSError("timeout")

    monkeypatch.setattr(dd, "bajar", bajar_falso)
    import pytest
    with pytest.raises(OSError):
        dd.bajar_con_espejo(a, tmp_path / "x.csv")
