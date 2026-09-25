"""Los scripts tienen que correr en una consola Windows que no es UTF-8 (cp1252, cp437).

Motivo: scripts/verificar_prior_pe.py se caía con UnicodeEncodeError al imprimir «∝» en cp1252.
"""

import ast
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
SCRIPTS = sorted((RAIZ / "scripts").glob("*.py"))
HDF5 = RAIZ / "data" / "raw" / "GW170817_GWTC-1.hdf5"


def imprime_fuera_de_ascii(ruta: Path) -> bool:
    fuente = ruta.read_text(encoding="utf-8")
    for nodo in ast.walk(ast.parse(fuente)):
        if isinstance(nodo, ast.Call) and getattr(nodo.func, "id", None) == "print":
            if any(ord(c) > 127 for c in ast.get_source_segment(fuente, nodo)):
                return True
    return False


@pytest.mark.parametrize("ruta", SCRIPTS, ids=lambda p: p.name)
def test_si_imprime_fuera_de_ascii_reconfigura_stdout(ruta):
    # stdout y stderr: descargar_datos.py manda los avisos por stderr, y el ensayo de reproducción
    # (validacion/ensayo_reproduccion_2026-09-25.md) los mostró con las tildes rotas.
    if imprime_fuera_de_ascii(ruta):
        fuente = ruta.read_text(encoding="utf-8")
        assert 'sys.stdout.reconfigure(encoding="utf-8")' in fuente
        assert 'sys.stderr.reconfigure(encoding="utf-8")' in fuente


@pytest.mark.skipif(not HDF5.exists(), reason="data/raw no está: correr scripts/descargar_datos.py")
def test_verificar_prior_pe_corre_en_cp437():
    # Solo lee datos y no escribe nada, así que se puede correr entero en el test.
    entorno = {**os.environ, "PYTHONIOENCODING": "cp437", "PYTHONUTF8": "0"}
    r = subprocess.run([sys.executable, str(RAIZ / "scripts" / "verificar_prior_pe.py")],
                       capture_output=True, env=entorno, cwd=RAIZ)
    assert r.returncode == 0, r.stderr.decode("utf-8", "replace")
    assert "∝" in r.stdout.decode("utf-8")
