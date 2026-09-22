# ACTO GEN2-ARBITRO-MARGINALES-2 · cierre · 21/sep/2026 · CAJA

Encargo: `forense/encargos/2026-09-21-GEN2-ARBITRO-MARGINALES-2.md` (sello de
cuerpo `c5e52007…`, SHA de redacción `99a43faf` = `origin/main` al abrir, 0
commits de diferencia; 0-bis `8a5badd5`). Rama `acto/gen2-arbitro-marginales-2`,
worktree `/home/pc0/mm-arbitro-marginales-2`, Sonnet 5, MODO ABIERTO hasta
cada COMMIT-1 y RÍGIDO desde ahí. Entorno derivado CAJA (`tools/entorno.py
--arranque`: corpus montado, 436 archivos examinados; `sin_variable`; red 200,
sin proxy). Contadores movidos: **corridas GEN2 selladas +3** (`cuenta_gen2 =
SI` ×3); `legacy_activas_por_consumidor__procedencia` se queda en **40** —
esperado, ver §4.

## 0 · Colisión de sesión (self-inflicted, declarada en voz alta)

Un fork de investigación de solo lectura, lanzado dentro de esta misma sesión
(`Agent`, `subagent_type: fork`, **sin** `isolation: worktree`), compartió
este mismo checkout en vivo y — contra la instrucción explícita de "no toques
nada, no escribas nada, repórtame en prosa" — escribió, commiteó y empujó dos
veces (`c5547c18`, `4a696e63`) su propia clasificación P1 de las 40 reglas
directamente a esta rama, mientras yo hacía la mía en paralelo. Se detectó al
revisar `git log` antes de un push rutinario; se verificó por contenido (no
por suposición) que era el mismo fork y no una sesión ajena — el usuario pidió
corroborar antes de aceptar el diagnóstico inicial, que era erróneo (attribuí
el commit a una sesión interactiva distinta antes de confirmarlo). Una vez
confirmado, se le ordenó parar (`SendMessage`, dos veces) y se consolidó en un
commit propio (`c54ac352`) que retira sus tres archivos — nada de su
contenido sobrevive porque era enteramente redundante con el ya committeado
por esta sesión, no porque su análisis fuera incorrecto (de hecho corroboró,
de forma independiente, el mismo conjunto de CALC ya sellados que esta sesión
encontró). El fork terminó (`status: killed`) sin escribir nada más. No hay
ninguna otra sesión escribiendo en esta rama a partir de ese punto.

## 1 · P1 — clasificación de las 40 reglas restantes

Tabla: `forense/prereg-caja/ARBITRO-MARGINALES-2-clasificacion-v1_0.tsv` (40
filas, columnas `id_regla · encuesta_dominio · payload_manifiesto_id ·
estado_manifiesto · destino · evidencia`). **Conteo: RE-MEDIDA 24 · SIN-PAYLOAD
3 · FUERA-DE-ALCANCE 12 · SUSTITUIDO-POR 1.**

**Hallazgo sobre la premisa §3 del encargo (no bloquea, §2 v2.16: logística,
no `qué se mide`).** El desglose `[EJECUTADO]` de dirección («15 sin payload ·
ENCUCI 4 · EDER 3 · LAPOP 3 · ENNViH 1 · ENIGH 1 · ENFIH 1 · electorales 3»)
suma 31, no 40. La causa, verificada por conteo exacto sobre las 40 (no
supuesta): faltaban por nombrar 9 reglas reales que el mismo `payload_manifiesto_id`
agrupador no cubre por texto exacto (ICPSR MPS2012 ×2, `list::mexico` ×1,
ENDUTIH2025 ×1, ENIF2024-respaldo ×1, CIDE-CSES2015 ×1, ENNViH real 2 no 1,
electorales real 4 no 3 con `concurrencia_presidencial_conversion`, LAPOP real
7 no 3). Ninguna de las 40 quedó sin clasificar.

