# Nota de cierre · ACTO GEN2-RELEVO-TANDA-4

**Fecha:** 21/sep/2026 · **Entorno:** NUBE (`cloud_default`), corpus NO montado, cero microdato
**Encargo:** `forense/encargos/2026-09-21-GEN2-RELEVO-TANDA-4.md` (0-bis A.3, verbatim, `.cuerpo.sha256`), SHA de redacción `deddfd42`
**Rama:** `acto/gen2-relevo-tanda-4` · **PR #959** (propuesto; mesa fusiona) · **`ADR-591`** · **MODO:** ABIERTO · **Compuertas:** solo la interna de §8 (tests de P1 y P3 en verde antes de escribir un pin) — cumplida.

---

## 1 · El contador, antes y después (re-derivado, no heredado)

`[EJECUTADO: python3 tools/corrida0.py status]`, al abrir y al cerrar:

| contador | antes | después | delta |
|---|---|---|---|
| `dependencias_numericas_legacy_activas` | **150** | **146** | **−4**, exactamente las cuatro lecturas pineadas |
| `legacy_activas_por_consumidor__marco_del_duelo` | 46 | 43 | −3 (los tres `::M` de ENIGH) |
| `legacy_activas_por_consumidor__motor` | 35 | 34 | −1 (RES-0028 en `milpa/tramite.yaml`) |
| `legacy_marco_M_por_campo__M` | 4 | 1 | −3 |
| `legacy_marco_M_celdas_M_pendientes` | `DIN-M-01,FAM-M-05,FAM-M-06,FAM-M-07` | `DIN-M-01` | — |
| `N_resultados_gen2_adoptados_activos` | 71 | **72** | **+1** (RES-0028; el número que el registro dijo, no uno esperado) |
| `N_corridas_selladas` | 119 | 119 | sin mover (este acto no sella nada) |

El punto de partida **se re-derivó en la sesión** y coincidió con el 150 que el encargo
declaraba. PARO (a) —«el contador baja en más lecturas que las pineadas»— **no se
disparó**: 4 pines escritos, 4 lecturas fuera de legacy.

Las **tres clases sin fundirse**, por primera vez (4.1: «el contador muestra las clases
sin fundirlas»):

```
relevadas_por_pin_de_mesa__i_CRUDO=14
relevadas_por_pin_de_mesa__ii_CONDUCTA_GEN2=13      (antes 10)
relevadas_por_pin_de_mesa__iii_DERIVADO_DE_GEN2=1   (clase nueva)
```

14 + 13 + 1 = 28, que es el total relevado por el canal. La tercera fila **no se
tecleó** en `status`: el desglose se deriva de `pines_mesa.VIAS`, así que una vía nueva
aparece el mismo día que se firma.

## 2 · Qué salió de legacy, y por qué puerta

| lectura | puerta | RESULT citado | por qué acredita |
|---|---|---|---|
| `marco-M::FAM-M-05::M` | **(ii) `ii-CONDUCTA-GEN2`** | `RESULT-B-ENIGH-2022-P` (`CALC-B-0001`) | la conducta `recibe_remesas` de `milpa/tramite.yaml` ya declara ese RESULT con `corrida0_generacion: GEN2` |
| `marco-M::FAM-M-06::M` | **(ii)** | igual | igual |
| `marco-M::FAM-M-07::M` | **(ii)** | igual | igual |
| `tramite::civico.denuncia.miedo_desconfianza::denuncia_por_otra_razon` (RES-0028) | **(iii) `iii-DERIVADO-DE-GEN2`** | `RESULT-ENVIPE-RES0028-Q-C2-U4` (`CALC-ENVIPE-RES0028-U4-DERIVADO-0001`) | `q = 1 − p` determinista sobre el RESULT del padre `CALC-ENVIPE-0001` (SELLADA · GEN2 · `cuenta_gen2=SI` · replay `REPRODUCE/IDENTICO`); todo lo ingerido es del padre; el padre no ingiere |

**El CONTEXTO va en la `nota` del pin, no en la guarda** (firma 7bf5-01). Para los tres
`::M`: `replay-evidencia.tsv:29` dice que `CALC-B-0001` es
`REPLICA-RESULTADO · CONTEXTO-DISTINTO` — el eje RESULTADO replica, y lo único que
cambió es **un** input, `IN-B-SELECTOR` (`tools/baseline_temporal.py`, commit `67aa13d`
del 11/sep/2026, posterior al sello). **Los cuatro inputs ENIGH COINCIDEN**: ese commit
no toca el número de ENIGH 2022. Ésa era la razón por la que tres lecturas cuyo número
sí volvió a salir igual seguían contando como legacy.

Para RES-0028 el estimando lo fija **FP-391** (`decisiones.tsv:161`): persona / U4, no
unidad delito. Su `cuenta_gen2 = SI` es la **firma 3A** (`decisiones.tsv:171`) y **no se
duplicó** — ver §5.

## 3 · Qué quedó pineable tras P1 y **no** se pineó

P1 abre el eje RESULTADO **solo para las vías (ii) y (iii)**. La vía (i) sigue exigiendo
`REPRODUCE` estricto y no se tocó (relajarla es PARO (b)).

`[EJECUTADO en la sesión sobre el registro derivado]` — corridas `SELLADA` con
`cuenta_gen2 = SI` cuyo replay es afirmativo en RESULTADO **pero no `REPRODUCE`
estricto**: **11**, todas `REPLICA-RESULTADO · CONTEXTO-DISTINTO`.

