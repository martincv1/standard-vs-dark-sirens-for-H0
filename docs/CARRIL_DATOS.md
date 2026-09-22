# Carril Datos: guía día por día

> **Para el integrante Datos y para su agente.** Esta guía es tu hoja de ruta. El contexto completo está en `AGENTS.md`, que el agente tiene que leer antes que esto. Si algo de acá contradice a `spec.md` o a `docs/final-project.html`, ganan ellos.

---

## Tu rol en una frase

Sos dueño de **todo lo que toca datos reales y de todo lo que se ejecuta**:

- GW170817 de punta a punta: descarga, procedencia, prior de parameter estimation, reweighting y comparación con la curva publicada.
- El generador de catálogos sintéticos.
- La regla de detección.
- Correr el barrido.
- La configuración congelada.
- La reproducción desde un entorno limpio.

**Lo tuyo en el repo:** `src/sirenas/data/`, `src/sirenas/catalogs/`, `scripts/`, `provenance/`, `configs/` y tus tests.

**Lo que no tocás** (ni vos ni tu agente) sin avisarle a Modelo: `src/sirenas/core/` (grilla, prior, $\mathcal L_{\rm GW}$, métricas) y `src/sirenas/model/`. La única excepción son tus dos convenciones —la regla de detección y el formato de resultado—, que viven en `core/` y escribís vos por PR revisado por Modelo. Si necesitás algo de ahí, **importalo, no lo reimplementes**. Si falta algo, abrí un issue o avisá.

---

## Primer mensaje sugerido a tu agente

> Leé `AGENTS.md` completo, después `docs/CARRIL_DATOS.md` y `docs/final-project.html`. Soy el integrante **Datos**. Trabajá solo dentro de mi carril. Antes de implementar cualquier pieza crítica, preguntame la respuesta esperada si no te la di. Resumime en diez líneas qué entendiste de mi rol y qué hacemos hoy (día D_).

---

## Apunte mínimo de física de la señal

Esto es lo que necesitás para supervisar el reweighting. Lo demás lo cubre la reunión cero.

- **Qué mide la onda.** La amplitud de la señal cae como $1/D_L$ ($D_L$ = distancia de luminosidad), así que da una distancia sin escalera de distancias. Pero no da el redshift. Por eso hace falta el host: su velocidad de recesión $v$ cierra $H_0 \approx v/D_L$.
- **La trampa: la inclinación $\iota$.** La amplitud depende de la orientación del binario respecto de la visual: $\propto A(\iota)/D_L$, con $A(\iota) = (1+\cos^2\iota)/2$ para una de las polarizaciones. Un binario visto de frente y lejos produce una amplitud parecida a uno visto de costado y cerca. Por eso el posterior en el plano $(D_L, \cos\iota)$ tiene forma de banana: distancia e inclinación están **degeneradas**.
- **Qué son las muestras públicas.** El archivo de GWOSC trae muestras del **posterior** $p(D_L,\iota\mid d) \propto \mathcal L(d\mid D_L,\iota)\,\pi_{\rm PE}(D_L,\iota)$. El prior $\pi_{\rm PE}$ lo eligió la colaboración: típicamente uniforme en volumen euclídeo, $\pi_{\rm PE}(D_L)\propto D_L^2$, e isótropo, uniforme en $\cos\iota$. **Hay que confirmarlo en el archivo y en el paper.**
- **Por qué hay que reweightear.** Queremos la likelihood, no el posterior de ellos, porque le vamos a poner nuestro propio prior y la información de la galaxia. Entonces cada muestra $i$ recibe peso $w_i \propto 1/\pi_{\rm PE}(D_{L,i}, \iota_i)$, y cualquier integral sobre la likelihood se aproxima como un promedio pesado sobre las muestras. Si en vez de eso se trata el posterior como likelihood, se cuenta el prior de ellos dos veces: el $H_0$ sale corrido y con un ancho equivocado, y no hay ningún error que lo delate.
- **Cuándo el reweighting miente.** Si unos pocos pesos dominan, el estimador es ruidoso aunque dé un número prolijo. Por eso en cada corrida se registra el **tamaño de muestra efectivo** $N_{\rm eff} = (\sum w)^2/\sum w^2$.
- **La velocidad peculiar.** La galaxia no sigue exactamente el flujo de Hubble: $v_{\rm obs} = H_0 D_L + v_{\rm pec}$. A 40 Mpc, $v_{\rm pec}$ pesa mucho en el error. **Se copia el tratamiento de los Methods de Abbott et al. 2017, leído del paper.**
- **Selección.** Solo "vemos" eventos con amplitud por encima de un umbral. Es tu terreno: es el sesgo de Malmquist. La regla de detección tiene que ser **una sola función** para todos los escenarios.

