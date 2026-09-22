# Carril Modelo: guía día por día

> **Para el integrante Modelo y su agente.** Leé primero `AGENTS.md`. Si algo de esta guía contradice a `spec.md` o a `docs/final-project.html`, valen ellos.

---

## Tu rol en una frase

Sos el dueño del **modelo estadístico**:

- el código compartido (`src/sirenas/core/`: grilla y prior de $H_0$, $\mathcal L_{\rm GW}$, métricas, combinación);
- la likelihood bright sintética y la oscura como mezcla;
- la predicción de $N_{\rm eq}$;
- el diseño y la lectura del barrido.

Además inicializás el repositorio.

**Lo tuyo:** `src/sirenas/core/` (del que sos dueño, salvo la regla de detección y el formato de resultado, que escribe Datos y revisás vos), `src/sirenas/model/`, tus derivaciones en `notes/` y tus tests.
**Lo que no tocás** sin avisarle a Datos: `src/sirenas/data/`, `src/sirenas/catalogs/`, `scripts/`, `provenance/` y la configuración congelada.

---

## Tu punto débil y cómo se compensa

Conocés los conceptos pero nunca armaste una likelihood desde cero. El agente te la escribe sin problema. El riesgo es otro: que no puedas darte cuenta cuando la escribe mal. Por eso:

1. **La respuesta esperada la escribís vos, el código lo escribe el agente.** Empezás por el toy de la derivación 4: lo derivás en papel, anotás el resultado cerrado, y recién ahí el agente lo implementa con un test contra esa fórmula.
2. **Esa pieza la leés línea por línea.** Es corta, y todas las likelihoods que vienen después son variaciones de ella.
3. **Antes de cada likelihood nueva, un bosquejo en papel:** dónde cae el pico, qué ancho tiene, si es unimodal.
4. **Escribís la especificación del test sintético del reweighting de Datos.** Es inferencia pura aplicada a un problema ajeno.

---

## Primer mensaje sugerido a tu agente

> Leé `AGENTS.md` completo, después `docs/CARRIL_MODELO.md` y `docs/final-project.html`. Soy el integrante **Modelo**. Trabajá solo dentro de mi carril. Para cada pieza crítica, pedime la respuesta esperada antes de implementar, escribí código corto y legible porque lo voy a leer línea por línea, y explicámelo en cinco líneas con la ecuación antes del merge. Resumime qué hacemos hoy (día D_).

---

## Tus piezas críticas

Estas se leen línea por línea y requieren la explicación de cinco líneas: grilla y prior de $H_0$; $\mathcal L_{\rm GW}$; la mezcla oscura; las métricas ($D_{\rm KL}$ e intervalos); la combinación de eventos.

---

## Día por día

### D1 · Crear el repo y leer

- **Repo (~1 h):** abrí tu agente en la carpeta con los archivos del kit y pedile:
  > Leé `docs/SETUP_REPO.md` y ejecutalo paso a paso. Frená antes de cada paso que cree algo en GitHub y mostrame qué vas a hacer.
- **Lecturas de la reunión cero (~3 h):** Schutz 1986; el cuerpo de Abbott et al. 2017; la intro y la ecuación de Fishbach et al. 2019; los fundamentos de Thrane & Talbot. Anotá lo que no entendiste.

### D2 · Reunión cero y `spec.md`

- **La reunión (con Datos, ~2 h):**
  - las seis decisiones;
  - las cinco convenciones: vos sos autor de la grilla y el prior, de $\mathcal L_{\rm GW}$ y de las métricas;
  - las decisiones abiertas mínimas de `AGENTS.md` §19;
  - media hora contando tu lectura, que incluye explicar la amplitud, la degeneración con la inclinación y la mezcla.
- **Después de la reunión**, pedile al agente que pase lo decidido a `spec.md` y abrí un PR. Lo revisan juntos.
- **Si te queda tiempo:** leé Fishbach completo y la parte de estimación de parámetros de Thrane & Talbot.

### D3 · Core y primera likelihood

