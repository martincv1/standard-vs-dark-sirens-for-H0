# AGENTS.md: contexto e instrucciones para agentes

> **Si sos un agente trabajando en este repositorio, leé este archivo entero antes de hacer cualquier cosa.** Las secciones que más limitan lo que podés hacer por tu cuenta son la 2 («Cómo trabajamos con vos»), la 12 («Reglas») y la 19 («Decisiones abiertas»).

Proyecto final del curso optativo *Investigación asistida por agentes de IA: aplicación a ondas gravitacionales*. El equipo tiene dos integrantes y **diez días a tiempo parcial**, y el cierre es una **presentación oral virtual de 10–15 minutos** sobre qué se hizo y hasta dónde se llegó. **El entregable principal es este repositorio.**

---

## 0. Mapa del repositorio y fuentes de verdad

| Archivo | Qué es |
|---|---|
| `docs/final-project.html` | **Consignas y entregables del profesor.** Leelo apenas empieces. Si contradice a este archivo, gana él. Si no está, avisale al usuario. |
| `AGENTS.md` (este) | Contexto completo: pregunta, método, alcance, reparto, reglas, plan. |
| `CLAUDE.md` | Importa este archivo para Claude Code. No se edita aparte. |
| `README.md` | Entrada para humanos: resumen, reparto y cómo empezar. |
| `docs/CARRIL_MODELO.md` | Guía día por día del integrante **Modelo**. |
| `docs/CARRIL_DATOS.md` | Guía día por día del integrante **Datos**. |
| `docs/SETUP_REPO.md` | Instrucciones de inicialización del repo (se usan una sola vez). |
| `docs/plan.html` | Versión visual del plan, la bibliografía y el reparto. Abrir en el navegador. |
| `spec.md` | Especificación técnica: convenciones compartidas, interfaz y decisiones de la reunión cero. **Es la referencia para implementar.** |
| `decisiones/` | Un archivo por decisión. |
| `validacion/registro_supervision.md` | Registro de errores del agente detectados por los humanos. |

**Orden de prioridad ante un conflicto:** lo que diga el usuario en la conversación > `docs/final-project.html` > `spec.md` > este archivo > las guías de carril.

---

## 1. Resumen en diez líneas

1. **Pregunta:** cuántas sirenas oscuras hacen falta para aportar la misma información sobre $H_0$ que una sirena brillante tipo GW170817, y cómo depende eso de $\sigma_D/D_L$ y de $N_{\rm gal}$.
2. **Método:** construir desde cero la likelihood cosmológica sobre una grilla 1D en $H_0$. Sin MCMC y sin reanalizar el strain.
3. **Brillante:** un host con redshift conocido. **Oscura:** una mezcla sobre galaxias candidatas.
4. **Información:** se mide con el ancho de un intervalo creíble fijo y con $D_{\rm KL}(\text{posterior}\,\|\,\text{prior})$.
5. $N_{\rm dark}^{\rm eq}$ es el menor $N$ para el cual la **mediana** sobre realizaciones alcanza la información de la brillante. También se reporta la dispersión.
6. **La brillante de referencia es sintética.** GW170817 real solo valida el pipeline bright.
7. **Validación:** reproducir el posterior publicado de $H_0$ de GW170817 con reweighting de las muestras públicas por el prior de PE.
8. **Reparto por perfil:** **Modelo** (likelihoods, mezcla, métricas, predicción) y **Datos** (datos reales, reweighting, catálogos, selección, ejecución, reproducibilidad).
9. **Forma de trabajo:** la implementación se delega en agentes. Los humanos supervisan escribiendo **respuestas esperadas** y controles con respuesta conocida (sección 2).
10. **Procedencia:** cada número y cada figura tiene procedencia registrada y al menos un control independiente.

---

## 2. Cómo trabajamos con vos (protocolo de supervisión)

Los integrantes **no son expertos en astronomía de ondas gravitacionales**. Uno viene de relatividad general y cosmología (hizo cursos de GW pero nunca aplicó esos conceptos ni construyó una likelihood desde cero). El otro viene de astrofísica y manejo de datos. Te van a delegar la mayor parte del código. **No pueden supervisarte por experiencia, así que te supervisan con controles.** Tu trabajo es que eso sea posible:

