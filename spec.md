# spec.md: especificación técnica

> **Estado: DECIDIDO, pendiente de revisión de Modelo en el PR.** La reunión cero (D2) no se hizo. Datos (Ulises) le delegó al agente todas las decisiones abiertas de `AGENTS.md` §19 el 2026-09-25. Cada una tiene su archivo en `decisiones/2026-09-25-UC-*.md`, con alternativas y justificación. **Es una excepción explícita a la regla «un agente no resuelve decisiones abiertas»** (`AGENTS.md` §19), pedida por el usuario; queda registrada como material para la slide de supervisión. Modelo acepta o cambia cada punto al revisar el PR; cualquier cambio posterior va con una decisión nueva.
>
> Este archivo es la referencia para implementar. Si hay conflicto, manda sobre `AGENTS.md`, pero no sobre `docs/final-project.html`.
>
> Los valores de GW170817 de §4 se leyeron del texto de Abbott et al. 2017 (arXiv:1710.05835v1, Methods), no de memoria. Los superíndices del PDF salen intercalados en la extracción de texto, así que el intervalo publicado se confirmó además contra las muestras de `Figure1.csv` (ver §4).

---

## 1. Notación y unidades

| Símbolo | Significado | Unidades |
|---|---|---|
| $H_0$ | Constante de Hubble | km s⁻¹ Mpc⁻¹ |
| $D_L$ | Distancia de luminosidad | Mpc |
| $\iota$ | Inclinación (se trabaja con $\cos\iota$) | — |
| $a_{\rm obs}$, $\sigma_a$ | Amplitud observada y su ruido (modelo sintético) | Mpc⁻¹ |
| $\varepsilon$ | Ruido fraccional de amplitud: $\sigma_a = \varepsilon / D_{\rm ref}$, con $D_{\rm ref} = 40$ Mpc | — |
| $v$ | Velocidad de Hubble de una galaxia, $v = cz$ | km s⁻¹ |
| $v_{\rm obs}$, $\sigma_v$ | Velocidad medida de una galaxia y su incertidumbre total (peculiar + medición) | km s⁻¹ |
| $N_{\rm gal}$, $w_g$, $p_g$ | Número de hosts candidatos, pesos, incertidumbre de la velocidad de cada candidata | — |
| $N$ | Número de eventos combinados | — |
| $c$ | 299 792,458 km s⁻¹ | km s⁻¹ |

**Bajo $z$:** $D_L(z, H_0) = cz/H_0 = v/H_0$ (ley de Hubble lineal, ec. 1 de Abbott et al. 2017). Con $v \le 4000$ km s⁻¹, $z \le 0{,}013$ y la corrección en $q_0$ es menor al 1 % (la cuantifica la derivación 3).

## 2. Las cinco convenciones compartidas

Todas viven en `src/sirenas/core/` y se importan desde ahí.

### 2.1 Grilla y prior de $H_0$ · autor: Modelo · revisor: Datos
- Rango: $H_0 \in [20, 250]$ km s⁻¹ Mpc⁻¹. Cubre todas las muestras de `Figure1.csv` ([48,4; 221,5]) y los picos de las galaxias del catálogo sintético ($v_g/D_L$ entre 2000/57 ≈ 35 y 4000/28,6 ≈ 140, más el ancho de cada pico).
- Resolución: $\Delta H_0 = 0{,}1$ (2301 puntos, extremos incluidos). **Convergencia:** con $\Delta H_0 = 0{,}05$ y con rango $[10, 300]$, el ancho y la $D_{\rm KL}$ cambian menos del 1 %.
- Prior de los escenarios sintéticos: **uniforme en $[20, 250]$**, el mismo en todos los escenarios.
- Prior de la validación con GW170817: $\pi(H_0)\propto 1/H_0$ sobre la misma grilla, como en Abbott et al. 2017 (Methods, después de la ec. 7). Solo se usa ahí.
- Integrales sobre la grilla: regla del trapecio. Todo array `L_j(H0)` se normaliza a integral 1 sobre la grilla.

