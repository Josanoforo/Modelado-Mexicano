# Informe del programa v1.0 · ANEXO TÉCNICO

Acompaña a `canon/informe-programa-v1_0.md`.

### `informe-programa-anexo` · **v1.0** · ANEXO TÉCNICO

> | | |
> |---|---|
> | **ARCHIVO** | `informe-programa-v1_0-ANEXO.md` |
> | **REEMPLAZA A** | — (artefacto nuevo; nace junto a `informe-programa` v1.0 y no se cita solo) |
> | **VERIFICAS ASÍ** | §A.2 y §A.3 traen el comando reproducible y su salida cruda, más el control positivo contra las cifras que las notas selladas ya publicaban; §A.7 declara cada negativo con cuántos archivos examinó el comando que lo produjo (`A.13`) |
> | **NOMBRE ESTABLE** | **`informe-programa-anexo`** — cítalo así, **nunca por nombre de archivo** |
 Aquí vive cada tabla con **su
universo** (A.10) y **el comando que la produce** (A.13: todo negativo declara
cuántos archivos examinó el comando que lo produjo).

> **Estampa global.** Derivado contra `origin/main = eba9fd2` (merge de
> `PR #788`), NUBE, `corpus=NO(examinados=0)`, sin red, sin microdato, sin
> llamadas a modelos. Todas las cifras del duelo se **copian** de notas y
> artefactos sellados; ninguna se re-mide aquí. Las dos derivaciones propias
> (§A.2 y §A.3) llevan control positivo.

---

## A.1 · Estado del registro, derivado en este acto

**Universo:** el registro GEN2 completo — 180 corridas, 4 913 resultados, 207
usos. **Comando:**

```
$ python3 tools/corrida0.py status
N_corridas_requeridas=82
N_corridas_selladas=72
N_resultados_sellados=3797
N_resultados_gen2_sellados=3255
N_resultados_gen2_adoptados_activos=18
N_resultados_gen2_pendientes_adopcion=12
N_resultados_gen2_vetados_por_decision=2
resultados_con_validacion_independiente=199
diferencias_materiales=0
no_corrido_abiertas=68
corredores_envueltos_legacy=18
# derivado de 180 corridas · 4913 resultados · 207 usos
```

**Re-sello por crecimiento del universo (A.10, corolario 1).** Estas cifras se
derivaron primero contra `5973f12`. Al integrar `origin/main = eba9fd2`, tres se
movieron por `PR #788` (`ACTO GEN2-RELEVO-USOS-1`) y **se re-derivaron, no se
editaron a mano**: `adoptados_activos` **16 → 18**, `no_corrido_abiertas`
**60 → 68** (67 de `main` + las 2 de este acto − `NC-0152`, que este acto cierra),
y `dependencias_numericas_legacy_activas` **191 → 189**, la primera bajada de ese
contador en el programa. Las demás no se movieron. **Ninguna cifra del duelo
cambió:** los tres insumos sellados que §A.2–§A.4 citan están intactos entre las
dos bases (`git diff --quiet 5973f12..eba9fd2 -- <ruta>` → INTACTO en los tres) y
el comando de §A.2 reproduce su salida al dígito sobre el árbol fusionado.

**Lectura, y su límite.** `diferencias_materiales=0` dice que ninguna corrida
re-verificada difiere materialmente de su asiento; **no** dice que las 72 estén
validadas independientemente — eso son 199 RESULT de 3 255 (6.1%). El
denominador se declara en vez de omitirse.

Contexto del modelo (`tools/tablero_programa.py --json`, mismo commit): 22
reglas en el motor vivo, 21 con dato, tiers `FUERTE=20 · MEDIA=2`; 49 reglas en
`canon/modelo-decision-v4_0.md`, 27 en perímetro. `adr_max=513`, `fp_max=375`.

---

## A.2 · La dependencia de composición del resultado primario

**Universo:** `U3 = 12` celdas — las 14 del marco F5 menos `DIN-M-01` y
`TRA-M-07`, que quedaron sin punto `L_CORPUS` (16/16 abstenciones válidas) y no
aportan al denominador común. **Fuente:**
`forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/familias.tsv`, sellado por
`ACTO GEN2-F5-APRENDIZAJES-Y-SUCESOR` (10/sep/2026).

### A.2.1 · Contribuciones al MAE, por familia (verbatim del TSV sellado)

