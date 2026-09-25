# Decisión: umbral de detección y selección dentro del dominio

- **Decisión:** un evento se detecta si $a_{\rm obs}\ge 1/(190\ {\rm Mpc})$. La regla es igual en todos los escenarios y vive en una sola función, `detectado`. La selección **está dentro** del dominio: cada likelihood se divide por $\alpha(H_0)$, calculado con el mismo modelo generativo (`spec.md` §2.4).
- **Alternativas consideradas:**
  1. Umbral en SNR, $a_{\rm obs}/\sigma_a\ge 8$: depende de $\varepsilon$, así que la población cambiaría entre celdas del barrido y dejaría de ser «la misma regla». Además, con $\varepsilon = 0{,}3$ no se detectaría casi nada.
  2. Declarar la selección fuera de alcance: es posible, pero con $\varepsilon=0{,}3$ el umbral recorta una fracción no despreciable de los eventos edge-on lejanos, y $\alpha(H_0)$ es una integral 2D barata.
- **Por qué:** 190 Mpc es el horizonte BNS que cita Abbott et al. 2017 (Methods). Convertirlo en amplitud face-on es un **supuesto**, porque el horizonte suele definirse para orientación óptima. La regla es simple, está fijada en amplitud y se comparte entre bright y dark.
- **Quién la tomó / aprobó:** la tomó el agente (Claude) el 2026-09-25, por pedido explícito de Datos (Ulises), porque la reunión cero no se hizo. **Pendiente de aprobación de Modelo en el PR de `datos/reunion-cero`.**
- **Afecta a:** `spec.md` §2.4, `src/sirenas/core/`, derivación 8, todos los experimentos sintéticos.
