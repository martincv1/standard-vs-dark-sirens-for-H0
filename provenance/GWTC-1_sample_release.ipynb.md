# Procedencia: GWTC-1_sample_release.ipynb

- **URL oficial:** https://dcc.ligo.org/public/0157/P1800370/005/GWTC-1_sample_release.ipynb
- **Bajado de:** **espejo** (https://web.archive.org/web/20251010125426id_/https://dcc.ligo.org/public/0157/P1800370/005/GWTC-1_sample_release.ipynb), porque la URL oficial no respondía. Ver «Verificación del espejo» abajo.
- **Página fuente:** https://dcc.ligo.org/LIGO-P1800370/public
- **Referencia / DOI:** DCC LIGO-P1800370-v5; notebook oficial que documenta el contenido de los HDF5
- **Fecha de descarga:** 2026-09-24 01:44 UTC
- **SHA-256:** `c00155bab9672e6ba8ab1420b81b675276e371c33941928a0817db11fba2e436`
- **Tamaño:** 3156202 bytes
- **Lo baja:** `scripts/descargar_datos.py`

## Columnas usadas y unidades
No es un dato: es la documentación oficial del formato de los HDF5 de GWTC-1. De acá se copiaron las descripciones de columnas en `GW170817_GWTC-1.hdf5.md`.

## Prior con que se generaron las muestras
No aplica.

## Scripts que lo consumen
Ninguno: se lee a mano.
- `scripts/verificar_espejos.py` (verificación del espejo)

## Verificación del espejo (`scripts/verificar_espejos.py`, 2026-09-25)
- **URL oficial, 2026-09-25:** no responde desde nuestra red (timeout de conexión; `gwosc.org` tampoco, mientras que `zenodo.org` y `arxiv.org` sí). GWTC-1 no está publicado en Zenodo. **Sigue pendiente la comparación con el archivo oficial.**
- **Capturas de la Wayback Machine:** la de **2025-10-10** coincide con el archivo local (es de la que se bajó). La de **2022-09-26** no coincide, pero está **truncada**: tiene exactamente 1 MiB y su primer MiB es idéntico byte a byte al archivo local.
- **Conclusión provisoria:** no hay evidencia de que haya cambiado. Solo hay una captura completa, así que la verificación es más débil que la del HDF5.
