# Motor v5 = núcleo medible

### `motor-nucleo-medible` · **v1.0** · CANÓNICO OPERATIVO

> | | |
> |---|---|
> | **ARCHIVO** | `motor-nucleo-medible-v1_0.md` |
> | **REEMPLAZA A** | — (artefacto nuevo, sin predecesor; sellado por `ADR-237`, `ACTO MAESTRA32-E19 · SELLA-CAMINO-1`, 31/ago/2026) |
> | **VERIFICAS ASÍ** | §1 trae F-ALCANCE verbatim (firma de mesa, 31/ago/2026) · §2 trae la derivación de las fracciones `ASIGNADO`, con comando y salida cruda, fechada al escribir — no heredada de ningún acto anterior |
> | **NOMBRE ESTABLE** | **`motor-nucleo-medible`** — cítalo así, **nunca por nombre de archivo** |

*(F-CAMINO, `ACTO MAESTRA32-E19 · SELLA-CAMINO-1`, 31/ago/2026: el programa
adopta el camino 1 — re-anclar el motor al dato. Este documento es esa
ancla: define qué cuenta como el núcleo medible del programa, distinto de
la cartografía de los 30 reports temáticos.)*

---

## 1 · F-ALCANCE — texto canónico, verbatim (firma de mesa, 31/ago/2026)

El ejecutable del programa es su núcleo medible. Un dominio está ACTIVO
solo cuando tiene al menos una regla con desenlace sellado (encuesta +
variable + universo + ponderador) y `p` medida. Dominios activos a la
fecha del sello: trámite (mordida: ENCIG 2023, ENCUCI 2020). Dominios con
desenlace medido en la capa de coeficientes, candidatos inmediatos a
activación por la fase 1 de (i′): cívico/denuncia (ENVIPE 2025 `BP1_23`),
dinero/ahorro (ENNViH `cr27`, ENIF), familia/apoyo-corresidencia (EDER
2017, ENDIREH 2016, ENIF 2024). Los demás dominios del mapa conductual son
cartografía — válida como síntesis, no como salida del simulador — hasta
que crucen la misma puerta. La capa `ASIGNADO` no es deuda: es el corredor
de priors explícitos de M, parte del objeto que el duelo pone a prueba; su
fracción se reporta (hoy: 8 de 15 coeficientes y 4 de 5 reglas). Ningún
dominio se activa por prosa: se activa por regla + desenlace sellado + `p`
medida.

---

## 2 · Fracciones `ASIGNADO`, re-derivadas del árbol al escribir este acto

A.13/A.1: no se hereda la cifra de F-ALCANCE de memoria ni del acto que la
redactó — se deriva de nuevo aquí, contra el árbol tal como este acto lo
encontró (`aa920f1`), con `yaml.safe_load` y el comando a la vista.

### 2.1 · Coeficientes de generador

```
python3 -c "
import yaml
d = yaml.safe_load(open('milpa/procedencia.yaml'))
detalle = d['asignados_coeficiente']['detalle']
total = sum(len(row['coefs']) for row in detalle)
sellados = d['coeficientes_generador_sellados']
print('coeficientes totales:', total)
print('coeficientes sellados:', len(sellados))
print('coeficientes ASIGNADO restantes:', total - len(sellados))
"
```
```
coeficientes totales: 15
coeficientes sellados: 7
coeficientes ASIGNADO restantes: 8
```

**Confirma la cifra de mesa: 8 de 15.** `milpa/procedencia.yaml:asignados_coeficiente.detalle`
declara los 15 coeficientes de los seis generadores (G1×2, G2×2, G3×3,
G4×4, G5×3, G6×1). `coeficientes_generador_sellados` es la lista, en
orden de sello, de los 7 ya medidos: `G1.confianza_institucional`,
`G1.radio_confianza`, `G3.familismo_apoyo`, `G4.exposicion_violencia`,
`G4.confianza_institucional` (vía justicia), `G3.horizonte_temporal`,
`G5.familismo_apoyo` (el más reciente, `ACTO MAESTRA32-E16`, 31/ago/2026).
Los 8 restantes — `G2.sens_estatus`, `G2.aversion_riesgo`,
`G3.aversion_riesgo`, `G4.horizonte_temporal`, `G4.sens_estatus`,
`G5.familismo_obligacion`, `G5.radio_confianza`, `G6.deferencia` — siguen
`ASIGNADO`, sin estimación empírica.

### 2.2 · Reglas del dominio activo (trámite)

