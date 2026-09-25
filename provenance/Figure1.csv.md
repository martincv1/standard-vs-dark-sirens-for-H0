# Procedencia: Figure1.csv

- **URL oficial:** https://dcc.ligo.org/public/0145/P1700296/005/Figure1.csv
- **Bajado de:** **espejo** (https://web.archive.org/web/20231117133140id_/https://dcc.ligo.org/public/0145/P1700296/005/Figure1.csv), porque la URL oficial no respondía. Ver «Verificación del espejo» abajo.
- **Página fuente:** https://dcc.ligo.org/P1700296/public
- **Referencia / DOI:** DCC LIGO-P1700296-v5; Abbott et al. 2017, Nature 551, 85 (arXiv:1710.05835)
- **Fecha de descarga:** 2026-09-24 01:45 UTC
- **SHA-256:** `d1901efa8c4a76b5045e86c19be208f6f0a94256ee9b5c6423908fe5de3c77d2`
- **Tamaño:** 3276811 bytes
- **Lo baja:** `scripts/descargar_datos.py`

## Columnas usadas y unidades
**No es una curva: son muestras.** Una sola columna, `H0_samples`, con 131072 muestras del posterior de $H_0$. Las unidades no están en el archivo; se asumen km s⁻¹ Mpc⁻¹, como en la figura del paper.
Resumen (`scripts/verificar_prior_pe.py`): rango [48,4; 221,5], mediana 73,9, 16–84 % [66,1; 89,7].
La mediana no es el MAP publicado (70,0), porque el posterior es asimétrico. Para comparar el MAP y el intervalo mínimo al 68,3 % hay que estimar la densidad (histograma o KDE): **decisión pendiente**.

## Prior con que se generaron las muestras
No aplica al archivo en sí. El análisis que lo produjo usa un prior $\propto 1/H_0$ (Abbott et al. 2017, Methods, después de la ec. 7).

## Scripts que lo consumen
- `scripts/verificar_prior_pe.py`
- `scripts/validar_gw170817.py` (experimento 2)
- `scripts/verificar_espejos.py` (verificación del espejo)

## Verificación del espejo (`scripts/verificar_espejos.py`, 2026-09-25)
- **URL oficial, 2026-09-25:** no responde desde nuestra red (timeout de conexión; `gwosc.org` tampoco, mientras que `zenodo.org` y `arxiv.org` sí). GWTC-1 no está publicado en Zenodo. **Sigue pendiente la comparación con el archivo oficial.**
- **Capturas de la Wayback Machine:** hay una sola (**2023-11-17**), que es de la que se bajó. No hay otra captura contra la cual compararla.
- **Contenido:** con estas muestras, el MAP y el HPD 68,3 % dan 69,5 y [62,5; 82,5] (histograma suavizado, `scripts/validar_gw170817.py`). Coinciden con el $70{,}0^{+12{,}0}_{-8{,}0}$ del texto de Abbott et al. 2017. Es un control independiente del contenido.
- **Conclusión provisoria:** el contenido reproduce lo publicado. Falta la comparación de bytes con la fuente oficial.