1. **Sin respuesta esperada no hay implementación.** Antes de implementar una pieza, preguntá qué debería dar (un número, una forma, un límite, un orden de magnitud) si el pedido no lo dice. Guardá esa respuesta junto al test, o en `decisiones/` si es una decisión.
2. **Todo número tiene un test contra algo conocido:** una fórmula analítica, un caso límite, la curva publicada o la predicción registrada. No entregues números que solo «parecen razonables».
3. **Piezas críticas:** la grilla y el prior de $H_0$, $\mathcal L_{\rm GW}$, la mezcla oscura, las métricas ($D_{\rm KL}$, intervalos), el reweighting y la regla de detección. Para cada una:
   - escribí código corto y legible, sin abstracciones innecesarias, porque un humano lo va a leer línea por línea;
   - antes de pedir el merge, **explicala en cinco líneas con la ecuación exacta que implementa**, usando la notación de `spec.md`;
   - marcá explícitamente cualquier supuesto que no esté en `spec.md`.
4. **Nunca modifiques un test para que pase.** Si un test falla, decí qué falla y proponé las tres hipótesis posibles (el código está mal, el test está mal, la respuesta esperada está mal). Decide el humano.
5. **Decí cuándo no estás seguro.** Si una convención física o un dato del paper lo estás suponiendo o recordando y no lo leíste de la fuente, decilo. Los valores numéricos del paper (velocidades, priors, intervalos) **se leen del paper o del archivo, nunca de memoria.**
6. **Registro de supervisión.** Cuando el humano detecte un error tuyo, agregá una entrada a `validacion/registro_supervision.md` con qué hiciste mal, cómo se detectó (control / lectura / intuición) y la gravedad. Es material de la presentación, así que no lo edulcores.
7. **Identificá con quién trabajás.** Si no está claro si es Modelo o Datos, preguntá, y leé `docs/CARRIL_MODELO.md` o `docs/CARRIL_DATOS.md`. Trabajá solo dentro de ese carril (sección 12).

---

## 3. La pregunta, término por término

> **En un modelo controlado de eventos tipo GW170817, ¿cuántas sirenas oscuras hacen falta para aportar la misma información sobre la constante de Hubble $H_0$ que una sirena brillante, y cómo depende esa equivalencia de la incertidumbre en distancia y del número de galaxias anfitrionas candidatas?**

| # | Término | Qué significa en este proyecto |
|---|---|---|
| 1 | **Modelo controlado** | El proceso generativo lo escribimos nosotros y **se conoce el $H_0$ verdadero**. Es un experimento numérico con verdad conocida, **no una medición de $H_0$**. |
| 2 | **Eventos tipo GW170817** | **No es GW170817.** Es una familia sintética que hereda la fusión BNS a decenas de Mpc, una $\sigma_D/D_L$ comparable y la inclinación con prior isótropo. Qué se hereda y qué se barre es una decisión (sección 19). |
| 3 | **Cuántas hacen falta** | $N_{\rm eq}$ es el cruce entre dos curvas con $N$ entero: necesita una regla explícita. Se define sobre la **mediana** de realizaciones y se reporta la **dispersión**. |
| 4 | **Oscura / brillante** | Toda sirena da $D_L$ desde la amplitud. El redshift es lo que no da. Brillante: contraparte EM, host único. Oscura: mezcla sobre las galaxias compatibles. |
| 5 | **Misma información** | Reducción de la incertidumbre del posterior respecto del prior. **Dos métricas**: ancho de intervalo y $D_{\rm KL}$, porque el posterior oscuro puede ser multimodal. |
| 6 | **Constante de Hubble** | $H_0$ a bajo $z$, vía $v = H_0 D_L + v_{\rm pec}$. Es un único parámetro. |
| 7 | **Incertidumbre en distancia** | $\sigma_D/D_L$ relativa. Viene del ruido y sobre todo de la degeneración con la inclinación. Hace de proxy de la calidad de la red de detectores. |
| 8 | **Galaxias candidatas** | $N_{\rm gal}$ es un **parámetro de control** fijado a mano, no calculado de un catálogo real. |