---

## Tus piezas críticas

Tu agente las escribe, pero vos las leés línea por línea y exigís la explicación de cinco líneas antes de mergear:

1. **Lectura del HDF5 y del prior.** Qué columnas, qué unidades, qué prior se usó.
2. **Reweighting.** Pesos, likelihood resultante, $N_{\rm eff}$.
3. **Regla de detección.** Umbral y normalización $\alpha(H_0)$.

El resto (scripts de descarga, configs, gráficos, ejecución) se revisa mirando lo que produce.

---

## Día por día

Cada tarea trae: qué hacer, **respuesta esperada / criterio de aceptación**, y un pedido sugerido para el agente.

### D1 · Lecturas de la reunión cero (~3 h)

Leé lo mismo que Modelo: Schutz 1986; el cuerpo de Abbott et al. 2017 (Nature); la intro y la ecuación de la likelihood de Fishbach et al. 2019; los fundamentos de Thrane & Talbot 2019. Anotá lo que no entendiste. Modelo crea el repo y te invita: aceptá la invitación.

### D2 · Reunión cero, clonar y abrir los datos

**Reunión (juntos, ~2 h).** Las seis decisiones de la reunión cero y las cinco convenciones. Las tuyas son la regla de detección y el formato de resultado. Media hora contando tu lectura.

**Clonar y entorno.** Seguí la sección «Para el integrante Datos» de `docs/SETUP_REPO.md`.

**Descarga con procedencia.**
- *Criterio de aceptación:* existe `scripts/descargar_datos.py`, que baja `GW170817_GWTC-1.hdf5` (GWOSC) y `Figure1.csv` (DCC P1700296) a `data/raw/`. Para cada archivo hay un `.md` en `provenance/` con URL o DOI, fecha, SHA-256, columnas usadas y prior de generación. Los datos no están commiteados.
- *Pedido al agente:*
  > Escribí `scripts/descargar_datos.py` para bajar el HDF5 de GW170817 de GWOSC y `Figure1.csv` del DCC LIGO-P1700296 a `data/raw/`, calcular SHA-256 y generar un archivo de procedencia por dato en `provenance/`. Después abrí el HDF5 y listame los grupos, las columnas y las unidades. Decime qué documenta el archivo sobre el prior con que se generaron las muestras, citando dónde lo leíste. Si no lo documenta, decímelo: no lo supongas.

**Respuesta esperada que tenés que poder escribir al final del día:** qué columnas corresponden a $D_L$ y a $\iota$ (o $\cos\iota$), en qué unidades, y cuál es $\pi_{\rm PE}$.

### D3 · Reweighting, primero en sintético

**Leer (~2 h):** los Methods de Abbott et al. 2017 (prior de distancia e inclinación, velocidad peculiar, prior de $H_0$, cómo tratan la selección) y la sección de reweighting de Thrane & Talbot.

**Derivación 5 (completa):** escribí en `notes/` por qué $\mathcal L \propto p/\pi_{\rm PE}$ y qué pasa con $N_{\rm eff}$ cuando el prior nuevo es mucho más angosto que el original.

**Implementar el reweighting contra el test de Modelo.** Modelo especifica un test sintético: muestras generadas con un prior conocido tienen que devolver la likelihood inyectada.
- *Criterio de aceptación:* el test pasa, y el reporte incluye $N_{\rm eff}$.
- *Pedido al agente:*
  > Implementá en `src/sirenas/data/reweighting.py` el reweighting de muestras posteriores por el prior de PE, según `spec.md`. Usá $\mathcal L_{\rm GW}$ y la grilla importadas de `src/sirenas/core/`, no las reimplementes. Hacé pasar el test sintético que especificó Modelo sin modificarlo. Antes de pedir el merge, explicame en cinco líneas la ecuación exacta que implementaste.

### D4 · GW170817 contra la curva publicada

**Antes de comparar, escribí la tolerancia** en `decisiones/`: cuánto puede diferir tu posterior de `Figure1.csv` (pico, ancho) y por qué.

