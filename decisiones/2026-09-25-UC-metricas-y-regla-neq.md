# Decisión: nivel del intervalo y regla del cruce de N_eq

- **Decisión:**
  - Ancho = medida del conjunto HPD al 68,3 % (suma de tramos si es disjunto).
  - $D_{\rm KL}$ en nats.
  - $N_{\rm eq}$ = menor entero $N\in[1, 200]$ para el cual la mediana de la métrica oscura alcanza la mediana de la brillante de referencia. Se calcula uno por métrica.
  - Dispersión = percentiles 16–84 del $N_{\rm eq}$ por realización.
- **Alternativas consideradas:**
  1. 90 %: más sensible a las colas y a los bordes de la grilla.
  2. Intervalo simétrico (percentiles): con un posterior multimodal cuenta los valles como región creíble y sobreestima el ancho.
  3. Interpolar entre enteros: innecesario si se evalúan todos los $N$, que en 1D es barato.
- **Por qué:** el 68,3 % mínimo es la convención de Abbott et al. 2017, así que la validación y los sintéticos usan la misma métrica. El HPD disjunto es la versión del ancho que menos falla con multimodalidad (derivación 6), y de todos modos se reporta siempre junto con $D_{\rm KL}$.
- **Quién la tomó / aprobó:** la tomó el agente (Claude) el 2026-09-25, por pedido explícito de Datos (Ulises), porque la reunión cero no se hizo. **Pendiente de aprobación de Modelo en el PR de `datos/reunion-cero`.**
- **Afecta a:** `spec.md` §2.3, métricas en `src/sirenas/core/`, experimentos 3–6, figuras de $N_{\rm eq}$.
