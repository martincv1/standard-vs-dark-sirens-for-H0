"""Verifica los archivos de data/raw/ contra la fuente oficial y contra las capturas de la Wayback Machine.

Uso:  uv run python scripts/verificar_espejos.py

1. Intenta bajar cada archivo de su URL oficial y compara el SHA-256 con el local.
2. Lista todas las capturas de la URL oficial en el índice CDX de la Wayback Machine y compara su
   digest (SHA-1 del contenido, en base32) con el SHA-1 del archivo local. Una captura que no coincide
   y cuyo tamaño bajado es exactamente 1 MiB suele ser una captura truncada: se informa, no se decide acá.

No modifica nada: solo imprime. Lo que se concluye se escribe a mano en provenance/.
"""

import base64
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
OFICIALES = {
    "GW170817_GWTC-1.hdf5": "https://dcc.ligo.org/public/0157/P1800370/005/GW170817_GWTC-1.hdf5",
    "GWTC-1_sample_release.ipynb": "https://dcc.ligo.org/public/0157/P1800370/005/GWTC-1_sample_release.ipynb",
    "Figure1.csv": "https://dcc.ligo.org/public/0145/P1700296/005/Figure1.csv",
}


def bajar(url: str, timeout: float = 60) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def main() -> int:
    for nombre, url in OFICIALES.items():
        datos = (RAW / nombre).read_bytes()
        sha256 = hashlib.sha256(datos).hexdigest()
        sha1_b32 = base64.b32encode(hashlib.sha1(datos).digest()).decode()
        print(f"== {nombre}\n   local: SHA-256 {sha256}, SHA-1(b32) {sha1_b32}, {len(datos)} bytes")

        try:
            oficial = bajar(url)
            igual = hashlib.sha256(oficial).hexdigest() == sha256
            print(f"   oficial: {'IGUAL' if igual else 'DISTINTO'} ({len(oficial)} bytes)")
        except Exception as e:  # la URL oficial puede no responder; se informa y se sigue
            print(f"   oficial: no se pudo bajar ({type(e).__name__}: {e})")

        cdx = f"https://web.archive.org/cdx/search/cdx?url={url.removeprefix('https://')}&output=json&fl=timestamp,statuscode,digest"
        try:
            filas = json.loads(bajar(cdx, timeout=90))[1:]
        except Exception as e:
            print(f"   CDX: no se pudo consultar ({type(e).__name__}: {e})")
            continue
        for ts, status, digest in filas:
            if status != "200":
                continue
            marca = "IGUAL" if digest == sha1_b32 else "distinto"
            print(f"   captura {ts}: {marca}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
