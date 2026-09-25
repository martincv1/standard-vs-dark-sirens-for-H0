# Sirenas oscuras y H₀: ¿cuánto vale identificar la galaxia anfitriona?

Proyecto final del curso *Investigación asistida por agentes de IA: aplicación a ondas gravitacionales*.

> **En un modelo controlado de eventos tipo GW170817, ¿cuántas sirenas oscuras hacen falta para aportar la misma información sobre la constante de Hubble que una sirena brillante, y cómo depende esa equivalencia de la incertidumbre en distancia y del número de galaxias anfitrionas candidatas?**

Construimos desde cero la likelihood cosmológica de una sirena estándar. La validamos contra el posterior publicado de GW170817 y medimos, con eventos sintéticos, cuántas sirenas oscuras equivalen a una brillante. El resultado vale dentro del modelo declarado: **no es una medición nueva de $H_0$**.

La implementación está delegada en agentes de IA. Los supervisamos con controles de respuesta conocida, y los errores que les detectamos quedan registrados en `validacion/registro_supervision.md`.

---

## Quién hace qué

| | **Modelo** | **Datos** |
|---|---|---|
| Perfil | Relatividad general, cosmología, cursos de GW | Astrofísica y manejo de datos |
| Es dueño de | Código compartido (`src/sirenas/core/`): grilla, prior, $\mathcal L_{\rm GW}$, métricas. Likelihoods sintéticas y mezcla oscura. Predicción de $N_{\rm eq}$. Diseño del barrido | GW170817 real: descarga, procedencia, prior de PE, reweighting y validación. Catálogos sintéticos y regla de detección. Ejecución del barrido. Configuración congelada. Reproducibilidad |
| Directorios | `src/sirenas/core/`, `src/sirenas/model/` | `src/sirenas/data/`, `src/sirenas/catalogs/`, `scripts/`, `provenance/`, `configs/` |
| Guía | [`docs/CARRIL_MODELO.md`](docs/CARRIL_MODELO.md) | [`docs/CARRIL_DATOS.md`](docs/CARRIL_DATOS.md) |

**Se divide el hacer, se comparte solo el decidir.** Las cinco convenciones compartidas, la aceptación de los controles del otro, las limitaciones y las conclusiones se deciden entre los dos. Un evento pasa de un carril al otro por una sola interfaz: `L_j(H0)` sobre la grilla compartida, más su procedencia. Detalle en [`AGENTS.md`](AGENTS.md) §11.

---

## Cómo empezar

```bash
git clone https://github.com/martincv1/standard-vs-dark-sirens-for-H0.git
cd standard-vs-dark-sirens-for-H0
uv sync && uv run pytest
```

Sin datos, los tests que leen `data/raw/` se saltean (aparecen como `skipped`).

> **Windows: cloná en una ruta corta** (por ejemplo `C:\Users\<vos>\Desktop\...`). Si la carpeta del repo es muy profunda y las rutas largas de Windows están desactivadas (`LongPathsEnabled = 0`), las DLL de `scipy` dentro de `.venv` superan los 260 caracteres y `pytest` falla al importar, con `ModuleNotFoundError: No module named 'scipy.linalg._cythonized_array_utils'`. Pasó en el ensayo de reproducción: `validacion/ensayo_reproduccion_2026-09-25.md`.

### Reproducir todo, en orden

```bash
uv run python scripts/descargar_datos.py     # 1. baja los insumos a data/raw/
uv run python scripts/verificar_prior_pe.py  # 2. prior de PE de GW170817 (spec.md §4)
uv run pytest                                # 3. todos los tests, ahora también los que usan data/raw/
uv run python scripts/validar_gw170817.py    # 4. experimento 2: GW170817 contra el paper
git diff --stat results figures              # 5. control de reproducción
```

1. **Descarga.** Si la URL oficial no responde, usa la copia archivada en la Wayback Machine y lo registra. Compara el SHA-256 de cada archivo con el de `provenance/` y **aborta si no coincide**. No se commitean datos crudos (`data/raw/` está en `.gitignore`).
2. **Prior de PE.** Imprime los tests KS que verifican el prior $d^2$ e isótropo. Los valores esperados están en `provenance/GW170817_GWTC-1.hdf5.md`.
3. **Tests.** Sin datos se saltean los que leen `data/raw/`; con datos corren todos.
4. **Validación.** Reescribe `results/validacion_gw170817/` y `figures/validacion_gw170817.*`, e imprime los tres criterios de tolerancia. El resultado esperado (fuera de tolerancia, plan B) está en `decisiones/2026-09-25-UC-plan-b-validacion-gw170817.md`.
5. **Control de reproducción.** En la máquina donde se generaron (Windows 10, con las versiones de `uv.lock`), `posterior.npz` y el `.png` salen **idénticos byte a byte** a los commiteados, y solo cambian los `.json` de procedencia (commit y fecha). En otra plataforma, el `.png` puede diferir en píxeles (fuentes) y el `.npz` en los últimos bits. Ahí el criterio es numérico: los tres números que imprime el paso 4 tienen que coincidir con los de `results/validacion_gw170817/procedencia.json` a la décima.

Opcional: `uv run python scripts/verificar_espejos.py` vuelve a comparar `data/raw/` contra la fuente oficial y contra las capturas de la Wayback Machine. `uv run python scripts/inspeccionar_hdf5.py` lista el contenido del HDF5.

Si no usás `uv`, ver la sección «Para el integrante Datos» de [`docs/SETUP_REPO.md`](docs/SETUP_REPO.md).

Después abrí tu agente dentro del repo y mandale el primer mensaje sugerido en la guía de tu carril.

**Qué leer:**

| Archivo | Para qué |
|---|---|
| [`docs/final-project.html`](docs/final-project.html) | Consignas y entregables del curso |
| [`AGENTS.md`](AGENTS.md) | Contexto completo; es lo que leen los agentes |
| [`docs/plan.html`](docs/plan.html) | Versión visual del plan, el reparto y la bibliografía (abrir en el navegador) |
| [`spec.md`](spec.md) | Convenciones y decisiones técnicas: la referencia para implementar |

---

## Flujo de trabajo

- Ramas `modelo/<tema>` y `datos/<tema>`. PRs chicos y diarios a `main`, revisados por el otro integrante.
- Un archivo por decisión en `decisiones/`.
- Cada error del agente va a `validacion/registro_supervision.md`.
- Los datos crudos no se commitean: se bajan con `scripts/` y su procedencia queda en `provenance/`.
- Sincronización diaria de 15 minutos: *¿qué decidiste y qué error del agente encontraste?*

## Estado

| Hito | Estado |
|---|---|
| D2 · Reunión cero y `spec.md` | ☑ sin reunión: decisiones en `spec.md` y `decisiones/`, pendientes de revisión de Modelo |
| D5 · Punto de control (GW170817 contra la curva publicada) | ☐ |
| D7 · Resultados y configuración congelados | ☐ |
| D8 · Reproducción en entorno limpio y auditoría por agente sin contexto | ☐ |
| D10 · Presentación | ☐ |