### 2.2 $\mathcal L_{\rm GW}(D_L,\iota)$ · autor: Modelo · revisor: Datos
- Modelo: $a_{\rm obs} = A(\iota)/D_L + \epsilon$, $A(\iota)=(1+\cos^2\iota)/2$, $\epsilon\sim\mathcal N(0,\sigma_a)$.
- $\sigma_a$: $\sigma_a = \varepsilon / D_{\rm ref}$, con $D_{\rm ref} = 40$ Mpc. $\varepsilon$ es el error fraccional de amplitud de un evento face-on a 40 Mpc. Es el **parámetro de control** del barrido. El $\sigma_D/D_L$ que se reporta **se mide**: es la mediana, sobre realizaciones, de (semiancho 16–84 %)/mediana del posterior marginal de $D_L$ de cada evento, incluida la degeneración con $\cos\iota$. Así, la respuesta se expresa en $\sigma_D/D_L$ como pide la pregunta, pero el control es un número que el modelo fija sin calibración iterativa.
- Firma:
  ```python
  def l_gw(a_obs: float, d_l: np.ndarray, cos_iota: np.ndarray, sigma_a: float) -> np.ndarray:
      """Densidad N(a_obs; A(iota)/d_l, sigma_a), sin normalizar en (d_l, cos_iota). Vectorizada por broadcasting."""
  ```
- Marginalización de $\cos\iota$: numérica, con prior uniforme en $[-1, 1]$ y una grilla de $\cos\iota$ cuya convergencia se verifica igual que la de $H_0$.

### 2.3 Métricas de información · autor: Modelo · revisor: Datos
- **Ancho:** medida (en km s⁻¹ Mpc⁻¹) del **conjunto de máxima densidad posterior al 68,3 %**, es decir, la suma de los largos de sus tramos si es disjunto. Es el mismo nivel y el mismo tipo de intervalo («minimal 68.3 % credible interval») que usa Abbott et al. 2017, y con un posterior multimodal no cuenta los valles como región creíble.
- $D_{\rm KL}(\text{posterior}\,\|\,\text{prior}) = \int p\,\ln(p/\pi)\,dH_0$, en nats, sobre la grilla (con $0\ln 0 = 0$).
- **Referencia brillante:** para cada celda ($\varepsilon$), la mediana de la métrica sobre las realizaciones de **un** evento brillante sintético con el mismo $\varepsilon$.
- **Regla de $N_{\rm eq}$:** se evalúan **todos los enteros** $N = 1, \dots, N_{\max}$ (el costo es despreciable en 1D, así que no hace falta interpolar). $N_{\rm eq}$ es el **menor $N$ entero** para el cual la mediana sobre realizaciones cumple $\text{ancho}_{\rm dark}(N) \le \text{ancho}_{\rm bright}$ (y, por separado, $D_{\rm KL,dark}(N) \ge D_{\rm KL,bright}$). Se reportan los dos $N_{\rm eq}$, uno por métrica. Si no se alcanza en $N_{\max}$, se reporta «$> N_{\max}$».
- **Dispersión:** el mismo criterio aplicado a cada realización por separado da un $N_{\rm eq}$ por realización. Se reportan sus percentiles 16 y 84.

### 2.4 Regla generativa de detección · autor: Datos · revisor: Modelo
- Un evento se detecta si $a_{\rm obs} \ge a_{\rm th}$, con $a_{\rm th} = 1/(190\ \text{Mpc})$: la amplitud de un evento face-on en el horizonte BNS de ≈190 Mpc que cita Abbott et al. 2017 (Methods, efectos de selección). Umbral fijo en amplitud, **igual para todos los escenarios**, en una sola función `detectado(a_obs)` en `src/sirenas/core/` con su test.
- **La selección está dentro del dominio de validez.** Se incluye $\alpha(H_0)$:
  $$\alpha(H_0) = \int dv\,p_0(v)\int d\cos\iota\ \tfrac12\ P\!\left(a_{\rm obs}\ge a_{\rm th}\ \middle|\ \tfrac{A(\iota)\,H_0}{v},\ \sigma_a\right)$$
  con $p_0(v)$ uniforme en $[v_{\min}, v_{\max}]$ (§3), y $P$ la probabilidad gaussiana de superar el umbral. Se divide la likelihood de cada evento por $\alpha(H_0)$, igual en bright y en dark.
