# spec.md: especificación técnica

> **Estado: BORRADOR.** Se completa en la reunión cero (D2), a partir de lo que decidan los dos integrantes. **Un agente no completa los campos `TODO` por su cuenta.** Puede proponer valores marcados como `PROPUESTA` para que los humanos decidan. Cada decisión cerrada tiene además su archivo en `decisiones/`.
>
> Una vez aprobado, este archivo es la referencia para implementar. Si hay conflicto, manda sobre `AGENTS.md`, pero no sobre `docs/final-project.html`.

---

## 1. Notación

| Símbolo | Significado | Unidades |
|---|---|---|
| $H_0$ | Constante de Hubble | km/s/Mpc |
| $D_L$ | Distancia de luminosidad | Mpc |
| $\iota$ | Inclinación (se trabaja con $\cos\iota$) | — |
| $a_{\rm obs}$, $\sigma_a$ | Amplitud observada y su ruido (modelo sintético) | TODO |
| $v_{\rm obs}$, $v_{\rm pec}$ | Velocidad de recesión observada y velocidad peculiar | km/s |
| $N_{\rm gal}$, $w_g$, $p_g(z)$ | Número de hosts candidatos, pesos, incertidumbre de redshift | — |
| $N$ | Número de eventos combinados | — |

## 2. Las cinco convenciones compartidas

Todas viven en `src/sirenas/core/` y se importan desde ahí.

### 2.1 Grilla y prior de $H_0$ · autor: Modelo · revisor: Datos
- Rango: TODO
- Resolución: TODO (se verifica convergencia al duplicarla)
- Prior: TODO (el mismo en todos los escenarios)

### 2.2 $\mathcal L_{\rm GW}(D_L,\iota)$ · autor: Modelo · revisor: Datos
- Modelo: $a_{\rm obs} = A(\iota)/D_L + \epsilon$, $A(\iota)=(1+\cos^2\iota)/2$, $\epsilon\sim\mathcal N(0,\sigma_a)$.
- Cómo se fija $\sigma_a$ para obtener un $\sigma_D/D_L$ dado: TODO
- Firma de la función: TODO

### 2.3 Métricas de información · autor: Modelo · revisor: Datos
- Nivel del intervalo creíble: TODO (¿68 %? ¿90 %?)
- $D_{\rm KL}(\text{posterior}\,\|\,\text{prior})$ en nats, integrada sobre la grilla.
- Regla del cruce para $N_{\rm eq}$: TODO (interpolar / primer $N$ que supera)

### 2.4 Regla generativa de detección · autor: Datos · revisor: Modelo
- Umbral: TODO
- Se usa la misma función en todos los escenarios: **sí** (tiene test)
- ¿Selección dentro o fuera del dominio de validez?: TODO

### 2.5 Formato de resultado y procedencia · autor: Datos · revisor: Modelo
- La interfaz de un evento:
  ```
  evento → L_j(H0): array normalizado sobre la grilla compartida
                + procedencia: {origen, semilla, config, versión del generador}
  ```
- Formato en disco: TODO (p. ej. `.npz` + `.json` o `.yaml` de metadatos)
- Qué se guarda por celda del barrido: config, semilla, hash de commit, TODO

## 3. Eventos sintéticos «tipo GW170817»

- Parámetros heredados del evento real: TODO
- Parámetros que se barren: $\sigma_D/D_L$ y $N_{\rm gal}$
- $H_0$ inyectado: TODO
- Distribución de hosts en $z$: uniforme en TODO
- Modelo de $p_g(z)$: TODO
- Sirena brillante de referencia: **sintética**, con los parámetros de arriba

## 4. Validación con GW170817

- Archivo de muestras y columnas usadas: TODO (lo completa Datos el D2)
- Prior de PE ($\pi_{\rm PE}$), leído del archivo o del paper, con la cita: TODO
- $v_{\rm obs}$, $v_{\rm pec}$, prior de $H_0$ y tratamiento de la selección, copiados de los Methods de Abbott et al. 2017, con la cita: TODO
- Tolerancia contra `Figure1.csv`, escrita antes de comparar: TODO

## 5. Barrido (se fija después del piloto del D6)

- Valores de $\sigma_D/D_L$: TODO
- Valores de $N_{\rm gal}$: TODO
- Valores de $N$: TODO
- Semillas por celda: TODO
- Costo medido del piloto: TODO

## 6. Test sintético del reweighting (lo especifica Modelo, D3)

- Prior conocido con que se generan las muestras: TODO
- Likelihood inyectada: TODO
- Qué tiene que devolver y con qué tolerancia: TODO

## 7. Predicción de $N_{\rm eq}$ (Modelo, D4)

- Referencia al commit y al archivo en `notes/`: TODO
