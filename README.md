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
gh repo clone <owner>/<nombre> && cd <nombre>
uv sync && uv run pytest
```

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
| D2 · Reunión cero y `spec.md` | ☐ |
| D5 · Punto de control (GW170817 contra la curva publicada) | ☐ |
| D7 · Resultados y configuración congelados | ☐ |
| D8 · Reproducción en entorno limpio y auditoría por agente sin contexto | ☐ |
| D10 · Presentación | ☐ |
