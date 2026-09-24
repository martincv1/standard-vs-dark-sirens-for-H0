"""Imprime la estructura de un HDF5: grupos, datasets, formas, dtypes y atributos.

Uso:  uv run python scripts/inspeccionar_hdf5.py [ruta]      (por defecto GW170817_GWTC-1.hdf5)

Solo describe lo que el archivo dice. Qué columna es D_L o iota, sus unidades y el prior
de PE se leen de esta salida y del paper, y se anotan en provenance/ con la cita.
"""

import sys
from pathlib import Path

import h5py

POR_DEFECTO = Path(__file__).resolve().parents[1] / "data" / "raw" / "GW170817_GWTC-1.hdf5"


def describir(nombre: str, obj) -> None:
    if isinstance(obj, h5py.Dataset):
        campos = f"  campos={obj.dtype.names}" if obj.dtype.names else ""
        print(f"[dataset] {nombre}  forma={obj.shape}  dtype={obj.dtype}{campos}")
    else:
        print(f"[grupo]   {nombre}")
    for k, v in obj.attrs.items():
        print(f"            @{k} = {v!r}")


def main() -> int:
    ruta = Path(sys.argv[1]) if len(sys.argv) > 1 else POR_DEFECTO
    if not ruta.exists():
        print(f"No existe {ruta}. Correr primero scripts/descargar_datos.py.", file=sys.stderr)
        return 1
    with h5py.File(ruta, "r") as f:
        print(f"Archivo: {ruta}")
        for k, v in f.attrs.items():
            print(f"  @{k} = {v!r}")
        f.visititems(describir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