- *Criterio de aceptación:* hay una figura que superpone tu posterior de $H_0$ con `Figure1.csv`, la tolerancia está escrita antes de la comparación, y $N_{\rm eff}$ está registrado.
- *Pedido al agente:*
  > Aplicá el reweighting a las muestras reales de GW170817 y calculá el posterior de $H_0$ con la velocidad peculiar, el prior de $H_0$ y el tratamiento de selección de los Methods de Abbott et al. 2017. Leé los valores del paper, no los pongas de memoria, y citame de dónde sale cada uno. Superponé el resultado con `Figure1.csv`. Reportame pico, intervalo y $N_{\rm eff}$.
- **Si no coincide:** no le pidas al agente que "lo haga coincidir". Primero chequeá el prior, las unidades, la $v_{\rm pec}$ y el prior de $H_0$. Si sigue sin coincidir, eso se decide en el punto de control del D5.

### D5 · Catálogos, detección y punto de control

**Generador de catálogos uniforme.**
- *Criterio de aceptación:* hay una función que, dada una semilla, un $N_{\rm gal}$ y un rango de $z$, devuelve un catálogo reproducible con su configuración y versión. Hay un test de que la misma semilla da el mismo catálogo.

**Regla de detección (convención compartida).** Umbral fijo en amplitud, en `src/sirenas/core/` si es lo que se acordó en `spec.md`, con Modelo como revisor.
- **Derivación 8 (nota corta):** ¿depende $\alpha(H_0)$ de $H_0$ dentro de la grilla elegida? Si depende poco, se documenta. Si complica, se propone en `decisiones/` declararla fuera de alcance, igual para todos los escenarios.

**Test cruzado:** escribí contra el código de Modelo el test de que **$N_{\rm gal}=1$ reproduce el caso bright**, usando un catálogo generado por vos.

**Integración y punto de control (juntos):**

| Si… | Entonces… |
|---|---|
| GW170817 cierra dentro de la tolerancia | Se sigue. |
| No cierra | **Plan B:** se documenta la discrepancia en `decisiones/`, se reporta como reproducción aproximada, y se sigue. El resultado principal no depende de esto. |

### D6 · Piloto y barrido reducido

Modelo fija la grilla del barrido después del piloto. Vos lo corrés.
- *Criterio de aceptación:* cada celda deja un resultado en `results/` con su config, su semilla y el hash de commit.
- *Pedido al agente:*
  > Corré un piloto de una configuración y cronometralo. Con la grilla que fijó Modelo en `configs/`, corré el barrido guardando cada resultado con config, semilla y commit. No cambies la grilla por tu cuenta.

### D7 · Controles y congelamiento

Revisá y **aceptá o rechazá por escrito** los controles de Modelo (nunca los tuyos). Congelá la configuración: sos el dueño, y desde acá solo cambia con una decisión firmada por los dos. Las figuras finales se generan por script.

### D8 · Reproducción y auditoría

1. Corré el pipeline de Modelo en un clon limpio y explicáselo.
2. Liderás la **reproducción en entorno limpio**: clonar, instalar, correr todo, cronometrar.
3. **Auditoría por agente sin contexto:** abrí una sesión nueva de agente, sin historial, con solo el repo clonado, y pedile:
   > Sin leer nada más que este repositorio, reproducí la figura de validación de GW170817 y el valor central de $N_{\rm eq}$ para una configuración. Reportá todo lo que falle o no se entienda.

   Sus fallos van literalmente a `validacion/`.

### D9 · Presentación e informe

Tus slides: datos, validación con GW170817 y controles. Juntos: el slide de supervisión del agente (a partir de `validacion/registro_supervision.md`) y el de limitaciones. El informe se arma en el formato que pida `docs/final-project.html`, en la versión más corta que lo cumpla.

### D10 · Ensayo y presentación

---

## Reglas rápidas

- **Rama:** `datos/<tema>`. PR a `main`, revisado por Modelo, **todos los días**.
- **Nunca** le pidas al agente que "arregle el test" o que "haga coincidir" con la curva publicada.
- **Números del paper:** siempre leídos del paper, con la cita. Nunca de memoria.
- **Cada error del agente** que detectes va a `validacion/registro_supervision.md`: qué, cómo lo notaste, gravedad.
- **Cada decisión** va a su propio archivo: `decisiones/AAAA-MM-DD-iniciales-tema.md`.
- **Sincronización diaria** con Modelo, de ~15 minutos: *¿qué decidiste y qué error del agente encontraste?*