- Si el control de recuperación del $H_0$ inyectado (experimento 1) muestra un sesgo atribuible a la selección, se registra una decisión nueva y se cambia **en todos los escenarios a la vez**.

### 2.5 Formato de resultado y procedencia · autor: Datos · revisor: Modelo
- La interfaz de un evento:
  ```
  evento → L_j(H0): array normalizado sobre la grilla compartida
                + procedencia: {origen, semilla, config, versión del generador}
  ```
- En disco, por celda del barrido, `results/<experimento>/<celda>/`:
  - `likelihoods.npz`: `h0` (la grilla), `L` (array `[realizacion, evento, h0]`), `a_obs`, `cos_iota_true`, `v_true` y `detectado`;
  - `procedencia.json`: `origen` (módulo y función), `semilla`, `config` (copia literal del YAML de la celda), `version_generador`, `git_commit`, `git_dirty`, versiones de `numpy`/`scipy`/`python` y fecha UTC.
- Configuraciones: un YAML por experimento en `configs/`. Semillas: `numpy.random.default_rng(semilla)`, con semilla por celda = `semilla_base + indice_celda` y semillas por realización generadas con `SeedSequence(semilla_celda).spawn(n_realizaciones)`.
- Las figuras se hacen por script desde `results/`, nunca a mano, y cada figura lleva al lado un `.json` con los archivos de entrada y el commit.

## 3. Eventos sintéticos «tipo GW170817»

Modelo generativo, idéntico a la likelihood (así el experimento 1 puede exigir recuperación sin sesgo):

1. $H_0^{\rm true} = 70$ km s⁻¹ Mpc⁻¹ (el MAP publicado de GW170817, redondeado).
2. Velocidad de Hubble del host verdadero: $v_{\rm true} \sim \mathcal U[2000, 4000]$ km s⁻¹, que contiene los 3017 km s⁻¹ de NGC 4993. Distancia: $D_L = v_{\rm true}/H_0^{\rm true}$, entre 28,6 y 57,1 Mpc.
3. $\cos\iota \sim \mathcal U[-1, 1]$ (prior isótropo).
4. $a_{\rm obs} \sim \mathcal N(A(\iota)/D_L, \sigma_a)$; se aplica `detectado` y se vuelve a sortear si no pasa. Los eventos no detectados se cuentan y se guardan.
5. Velocidad medida de cada galaxia: $v_{\rm obs} \sim \mathcal N(v, \sigma_v)$ con $\sigma_v = 166$ km s⁻¹, la incertidumbre total de $v_H$ de GW170817 (150 de velocidad peculiar + 72 de medición en cuadratura; Abbott et al. 2017). El sintético no tiene la corrección de 310 km s⁻¹: sus velocidades peculiares son de media cero.
6. **Oscura:** el catálogo tiene el host verdadero más $N_{\rm gal}-1$ galaxias con $v \sim \mathcal U[2000, 4000]$ km s⁻¹ (uniforme en $z$ en $[0{,}00667;\ 0{,}01334]$, completo por construcción: `src/sirenas/catalogs/`). El orden de las galaxias se baraja. Pesos iguales, $w_g = 1/N_{\rm gal}$.
7. **Modelo de $p_g$:** gaussiano en velocidad, $p_g(v) = \mathcal N(v; v_{{\rm obs},g}, \sigma_v)$.
8. **Likelihood** (una sola forma; la brillante es la oscura con $N_{\rm gal}=1$, así que el límite de la derivación 7 se cumple por construcción y el test cruzado igual lo verifica numéricamente):
   $$\mathcal L(H_0) = \frac{1}{\alpha(H_0)}\sum_{g=1}^{N_{\rm gal}} w_g \int dv\ \mathcal N(v; v_{{\rm obs},g}, \sigma_v)\int \tfrac{d\cos\iota}{2}\ \mathcal L_{\rm GW}\!\left(\tfrac{v}{H_0}, \iota\right)$$
   con $\int dv$ sobre $[v_{{\rm obs},g} - 5\sigma_v,\ v_{{\rm obs},g} + 5\sigma_v]$.
