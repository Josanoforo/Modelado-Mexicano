# HITO D · Paso 2 · Corrida **R1.3** — propuesta de veredicto, no adjudicada
### `hitoD-R1.3` · **v1.0** · 4 de agosto de 2026 · **Canal de confianza personal → adopción**

> | | |
> |---|---|
> | **ARCHIVO** | `hitoD-R1_3-veredicto-v1_0.md` |
> | **REEMPLAZA A** | — *(nuevo)* |
> | **VERIFICAS ASÍ** | la propuesta es fila `E` (acotada), trae penetración y brecha rural-urbana con IC95%, la validación de canalización, y la corrección de canalización del join `NIV` declarada antes de reportar cifra alguna |
> | **NOMBRE ESTABLE** | **`hitoD-R1.3`** |
> | **ESPECIFICACIÓN CONGELADA** | `forense/hitoD-R1_3-especificacion-v1_0.md`, commit previo a este — no se editó tras ver el resultado |

> ⚠️ **ARTEFACTO FORENSE FECHADO — append-only.** Registra lo hallado el 4/ago/2026 contra ENIF 2024 (microdato, tabla `TMODULO`, payload `enif2024_csv.zip`, hash verificado COINCIDE antes de abrir el ZIP — ver reporte de arranque de este acto). No se actualiza: reescribirlo para que cuadre con el estado posterior sería la racionalización post-hoc que el Bloque C prohíbe. **Este veredicto NO está archivado** — es una propuesta para que mesa adjudique (Nota 29 de `hitoD-preregistro-v2_0.md`).

---

## 1 · Lo que estaba pre-registrado *(citado literal, para probar que no se movió)*

> **Regla.** `hitoD-preregistro-v2_0.md`, R1.3: *"SI se ofrece un producto financiero por un canal de confianza personal ENTONCES sube la adopción; sin puente, desconfía — PORQUE G1"* — `[FUERTE]`.
>
> **Falsador.** Producto con penetración masiva en el segmento popular por canal 100% digital, sin sucursal y sin recomendación estructurada.
>
> **Umbral (tres condiciones).** Penetración ≥10% de adultos del segmento popular · brecha rural-urbana <10 puntos · sin programa de referidos que explique el grueso de las altas.
>
> **Construibilidad, resuelta en la especificación (§1), ANTES de abrir el ZIP:** condiciones 1 y 2 construibles con ENIF 2024 (mismo instrumento); condición 3 inconstruible en ninguna fuente pública — confirmado contra `cruce-catalogo-fichas-v2_0.md:50-51`, ya archivado.
>
> **Árbol de decisión fijado ANTES de correr (`especificacion §2`):** si falla al menos una de las dos condiciones evaluables → propuesta `E` (acotada); si ambas cruzan su umbral → propuesta `C` (el umbral de tres condiciones no puede decidirse sin la tercera). Nunca `A` — la condición 3 nunca es evaluable con estas fuentes.

---

## 2 · Corrección de canalización — declarada antes de reportar cifra sustantiva

La especificación (§3.3) preveía leer `NIV` (proxy de segmento popular) uniendo `TMODULO.LLAVEMOD = TSDEM.LLAVESDE`. Al ejecutar la unión, `TSDEM.niv` resultó blanco en **30,866 de 44,374 filas (69.6%)** del roster completo de personas del hogar — incluidas filas que, verificadas contra `EDAD`, corresponden exactamente al respondiente del módulo (edad idéntica entre `TSDEM.edad` y `TMODULO.edad_v` para la misma llave), es decir, blanco incluso para la persona cuya educación se necesitaba. `TMODULO` trae su propia copia de `niv`/`gra`/`edad_v` (mismos códigos, misma pregunta 2.6, mismo catálogo de 13 valores del FD) **sin ningún blanco: 0 de 13,502 filas**.

