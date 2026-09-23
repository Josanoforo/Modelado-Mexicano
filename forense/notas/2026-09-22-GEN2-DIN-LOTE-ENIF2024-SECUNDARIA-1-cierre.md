# Nota de cierre · `ACTO GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1` · 22/sep/2026 · CAJA

ADR raíz: `ADR-260922-GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1-65c3-01`. Encargo:
`forense/encargos/2026-09-22-GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1.md`. Ejecuta
la opción A de `FP-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01` (FIRMADA,
asentada en PR #1003).

## 0 · Qué se probó

`CALC-DIN-LOTE-ENIF2024-ADJUDICACION-T-0001`: adjudica los 5 pares
`formalidad × {sexo, edad, escolaridad, localidad, cuenta_formal}` del lote
ENIF 2024 (`ahorra_solo_informal`) en su propio estrato «universo T» (quien
trabaja, `P3_13`/`P3_10`), citando el piso C2R ya sellado de
`CALC-C2-RESTRINGIDO-IC-ENIF2024-0001` por id de RESULT y re-derivando sus
réplicas con el mismo procedimiento. `verify`: `REPRODUCE` (CONTEXTO
`IDENTICO`, 927/927 RESULT sin discrepancia). Control de reproducción del
piso: `RESULT-…-G-C2R-CONTROL-VEREDICTO = REPRODUCE`, peor delta = `0.0`
(punto re-derivado con `piso_log_aditivo` sobre marginales T re-derivadas de
esta corrida, contra el punto citado del CALC sellado — coinciden a cero
exacto, confirmando que el universo T reconstruido aquí es idéntico al que
selló C2-RESTRINGIDO).

## 1 · Corrección de premisa declarada (A.12/§0, logística, no PARO)

El encargo (§1) y la propia `FP-…4e12-01` (ya FIRMADA) citan «régimen
ARBITRO-2024, firma Q2 (`FP-260921-GEN2-DIN-LOTE-ENIF2024-COMMIT-1-6c10-04`)».
`…6c10-04` responde **Q3** (agregador de L, tema ajeno). La firma real de
**Q2** (régimen de universo del lote) es `…6c10-03`, FIRMADA
(`ADR-260922-GEN2-TRAMITE-FIRMAS-6-7c2c-01`); su verbatim en la nota de
cierre de ese acto: «Fija régimen ARBITRO-2024 para comparaciones contra el
árbitro; PILOTO-1 sólo dentro de sus celdas-D ya selladas». El intercambio
de etiquetas Q2/Q3 entre `…6c10-03`/`…6c10-04` ya fue declarado una vez
(`GEN2-TRAMITE-FIRMAS-6`) como «logística de citación, no premisa sobre qué
se mide» — y sobrevivió a esa corrección cuando se redactó `FP-…4e12-01`
horas después. Este acto usa **ARBITRO-2024** (la premisa sustantiva del
encargo se sostiene: es lo que Q2 realmente fija para comparaciones contra
el árbitro, y este CALC compara contra un piso sellado bajo ese régimen) y
corrige la cita al id real (`…6c10-03`). Detalle completo en
`forense/prereg-caja/DIN-lote-enif2024-spec-v1_0-ENMIENDA-1.md` §4.

## 2 · SUPUESTO de la cabecera — verificado, resultó falso (rama ya prevista)

«R de estos 5 pares ya fue derivado en COMMIT-3 del lote» es **falso**:
`forense/notas/2026-09-21-GEN2-DIN-LOTE-ENIF2024-COMMIT-2-3-cierre.md` §1,
verbatim, dice que los pares con `formalidad` salieron
`NO-ADJUDICABLE-SIN-PISO` — «no existe comparador R fuera de los 5 pares
primarios en este CALC»; sólo se calculó `P2` descriptivo. Además, R
restringido a T no pudo haberse derivado antes porque el piso T
(`CALC-C2-RESTRINGIDO`) no existía. El propio encargo previó esta rama:
«si resulta falso… la adjudicación es PROSPECTIVA: mejor, y se dice». Las
**28 celdas se rotulan `PROSPECTIVA`** (verificado por comando, campo
`-ROTULO` de cada celda en `resultados.json`, 28/28).

## 3 · Veredicto por par (regla v0.3, retador primario `R2`, λ = ½ fija)

| par | veredicto | ΔMAE (pp) | IC95 |
|---|---|---|---|
| `formalidadxsexo` | `NADIE-VENCE` | 0.41 | [−0.63, 0.96] |
| `edadxformalidad` | `NADIE-VENCE` | 0.61 | [−0.40, 1.14] |
| `escolaridadxformalidad` | `NADIE-VENCE` | 0.59 | [−0.23, 1.09] |
| `formalidadxlocalidad` | `PROPUESTA-CON-RESERVA` | 0.81 | [0.05, 1.37] |
| `cuenta_formalxformalidad` | `VENCE-RETADOR` | 1.29 | [0.64, 2.78] |

**Agregado sobre las 28 celdas de los 5 pares juntos** (análogo a la
comparación primaria del lote sobre sus 44, pero en T y con prefijo de
RESULT distinto — nunca sumado a esa cifra): `PROPUESTA-CON-RESERVA`,
ΔMAE = 0.70 pp, IC95 = [0.23, 1.00]. Mismo sabor cualitativo que el
veredicto primario del lote (0 < IC95inf ≤ 0.5 pp, `PROPUESTA-CON-RESERVA`,
ΔMAE = 0.48 pp) — el retador encogido por interacción histórica también
mejora modestamente sobre el piso composicional dentro de quien trabaja.

`cuenta_formalxformalidad` (la LATITUD del encargo: ¿degenerado/colineal?):
**no degenerado** — sus cuatro marginales T (dos ejes × dos categorías) dan
puntos finitos estrictamente dentro de `(0,1)` en la corrida real; ninguna
celda cayó en `NO-CONSTRUIBLE`. Es también el único par que vence
(`VENCE-RETADOR`), con el ΔMAE más grande del estrato — se reporta tal cual,
sin ajustar el procedimiento porque el resultado "se ve bien" o "mal".

## 4 · La frase de producto de las 44 celdas no cambia

```
$ grep -c "RESULT-DIN-LOTE24-ADJ-T" \
    data/corrida0/CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/resultados.json \
    data/corrida0/CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/resultados.json
data/corrida0/CALC-DIN-LOTE-ENIF2024-EMISIONES-0001/resultados.json:0
data/corrida0/CALC-DIN-LOTE-ENIF2024-ADJUDICACION-0001/resultados.json:0
```

Cero coincidencias en los dos CALC primarios del lote: el estrato T no
aparece ahí, no por acuerdo sino porque los RESULT de este CALC llevan un
prefijo propio (`RESULT-DIN-LOTE24-ADJ-T`) que ningún cómputo primario lee.
El veredicto primario del lote (`PROPUESTA-CON-RESERVA`, `R2`, ΔMAE=0.4798pp,
44 celdas) y la frase de las 44 celdas de producto **no cambian**.

## 5 · Auditoría (módulo, v2.16 §5 — este artefacto afirma algo sobre México)

Universo restringido a **quien trabaja** (T, 68–69 % de la población
elegible): sesgo de clase declarado desde `A-bis 4` — el estrato excluye a
quien no participa en el mercado laboral formal/informal (jubilados,
estudiantes, hogar, desempleo), que no es una muestra aleatoria de la
población general y sesga hacia edades económicamente activas. `formalidad`
es posición en el mercado de trabajo (acceso, no preferencia); `cuenta_formal`
es estructura de acceso bancario, no un rasgo de la persona. Ninguna cifra
de este CALC se compara contra el universo poblacional (`A-bis 4`,
`RESULT-…-G-COMPARACION-POBLACIONAL = NINGUNA`, igual que C2-RESTRINGIDO).
El par que vence (`cuenta_formalxformalidad`) cruza dos ejes de acceso
financiero entre sí — no es evidencia de un rasgo psicológico, es
estructura sobre estructura.

## 6 · Contador

`cuenta_gen2 = SI` (etiqueta de la spec, `#`927 RESULT); **no adopta** (el
piso T no se compara contra ningún estimador previo para reemplazarlo —
sucesor de firma si algún par vence). `celdas_validadas` sube en 28 (celda-D
con veredicto sellado, PROSPECTIVA). El veredicto primario del lote y la
frase de las 44 celdas no se mueven (§4). `N_resultados_gen2_adoptados_activos`
intocado.

## 7 · Latitud ejercida (§6 del encargo)

Pregunta del encargo: si `cuenta_formal × formalidad` es degenerado,
¿NO-CONSTRUIBLE o emitir? Se verificó (§3): no es degenerado en esta
corrida — se emite, con su ΔMAE y veredicto reales, sin ajuste.

## 8 · NO-CORRIDO / RESERVAS

Ninguno. Las cinco piezas (COMMIT-1, COMMIT-2, registro, esta nota, cierre)
corrieron en esta sesión.

## 9 · CONSUMIDO

`forense/encargos/2026-09-22-GEN2-DIN-LOTE-ENIF2024-SECUNDARIA-1.md` — PR
#1026. `FP-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-01`: pasa de `PENDIENTE`
a `EJECUTADA` por este acto (opción A consumida). `NC-260922-GEN2-DIN-LOTE-C2-RESTRINGIDO-1-4e12-02`
(desenlace secundario `informal_cualquiera`) sigue fuera, sin tocar.

## 10 · Corrección declarada post-ARRANQUE — E11/E13 sí eran rótulos reales

La VERIFICACIÓN A.8 de ARRANQUE (antes de que `TANDA-5-ENCARGOS-C`/PR #1016
fusionara) concluyó, correctamente para ese momento, que `E11` (§3/§8 del
encargo) y `E13` (§4) no tenían artefacto censado en el árbol. Tras fusionar
origin/main a mitad de este acto (PR #1016), quedó claro que sí lo tienen:
la propia tanda numera sus cinco encargos hermanos `E11..E15`
(`E11 = GEN2-TUBERIA-CANAL-PUBLICACION-1`, `E12 = GEN2-TRAMITE-FIRMAS-7`,
`E13 = GEN2-DUELO-ENVIPE2026-MARGINALES-2`, `E14` = este acto,
`E15 = GEN2-ADQ-F6-DIRIGIDA-1`). Consecuencias verificadas: `E11`
(TUBERIA-CANAL-PUBLICACION-1) ya fusionó antes de que este acto registrara
su corrida, así que el «orden sugerido» del encargo (§8) se cumplió sin
intervención; `E13` (DUELO-ENVIPE2026-MARGINALES-2) corrió en paralelo con
este acto (confirmado: `#1021`, COMMIT-1/2 sellados durante la misma
ventana) — sin choque de archivo ni de universo (ENVIPE 2026 vs ENIF 2024,
CALC y prefijos de RESULT disjuntos), así que la advertencia «no correr a
la vez» no se materializó en ningún conflicto real. `tests/check.py::_T25_ARCHIVOS_CONOCIDOS`
y `canon/registro-rotulos.tsv` quedaron corregidos con esta lectura al
fusionar (commit `9ae48e1a`), citando la fuente real en vez de «abreviatura
externa sin artefacto».