9. **Sirena brillante de referencia:** sintética, con este mismo modelo y $N_{\rm gal}=1$.

Parámetros heredados de GW170817: fusión BNS a decenas de Mpc (rango de $v$ que contiene a NGC 4993), inclinación isótropa, $\sigma_v$ y el horizonte que fija $a_{\rm th}$. Parámetros que se barren: $\varepsilon$ (reportado como $\sigma_D/D_L$ medido) y $N_{\rm gal}$.

## 4. Validación con GW170817

- **Archivo y columnas:** `GW170817_GWTC-1.hdf5`, dataset `IMRPhenomPv2NRT_lowSpin_posterior` (8078 muestras), columnas `luminosity_distance_Mpc` y `costheta_jn`. Se usa `lowSpin` porque los spins bajos son lo esperado para una BNS, y con spins chicos $\theta_{JN}\approx\iota$. **Supuesto declarado:** `costheta_jn` se usa como $\cos\iota$. `highSpin` queda como control de sensibilidad si sobra tiempo.
- **Prior de PE:** $\pi_{\rm PE}(D_L)\propto D_L^2$ y uniforme en $\cos\theta_{JN}$, verificado con las muestras de prior del propio HDF5 (`provenance/GW170817_GWTC-1.hdf5.md`: KS p = 0,28 para $d^2$, exponente de MV 2,01; KS p = 0,31 para $\cos\theta_{JN}$). Coincide con Abbott et al. 2017, Methods («volumetric prior, $p(d)\propto d^2$»; «flat (i.e. isotropic) prior on $\cos\iota$»). Pesos del reweighting: $w_i \propto 1/D_{L,i}^2$. Se registra $n_{\rm eff} = (\sum w)^2/\sum w^2$ en cada corrida.
- **Valores copiados de Abbott et al. 2017 (Methods, ecs. 5–7 y párrafos previos):**
  - $v_r = 3327$ km s⁻¹, $\sigma_{v_r} = 72$ km s⁻¹ (grupo de NGC 4993, sistema de la CMB);
  - $\langle v_p\rangle = 310$ km s⁻¹, $\sigma_{v_p} = 150$ km s⁻¹;
  - prior de $v_p$ uniforme en $[-1000, 1000]$ km s⁻¹;
  - prior de $H_0 \propto 1/H_0$;
  - selección: $N_s(H_0)$ constante (argumento de los Methods: la selección GW depende solo de $d$ y el prior está puesto en $d$).
  - Likelihood a reproducir (ec. 9): $p(H_0\mid\cdot)\propto p(H_0)\int dd\,dv_p\,d\cos\iota\ p(x_{\rm GW}\mid d,\cos\iota)\,\mathcal N(v_r; v_p + H_0 d, \sigma_{v_r})\,\mathcal N(\langle v_p\rangle; v_p, \sigma_{v_p})\,p(d)\,p(v_p)\,p(\cos\iota)$, donde $p(x_{\rm GW}\mid d,\cos\iota)\,p(d)\,p(\cos\iota)$ se representa con las muestras de PE (ya incluyen $p(d)$), así que en este caso **no** se divide por $\pi_{\rm PE}$: el prior $d^2$ del paper es el mismo que el de PE. El reweighting por $1/\pi_{\rm PE}$ se usa en el camino general y en su test sintético (§6); acá es un control: dividir por $d^2$ y volver a multiplicar por $d^2$ tiene que dar lo mismo.