```
python3 -c "
import yaml
t = yaml.safe_load(open('milpa/tramite.yaml'))
reglas = t['reglas']
n = len(reglas)
n_asig = sum(1 for r in reglas if set(e.get('clase') for e in r['entonces']) == {'ASIGNADO'})
print('reglas totales:', n)
print('reglas 100% clase ASIGNADO (ninguna rama medida/cargada):', n_asig)
"
```
```
reglas totales: 5
reglas 100% clase ASIGNADO (ninguna rama medida/cargada): 5
```

**Difiere de la cifra de mesa (4 de 5) — declarado, no reconciliado en
silencio (A.10/A.13).** `milpa/tramite.yaml` (el archivo que el motor
carga) trae hoy sus 5 reglas con las 10 probabilidades de sus ramas
`entonces` marcadas `clase: ASIGNADO`, sin excepción — 5 de 5, no 4 de 5.
La medición que mesa cuenta como la quinta ya no-`ASIGNADO` — la enmienda
ENCUCI a `tramite.mordida.discrecional` (`p=0.125822` IC95%
`[0.116323,0.135544]` `n=13435`, `ACTO MAESTRA32-E18 · REGLAS-OLA5-FASE1`,
`ADR-236`) — existe, medida y sellada, pero vive únicamente en
`milpa/tramite-ola5-propuesta-v0.yaml`; su carga a `tramite.yaml` está
gateada a la firma `FP-200` (tablero, `ABIERTA` a la fecha de este acto).
"4 de 5" describe el estado que sigue a ese sello, no el estado del
archivo que el motor ejecuta hoy. Ninguna de las dos cifras es un error:
son dos universos distintos (el ejecutable cargado vs. lo medido y
pendiente de carga) — exactamente la distinción que este documento existe
para hacer explícita. F-ALCANCE, arriba, no se edita: es cita verbatim de
mesa. Esta nota es la enmienda in situ, fechada, que la acompaña.

### 2.3 · Por qué el dominio trámite cuenta como ACTIVO pese a lo anterior

La activación (F-ALCANCE §1) no exige que el `p` de decisión de
`tramite.yaml` esté medido — exige que **alguna** regla del dominio tenga
desenlace sellado y `p` medida en algún punto del árbol. `tramite.mordida.discrecional`
lo satisface por dos vías, ninguna de ellas la `clase:` de su propio
archivo: (a) los coeficientes sellados de §2.1 que miden asociación contra
ese mismo desenlace (`G1.confianza_institucional`, `G1.radio_confianza`,
vía ENCIG2023/ENCUCI2020, ver `milpa/procedencia.yaml:coeficientes_generador_medidos`),
y (b) la enmienda ENCUCI de §2.2, medida y sellada aunque no cargada. Es
la misma distinción que separa "dominio activo" (una propiedad del
conocimiento medido en el árbol) de "regla cargada sin `ASIGNADO`" (una
propiedad del archivo que el motor ejecuta hoy) — y es exactamente lo que
F-ALCANCE, §1, nombra al decir que ningún dominio se activa por prosa.

---

## 3 · Criterios de apertura (Ola 6) y de activación (corredor E) —
## enmienda fechada, 1/sep/2026

`ACTO MAESTRA33-E11 · CRITERIOS-Y-VENCIMIENTOS`, firmas de mesa 9 y 10
(verbatim, 1/sep/2026). **No sustituye ni relaja F-ALCANCE (§1) ni la
puerta de activación general que ahí queda sellada** — "ningún dominio
se activa por prosa: se activa por regla + desenlace sellado + `p`
medida" sigue vigente sin cambio. Esta sección da los criterios
*específicos*, ausentes hasta hoy (`A.8` de este acto, contra
`c7fa424`: `NO-ENCONTRADO` en este documento), para dos preguntas que
F-ALCANCE no cubre por diseño: cuándo un dominio de Ola 6 cruza la
puerta, y cuándo el corredor `E` (`L⊕M`, `ADR-141`) se considera
utilizable. Ninguno de los dos criterios se evalúa como cumplido por
este acto — ambos quedan abiertos, con su primera revisión fechada (ver
`forense/firmas-pendientes.tsv` `FP-220`/`FP-221`). `LO QUE NO HACE` del
encargo aplica sin excepción: este acto no abre ningún dominio de Ola 6,
no activa el corredor `E`.

### 3.a · Apertura de dominio, Ola 6

Firma de mesa, verbatim: **«9. Si pero dejando claro cuando se abren o
bajo qué criterios se abren».**