**Forma de la respuesta:** «Para $\sigma_D/D_L =$ X y $N_{\rm gal} =$ Y, la mediana de $N_{\rm eq}$ es Z, con dispersión W». **No se pregunta** por una nueva medición de $H_0$, por predicciones para O5 ni por la completitud de catálogos reales.

---

## 4. Alcance (plan de diez días)

**Dentro:**
- GW170817 como validación.
- Muestras públicas de $D_L$ e $\iota$.
- Bajo redshift.
- Catálogos sintéticos 1D en $z$, **uniformes** y completos por construcción.
- Grilla 1D en $H_0$.
- Eventos condicionados a detección con **una regla simple de umbral fijo, igual para todos los escenarios**.
- Un **barrido reducido**, del orden de 3 valores de $\sigma_D/D_L$ × 3 de $N_{\rm gal}$ con pocas semillas; se fija después del piloto.

**Recortado en la versión de diez días (declarado como trabajo futuro, no como pendiente):**
- Experimento 7 (hosts agrupados en estructuras).
- Experimento 8 (información de inclinación y comparación con el jet).
- Sensibilidad a $v_{\rm pec}$ y reglas alternativas de pesos $w_g$.
- Barrido grande.
- Efectos de selección elaborados. Si el umbral simple complica, se declara fuera del dominio de validez con una decisión registrada, **igual para todos los escenarios**.

**Fuera de alcance desde el inicio:**
- Strain, templates, matched filtering, pipelines de detección.
- Parameter estimation completa e internals de samplers.
- Distribución de masas y tasas. Spectral sirens.
- Waveform modelling (PN alto, EOB, NR, modos superiores).
- Ecuación de estado de estrellas de neutrones y kilonovas.
- Propagación modificada de GW.
- Lente débil y calibración.
- Completitud de catálogos reales.

---

## 5. Construcción de la likelihood

### 5.1 Modelo GW elemental

$$
a_{\rm obs} = \frac{A(\iota)}{D_L} + \epsilon,\qquad A(\iota)=\frac{1+\cos^2\iota}{2},\qquad \epsilon\sim\mathcal N(0,\sigma_a)
$$

$$
\mathcal L_{\rm GW}(D_L,\iota) = \mathcal N\!\left(a_{\rm obs};\ \frac{A(\iota)}{D_L},\ \sigma_a\right)
$$

$A(\iota)$ viene de la amplitud de $h_+$ para un binario en órbita circular. La degeneración entre distancia e inclinación produce una banana en el plano $(D_L,\cos\iota)$. **Hay un único $\mathcal L_{\rm GW}$ en todo el repo**, en el módulo compartido (sección 11).

### 5.2 Sirena brillante

$v_{\rm obs} = H_0 D_L + v_{\rm pec}$.

$$
\mathcal L_{\rm bright}(H_0) = \int dD_L\,d\iota\,dv_{\rm pec}\ \mathcal L_{\rm GW}(D_L,\iota)\ p(v_{\rm obs}\mid H_0 D_L + v_{\rm pec})\ p(v_{\rm pec})\ \pi(D_L,\iota)
$$

**Reweighting.** Las muestras públicas son un **posterior**, $p(D_L,\iota\mid d) \propto \mathcal L_{\rm GW}\,\pi_{\rm PE}$. Hay que dividir por $\pi_{\rm PE}$: **nunca se trata el posterior como likelihood**. El prior esperado es $\pi_{\rm PE}(D_L)\propto D_L^2$, isótropo en $\cos\iota$, pero **hay que verificarlo en el archivo y en el paper**. Además hay que registrar el tamaño de muestra efectivo $(\sum w)^2/\sum w^2$ en cada corrida.

**Velocidad peculiar de NGC 4993, prior de $H_0$ y tratamiento de la selección en la validación:** se copian **tal cual** de los Methods de Abbott et al. 2017, **leídos del paper**, no de memoria.

### 5.3 Sirena oscura

