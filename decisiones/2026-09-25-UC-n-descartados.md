# Decisión: guardar n_descartados en lugar de detectado

- **Decisión:** en el formato de resultado (`spec.md` §2.5), el campo por evento `detectado` se reemplaza por `n_descartados`: un entero ≥ 0 con forma [realización, evento], que cuenta cuántos sorteos del modelo generativo no pasaron `detectado` antes de aceptar ese evento. El total por realización es la suma sobre eventos.

- **Por qué:** el modelo generativo (`spec.md` §3, paso 4) vuelve a sortear cada evento hasta que se detecta, así que todo evento guardado tiene `detectado = True` y el campo no aporta información. `n_descartados` sí la aporta: la fracción aceptada, $E / (E + \sum n_{\rm descartados})$, estima $\alpha(H_0^{\rm true})$ para esa celda, y se puede comparar con `alfa` de `core/deteccion.py` (con ε = 0,30 tiene que dar ≈ 0,89). Es un control de consistencia gratis entre la regla generativa y la normalización.

- **Alternativas consideradas:**
  1. Dejar `detectado`: es redundante, y un lector podría pensar que en el archivo hay eventos no detectados.
  2. Guardar también los eventos descartados completos (con su $a_{\rm obs}$, etc.): multiplica el tamaño de los resultados y no lo usa ningún análisis previsto.
  3. Un solo contador por realización: pierde el detalle por evento sin ahorrar nada relevante, y rompe la forma común [realización, evento] que se valida para todos los campos.

- **Quién la tomó / aprobó:** Datos (Ulises), el 2026-09-25; la redactó el agente. Es una convención compartida (autor Datos, revisor Modelo), así que **queda pendiente de aprobación de Modelo en el PR de `datos/resultado`.**

- **Afecta a:** `spec.md` §2.5 y §3, `src/sirenas/core/resultado.py`, `tests/test_resultado.py`, y todo generador de eventos sintéticos (tiene que contar los descartes).