Un dominio candidato de Ola 6 — la ronda siguiente a Ola 5
(`milpa/tramite-ola5-propuesta-v0.yaml`), sobre dominios de
`canon/modelo-decision-v4_0.md` que Ola 5 no tocó y que hoy siguen sin
ninguna regla con desenlace sellado — **se abre**, pasa a `ACTIVO` bajo
el sentido de F-ALCANCE §1, cuando se cumplen, las tres a la vez:

1. **Scoreboard agregado con `L` sobre los 4 activos.** Existe un
   agregado publicado (`scoreboard-v1_1.md` o su sucesor) con puntos de
   `L` — no solo `M`/`R` — sobre los cuatro dominios ya `ACTIVO`
   (trámite; y los que Ola 6 mismo vaya activando, una vez abiertos)
   simultáneamente. Antes de que `L` tenga al menos un agregado
   publicado, ningún candidato de Ola 6 puede evaluarse contra este
   criterio — es lógicamente imposible que se cumpla.
2. **≥2 encuestas en corpus, ≥3 reglas candidatas `EXISTE-SATISFACE`.**
   El candidato (dominio o celda) tiene al menos dos encuestas
   distintas ya en el corpus (`data/manifiesto.yaml`/inventarios) que lo
   cubren, y `/mapea` (`.claude/commands/mapea.md`, `ADR-247`) produjo
   al menos tres reglas candidatas con veredicto `EXISTE-SATISFACE` —
   no `EXISTE-NO-SATISFACE` ni `NO-ENCONTRADO` — para ese candidato.
3. **Caja libre.** El entorno `CAJA`/Ubuntu que abre el microdato para
   verificar (2) está disponible — sin esto, (2) no se puede confirmar
   por comando, solo declarar.

**Primera evaluación:** al primer agregado que satisfaga (1), o el
15/sep/2026, lo que ocurra primero (firma 9). Recibo:
`forense/firmas-pendientes.tsv` `FP-220`
(`EVALUACION-OLA6`, dirección, `vence: 2026-09-15`).

### 3.b · Activación del corredor E

Firma de mesa, verbatim: **«10. Banca, pero deja claro los criterios de
avance».** ("Banca" = queda en la banca — definido pero no activo
todavía — hasta que los criterios se satisfagan; no es un sello de
activación inmediata.)

El corredor `E` (`E = mediana_por_cuantil({L-solo, L+corpus, M})`,
definición sellada `ADR-141`, `forense/prereg-duelo-v2/corredor-E-
combinacion-LM.py`) **se activa** — se considera utilizable para
reportar, no solo definido — cuando se cumplen, las dos a la vez:

1. **`L` y `M` con puntos en ≥8 celdas comunes.** Existen puntos de
   ambos corredores, `L` y `M`, sobre el mismo conjunto de al menos 8
   celdas del marco-M (`marco-M-sorteado-v1_1.tsv`) — la mediana de
   `E` no está bien definida con menos de tres componentes por celda
   (`L-solo`, `L+corpus`, `M`; razón ya citada en la cabecera de
   `corredor-E-combinacion-LM.py`) y con menos de 8 celdas comunes el
   agregado por corredor de `procedimiento-scoring-v1_1-PROPUESTA.md`
   no tiene base suficiente para leerse.
2. **Scoring v1_1 sellado.** `procedimiento-scoring-v1_1-PROPUESTA.md`
   (`ACTO MAESTRA33-E10`, `mesa-pendientes.md` §5) tiene la firma de
   mesa que lo sella — sin eso, "puntos" de `L`/`M` en unidades
   comparables (`z = dif/EE(R)`) no existen todavía como agregado
   oficial.

**Revisión:** al publicarse el agregado que satisfaga (1) con (2) ya
sellado, o el 30/sep/2026, lo que ocurra primero (firma 10). Recibo:
`forense/firmas-pendientes.tsv` `FP-221`
(`REVISION-CORREDOR-E`, dirección, `vence: 2026-09-30`).

**Criterio CUMPLIDO por conteo (declarado, no activado) — 3/sep/2026,
`ACTO MAESTRA36-N2 · CIERRA-N3-AGREGA-2`.** `L`/`M` con puntos en **14
celdas comunes** de `marco-M-sorteado-v1_2.tsv` (≥8; conteo mecánico en
`forense/prereg-duelo-v2/scoreboard-v1_2-AGREGADO.md` §7,
`forense/firmas-pendientes.tsv` `FP-260`, sucesora de `FP-221`) y (2)
scoring v1_1 sellado (`ADR-262`, sin cambio). Las dos condiciones de
arriba se cumplen — el criterio de activación queda declarado cumplido
**por conteo**; esta línea **no activa** el corredor `E`: la activación
es firma de mesa aparte, todavía no dada.