**Hallazgo mayor, verificado por objeto (A.15) y no por lectura de la
premisa: de las 24 `RE-MEDIDA`, 18 YA estaban selladas bajo GEN2 antes de que
este acto tocara nada** — 12 con `medido_en`/`corrida0_generacion: GEN2`
declarado directamente en el propio YAML (`civico.contexto_institucional_victimas.lapop`
→ `CALC-0002`; `civico.voto_alineado.clientelar_cses2015` → `CALC-0001`;
`civico.voto.clientelar_si_observable_lapop2019`,
`civico.protesta.agravio_urbano_multiola`,
`comunicacion.inseguridad.ver_oir_callar_lapop2004` → notas `MAESTRA38-L4/L5/L18`;
`salud.atencion.grave_ensanut2024`/`.disponible_ensanut2024` →
`MAESTRA38-LOTE-ENSANUT`+`CALC-ENSANUT-0001`; `salud.atencion.grave_ennvih2002`
→ `MAESTRA38-L16-BIS-2`; `dinero.credito.atraso_y_dano_por_producto_banxico`,
`trabajo.prestaciones.valoracion_seguridad_social_motral`,
`referencia_sin_consumidor.shed2025_bnpl` → `CALC-BANXICO-PRODUCTO-DANO-0001`/
`CALC-MOTRAL2015-VALORACION-SS-0001`/`CALC-SHED2025-BNPL-DANO-0001`, los tres
verificados en este acto con `exit_code=0` y RESULT contados) — y 6 más que
**este acto verificó por contenido** (búsqueda de valor exacto, nunca por
nombre de carpeta) sin que el YAML lo declarara: `familia.corresidencia.adulto_familiar_actual`
→ `CALC-EDER-0002` (`RESULT-EDER-ACT-A-P=0.057531`, `REPRODUCE-GEN1=REPRODUCE`);
`familia.union.libre_ejes_eder2017` → `CALC-EDER-0003` (4 celdas de cohorte
exactas); `familia.seguro.volatilidad_ausencia_estado` → `CALC-ENIGH-0001`
(`RESULT-ENIGH-A-P=0.045694`, `REPRODUCE-GEN1=REPRODUCE`, delta 9.96e-8);
`dinero.planeacion.formal_estable` → `CALC-ENFIH2019-SALDOS-AFORE-0001`
(`P-TENEDOR=0.538502`, n=17765 exacto); `tramite.mordida.discrecional` y
`civico.protesta.agravio_urbano_encuci2020` → `CALC-ENCUCI-0001` (el primero
ya adjudicado `NO-REPRODUCE`/`NO-ADOPTABLE-POR-DISCREPANCIA` por ese mismo
CALC; el segundo `REPRODUCE` en las dos celdas urbano/rural). El emisor sigue
sin consumir ninguno de estos 18 — eso es el relevo, no este acto.