**Decisión:** se usa `TMODULO.niv` directamente. No hay unión a `TSDEM` en el cómputo final — ambas tablas comparten universo de llave, pero solo `TMODULO` trae el campo poblado en este release público. **No es cambio de especificación:** la variable (escolaridad, códigos 00-11/99, wording de la pregunta 2.6) y su punto de corte (`NIV`∈{00,01,02,03}) son exactamente los que el commit 1 congeló; lo único que cambió es de qué tabla física se lee un campo duplicado entre `TMODULO` y `TSDEM`. El defecto es indiferente al valor de `P5_4_8` (no hay selección sobre el desenlace) y se descubrió sin haber visto ninguna cifra sustantiva de penetración o brecha.

```
tmodulo rows: 13502
TSDEM.niv blanco: 30866/44374 (69.6%), incluye respondientes edad-verificados
TMODULO.niv blanco: 0/13502
```

---

## 3 · Universo y composición

| | n |
|---|---|
| Universo TMODULO (ENIF 2024, personas 18+ seleccionadas) | 13,502 |
| Segmento popular (`NIV`∈{00,01,02,03}) | 6,884 (50.9%) |
| — urbano (`TLOC` 1-3) dentro de segmento popular | 4,672 |
| — rural (`TLOC` 4) dentro de segmento popular | 2,212 |

Distribución `NIV` completa del universo: 00=532 · 01=20 · 02=2,697 · 03=3,635 · 04=15 · 05=261 · 06=2,808 · 07=324 · 08=2,853 · 09=52 · 10=256 · 11=44 · 99=5.

---

## 4 · Validación de canalización

Penetración de `P5_4_8=1` ("¿Usted tiene cuenta contratada por internet o aplicación (no bancaria) como Mercado Pago, Nu o Spin de Oxxo?") sobre el **universo TOTAL** (sin restringir a segmento popular), como chequeo de que la unión/filtro/ponderador está bien construido — no es ancla académica, es chequeo de orden de magnitud declarado en `especificacion §4`:

**p_hat = 9.47%**, SE=0.37pp, IC95%=[8.75%, 10.19%], n=13,502, 190 estratos, 2,164 UPM, 0 estratos singleton.

Orden de magnitud consistente con la "paradoja fintech" ya citada en `canon/integrador-psicologia-mexicano.md:214` (Nu >13M usuarios) — sin ser la misma escala (cifra de empresa sobre su propia base vs. tasa poblacional con denominador de adultos ENIF), la canalización no arroja un número absurdo (ni 0.1%, ni 90%), lo que corrobora que el join/filtro/ponderador de este pipeline está razonablemente construido.

---

## 5 · Condición 1 — Penetración, segmento popular

`prop_ultimate_cluster` sobre `(EST_DIS, UPM_DIS, FAC_PER, y=P5_4_8)`, universo = segmento popular (n=6,884):

**p_hat = 3.86%**, SE=0.32pp, IC95%=[3.23%, 4.48%], 189 estratos (4 singleton), 1,773 UPM.

**No cruza el umbral de ≥10%.** Decisivo, no caso límite: el límite superior del IC95% (4.48%) queda muy por debajo del umbral — a diferencia de `R5.2`/Nota 18, aquí no hay reserva estadística que declarar, la no-satisfacción es limpia.

---

## 6 · Condición 2 — Brecha rural-urbana, segmento popular

| | p_hat | SE | IC95% | n | estratos (singleton) | UPM |
|---|---|---|---|---|---|---|
| Urbano (`TLOC` 1-3) | 4.74% | 0.43pp | [3.90%, 5.59%] | 4,672 | 150 (4) | 1,593 |
| Rural (`TLOC` 4) | 1.76% | 0.31pp | [1.15%, 2.37%] | 2,212 | 51 (10) | 180 |

**Brecha = |4.74% − 1.76%| = 2.98pp**, SE_brecha = √(0.43² + 0.31²) = 0.53pp, IC95%=[1.94pp, 4.03pp] (asumiendo independencia entre submuestras rural/urbana — válido: son estratos de diseño disjuntos, ninguna UPM pertenece a ambos).

**Sí satisface el umbral de <10 puntos.** También decisivo: el límite superior del IC95% (4.03pp) queda muy por debajo de 10pp.

---

## 7 · Aplicación del árbol de decisión — propuesta: fila `E` (acotada)

