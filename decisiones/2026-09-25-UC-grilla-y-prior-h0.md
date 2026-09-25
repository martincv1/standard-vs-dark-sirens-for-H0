# Decisión: grilla y prior de H0

- **Decisión:** grilla $H_0\in[20, 250]$ km/s/Mpc, con $\Delta H_0 = 0{,}1$ (2301 puntos) e integración por trapecio. Prior uniforme en todo el rango para los escenarios sintéticos; $1/H_0$ solo para la validación con GW170817. Convergencia: con $\Delta H_0=0{,}05$ y con rango $[10, 300]$ las métricas cambian menos del 1 %.
- **Alternativas consideradas:**
  1. Rango [50, 140], como la figura del paper: se descartó porque `Figure1.csv` tiene muestras hasta 221,5 y la comparación de CDF quedaría truncada.
  2. Prior $1/H_0$ también en los sintéticos: se descartó porque la pregunta es sobre información relativa, y con un prior uniforme $D_{\rm KL}$ se interpreta directamente (el test gaussiano analítico de `AGENTS.md` §6 es contra un prior uniforme).
  3. Grilla más gruesa ($\Delta=1$): con $\varepsilon=0{,}03$ el ancho de un pico brillante puede ser de pocos km/s/Mpc, y en 1D el costo de $\Delta=0{,}1$ es despreciable.
- **Por qué:** una sola grilla sirve para la validación y para los sintéticos, y cubre todo el soporte relevante.
- **Quién la tomó / aprobó:** la tomó el agente (Claude) el 2026-09-25, por pedido explícito de Datos (Ulises), porque la reunión cero no se hizo. **Pendiente de aprobación de Modelo en el PR de `datos/reunion-cero`.**
- **Afecta a:** `spec.md` §2.1, `src/sirenas/core/`, todos los experimentos.
