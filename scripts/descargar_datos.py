"""Baja los insumos externos a data/raw/ y deja su procedencia en provenance/.

Uso:  uv run python scripts/descargar_datos.py [--force]

- Si el archivo ya está en data/raw/, no se vuelve a bajar (salvo --force).
- Si ya hay un archivo de procedencia, su SHA-256 tiene que coincidir con el del
  archivo local o recién bajado. Si no, aborta: nunca se sobrescribe en silencio.
- Las secciones que hay que leer del archivo o del paper quedan como POR COMPLETAR;
  no se rellenan con supuestos.
"""

import argparse
import hashlib
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
RAW = RAIZ / "data" / "raw"
PROVENANCE = RAIZ / "provenance"

# url=None significa "todavía no verificada contra la página oficial": el script no corre.
# Las URLs directas se copian de la página de descarga, nunca de memoria.
# Las de abajo se copiaron el 2026-09-23 de copias archivadas en Wayback de las páginas
# oficiales (DCC P1800370-v5, DCC P1700296-v5 y el evento GW170817 v3 de GWOSC), porque
# gwosc.org y dcc.ligo.org no respondían.
# "espejo": copia del mismo archivo en Wayback (el "id_" pide los bytes originales, sin
# reescribir). Se usa solo si la URL oficial falla, y la procedencia registra cuál se usó.
ARCHIVOS = [
    {
        "nombre": "GW170817_GWTC-1.hdf5",
        "url": "https://dcc.ligo.org/public/0157/P1800370/005/GW170817_GWTC-1.hdf5",
        "espejo": "https://web.archive.org/web/20250920104736id_/https://dcc.ligo.org/public/0157/P1800370/005/GW170817_GWTC-1.hdf5",
        "pagina": "https://gwosc.org/eventapi/html/GWTC-1-confident/GW170817/v3/",
        "referencia": "GWTC-1, DCC LIGO-P1800370-v5 (waveform IMRPhenomPv2NRT_lowSpin_prior)",
    },
    {
        "nombre": "GWTC-1_sample_release.ipynb",
        "url": "https://dcc.ligo.org/public/0157/P1800370/005/GWTC-1_sample_release.ipynb",
        "espejo": "https://web.archive.org/web/20251010125426id_/https://dcc.ligo.org/public/0157/P1800370/005/GWTC-1_sample_release.ipynb",
        "pagina": "https://dcc.ligo.org/LIGO-P1800370/public",
        "referencia": "DCC LIGO-P1800370-v5; notebook oficial que documenta el contenido de los HDF5",
    },
    {
        "nombre": "Figure1.csv",
        "url": "https://dcc.ligo.org/public/0145/P1700296/005/Figure1.csv",
        "espejo": "https://web.archive.org/web/20231117133140id_/https://dcc.ligo.org/public/0145/P1700296/005/Figure1.csv",
        "pagina": "https://dcc.ligo.org/P1700296/public",
        "referencia": "DCC LIGO-P1700296-v5; Abbott et al. 2017, Nature 551, 85 (arXiv:1710.05835)",
    },
]


def sha256_de(ruta: Path) -> str:
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(1 << 20), b""):
            h.update(bloque)
    return h.hexdigest()


def sha256_registrado(ruta_prov: Path) -> str | None:
    """SHA-256 escrito en un archivo de procedencia previo, o None si no hay."""
    if not ruta_prov.exists():
        return None
    m = re.search(r"SHA-256:\*{0,2}\s*`([0-9a-f]{64})`", ruta_prov.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def bajar(url: str, destino: Path) -> None:
    parcial = destino.with_suffix(destino.suffix + ".part")
    with urllib.request.urlopen(url, timeout=60) as r, open(parcial, "wb") as f:
        while bloque := r.read(1 << 20):
            f.write(bloque)
    parcial.replace(destino)


def bajar_con_espejo(a: dict, destino: Path) -> str:
    """Baja de la URL oficial; si falla y hay espejo, del espejo. Devuelve la URL usada."""
    try:
        bajar(a["url"], destino)
        return a["url"]
    except OSError as e:
        if not a.get("espejo"):
            raise
        print(f"{a['nombre']}: la URL oficial falló ({e}); uso el espejo.", file=sys.stderr)
        bajar(a["espejo"], destino)
        return a["espejo"]


def escribir_procedencia(a: dict, ruta_prov: Path, sha: str, tamano: int, url_usada: str | None = None) -> None:
    fecha = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if url_usada is None:
        origen = "desconocido: el archivo ya estaba en data/raw/ cuando se escribió esta procedencia"
    elif url_usada == a["url"]:
        origen = "URL oficial"
    else:
        origen = (
            f"**espejo** ({url_usada}), porque la URL oficial no respondía. "
            "PENDIENTE: comparar el SHA-256 contra el archivo oficial cuando vuelva a estar accesible."
        )
    ruta_prov.write_text(
        f"""# Procedencia: {a['nombre']}

- **URL oficial:** {a['url']}
- **Bajado de:** {origen}
- **Página fuente:** {a['pagina']}
- **Referencia / DOI:** {a['referencia']}
- **Fecha de descarga:** {fecha}
- **SHA-256:** `{sha}`
- **Tamaño:** {tamano} bytes
- **Lo baja:** `scripts/descargar_datos.py`

## Columnas usadas y unidades
POR COMPLETAR (leer del archivo, ver `scripts/inspeccionar_hdf5.py`).

## Prior con que se generaron las muestras
POR COMPLETAR (leer del archivo y del paper; si no está documentado, decirlo, no suponerlo).

## Scripts que lo consumen
POR COMPLETAR.
""",
        encoding="utf-8",
    )


def main() -> int:
    # Imprime caracteres fuera de ASCII (∝, ±, tildes); una consola Windows en cp1252/cp437 no los codifica.
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--force", action="store_true", help="volver a bajar aunque ya exista")
    args = ap.parse_args()

    pendientes = [a["nombre"] for a in ARCHIVOS if a["url"] is None]
    if pendientes:
        print(f"Falta verificar la URL directa de: {', '.join(pendientes)}.", file=sys.stderr)
        print("Copiarla de la página fuente en ARCHIVOS y volver a correr.", file=sys.stderr)
        return 1

    RAW.mkdir(parents=True, exist_ok=True)
    PROVENANCE.mkdir(exist_ok=True)

    for a in ARCHIVOS:
        destino = RAW / a["nombre"]
        ruta_prov = PROVENANCE / (a["nombre"] + ".md")

        url_usada = None
        if destino.exists() and not args.force:
            print(f"{a['nombre']}: ya está en data/raw/, no se baja.")
        else:
            print(f"{a['nombre']}: bajando de {a['url']}")
            url_usada = bajar_con_espejo(a, destino)

        sha = sha256_de(destino)
        previo = sha256_registrado(ruta_prov)
        if previo is not None and previo != sha:
            print(
                f"{a['nombre']}: el SHA-256 cambió.\n  registrado: {previo}\n  actual:     {sha}\n"
                "Abortando. Decidir a mano cuál es el archivo correcto.",
                file=sys.stderr,
            )
            return 2
        if previo is None:
            escribir_procedencia(a, ruta_prov, sha, destino.stat().st_size, url_usada)
            print(f"{a['nombre']}: procedencia escrita en {ruta_prov.relative_to(RAIZ)}")
        print(f"{a['nombre']}: SHA-256 {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