- **Resultado publicado:** MAP y HPD 68,3 % = $70{,}0^{+12{,}0}_{-8{,}0}$ km s⁻¹ Mpc⁻¹, es decir [62,0; 82,0]; media 78, desvío 15 (Methods, después de la ec. 9). Chequeo con las muestras de `Figure1.csv` (histograma de 1 km s⁻¹ Mpc⁻¹ suavizado con una gaussiana de σ = 2 bins): MAP 69,5, HPD [62,5; 82,5], media 77,8, desvío 14,5.
- **Tolerancia, escrita antes de comparar:**
  1. $|{\rm MAP} - 70{,}0| \le 3$ km s⁻¹ Mpc⁻¹;
  2. cada borde del HPD 68,3 % a $\le 3$ km s⁻¹ Mpc⁻¹ de [62,0; 82,0];
  3. distancia de Kolmogorov (máxima diferencia de CDF) entre nuestro posterior en la grilla y la CDF empírica de `Figure1.csv`: $\le 0{,}05$.

  Pasa si se cumplen las tres. Nota: las muestras de GWTC-1 no son exactamente las del paper de 2017 (el paper da $d_{\rm MAP} = 43{,}8$ Mpc; la mediana `lowSpin` es 40,0 Mpc), así que una discrepancia chica es esperable. Si no cierra en el D5, se aplica el plan B de `AGENTS.md` §14.

## 5. Barrido (provisional; se confirma después del piloto del D6)

- $\varepsilon \in \{0{,}03;\ 0{,}10;\ 0{,}30\}$. Con el ruido de amplitud más chico domina la degeneración con la inclinación, y el $\sigma_D/D_L$ medido de GW170817 (0,18 en `lowSpin`) tiene que caer dentro del rango medido. Si no cae, el piloto ajusta los valores.
- $N_{\rm gal} \in \{3,\ 10,\ 100\}$ (catálogo ralo, intermedio y casi continuo en el rango de $v$).
- $N = 1, \dots, 200$, todos los enteros.
- 200 realizaciones por celda; 9 celdas; `semilla_base = 20260925`.
- Costo medido del piloto: TODO (D6, lo mide Datos).

## 6. Test sintético del reweighting (lo especifica Modelo, D3; propuesta inicial)

- Muestras generadas con prior conocido $\pi(D_L)\propto D_L^2$ en $[1, 100]$ Mpc y $\cos\iota\sim\mathcal U[-1,1]$, con una likelihood $\mathcal L_{\rm GW}$ conocida ($D_L^{\rm true}=40$ Mpc, $\cos\iota^{\rm true}=0{,}5$, $\varepsilon = 0{,}1$), por muestreo de rechazo, $\ge 10^4$ muestras.
- Tiene que devolver la likelihood brillante $\mathcal L(H_0)$ obtenida al repesar esas muestras por $1/\pi$, comparada con la integral directa en grilla de §3.
- Tolerancia: máxima diferencia de CDF $\le 0{,}02$, y $n_{\rm eff}$ reportado.

## 7. Predicción de $N_{\rm eq}$ (Modelo, D4)

- Referencia al commit y al archivo en `notes/`: TODO (Modelo, **antes** del primer barrido).

## 8. Entregables

- Según `docs/final-project.html`: todo en el repositorio de GitHub, más **una página HTML y un PDF** para presentar.
- Idioma: castellano (el del curso y el del repo).
- `report/index.html` autocontenido (figuras en PNG desde `figures/`), y `report/informe.pdf` generado por script desde el mismo contenido. Las slides de la presentación oral (10–15 min) se arman sobre la misma página HTML, por secciones.
- Reproducción: `uv sync && uv run pytest`, más un script por experimento documentado en el `README.md`.