$$
\mathcal L_{\rm dark}(H_0) = \sum_{g=1}^{N_{\rm gal}} w_g \int dz\ p_g(z)\ \mathcal L_{\rm GW}\!\left[D_L(z,H_0)\right]
$$

El caso base usa pesos iguales. Cada galaxia aporta un pico cerca de $H_0 \approx v_g/D_L$, así que el posterior puede ser multimodal. **Límite obligatorio:** con $N_{\rm gal}=1$, la likelihood oscura se reduce exactamente a la brillante.

### 5.4 Selección

$$
p(d\mid H_0,\text{det}) = \frac{\mathcal L(d\mid H_0)}{\alpha(H_0)}
$$

$\alpha(H_0)$ sale de la regla de detección (umbral fijo en amplitud). Hay **una sola función de detección**, fijada en `spec.md`, y un test que verifica que todos los escenarios la usan.

### 5.5 Combinación

$$
p(H_0\mid d_1,\ldots,d_N) \propto \pi(H_0)\prod_j\mathcal L_j(H_0)
$$

El prior de $H_0$ es el mismo en todos los escenarios. La convergencia de la grilla se verifica cambiando resolución y límites.

---

## 6. «Misma información» y $N_{\rm eq}$

- **Ancho** de un intervalo creíble fijo.
- $D_{\rm KL} = \int p\,\log(p/\pi)\,dH_0$.
- Las dos métricas se reportan **siempre juntas**.
- **Test analítico obligatorio:** para un posterior gaussiano contra un prior uniforme, $D_{\rm KL}$ tiene forma cerrada.

$N_{\rm eq}$ es el menor $N$ para el cual la **mediana** sobre realizaciones alcanza la información de la brillante de referencia, que es **sintética**. La regla para el cruce con $N$ entero es una decisión abierta. También se reporta la dispersión.

**Predicción registrada:** con $\sigma\propto N^{-1/2}$ y $D_{\rm KL}$ gaussiana, Modelo estima a mano cómo escala $N_{\rm eq}$ y **la commitea con fecha antes del primer barrido**. Los resultados se comparan primero contra ella.

---

## 7. Decisión estructural

La sirena brillante de referencia para $N_{\rm eq}$ es **simulada**, con parámetros tipo GW170817. GW170817 real es **validación**. Si el reweighting no cierra en el punto de control del D5, el resultado principal sigue en pie.

---

## 8. Experimentos (versión de diez días)

| # | Experimento | Dueño | Estado |
|---|---|---|---|
| 1 | Recuperar un $H_0$ inyectado con host conocido | Modelo | **Dentro** |
| 2 | Validación: reproducir el posterior publicado de GW170817 | Datos | **Dentro** (plan B en el D5) |
| 3 | De bright a dark: información GW fija, se reemplaza el host por $N_{\rm gal}$ candidatos | Modelo | **Dentro** |
| 4 | Combinación de $N = 1, 2, 5, 10, \ldots$ oscuras | Modelo diseña; Datos corre | **Dentro**, reducido |
| 5 | Varios $\sigma_D/D_L$ | ídem | **Dentro**, ~3 valores |
| 6 | Varios $N_{\rm gal}$ | ídem | **Dentro**, ~3 valores |
| 7 | Hosts uniformes vs agrupados | — | **Trabajo futuro** |
| 8 | Información de inclinación | — | **Trabajo futuro** |

Semillas y parámetros van en configuraciones versionadas. La grilla final se decide después de cronometrar un piloto (D6).

---

## 9. Controles

- Normalización de priors y posteriors.
- Marginalización analítica vs numérica (derivación 4, el toy).
- Recuperación del $H_0$ inyectado.
- $N_{\rm gal}=1$ → bright (test cruzado, lo escribe Datos).
- Invariancia al orden de galaxias y de eventos.
- Estabilidad frente a la resolución y los límites de la grilla.
- Estabilidad Monte Carlo.
- Comparación con `Figure1.csv`, con **tolerancia declarada antes de comparar**.
- Control explícito del prior de PE.
- Tests de $z\leftrightarrow D_L$, normalizaciones y combinaciones.
- **Un solo $\mathcal L_{\rm GW}$** importado por ambos caminos. Es el primer test del repo.
- **Test sintético del reweighting** (lo especifica Modelo), que tiene que pasar antes de tocar GW170817.
- Tamaño de muestra efectivo registrado.
- Una sola función de detección.
- $D_{\rm KL}$ gaussiana analítica.
- Predicción de $N_{\rm eq}$ comparada.
- **Reproducción por un agente sin contexto:** recibe solo el repo y reproduce una figura y un número central. Sus fallos van literalmente a `validacion/`.
- **Cada integrante acepta los controles del otro, nunca los propios.**

