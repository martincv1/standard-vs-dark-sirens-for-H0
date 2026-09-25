# Decisión: barrido reducido (provisional hasta el piloto del D6) y semillas

- **Decisión:**
  - $\varepsilon\in\{0{,}03; 0{,}10; 0{,}30\}$ × $N_{\rm gal}\in\{3, 10, 100\}$.
  - $N=1..200$.
  - 200 realizaciones por celda.
  - `semilla_base = 20260925`; semilla de celda = base + índice; semillas de las realizaciones por `SeedSequence.spawn`.
- **Alternativas consideradas:**
  1. Barrer $\sigma_D/D_L$ directamente: ver la decisión del modelo generativo.
  2. $N_{\rm gal}$ hasta 1000: los picos tienen un ancho de ≈ $H_0\,\sigma_D/D_L$ ≈ 10 km/s/Mpc en un rango de ≈100, así que con 100 galaxias el catálogo ya es casi continuo.
  3. Menos realizaciones: para que la mediana y los percentiles 16–84 sean estables hacen falta del orden de 10².
- **Por qué:** 3×3 es lo que fija `AGENTS.md` §4, y los valores cubren el $\sigma_D/D_L$ real de GW170817 (0,18, medido en `lowSpin`). **Se confirma o se cambia después de cronometrar el piloto**; si cambia, va con una decisión nueva.
- **Quién la tomó / aprobó:** la tomó el agente (Claude) el 2026-09-25, por pedido explícito de Datos (Ulises), porque la reunión cero no se hizo. **Pendiente de aprobación de Modelo en el PR de `datos/reunion-cero`.**
- **Afecta a:** `spec.md` §5, `configs/`, experimentos 4–6.
