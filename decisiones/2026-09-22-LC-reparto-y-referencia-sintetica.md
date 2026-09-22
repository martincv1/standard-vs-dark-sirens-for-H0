# Decisión: reparto por perfil y referencia sintética

- **Decisión:**
  1. El equipo se reparte por perfil — **Modelo** (likelihoods, mezcla, métricas, predicción) y **Datos** (datos reales, reweighting, catálogos, selección, ejecución, reproducibilidad) — en lugar de "A brillante / B oscura".
  2. La sirena brillante de referencia usada para calcular $N_{\rm eq}$ es **sintética**, con parámetros tipo GW170817. GW170817 real se usa únicamente para **validar** el pipeline bright, no como referencia de $N_{\rm eq}$.
  3. Los eventos sintéticos se recortan a un plan de **diez días** a tiempo parcial.

- **Alternativas consideradas:**
  1. Reparto por A brillante / B oscura: se descartó porque separa el trabajo por tipo de sirena en vez de por la habilidad de cada integrante (relatividad/cosmología vs. astrofísica/datos), generando dependencias cruzadas innecesarias durante los diez días.
  2. Usar GW170817 real como referencia directa de $N_{\rm eq}$: se descartó porque el reweighting y la comparación con `Figure1.csv` pueden no cerrar en el plazo (D5), y eso pondría en riesgo el resultado principal del proyecto.

- **Por qué:**
  - El reparto por perfil (AGENTS.md §13) aprovecha el bagaje de cada integrante: Modelo viene de relatividad general y cosmología; Datos, de astrofísica y manejo de datos.
  - La referencia sintética (AGENTS.md §7) hace que el resultado principal no dependa de que el reweighting real cierre a tiempo: "Si el reweighting no cierra en el punto de control del D5, el resultado principal sigue en pie."
  - El recorte a diez días (AGENTS.md §4) fija el alcance dentro/fuera declarado en la sección 4 de `AGENTS.md`, evitando ambigüedad sobre qué queda como trabajo futuro.

- **Quién la tomó / aprobó:** los dos integrantes (Modelo y Datos).

- **Afecta a:** el reparto de tareas y directorios (`src/sirenas/model/`, `src/sirenas/data/`, `src/sirenas/catalogs/`), el plan de diez días (`AGENTS.md` §14), y el experimento de validación con GW170817 (`AGENTS.md` §8, experimento 2).
