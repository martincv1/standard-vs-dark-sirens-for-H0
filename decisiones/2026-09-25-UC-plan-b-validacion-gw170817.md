# Decisión: plan B para la validación con GW170817

- **Decisión:** la validación con GW170817 (experimento 2) se reporta como **reproducción aproximada**, con la discrepancia documentada, y el proyecto sigue (plan B de `AGENTS.md` §14). No se cambia el dataset (`lowSpin`), ni la tolerancia, ni el análisis. El resultado principal ($N_{\rm eq}$) no depende de esta validación, porque la brillante de referencia es sintética (`decisiones/2026-09-22-LC-reparto-y-referencia-sintetica.md`).

- **Resultado que motiva la decisión** (`results/validacion_gw170817/procedencia.json`, generado en el commit `af39070` con el árbol limpio, y comparado contra la tolerancia de `spec.md` §4, fijada antes de comparar):

  | | Este trabajo | Publicado (Abbott et al. 2017) | Tolerancia | ¿Dentro? |
  |---|---|---|---|---|
  | MAP | 68,5 | 70,0 | ± 3 | sí |
  | HPD 68,3 % | [60,8; 86,7] | [62,0; 82,0] | ± 3 por borde | no (el borde superior se pasa por 1,7) |
  | KS contra `Figure1.csv` | 0,085 | — | ≤ 0,05 | no |
  | Media / desvío | 81,6 / 19,8 | 78 / 15 | (no es criterio) | — |

  En la figura (`figures/validacion_gw170817.png`) el flanco de $H_0$ bajo coincide, y la diferencia está en la cola de $H_0$ alto.

- **Causa más probable (diagnóstico, no demostrado):** las muestras de GWTC-1 no son las del paper de 2017. El HPD 68,3 % de $D_L$ de `lowSpin` es [34,4; 47,6] Mpc, contra $43{,}8^{+2{,}9}_{-6{,}9}$ = [36,9; 46,7] Mpc del paper. La cola más pesada hacia distancias chicas se traduce en una cola más pesada hacia $H_0$ alto ($H_0 \approx v_H/d$). El código está verificado por separado: la integral en $v_p$ contra cuadratura numérica, el límite de distancia fija contra $3017/d_0$, y MAP, HPD y KS contra formas cerradas (`tests/test_gw170817.py`).

- **Alternativas consideradas:**
  1. **Pasar a `highSpin`:** con esas muestras el HPD da [61,3; 80,7] (dentro), pero la KS da 0,063 (fuera). Además sería elegir los datos después de ver el resultado. Se descartó. El número queda registrado solo como diagnóstico de sensibilidad.
  2. **Aflojar la tolerancia:** se fijó antes de comparar justamente para evitar esto. Se descartó.
  3. **Buscar las muestras exactas del paper de 2017:** no están entre los insumos verificados (`AGENTS.md` §10), y conseguirlas y validarlas no entra en el plazo. Queda como trabajo futuro.

- **Cómo se reporta:** en el informe y en la slide de validación se muestran la figura, esta tabla y el diagnóstico de $D_L$, con el título «reproducción aproximada». Se dice explícitamente que dos de los tres criterios fijados de antemano no se cumplieron.

- **Quién la tomó / aprobó:** Datos (Ulises), el 2026-09-25; la redactó el agente. El punto de control del D5 es conjunto, así que **queda pendiente de aprobación de Modelo en el PR de `datos/validacion-gw170817`.**

- **Afecta a:** `spec.md` §4, experimento 2, informe y slides de validación. No afecta a los experimentos 1 y 3–6.
