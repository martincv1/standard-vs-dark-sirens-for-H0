# Revisión pendiente del carril Datos (2026-09-25)

Para Modelo. Seis ramas de Datos encadenadas, cada una sale de la anterior. Conviene revisarlas y mergearlas **en este orden**; cada PR muestra solo lo nuevo si se apunta a la rama anterior, o todo junto si se apunta a `main`. Todo el código lo escribió el agente y lo supervisó Datos (Ulises). Con la última rama pasan 74 tests (`uv sync && uv run pytest`).

**Lo que más necesita tu ojo**, porque toca tu carril o tus decisiones:
1. Las decisiones de la reunión cero, que se tomaron sin vos (rama 1).
2. `src/sirenas/core/grilla.py`, que es tuyo y lo escribimos nosotros (rama 2).
3. El plan B de la validación, porque el punto de control del D5 es conjunto (rama 2).
4. Las dos convenciones de Datos en `core/`: detección y formato de resultado (ramas 3 y 5).

---

## 1. `datos/reunion-cero`: decisiones de la reunión cero

La reunión cero no se hizo. Datos le delegó al agente todas las decisiones abiertas de `AGENTS.md` §19. Es una excepción a la regla, y quedó anotada en `spec.md` y en `AGENTS.md` §19.

- `spec.md` completo, más un archivo por decisión en `decisiones/2026-09-25-UC-*.md`: grilla y prior, modelo generativo de los sintéticos, métricas y regla de $N_{\rm eq}$, detección y selección, validación de GW170817, barrido provisional, y formato de resultados e informe.
- Los valores de GW170817 se copiaron de los Methods de Abbott et al. 2017, no de memoria.
- También trae la descarga de datos (`e2b0702`, que no estaba en `main`) y el catálogo uniforme en $z$.

**Para aprobar o cambiar, punto por punto.** Los supuestos que más conviene mirar:
- el horizonte de 190 Mpc tomado face-on para el umbral;
- `costheta_jn` usado como $\cos\iota$;
- barrer el ruido de amplitud ε y **medir** $\sigma_D/D_L$ en lugar de fijarlo;
- que la likelihood sintética no lleve $\pi(D_L)\propto D_L^2$, para que $N_{\rm gal}=1$ dé exactamente la brillante.

Los §6 (test sintético del reweighting) y §7 (predicción de $N_{\rm eq}$) son tuyos: el §6 es solo una propuesta y el §7 sigue en TODO.

## 2. `datos/validacion-gw170817`: grilla y experimento 2

- **`core/grilla.py` (tuyo):** $H_0\in[20, 250]$ con paso 0,1 y priors uniforme y $1/H_0$. Tests contra forma cerrada.
- **`data/gw170817.py`:** la ec. 9 de Abbott sobre las muestras `lowSpin`, con la integral en $v_p$ analítica (prior uniforme truncado). Está testeada contra cuadratura numérica y contra el límite de distancia fija ($H_0 = 3017/d_0$).
- **Resultado:** MAP 68,5 (dentro de la tolerancia); HPD [60,8; 86,7] y KS 0,085 (**fuera**). La tolerancia se fijó antes de comparar.
- **Diagnóstico:** las muestras de GWTC-1 tienen más peso a distancias chicas que las del paper de 2017. Es un diagnóstico, no algo demostrado.
- **Plan B** (`decisiones/2026-09-25-UC-plan-b-validacion-gw170817.md`): se reporta como reproducción aproximada, sin cambiar el dataset ni la tolerancia. **Necesita tu aprobación.**
- **MAP, HPD y KS de la validación** están en `data/comparacion.py`. Cuando publiques las métricas en `core/`, se pasa a importar las tuyas.

## 3. `datos/deteccion`: regla de detección y α(H0)

- **`core/deteccion.py`:** `detectado(a_obs)` con umbral $1/(190\ \text{Mpc})$, y `alfa(h0, ...)` como integral doble en $(v, \cos\iota)$.
- **$A(\iota)$ entra como argumento** para no duplicar la tuya. Cuando publiques $\mathcal L_{\rm GW}$, se le pasa la de `core/`.
- **Tests:** forma cerrada con $\sigma_a\to 0$, **simulación directa del proceso generativo** para los tres ε, convergencia y monotonía.
- **$\alpha$ depende mucho de $H_0$:** con ε = 0,30 vale 0,47 en $H_0=20$ y 0,89 en $H_0=70$. Calcularla en toda la grilla tarda unos 21 s por ε.

## 4. `datos/procedencia`: verificación de los datos crudos

- Las URLs oficiales (`dcc.ligo.org`, `gwosc.org`) no responden desde nuestra red. Como control parcial, `scripts/verificar_espejos.py` compara nuestros archivos con todas las capturas de la Wayback Machine:
  - **HDF5:** dos capturas completas (2024 y 2025) coinciden. La de 2022 está truncada en 1 MiB, con prefijo idéntico y el mismo tamaño declarado.
  - **Notebook:** coincide una captura completa. La de 2022 está truncada igual.
  - **`Figure1.csv`:** tiene una sola captura, pero su contenido reproduce el MAP y el HPD publicados.
- Datos confirmó el prior de PE ($d^2$ y $\cos\theta_{JN}$ uniforme).
- Sigue pendiente comparar con el archivo oficial: hay que correr el script cuando el DCC responda.

## 5. `datos/resultado`: formato de resultado (convención de Datos)

- **`core/resultado.py`:** `procedencia`, `guardar_celda` y `leer_celda`, con `likelihoods.npz` + `procedencia.json` por celda.
- **Validación al guardar y al leer:** forma, normalización de cada $L$, valores finitos y no negativos, campos y claves completos. Una celda existente no se sobrescribe si no se pide.
- **Cambio de convención** (`decisiones/2026-09-25-UC-n-descartados.md`): `detectado` se reemplaza por `n_descartados`. Como el modelo generativo sortea hasta detectar, `detectado` era siempre `True`. La fracción aceptada estima $\alpha(H_0^{\rm true})$ y sirve de control contra `alfa`. **Necesita tu aprobación.**

## 6. `datos/catalogo-host`: catálogo con el host verdadero

- **`catalogo_con_host`:** el host más $N_{\rm gal}-1$ galaxias uniformes en $z$, barajadas, con `indice_host`. Con $N_{\rm gal}=1$ es solo el host.
- **Tests:** ese límite, uniformidad de las demás galaxias, posición del host uniforme entre índices, y reproducibilidad.
- **Pregunta abierta:** ¿quién sortea $v_{\rm obs}\sim\mathcal N(v,\sigma_v)$ (paso 5 de §3)? El catálogo guarda redshifts verdaderos. Nuestra propuesta: el generador de eventos, con la semilla de cada realización.

---

## Qué necesitamos de vos, además de la revisión

- **$\mathcal L_{\rm GW}$ y $A(\iota)$ en `core/`.** Destraban el reweighting general, `alfa` con tu $A(\iota)$, el test cruzado $N_{\rm gal}=1$ → bright y el test de que todos los escenarios usan `detectado`.
- **El test sintético del reweighting (§6) especificado por vos.** Una aclaración honesta: `AGENTS.md` §9 pedía que ese test pasara *antes* de tocar GW170817, y lo hicimos al revés. Con pesos $d^2/d^2 = 1$ el resultado no cambia, pero el control quedó fuera de orden.
- **La predicción de $N_{\rm eq}$ commiteada antes del barrido (§7).**