| familia/mecanismo | n celdas | n en `U3` | `L_SOLO` | `L_CORPUS` | `M` |
|---|---:|---:|---:|---:|---:|
| CIV-ENVIPE | 6 | 6 | 1.014777 | 0.842274 | **3.434614** |
| DIN-ENNViH | 1 | 0 | — | — | — |
| FAM-ENIF-APOYO | 1 | 1 | **2.143271** | **2.143271** | 0.829046 |
| FAM-ENIGH-REMESAS | 3 | 3 | 0.095670 | 0.074837 | 0.043955 |
| TRA-ENCIG | 2 | 1 | 0.503850 | 0.628850 | 0.338167 |
| TRA-ENCUCI | 1 | 1 | 0.199793 | 0.199793 | 0.340891 |

Unidad: **contribución acumulada al MAE de `U3`, en puntos porcentuales** de una
proporción ponderada. No son MAE de familia: hay que dividir entre su peso.

### A.2.2 · Las dos composiciones, y la inversión

**Comando (reproducible tal cual, sin microdato):**

```
$ python3 - <<'PY'
import csv
rows = list(csv.DictReader(
    open('forense/prereg-duelo-v2/F5-aprendizajes-sucesor-v1_0/familias.tsv'),
    delimiter='\t'))
U3, brazos = 12, ['l_solo', 'l_corpus', 'm']
tot = {b: 0.0 for b in brazos}; fam = {}
for r in rows:
    n = int(r['n_u3'])
    if n == 0: continue
    fam[r['familia_mecanismo']] = {}
    for b in brazos:
        c = float(r[f'contrib_mae_{b}_pp']); tot[b] += c
        fam[r['familia_mecanismo']][b] = c * U3 / n
for b in brazos:
    print(b, 'por_celda=%.6f' % tot[b],
          'por_grupo=%.6f' % (sum(v[b] for v in fam.values()) / len(fam)))
print('share civico en M = %.2f%%' %
      (float(rows[0]['contrib_mae_m_pp']) / tot['m'] * 100))
PY
l_solo por_celda=3.957361 por_grupo=7.315040
l_corpus por_celda=3.889025 por_grupo=7.529373
m por_celda=4.986673 por_grupo=5.028459
share civico en M = 68.88%
```

| ponderación | `M` | `L_SOLO` | `L_CORPUS` | orden |
|---|---:|---:|---:|---|
| **igual peso por celda** (la del duelo, `n=12`) | 4.986673 | 3.957361 | 3.889025 | M **último** |
| **igual peso por grupo** (`n=5` familias) | **5.028459** | 7.315040 | 7.529373 | M **primero** |

**Control positivo de esta derivación:** la columna «por celda» reproduce
exactamente los tres MAE que la nota sellada publica antes del redondeo tabular
—`L_SOLO=3.9573621816`, `L_CORPUS=3.8890257471`, `M=4.9866732398`— y el 68.88%
que cita en prosa. Sin ese control, la tabla de la derecha podría ser un error
de aritmética y no una propiedad del panel.

**MAE por familia, que es de donde sale la inversión** (contribución × 12 / n):

| familia | `L_SOLO` | `L_CORPUS` | `M` |
|---|---:|---:|---:|
| CIV-ENVIPE (n=6) | 2.029554 | 1.684548 | 6.869228 |
| FAM-ENIF-APOYO (n=1) | 25.719252 | 25.719252 | **9.948552** |
| FAM-ENIGH-REMESAS (n=3) | 0.382680 | 0.299348 | **0.175820** |
| TRA-ENCIG (n=1) | 6.046200 | 7.546200 | **4.058004** |
| TRA-ENCUCI (n=1) | 2.397516 | 2.397516 | 4.090692 |

**Qué hace la inversión, en una frase:** M es peor que L en la familia con más
celdas (cívica, 6) y mejor que L en tres de las otras cuatro. Pesar por celda
premia a quien gana donde hay más celdas; pesar por familia, a quien gana en más
familias. **El panel no distingue cuál de las dos ponderaciones es la correcta**,
y ése es el contenido real de `SIN-GANADOR-UNICO`.

**Lo que esta tabla NO es:** no es inferencia. Una familia comparte parámetro o
mecanismo y **no aporta réplicas independientes**; cuatro de las cinco tienen
una sola celda en `U3`. No hay IC, no hay prueba, no hay adjudicación.

---