| corrida | ¿algún RESULT suyo lo declara una conducta GEN2? | estado tras este acto |
|---|---|---|
| `CALC-B-0001` | **sí** — `RESULT-B-ENIGH-2022-P` | **pineado** por los tres `::M` de P2; no queda ninguna otra lectura legacy que pudiera citarlo (`[EJECUTADO]`: 0 usos legacy con ese valor o ese consumidor) |
| `CALC-ENCIG2021-CRUCES-HISTORICOS-0003` | no | **no pineable** por (ii) |
| `CALC-ENCIG2023-CRUCES-HISTORICOS-0002` | no | idem |
| `CALC-R-DIN-M-01`, `CALC-R-FAM-M-01`, `CALC-R-FAM-M-05`, `CALC-R-FAM-M-06`, `CALC-R-FAM-M-07`, `CALC-R-TRA-M-02`, `CALC-R-TRA-M-03`, `CALC-R-TRA-M-07` (8) | no | **no pineables**: son medidores de campo `R`, su puerta natural es la vía (i), que **no se relajó** |

**Conclusión, contra el `[REPORTADO]` del encargo §3:** la consecuencia de abrir el eje
no fueron «hasta 17 corridas pineables», sino **una sola** —`CALC-B-0001`— y sus tres
lecturas, que son exactamente las tres firmadas. Los 17 asientos
`REPLICA-RESULTADO · CONTEXTO-DISTINTO` del TSV se reparten entre corridas que no
cuentan, no están selladas, o cuyo camino sería la vía (i). **Este acto no pineó nada
más** (§7(c) y §10). Si mesa quisiera alcanzar esas ocho `CALC-R-*`, la pregunta que
tendría delante es la de la vía (i), que es precisamente la que el encargo declara PARO:
va a mesa como sucesor, no se resuelve aquí.

## 4 · Los 9 L: rótulo que dice lo medido

Sucesor escrito en
`forense/analisis/relevo-tanda-4/P4-los-9-L-rotulo-sucesor-v1_1.md`, **sin tocar el
`v1_0`** (A.10 · PARO (d)). Adopta `RE-DERIVADO-CON-ESTIMANDO-DISTINTO` en lugar de
`REHECHO-CON-DIFERENCIA`, porque lo medido son **dos** diferencias —agregador (media de
GEN1 vs mediana de la spec sellada) y conjunto de extracción (`L-extraido-v1_2.tsv` vs
re-extracción de las 224 capturas con `extrae_l_v1_3.py`)— y dos de las cinco
dimensiones del estimando no casan. Rótulo censado en `canon/registro-rotulos.tsv`.

La clase (iii) **no** los alcanza: `CALC-TRIADA-0001` ingiere
`snapshot-M-triada-v1_0.json`, un número de GEN1, y la guarda lo rechaza con
`RECHAZADO-DERIVADO-INGIERE-AJENO`. Hay prueba por mutación de que seguirá así.
`legacy_marco_M_celdas_M_pendientes` no los nombra y **la vista no los ofrece** como
candidatos. El CALC de L desde capturas **no se construye aquí**: queda como NC con
sucesor sin dueño.

## 5 · Hallazgo de precedencia (reportado, no reescrito)

`data/corrida0/corridas.tsv` —archivo **DERIVADO**— traía
`CALC-ENVIPE-RES0028-U4-DERIVADO-0001 · cuenta_gen2 = PENDIENTE-DE-MESA`, mientras
`data/corrida0/decisiones.tsv:171` ya declaraba `cuenta_gen2 = SI` desde la firma 3A
(commit `00ac06e9`, 21/sep 03:12); el último commit que había tocado `corridas.tsv` era
anterior (`56dc64ca`, 20/sep 21:37). **Re-derivado en esta sesión**, `corrida0` resuelve
`cuenta_gen2 = SI` con motivo «decisión de mesa (`decisiones.tsv`)»: la fuente manda y el
derivado estaba atrasado, no en conflicto. **No se escribió una segunda fila** de
decisión; el TSV derivado se re-emite por comando en la cascada de este acto. El
hallazgo es que un derivado en disco puede contradecir a su fuente durante horas sin que
nada lo grite — va a `forense/hallazgos.md`.

Segundo hallazgo, menor, también asentado: `corrida0.py status` reportaba
`relevadas_por_pin_de_mesa__ii_CONDUCTA_GEN2 = 10` mientras
`data/corrida0/pines-de-mesa.tsv` traía **12** filas `ii-CONDUCTA-GEN2`. No es un
defecto: `status` cuenta **usos activos relevados**, no filas firmadas, y dos pines de
esa vía no alcanzan hoy un uso activo. Queda dicho para que nadie lea el desglose como
un censo del TSV.

## 6 · Lo que este acto NO hizo

No relajó la vía (i) · no re-selló `CALC-B-0001` · no construyó el CALC de L · no tocó
`DIN-M-01:M` (sigue legacy, mesa lo vetó — PARO (e) respetado) · no escribió en
`milpa/**`, en `forense/prereg-duelo-v2/**` ni en ninguna spec sellada · no editó el
análisis `v1_0` · no descargó nada (el paso anti-PR#77 **no aplica**: cero payloads) ·
no adoptó nada por sí solo — la adopción es el merge de mesa (E.2).

**Falsador a tres meses (§10 del encargo):** si la clase `iii-DERIVADO-DE-GEN2` no
vuelve a usarse para el 21/dic/2026, se anota y **no se generaliza**: una puerta con un
solo habitante es una excepción con nombre, no una regla.