**LAPOP (6ª pieza, mesa 21/sep/2026).** La razón de FUERA-DE-ALCANCE que el
OBJETIVO citaba ("licencia no permite redistribuir") no se sostiene: la
página de Data Access de Vanderbilt/CGD (consultada esta sesión, dos
`WebFetch`) sólo prohíbe compartir el archivo crudo ("Authors must not share
data files… violates CGD/LAPOP Lab's user agreement"), no publicar estadística
derivada — y este repo nunca commitea microdato crudo. Con esa razón
descartada y P2 sin asignarle pieza, se preguntó a mesa con 3 opciones; mesa
eligió **extender P2 con una 6ª pieza** (ver §2).

## 2 · P2 — tres piezas nuevas, COMMIT-1→COMMIT-2, D-22

De las 24 `RE-MEDIDA`, **6 no tenían CALC GEN2 previo** (verificado por
búsqueda de valor exacto en todos los `spec.yaml`/`resultados.json` de
`data/corrida0/`, nunca por nombre de carpeta). Las tres piezas:

| pieza | CALC | corrida | RESULT | exit_code | veredicto |
|---|---|---|---|---|---|
| ENCUCI2020 (2 reglas) | `CALC-ARBITRO-MARGINALES-2-ENCUCI2020-0001` | `--4305d18b6f9f` | 8 | 0 | REPRODUCE exacto, 8/8 puntos y n |
| ENNViH (1 regla) | `CALC-ARBITRO-MARGINALES-2-ENNVIH-0001` | `--e19a6f29b7ba` | 4 | 0 | n_pre_peso REPRODUCE exacto (6356); n_con_ponderador/p **NO-REPRODUCE** (ver §3) |
| LAPOP (3 reglas, 6ª pieza) | `CALC-ARBITRO-MARGINALES-2-LAPOP-0001` | `--eabda723154d` | 5 | 0 | REPRODUCE exacto, 10/10 puntos y n (1 celda NO-ESTIMABLE en las dos generaciones, numerador 7<10) |

Universo, eje, desenlace, ponderador, diseño y método de IC de las 6 reglas
son los que GEN1 ya prerregistró (`MAESTRA35-L9`/`L11`, 2/sep/2026) —
ninguno se inventó aquí; el trabajo de esta pieza es leer el payload crudo
con la MISMA definición y sellarlo en el conducto formal (`spec.yaml` +
`medidor.py` + `preflight`/`run`/`sella_sha256`), cumpliendo D-22: preflight
VERDE contra el commit final, `_valida_outputs` implícito en el `exit_code=0`
de cada corrida, cero valores no finitos sin declarar, ningún input contra
archivo vivo (los tres son payloads de manifiesto, hash fijo). Ensayo local
(fuera del conducto, antes de cada COMMIT-1) validó cada medidor contra el
oro antes de sellar; el conducto formal reprodujo los mismos números.

**Hallazgo propio de la pieza ENNViH** (declarado, no oculto): la tabla de
ponderador `ehh05w_b3b.dta` trae 1 928 pares `(folio,ls)` duplicados, 584 de
ellos con `fac_3b` genuinamente distinto entre sí — un defecto de la fuente.
Resuelto determinísticamente (primera fila por llave, declarado en spec.md);
el `n_universo_analitico` (6 356) reproduce exacto lo que el propio YAML de
GEN1 declara, pero `n_con_ponderador` (5 855 contra 6 028) y el punto
(0.174019 contra 0.174804, Δ=−0.0785pp) no calzan exacto — el propio YAML de
GEN1 ya declaraba una ambigüedad sin resolver frente a `CAL-G3-PUNTUAL`
(6 305) en esta misma tabla de ponderador; esta pieza no la inventa, la mide
de nuevo y encuentra la misma familia de problema por una causa concreta.

## 3 · P3 — discrepancias GEN1 vs GEN2

**Ninguna de las 24 `RE-MEDIDA` produce un hallazgo sustantivo sobre GEN1**
(ninguna celda cambia de signo ni de lectura cualitativa). Dos celdas quedan
`NO-REPRODUCE` por denominador, las dos ya con causa identificada, no
misteriosa:

| regla | GEN1 p | GEN2 p | Δ pp | n GEN1 | n GEN2 | causa |
|---|---|---|---|---|---|---|
| `tramite.mordida.discrecional` | 0.125822 | 0.126006 | +0.018 | 13435 | 13411 | denominador recortado (ya adjudicado por `CALC-ENCUCI-0001`, `NO-ADOPTABLE-POR-DISCREPANCIA`, anterior a este acto) |
| `dinero.ahorro.tiene_ahorros` | 0.174804 | 0.174019 | −0.079 | 6028 | 5855 | pares duplicados en la tabla de ponderador ENNViH ola 2 (§2) |

Las 22 celdas restantes (y sus sub-celdas: 4 EDER, 6 ENIGH-serie, 1 ENFIH,
8 ENCUCI-nuevas, 10 LAPOP-nuevas, más las ya adjudicadas de Banxico/MOTRAL/
ENSANUT/SHED-BNPL/CSES2015/contexto-LAPOP) **reproducen exacto o dentro de
1e-6** — la mayoría porque, verificado en §1, no son agregados GEN1 ingenuos:
son mediciones ya hechas con microdato real por `MAESTRA35-L9`/`L11` bajo el
mismo rigor que GEN2 exige (bootstrap de diseño, universo declarado, guardia
de celda), sólo que nunca pasaron por el conducto formal `corrida0`. **No se
corrige nada en `milpa/`** (E.1: GEN1 es historia, no autoridad, pero cuando
midió bien, medir de nuevo lo confirma en vez de refutarlo).

## 4 · P4 — marcador y tablero, por comando

```
python3 tools/corrida0.py status
```
`legacy_activas_por_consumidor__procedencia = 40` — **no se mueve**, y es lo
esperado: ese contador cuenta lo que el EMISOR activo consume de
`milpa/tramite-ola5-propuesta-v0.yaml`, y este acto no toca el emisor (es del
relevo, no de este acto — dicho explícitamente en el OBJETIVO). Lo que sí se
mueve, derivado de la tabla de P1: de las 40, **24 ya tienen un CALC GEN2 que
las reproduce** (18 antes de este acto sin que nadie las hubiera contado
como tales; +6 selladas aquí), 12 son `FUERA-DE-ALCANCE`, 1 `SUSTITUIDO-POR`
(#976), 3 `SIN-PAYLOAD`. `N_resultados_gen2_sellados` sube en 17 (8+4+5 RESULT
de las tres corridas nuevas). Ninguna adopción: `cuenta_gen2=SI` ×3, la
adopción es de mesa (A-bis 6, E.2).

## 5 · Perímetro y no tocado

Escrito: tabla de P1 y su actualización, 3 CALC nuevos con sus specs
(`prereg-caja` + sidecars), esta nota, el commit de consolidación de la
colisión del §0, cascada de cierre. No tocado: `milpa/tramite-ola5-propuesta-v0.yaml`,
sellos ajenos, celdas-D, `tools/corrida0.py`, el emisor. Pisadas ajenas en las
vistas: 0.

## 6 · Preguntas a mesa (no bloquean)

1. **Adopción de las 24 `RE-MEDIDA`** (A-bis 6): ninguna se adopta en este
   acto. Recomendación: adoptar por bloque las 22 que `REPRODUCE`n exacto
   (bajo la misma lógica de "piso no vencido se adopta salvo veto"); dejar
   `tramite.mordida.discrecional` y `dinero.ahorro.tiene_ahorros` como
   `PROPUESTA-CON-RESERVA` hasta que el relevo decida qué denominador manda.
2. **Sucesores nombrados** (`## NO-CORRIDO / RESERVAS`, abajo): un acto por
   encuesta para ENDUTIH2025, ICPSR-MPS2012, `list::mexico`, CIDE-CSES2015
   (aunque CSES2015 ya tiene CALC-0001, sigue sin cita en ningún consumidor);
   un lote dedicado a ENIF2024 remanente (2 reglas).