## A.3 · La comparación descriptiva de 9 celdas (§D2)

**Estado: derivación propia de este informe, NO el sello de D-A.** D-A no existe
en el árbol al fecharse esto (verificado: `git ls-remote --heads origin` → 0
coincidencias con `d-a`/`informe` sobre 1 remoto; `ls forense/encargos/ | grep -c
"GEN2-D-A"` → 0 sobre 336 archivos). Cuando D-A selle, esta tabla queda
`VENCIDA EN ALCANCE` y se re-sella contra su universo — no se edita ésta.

**Universo:** las **9 celdas** que tienen simultáneamente punto de los cuatro
brazos: `B·PERSISTENCIA`, `M`, `L_SOLO` y `L_CORPUS`. Son las 10 con
`B·PERSISTENCIA` menos `CIV-M-04`, que no tiene punto `L_SOLO`.

**Procedencia de cada columna** (nada se re-mide aquí):
`B` de `ACTO GEN2-B-MARCO` (`forense/notas/2026-09-14-GEN2-B-MARCO-cierre.md` §3,
sellado); `M`, `L_SOLO`, `L_CORPUS` y `EE_R` copiados por esa misma nota desde
`CALC-C0D-MARCADOR-v3`, sellado y no re-corrido. Unidad:
`err_pp = 100·(punto − R)`.

| celda | `B`·PERS | `M` | `L_SOLO` | `L_CORPUS` | 1.96·EE_R (pp) | `B` dentro del ruido de `R` |
|---|---:|---:|---:|---:|---:|---|
| CIV-M-01 | −0.2485 | +3.5314 | −1.2749 | +4.1001 | 1.3663 | SÍ |
| CIV-M-02 | +1.5599 | +5.0913 | +60.6600 | +53.9934 | 1.2226 | NO |
| CIV-M-10 | −0.1125 | +8.9379 | +17.0066 | +49.8066 | 0.9356 | SÍ |
| CIV-M-12 | +0.5014 | +8.6201 | +1.6888 | +25.5013 | 0.9330 | SÍ |
| CIV-M-13 | +1.3500 | +9.9701 | +18.3960 | +9.9763 | 1.0567 | NO |
| FAM-M-05 | −0.6675 | −0.1765 | −0.1334 | −0.1584 | 0.2474 | NO |
| FAM-M-06 | +0.0173 | −0.1591 | +0.1465 | −0.0035 | 0.2343 | SÍ |
| FAM-M-07 | +0.3510 | +0.1919 | +0.9100 | +0.7850 | 0.1983 | NO |
| TRA-M-07 | +1.2669 | +1.3303 | +7.2435 | +7.5185 | 0.4697 | NO |

*(`CIV-M-04` queda fuera por no tener `L_SOLO`: `B`·PERS `+3.1544`, `B`·OP
`−0.0269`, `M` `+5.0645`, `L_CORPUS` `+61.3832`.)*

**Agregados, descriptivos, sin IC y sin ordenación adjudicada:**

| universo | `MAE_pp(B)` | `MAE_pp(M)` | `MAE_pp(L_SOLO)` | `MAE_pp(L_CORPUS)` |
|---|---:|---:|---:|---:|
| **9 celdas comunes** (derivación de este informe) | **0.6750** (n=9) | 4.2232 (n=9) | 11.9400 (n=9) | 16.8715 (n=9) |
| 10 celdas con `B`·PERSISTENCIA (**sellado**, B-MARCO §3) | **0.9229** (n=10) | 4.3073 (n=10) | 11.9399 (n=9) | 21.3226 (n=10) |
| 5 celdas con `B`·OPERATIVO (**sellado**, B-MARCO §3) | **0.6515** (n=5) | 6.7846 (n=5) | 11.0837 (n=4) | 30.8372 (n=5) |

**Control positivo de la derivación:** recalculando desde los `err_pp` de la
tabla de arriba, la fila de 10 celdas devuelve `0.9229 · 4.3073 · 11.9400 ·
21.3226` — idénticas al cuarto decimal a las que la nota sellada publica. Por
eso la fila de 9 celdas, obtenida con el mismo código sobre el mismo insumo, se
presenta como derivación válida y no como cifra nueva.

