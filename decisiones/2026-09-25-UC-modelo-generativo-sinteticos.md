# Decisión: eventos sintéticos «tipo GW170817» y modelo de p_g

- **Decisión:**
  - $H_0^{\rm true}=70$.
  - $v_{\rm true}\sim\mathcal U[2000, 4000]$ km/s y $D_L = v/H_0^{\rm true}$.
  - $\cos\iota\sim\mathcal U[-1,1]$.
  - $\sigma_a=\varepsilon/(40\ {\rm Mpc})$, con $\varepsilon$ como parámetro de control; el $\sigma_D/D_L$ se **mide** y se reporta.
  - $\sigma_v = 166$ km/s (la incertidumbre total de GW170817).
  - $p_g$ gaussiano en velocidad.
  - Interlopers uniformes en $v$ (es decir, uniformes en $z$), en el mismo rango, con pesos iguales.
  - La likelihood brillante es la oscura con $N_{\rm gal}=1$.

  Detalle en `spec.md` §3.
- **Alternativas consideradas:**
  1. Todos los eventos a $D_L=40$ Mpc fijo: se descartó porque, combinado con un prior en distancia o en $z$ distinto del generativo, sesga el $H_0$ combinado a medida que crece $N$, y el experimento 1 fallaría por construcción.
  2. Usar $\pi(D_L)\propto D_L^2$ en la likelihood sintética (como Abbott): se descartó porque el catálogo ya es el prior sobre la posición del host; usar los dos es contar dos veces y rompe el límite $N_{\rm gal}=1$ → bright.
  3. Calibrar $\sigma_a$ para obtener un $\sigma_D/D_L$ exacto: exige iterar sobre realizaciones con inclinación aleatoria. Medir $\sigma_D/D_L$ es más simple y no pierde información.
- **Por qué:** el modelo generativo coincide exactamente con la likelihood, así que la recuperación del $H_0$ inyectado es un control con respuesta conocida (sin sesgo). El rango de $v$ contiene a NGC 4993 (3017 km/s, Abbott et al. 2017) y deja las distancias en «decenas de Mpc» (28,6–57,1).
- **Quién la tomó / aprobó:** la tomó el agente (Claude) el 2026-09-25, por pedido explícito de Datos (Ulises), porque la reunión cero no se hizo. **Pendiente de aprobación de Modelo en el PR de `datos/reunion-cero`.**
- **Afecta a:** `spec.md` §2.2 y §3, `src/sirenas/model/`, `src/sirenas/catalogs/`, experimentos 1 y 3–6.