Por `especificacion §2`, Rama 1 aplica cuando falla **al menos una** de las dos condiciones evaluables — no requiere que fallen ambas. Aquí la Condición 1 falla de forma decisiva (3.86% << 10%); la Condición 2 sí se satisface (2.98pp < 10pp), pero eso no mueve el resultado a Rama 2, porque Rama 2 exige que **ambas** crucen.

**Propuesta: `E`** — *"el falsador corrió limpio en penetración y brecha rural-urbana, y no se satisfizo — la regla sobrevive esta prueba, acotada porque la condición 3 (canal de alta desagregado) nunca pudo evaluarse."*

**Lectura del desenlace, tal como se pre-declaró en `especificacion §2` antes de correr nada:** las cifras de Nu que circulan en el corpus (13-15M de clientes, `canon/glosario-v5_6.md:152`, `canon/modelo-decision-v4_0.md:371`, `forense/hitoC-prueba-generadores.md:55`) tienen como denominador la propia base de clientes ya adoptantes de la empresa. Medida contra el denominador poblacional correcto — adultos del segmento popular, único disponible con el universo que la ficha exige — la penetración del canal 100% digital sin sucursal es 3.86%, lejos de "masiva". La brecha rural-urbana chica (2.98pp) es real entre quienes adoptaron, pero es consistente con una adopción todavía baja y pareja en ambos entornos, no con una adopción masiva sin brecha. **Nu es una vanguardia de mercado, no representativa aún del grueso del segmento popular medido a escala nacional** — el primer dato poblacional (no de la propia fintech) sobre esta pregunta específica en este corpus.

---

## 8 · Límites declarados, sin maquillar

- **"Segmento popular" = escolaridad ≤ secundaria (`NIV`∈{00-03}).** Único proxy disponible en ENIF — no hay ingreso ni NSE en el instrumento. Otra definición (AMAI, ingreso) podría diferir; no construible con esta fuente (declarado en `especificacion §3.3`, no descubierto después).
- **Estratos singleton** (varianza no estimable con `ultimate cluster`): 4/189 en la corrida de penetración popular, 10/51 en la corrida rural. Minoritarios — no invalidan los IC reportados, pero el rural tiene proporcionalmente más (n menor).
- **Condición 3 no se intentó** con el proxy imperfecto declarado en la especificación (`P5_14`/`P5_15_2`/`P5_16`, referidos a "última cuenta", no al producto bajo prueba): no era necesario para decidir la rama (la Condición 1 ya la decide por sí sola) y hacerlo hubiera sido verificación sin retorno sobre un resultado que no iba a cambiar.
- **ENDUTIH no se usó.** Solo se exploró su FD (estructura) — declarado como contaminación parcial en `especificacion §6`. No hay llave que lo una a ENIF a nivel de unidad, y su ítem más cercano a "banca digital" (`P8_13_7`/`P8_16_7`, banca móvil de BBVA/Citibanamex/Santander) mide justo el producto contrario (con sucursal) al que el falsador exige.
- **No hay ancla académica publicada** para "penetración de cuentas fintech 100%-digitales, segmento de baja escolaridad, por localidad rural/urbana" — declarado antes de correr, en `especificacion §4`. El chequeo de canalización (§4 de este documento) sustituye validación de estimando, no la reemplaza.

---

## 9 · Reproducibilidad

Script ejecutado (no commiteado — vive en scratchpad de sesión, mismo criterio que otros actos de este corpus para cómputos de una sola corrida): lee `enif2024_csv.zip:conjunto_de_datos_tmodulo_enif_2024/conjunto_de_datos/conjunto_de_datos_tmodulo_enif2024.csv`, filtra por `niv` (columna propia de `TMODULO`, no unión a `TSDEM`), llama `tests/svystat.py: prop_ultimate_cluster` con `(est_dis, upm_dis, fac_per, y)` para universo completo, segmento popular, y las dos particiones rural/urbana dentro de segmento popular. `tests/svystat.py` no se modificó.

**Declaración ADR-46:** al abrir `conjunto_de_datos_tmodulo_enif2024.csv`, esta sesión queda inhabilitada para pre-registrar ninguna otra ficha contra ENIF.