1. **Derivación 4 en papel (completa).** Con $\iota$ fija y $v_{\rm pec}$ gaussiana, la marginalización bright da una gaussiana en $H_0$. Escribí su media y su ancho en `notes/`.
2. **Core con el agente.**
   - *Criterio de aceptación:* grilla, prior, $\mathcal L_{\rm GW}$ y métricas en `src/sirenas/core/`. El toy numérico coincide con la fórmula cerrada dentro de una tolerancia que vos fijaste. La $D_{\rm KL}$ gaussiana numérica coincide con la analítica. Existe el test de que hay un único $\mathcal L_{\rm GW}$.
   - *Pedido al agente:*
     > Implementá en `src/sirenas/core/` la grilla y el prior de $H_0$, $\mathcal L_{\rm GW}(D_L,\iota)$ y las métricas según `spec.md`. Después el toy de la derivación 4, con un test contra esta fórmula cerrada: [pegar la fórmula]. Código corto y sin abstracciones. Antes del merge, explicame cada función en cinco líneas con su ecuación.
3. **Leé el toy línea por línea.**
4. **Especificá el test sintético del reweighting** para Datos. Qué prior conocido, qué likelihood inyectada, qué tiene que devolver y con qué tolerancia. Va en un issue o en `decisiones/`.

### D4 · Likelihoods sintéticas y predicción

- **Bright sintética y mezcla dark.** Antes de pedírselas al agente, bosquejá en papel cómo esperás que se vean.
  - *Criterio de aceptación:* los tests de normalización y de recuperación del $H_0$ inyectado pasan. La mezcla usa el mismo $\mathcal L_{\rm GW}$ del core.
- **Derivación 6 (completa):** los picos de la mezcla y por qué el ancho deja de medir información.
- **Derivación 9 (completa): la predicción de $N_{\rm eq}$.** Con $\sigma\propto N^{-1/2}$ y $D_{\rm KL}$ gaussiana, estimá cómo debería escalar $N_{\rm eq}$ con $N_{\rm gal}$ y con $\sigma_D/D_L$. **Commitealo con fecha antes de cualquier barrido.** Referencia: Chen, Fishbach & Holz 2018.

### D5 · Combinación y métricas

- Producto de likelihoods de $N$ eventos, invariancia al orden y métricas sobre posteriors combinados.
- **Derivación 7 (completa):** $N_{\rm gal}=1$ lleva al caso bright. El test lo escribe Datos contra tu código.
- **Integración y punto de control** con Datos (ver `AGENTS.md` §14).
- **Notas cortas de las derivaciones 1, 2 y 3:** un párrafo cada una, con la referencia.

### D6 · Barrido

Cronometrá el piloto con Datos y fijá la grilla en `configs/`: del orden de 3 valores de $\sigma_D/D_L$ por 3 de $N_{\rm gal}$, con pocas semillas. Cuando salgan resultados, **comparalos primero con tu predicción**. Si no coinciden, decidí si es un bug o un resultado, y anotalo.

### D7 · Controles

Revisá y **aceptá o rechazá por escrito** los controles de Datos, nunca los tuyos. No se toca más la física.

### D8 · Reproducción y auditoría

Corré el pipeline de Datos en un clon limpio y explicáselo. Participá de la auditoría con el agente sin contexto.

### D9 · Presentación

Tus slides son la pregunta, el método (bright contra dark en una ecuación y la definición de información) y el resultado de $N_{\rm eq}$ contra la predicción. Con Datos armás el slide de supervisión del agente y el de limitaciones.

### D10 · Ensayo y presentación

---

## Reglas rápidas

- **Rama:** `modelo/<tema>`. PR diario a `main`, revisado por Datos.
- **Sos dueño de `src/sirenas/core/`.** Si Datos necesita algo de ahí, lo agregás vos o lo aprueban en un PR.
- **Nunca "arreglá el test".** Si un test falla, decidí primero quién está mal: el código, el test o la respuesta esperada.
- **Cada error del agente** va a `validacion/registro_supervision.md`. **Cada decisión** va a su propio archivo en `decisiones/`.
