# Ensayo de reproducción en entorno limpio (2026-09-25)

Ensayo anticipado del paso 2 del D8 (`AGENTS.md` §14): se clonó la rama `datos/reproducibilidad` desde GitHub en una carpeta nueva y se siguió el `README.md` al pie de la letra, sin usar nada de la copia de trabajo (ni `data/raw/`, ni `.venv`). Lo hizo el agente (Claude), a pedido de Datos (Ulises). **No reemplaza la auditoría por un agente sin contexto del D8**: el agente que ensayó conocía el repo.

Máquina: Windows 10 Pro 10.0.19045, Python 3.13, `uv` con las versiones de `uv.lock`. Red: `dcc.ligo.org` y `gwosc.org` no responden (timeout).

## Resultado por paso

| Paso | Resultado | Tiempo |
|---|---|---|
| `git clone` | OK | 4 s |
| `uv sync` | OK | 12–31 s |
| `uv run pytest` sin datos | **Falló en la primera ruta** (ver hallazgo 1). En una ruta corta: 93 OK, 2 salteados (los que leen `data/raw/`), como dice el README | 100 s (primera corrida, compila `.pyc`) |
| 1. `descargar_datos.py` | OK. Las URLs oficiales dan timeout y usa el espejo. Los tres SHA-256 coinciden con `provenance/`. Tildes rotas en los avisos (hallazgo 2) | 87 s |
| 2. `verificar_prior_pe.py` | OK. Los mismos p-valores que `provenance/GW170817_GWTC-1.hdf5.md` (0,277 para $d^2$; 0,314 para $\cos\theta_{JN}$) | < 5 s |
| 3. `uv run pytest` con datos | 95 OK | 14 s |
| 4. `validar_gw170817.py` | OK. MAP 68,5; HPD [60,8; 86,7]; KS 0,085: los mismos números que el resultado commiteado | 25 s |
| 5. `git diff` | `posterior.npz` y `.png` **idénticos byte a byte** a los commiteados. Solo cambian los `.json` de procedencia (commit y fecha), como se espera | — |

## Hallazgos

1. **Ruta larga en Windows (gravedad: alta para un agente sin contexto).** El primer clon se hizo en una carpeta temporal de 208 caracteres. `pytest` no llegó a correr: 3 errores de colección con `ModuleNotFoundError: No module named 'scipy.linalg._cythonized_array_utils'`. El archivo **sí estaba** en `.venv`, pero su ruta completa rondaba los 254 caracteres, con `LongPathsEnabled = 0`, y el cargador de DLL de Windows respeta el límite de 260. Se confirmó repitiendo el clon en `C:\Users\...\Desktop\Sirenas\ensayo-limpio\repo`, donde todo pasó. **Qué se hizo:** una advertencia en el `README` con el mensaje de error textual. No tiene arreglo desde el repo.
2. **Tildes rotas en stderr (gravedad: baja).** `descargar_datos.py` manda los avisos de fallback por stderr, que no estaba reconfigurado a UTF-8 («la URL oficial fall�»). **Qué se hizo:** los tres scripts reconfiguran también stderr, y el test estático de `tests/test_scripts_consola.py` lo exige.
3. **Orden de los mensajes de la descarga (gravedad: cosmética).** Los avisos por stderr aparecen antes de los «bajando de…» por stdout, porque stderr no tiene buffer. Confunde, pero no afecta el resultado. No se cambió.

## Qué no cubre este ensayo

- Otra plataforma (Linux o macOS): la reproducción byte a byte del `.png` y del `.npz` solo se verificó en Windows.
- La comparación con la fuente oficial de los datos (`dcc.ligo.org` no responde): ver `provenance/`.
- Los experimentos que todavía no existen (1 y 3–6).