**Cobertura:** `B` cubre **10 de 14** bajo PERSISTENCIA (era 2) y **5 de 14**
bajo OPERATIVO (era 0). Las 4 sin `B`, con su razón verificada contra el
manifiesto y los codebooks: `DIN-M-01` (primera ola del panel ENNViH, 29
entradas en el manifiesto, ninguna anterior a 2002) · `FAM-M-01` (la batería 9.9
de ENIF **nace en 2018**; 0 coincidencias en las FD de 2015 y 2012) ·
`TRA-M-02` (ENCUCI: 2 entradas, ambas 2020 — serie de una sola ola) ·
`TRA-M-03` (ENCIG 2011 no tiene sección VIII).

**Lo que esta tabla NO hace:** no re-adjudica la tríada.
`RESULT-C0D-VEREDICTO-PAREADA = NO-DISCRIMINA` y
`RESULT-C0D-ADJUDICACION-HALLAZGO = INCONCLUSO` quedan intactos;
`SIN-GANADOR-UNICO` no se toca. No hay pareadas nuevas ni IC.

**Y la advertencia que viaja con toda lectura de B:** `B` **no es ciego**. La
contaminación está declarada **TOTAL** (`ADR-46`) — los `R`/`M`/`L` de las 14
celdas ya estaban en el repo cuando se congeló su spec. Lo que la protege no es
el desconocimiento sino la **regla fija, tonta y pre-declarada por serie**, sin
un solo parámetro que una sesión pueda calibrar hacia un resultado; y un control
positivo por celda, `REPRODUCE-EXACTO` con `Δ = 0.0` exacto en `float64`, 10 de
10, que prueba que `B` mide **el mismo estimando que el árbitro**.

---

## A.4 · La secundaria documental

**Universo:** 2 celdas (`DIN-M-01`, `TRA-M-07`) × 2 brazos contemporáneos
(`FUENTE-DIRIGIDA-v1`, `CONTEXTUAL-v2`) × 8 réplicas = **32 posiciones**, todas
corridas. **Fuente:** `forense/notas/2026-09-14-GEN2-F5-DOCUMENTAL-RUN-2-cierre.md`
(sellada), contrato `F5-documental-ejecucion-v1_1.md`, firma
`F5-documental-firma-v1_0.md` (`sha256 aa7135c8…`), aceptada por el verificador
sellado sin cambio.

| celda | dirigido | control | criterio §4.3 | veredicto |
|---|---|---|---|---|
| `TRA-M-07` | **8/8 PUNTO** trazables (7.18% las ocho; deriva de `P8_3_1`/`FAC_P18`) | 0/8 (8 ABSTENCIÓN) | ≥6/8 ✓ · 0 sustituciones ✓ · mejora 8 ≥ 4 ✓ | **ÉXITO** |
| `DIN-M-01` | **8/8 PUNTO** trazables (15.56% las ocho; deriva de `cr27`/`fac_3b`) | 0/8 (8 ABSTENCIÓN) | ≥6/8 ✓ · 0 sustituciones ✓ · mejora 8 ≥ 4 ✓ | **ÉXITO** |

Puntos verificados contra la distribución mecánica: `TRA-M-07`
`3 671 036 / 51 117 793 = 7.1815%`; `DIN-M-01`
`10 579 946 / 68 002 840 = 15.5581%`.

**Qué mide y qué no.** Mide **recuperación y análisis documental sobre el
paquete** (§4.1 de la spec). **No** prueba transferencia, **no** abre `FP-374`
ni F6, **no** toca la primaria y **no se lee junto con ella** — esa lectura
conjunta es de mesa y dirección.

**Por qué el control abstuvo, y por qué eso es correcto.** Las 16 abstenciones
previas de `L_CORPUS` en estas dos celdas fueron **válidas**: el acceso al
paquete funcionó (DIN recibió 108 455 caracteres, 40 extractos, 15 fuentes;
TRA 54 023 caracteres, 21 extractos, 9 fuentes) y en ambos prompts estaban
encuesta, año, unidad, universo, evento y codificación. Faltó **el documento
específico y evidencia cuantitativa convertible**. El brazo se abstuvo ante mucho
contexto temático no convertible — que es la respuesta correcta, no un fallo.

---

## A.5 · F6 y su compuerta

**Fuente:** `forense/prereg-duelo-v2/F5-transferencia-reservada-spec-v1_0.md`
(**PROPUESTA PARA MESA; NO AUTORIZA EMISIONES, R NI LLAMADAS**) y
`forense/firmas-pendientes.tsv` fila `FP-374`.