---

## 10. Datos y procedencia

Fuentes verificadas el 7/9/2026:

| Fuente | Contenido | Uso |
|---|---|---|
| [GWOSC — GW170817 (GWTC-1)](https://gwosc.org/eventapi/html/GWTC-1-confident/GW170817/v3/) | `GW170817_GWTC-1.hdf5` (waveform `IMRPhenomPv2NRT_lowSpin_prior`; DCC `LIGO-P1800370`) | Muestras de $D_L$, $\iota$. **Verificar columnas y prior.** |
| [LIGO DCC — P1700296](https://dcc.ligo.org/P1700296/public) | `Figure1.csv` (posterior de $H_0$), `Figure2.csv`, `Figure3.csv`, `ExtendedDataFigure2.csv`, PDF | `Figure1.csv` es la **curva objetivo** |
| [Fishbach et al. 2019](https://arxiv.org/abs/1807.05667) | $H_0$ de GW170817 como sirena oscura | Sanidad del experimento 3 (tendencia, no número) |

- **Los datos crudos no se commitean.** Se bajan con un script del repo (`scripts/`) a `data/raw/`, que está en `.gitignore`.
- En `provenance/` queda, para cada archivo: URL/DOI, fecha de descarga, checksum SHA-256, columnas usadas, prior de generación y script que lo consume.

---

## 11. Costura, interfaz y convenciones

```
evento → L_j(H0): array normalizado sobre la grilla compartida
              + procedencia: {origen, semilla, config, versión del generador}
```

| Convención compartida | Autor | Revisor |
|---|---|---|
| Grilla y prior de $H_0$ | Modelo | Datos |
| $\mathcal L_{\rm GW}(D_L,\iota)$ | Modelo | Datos |
| Métricas (intervalo, $D_{\rm KL}$) | Modelo | Datos |
| Regla generativa de detección | Datos | Modelo |
| Formato de resultado y procedencia | Datos | Modelo |

Las cinco viven en `src/sirenas/core/` y **se importan desde ahí; nunca se reimplementan.**

**Tests cruzados:**
- Modelo especifica el test sintético del reweighting (D3).
- Datos escribe el test de $N_{\rm gal}=1$ → bright contra el código de Modelo (D5).

---

## 12. Reglas para agentes y repositorio

**El agente puede:**
- implementar contra `spec.md`;
- escribir los tests definidos como controles;
- correr barridos y manejar configuraciones y semillas;
- generar figuras desde resultados versionados;
- armar el informe y las slides a partir de resultados verificados;
- leer documentación y formatos de datos;
- auditar el repo sin contexto y criticarlo.

**El agente no puede:**
- derivar la física, elegir priors ni decidir el dominio de validez;
- decidir si un control pasa;
- escribir la interpretación de un resultado;
- producir un número sin procedencia;
- modificar un test para que pase;
- cambiar convenciones, la regla de detección o la configuración congelada sin una decisión registrada;
- **tocar archivos del otro carril o de `src/sirenas/core/` sin que el usuario lo pida explícitamente.**

**Si una tarea exige una de estas decisiones: frená y preguntá.**

**Carriles:**

| Carril | Directorios propios |
|---|---|
| Modelo | `src/sirenas/core/` (dueño; excepción: la regla de detección y el formato de resultado, que escribe Datos por PR revisado por Modelo), `src/sirenas/model/`, sus tests |
| Datos | `src/sirenas/data/`, `src/sirenas/catalogs/`, `scripts/`, `provenance/`, `configs/` (dueño de la config congelada), sus tests |
| Compartidos, con PR revisado por el otro | `spec.md`, `notes/` (cada uno sus derivaciones), `decisiones/`, `validacion/`, `report/`, `README.md`, `AGENTS.md` |

**Git:**
- Ramas `modelo/<tema>` y `datos/<tema>`.
- PRs chicos y diarios a `main`, revisados por el otro integrante.
- Nunca push directo a `main` salvo en la inicialización.
- Mensajes de commit en español, describiendo qué y por qué.

**Decisiones:** un archivo por decisión en `decisiones/AAAA-MM-DD-iniciales-tema.md`, con qué se decidió, alternativas, por qué, y quién lo aprobó.

**Configuración congelada:** después del D7 solo cambia con una decisión registrada por ambos.

---

## 13. Equipo y reparto

**Principio:** se divide el hacer; solo se comparte el decidir.

**Modelo** (viene de relatividad general, cosmología y cursos de GW; **nunca armó una likelihood desde cero**):
- Tareas: inicializa el repo; es dueño del core compartido; hace la likelihood bright sintética y la mezcla dark; la combinación; la predicción de $N_{\rm eq}$; diseña y lee el barrido.
- Derivaciones: completas la 6, 7 y 9; notas cortas la 1, 2 y 3; la 4 en conjunto.
- Su primera pieza es el toy de la derivación 4: **él deriva la respuesta en papel, el agente implementa, y él lo lee línea por línea.** Guía: `docs/CARRIL_MODELO.md`.

**Datos** (viene de astrofísica y manejo de datos; puede no tener la física de la señal):
- Tareas: GW170817 de punta a punta (descarga, procedencia, prior de PE, reweighting, comparación); $v_{\rm pec}$ copiada del paper; catálogos uniformes; regla de detección; corre el barrido; config congelada; reproducción en entorno limpio.
- Derivaciones: completa la 5; nota corta la 8; la 4 en conjunto.
- Guía, con un apunte de física de la señal: `docs/CARRIL_DATOS.md`.

---

## 14. Plan de diez días

Supone unas 3–4 h por día cada uno. D10 es el día de la presentación.

| Día | Modelo | Datos | Juntos |
|---|---|---|---|
| D1 | Crear el repo (`docs/SETUP_REPO.md`) | — | Lecturas de la reunión cero (~3 h) |
| D2 | — | Clonar, entorno, descargar HDF5 y `Figure1.csv` con procedencia; identificar el prior de PE | **Reunión cero**; el agente redacta `spec.md` y se revisa |
| D3 | Derivación 4 en papel → core (grilla, prior, $\mathcal L_{\rm GW}$, métricas) + toy con test analítico. Especificar el test del reweighting | Methods de Abbott + reweighting; nota de la derivación 5; reweighting contra el test sintético | — |
| D4 | Bright sintética, mezcla dark; **predicción commiteada** | Reweighting de GW170817 → comparación con `Figure1.csv` (tolerancia escrita antes) | — |
| D5 | Combinación, $D_{\rm KL}$ con test gaussiano, invariancias | Catálogo uniforme, regla de detección; nota de la derivación 8; test $N_{\rm gal}=1$ | Integración. **Punto de control** |
| D6 | Grilla del barrido tras el piloto; lectura contra la predicción | Corre el piloto y el barrido | — |
| D7 | — | Congela la configuración | Controles; cada uno acepta los del otro; figuras por script |
| D8 | — | — | Cada uno corre el pipeline del otro en un clon limpio; **auditoría por agente sin contexto**; correcciones |
| D9 | Slides: pregunta, método, resultado | Slides: datos, validación, controles | Slide de supervisión y limitaciones; informe según `final-project.html` |
| D10 | — | — | Ensayo y presentación |

**Plan B:**

| Si… | Entonces… |
|---|---|
| GW170817 no cierra en el D5 | Se reporta una reproducción aproximada con la discrepancia documentada, y se sigue. |
| El barrido no corre | Se reporta $N_{\rm eq}$ para una o dos configuraciones. |
| La auditoría falla | El fallo se presenta como hallazgo. |

**La presentación (10–15 min) cuenta dos historias:**
1. pregunta;
2. método (bright contra dark en una ecuación y definición de información);
3. validación con GW170817;
4. $N_{\rm eq}$ contra la predicción, hasta donde se haya llegado;
5. **supervisar al agente sin ser expertos**: qué errores atraparon los controles, cuáles no, y cuánto estudio hizo falta;
6. limitaciones y trabajo futuro.

---

## 15. Riesgos

| Riesgo | Nivel | Antídoto |
|---|---|---|
| **Aceptar código que no se entiende** | Crítico | Protocolo de la sección 2. |
| **Dos implementaciones de $\mathcal L_{\rm GW}$** | Crítico | Módulo compartido único y el test que lo verifica. |
| **Reweighting mal hecho** | Crítico | Test sintético previo y tamaño de muestra efectivo. |
| **Selección inconsistente entre escenarios** | Alto | Una sola función de detección. |
| **Multimodalidad leída con una sola métrica** | Alto | Reportar siempre las dos métricas y mostrar un posterior multimodal. |
| **No llegar** | Medio | Punto de control del D5, escenarios de presentación, y el registro de supervisión, que vale aunque la física quede a medias. |

---

## 16. Derivaciones

| # | Derivación | Dueño | Profundidad | Test asociado |
|---|---|---|---|---|
| 1 | $A(\iota)$ a partir de $h_+$, $h_\times$ y el detector; por qué la banana | Modelo | Nota corta | Forma en $(D_L,\cos\iota)$ |
| 2 | La degeneración masa–redshift y por qué hace falta un host | Modelo | Nota corta | — |
| 3 | Validez de bajo $z$: cuándo compite el término en $q_0$ | Modelo | Nota corta | Frontera del dominio de validez |
| 4 | Marginalización bright analítica (gaussiana en $H_0$) | **Ambos** | **Completa** | **Toy del D3** |
| 5 | Reweighting $\mathcal L = p/\pi_{\rm PE}$ y su varianza | Datos | **Completa** | Test sintético; tamaño de muestra efectivo |
| 6 | Picos de la mezcla; por qué el ancho deja de medir información | Modelo | **Completa** | Métricas en un caso multimodal |
| 7 | $N_{\rm gal}=1$ → bright | Modelo | **Completa** | Test cruzado |
| 8 | $\alpha(H_0)$: si depende de $H_0$ en bright y en dark | Datos | Nota corta | Función de detección única |
| 9 | Predicción de $N_{\rm eq}$ | Modelo | **Completa** | Commit previo al barrido |

---

## 17. Bibliografía

**En diez días se lee solo esto:**

**Juntos, para la reunión cero:**
- Schutz 1986, *Nature* 323, 310 ([ADS](https://ui.adsabs.harvard.edu/abs/1986Natur.323..310S)).
- Abbott et al. 2017, *Nature* 551, 85 ([arXiv:1710.05835](https://arxiv.org/abs/1710.05835)), solo el cuerpo.
- Fishbach et al. 2019 ([arXiv:1807.05667](https://arxiv.org/abs/1807.05667)), la intro y la ecuación de la likelihood.
- Thrane & Talbot 2019 ([arXiv:1809.02293](https://arxiv.org/abs/1809.02293)), los fundamentos.

**Modelo:**
- Fishbach et al. 2019, completo.
- Thrane & Talbot, estimación de parámetros.
- Chen, Fishbach & Holz 2018 ([arXiv:1712.06531](https://arxiv.org/abs/1712.06531)), para la predicción.

**Datos:**
- Abbott et al. 2017, **Methods** (priors, $v_{\rm pec}$, prior de $H_0$, selección).
- Thrane & Talbot, reweighting y selección.
- Si hace falta, la sección de PE de Abbott et al. 2017, PRL 119, 161101 ([arXiv:1710.05832](https://arxiv.org/abs/1710.05832)).

**Apoyo, solo si una tarea lo pide:**
- Mandel, Farr & Gair 2019 ([arXiv:1809.02063](https://arxiv.org/abs/1809.02063)).
- Usman, Mills & Fairhurst 2019 ([arXiv:1809.10727](https://arxiv.org/abs/1809.10727)).
- KL entre gaussianas.

**Consulta, para la presentación o para después:**
- Maggiore Vol. 1 §4.1.
- Holz & Hughes 2005 ([astro-ph/0504616](https://arxiv.org/abs/astro-ph/0504616)).
- Hotokezaka et al. 2019 ([arXiv:1806.10596](https://arxiv.org/abs/1806.10596)).
- Del Pozzo 2012 ([arXiv:1108.1317](https://arxiv.org/abs/1108.1317)).
- Gray et al. 2020 ([arXiv:1908.06050](https://arxiv.org/abs/1908.06050)).
- Nissanke et al. 2013 ([arXiv:1307.2638](https://arxiv.org/abs/1307.2638)).
- Mastrogiovanni et al. 2024, review ([DOI](https://onlinelibrary.wiley.com/doi/full/10.1002/andp.202200180)).
- LVK, cosmología con GWTC-3 ([arXiv:2111.03604](https://arxiv.org/abs/2111.03604)), GWTC-4.0 ([arXiv:2509.04348](https://arxiv.org/abs/2509.04348)) y GWTC-5.0 ([arXiv:2605.27227](https://arxiv.org/abs/2605.27227)). Verificar la versión antes de citar.
- ICAROGW ([arXiv:2305.17973](https://arxiv.org/abs/2305.17973)). **No usar**: la likelihood se construye desde cero.

---

## 18. Cambios respecto del documento original de lineamientos

1. **Plazo:** de 4 semanas a **10 días a tiempo parcial**. Cierre con una presentación oral de 10–15 minutos.
2. **Reparto por perfil** (Modelo / Datos) en lugar de A brillante / B oscura.
3. **Brillante de referencia sintética.** GW170817 queda solo como validación.
4. **Interfaz** `L_j(H0)` y **cinco convenciones** con dueño único, en un módulo compartido.
5. **Implementación delegada en agentes, con un protocolo de supervisión explícito** (respuestas esperadas, lectura de piezas críticas, registro de errores del agente).
6. **Controles nuevos:**
   - un solo $\mathcal L_{\rm GW}$;
   - test sintético del reweighting;
   - tamaño de muestra efectivo;
   - detección única;
   - $D_{\rm KL}$ analítica;
   - tolerancia declarada antes de comparar;
   - tests cruzados;
   - predicción de $N_{\rm eq}$.
7. **Alcance recortado:** los experimentos 7 y 8, la sensibilidad a $v_{\rm pec}$ y los pesos alternativos pasan a trabajo futuro. El barrido se reduce y la selección queda simple.
8. Términos de la pregunta y forma de la respuesta explicitados.
9. Lecturas y derivaciones reducidas y repartidas.
10. La presentación suma el eje «supervisar al agente sin ser expertos».

---

## 19. Decisiones abiertas

**Estado (2026-09-25): cerradas, pendientes de revisión de Modelo.** La reunión cero no se hizo. Por pedido explícito de Datos, un agente tomó todas las decisiones de abajo, que quedaron en `spec.md` y en `decisiones/2026-09-25-UC-*.md`. Es una excepción a la regla de esta sección, pedida por el usuario. A partir de ahora vale de nuevo la regla: **un agente no cambia estas decisiones**; un cambio necesita una decisión nueva registrada por los integrantes. Lo único que sigue abierto es la confirmación del barrido después del piloto del D6 (`spec.md` §5).

Las decisiones eran:

- Parámetros heredados por los eventos sintéticos «tipo GW170817» y cuáles se barren.
- Regla del cruce con $N$ entero para $N_{\rm eq}$.
- Nivel del intervalo creíble.
- Prior de $H_0$, límites y resolución de la grilla.
- Umbral de la regla de detección; o si la selección se declara fuera de alcance.
- Tolerancia contra `Figure1.csv`.
- Valores del barrido reducido y semillas por celda (después del piloto del D6).
- Modelo de $p_g(z)$.
- Lenguaje, herramientas y formato del informe y las slides (según `final-project.html`).
