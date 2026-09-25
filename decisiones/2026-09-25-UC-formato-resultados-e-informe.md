# Decisión: formato de resultados en disco, e informe y slides

- **Decisión:**
  - Por celda: `likelihoods.npz` + `procedencia.json` (commit, dirty, semillas, config literal, versiones, fecha UTC).
  - Configs en YAML, en `configs/`.
  - Figuras solo por script, con un `.json` de procedencia al lado.
  - Entregables: `report/index.html` y `report/informe.pdf`, en castellano. Las slides salen de la misma página.
- **Alternativas consideradas:**
  1. HDF5 para los resultados: más pesado de inspeccionar, y `.gitignore` ya ignora `*.hdf5`.
  2. Quarto o LaTeX para el informe: suma una herramienta al entorno y le complica la reproducción a un agente sin contexto.
  3. Informe en inglés: el curso, el repo y el equipo trabajan en castellano.
- **Por qué:** `.npz` y `.json` se leen con numpy y con la biblioteca estándar, que ya están en el entorno. `docs/final-project.html` pide HTML + PDF en el repo, reproducibles por un agente.
- **Quién la tomó / aprobó:** la tomó el agente (Claude) el 2026-09-25, por pedido explícito de Datos (Ulises), porque la reunión cero no se hizo. **Pendiente de aprobación de Modelo en el PR de `datos/reunion-cero`.**
- **Afecta a:** `spec.md` §2.5 y §8, `results/`, `figures/`, `report/`.