- **Pregunta primaria propuesta:** en familias no vistas durante
  desarrollo/ajuste, ¿M reduce ≥ **2 pp** el error absoluto medio frente a
  `L_SOLO`, sin perder más de 5 pp de cobertura?
- **Unidad de partición:** la **familia** de estimando/fuente. No la réplica, no
  una etiqueta nueva de la misma encuesta, no otra ola. «Dos celdas de una
  familia aumentan cobertura, no el número de familias independientes.»
- **Estado de la compuerta (`FP-374`, ABIERTA):** el snapshot tiene **10
  familias conocidas durante el desarrollo**, sólo 5 con al menos dos celdas y
  **0 con rol retenido ejecutable**. Faltan **18 de 18** familias disjuntas para
  el mínimo de 6 piloto + 12 confirmatorias.
- **Presupuesto NO autorizado:** 576–1 152 llamadas lógicas y 1 728–3 456
  solicitudes máximas con reintentos; 36–72 M y 36–72 R.
- **Lo que desbloquea (§D4):** la **lista nominal** de 6 piloto + 12
  confirmatorias **antes de cualquier llamada**, con pregunta, dos celdas, qué
  emite M sin conocer el objetivo, material existente/faltante, exposición previa
  y cómo se preserva la reserva. Sin ruta realista, factibilidad acotada con
  producto y parada definidos.
- **Definición de reserva, verbatim de §D4:** «retenida = no evaluada y no usada
  para afinar M, elegir reglas ni construir el contexto de L».
- `NC-0161`/`NC-0162` salen de espera **como consecuencia** de esa lista, no
  como sustituto de ella.

---

## A.6 · Filas abiertas que este informe cita y NO cierra

| fila | qué pide | por qué no la cierra este acto |
|---|---|---|
| `NC-0152` | cobertura residual de `L_CORPUS` en `DIN-M-01`/`TRA-M-07` | la mesa la declara **CERRADA citando #764** (§D5). Este acto **no** la escribe: cerrarla es acto de registro, no de informe |
| `NC-0161`/`NC-0162` | piloto y confirmación de transferencia; evaluación de un M renovado | `DECISIÓN-DE-MESA-PENDIENTE`, sucesor `FP-374`. Salen por la lista nominal (§A.5) |
| `NC-0180` | la próxima tríada con `B` de cobertura real | la cierra **D-A** al consumir B-MARCO (§D2), no un informe |
| `NC-0187` | destino de los 471 RESULT de `CALC-B-MARCO-*` | `NO-ADOPTABLE-POR-DECISIÓN`: la spec congelada declara que ninguna cifra suya entra a un veredicto ni mueve una regla. Cierra **por consumo** en D-A |
| `NC-0179` | las 4 celdas no construibles para `B` | requiere autorizar un `B` por crosswalk — fuera de la familia, decisión de mesa |
| `FP-374` | decisión sobre el experimento de transferencia | ABIERTA. La mueve la lista nominal, no este documento |

**Contexto:** `no_corrido_abiertas = 68` tras integrar `main` (ver §A.1).

---

## A.7 · Negativos de este acto, con su universo (A.13)

| negativo | comando | archivos examinados | resultado |
|---|---|---|---|
| el índice de infraestructura no cubre «documento del programa» | `grep -c "documento del programa\|informe del programa\|lector externo" data/INFRAESTRUCTURA-v1_0.md` | 1 archivo (866 líneas) | `0` → hueco real; corregido en esta entrega por regla de conducto `ADR-70(c)` |
| D-A no existe | `git ls-remote --heads origin \| grep -icE "d-a\|informe"` · `ls forense/encargos/ \| grep -c "GEN2-D-A"` | 1 remoto · 336 archivos de encargo | `0` y `0` |
| la LECTURA ESTRATÉGICA F5 v1.1 no está en el árbol | `grep -rl "LECTURA ESTRAT" canon/ forense/` | 2 174 archivos | `0` — documento de mesa, no se reconstruye |

---

## A.8 · Qué NO se tocó

`data/corrida0/` y las tres vistas del registro · `milpa/` · `forense/prereg-duelo-v2/`
y `forense/prereg-caja/` · ninguna spec, medidor, sello ni corrida ·
`forense/firmas-pendientes.tsv` · `tools/` · `tests/`.

**Contadores movidos por este acto: cero.** No sella CALC, no emite RESULT, no
adopta al motor, no hace llamadas.
