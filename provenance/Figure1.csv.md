# Procedencia: Figure1.csv

- **URL oficial:** https://dcc.ligo.org/public/0145/P1700296/005/Figure1.csv
- **Bajado de:** **espejo** (https://web.archive.org/web/20231117133140id_/https://dcc.ligo.org/public/0145/P1700296/005/Figure1.csv), porque la URL oficial no respondía. PENDIENTE: comparar el SHA-256 contra el archivo oficial cuando vuelva a estar accesible.
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
