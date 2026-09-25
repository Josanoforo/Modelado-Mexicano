# ACTO GEN2-PISOS-GEN2-2 · censo completo de origen de los pisos · pisos ENIF 2024 y ENVIPE 2025 re-medidos · re-adjudicaciones -0002

24/sep/2026 · CAJA · rama `acto/gen2-pisos-gen2-2` · 0-bis `25185b7e` (hhhh `2518`) · base
`origin/main` `8358b891` (merge de #1120) · encargo `forense/encargos/2026-09-24-GEN2-PISOS-GEN2-2.md`
(SHA de redacción `474a126e`, ancestro de la base). La sesión se interrumpió porque se apagó la
máquina después de P1 (`c575fed5`); se retomó sobre el mismo árbol, que estaba limpio y al día con
`origin`. No se perdió trabajo ni hubo dos escritores.

**Contadores, en una línea:** se sellan 4 CALC (2 pisos + 2 sucesores; `cuenta_gen2: SI`, no
adoptan). `celdas_validadas` no cambia de número; las dos celdas-D citan otro champion (el -0002).

## 0 · Arranque y premisas

- ENTORNO (`tools/entorno.py --sonda-red`): `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=sin_variable`
  · `raices=data_raw:SI descargas_mx:SI` · `corpus=SI(examinados=511)` → CAJA. `data/raw` →
  `/home/pc0/mm-corpus/raw`; payloads `enif2024_csv` y `envipe2025_csv` COINCIDE.
- `git ls-remote --heads origin | grep -ic pisos-gen2-2` → 1: es la rama propia (P1 empujado),
  no otra sesión.

| premisa del encargo (rótulo) | verificación | resultado |
|---|---|---|
| `[EJECUTADO]` censo #1116: DIN y TRA HEREDADO-DE-LEGACY; ENCIG resuelto por el -0002 | `censo.py --ref 8358b891` | se sostiene: 20 RESULT legacy consumidos (DIN 8, TRA 12); ENCIG ya NUEVO |
| `[SUPUESTO]` las celdas-D de Astra tienen C2 medido desde microdato | censo sobre las 21 celdas-D | ninguna de Astra consume C2 (`champion_actual` ≠ C2); sus pisos citados son NUEVO |
| `[LEÍDO]` patrón `CALC-ENCIG2023-PISOS-GOBDIGITAL-0001` (#1116) | `ls data/corrida0` | **discrepancia de rótulo**: el CALC sellado es `CALC-ENCIG2025-PISOS-GOBDIGITAL-0001` |
| P2: «piso medido desde microdato de la **ola anterior**» | spec de las emisiones y de los -0001; v2.16 §4 | **INTERPRETACIÓN-DECLARADA**: el C2 es la composición de marginales de la **misma** ola; lo legacy son los números. Se re-mide la misma ola desde el manifiesto (precedente de mesa en #1116, «Marginales 2025») |
| P3: `…-ADJUDICACION-000N+1` | nombre de las adjudicaciones originales | los sucesores son `…-ARBITRO-CRUCE-0002` (cláusula 1) |

## 1 · P1 · censo completo

Script: `forense/analisis/pisos-gen2/censo.py`. Recorre las 21 celdas-D y los 57 pisos del árbitro
y sigue la cadena **del punto**, no la de todos los inputs. Cada CALC emisor declara en `PUNTO`
qué alimenta su punto, con la línea del medidor que lo prueba; un CALC sin esa entrada sale
`SIN-CLASE`. Hay dos tablas: `censo-antes-8358b891.tsv` (base) y
`censo-completo-v1_0.tsv` (cierre, la que pide el encargo).

| universo | consumido por el marcador | clase | antes (`8358b891`) | después (cierre) |
|---|---|---|---:|---:|
| celdas-D | SÍ | NUEVO | 32 | **52** |
| celdas-D | SÍ | HEREDADO-DE-LEGACY | **20** | **0** |
| celdas-D | NO | NUEVO | 13 | 13 |
| celdas-D | NO | HEREDADO-DE-LEGACY | 3 | 3 |
| pisos del árbitro | SÍ | NUEVO | 57 | 57 |
| **total** · sin clase | | | 125 · 0 | 125 · 0 |

Las 3 filas legacy que **no** consume el marcador son celdas-D con champion BASELINE sin CALC:
`G5.familismo_obligacion.actitud` y `G5.obligacion_medida.conducta` (BASELINE.ENASIC,
`data/curacion-registro/expedientes-produccion/…`), y `G5.radio_confianza.encuci_vs_enbiare`
(BASELINE.ENCUCI, `milpa/procedencia.yaml`). No entran al camino C2 del marcador
(`tools/marcador_segmento.py::_celdas_d_c2`) y quedan fuera del «hecho». Se declaran y no se tocan.

## 2 · P2 · pisos sellados

COMMIT-1 `7dbe6660` (+ sidecars `94a25d59`), empujado **antes** de abrir cualquier ola. Preflight
VERDE en los dos.

| CALC · corrida | control 1: oro de las emisiones (1e-10) | control 2: árbitro | control 3: C2 legacy (descriptivo) | IC |
|---|---|---|---|---|
| `CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001--94a25d59af3c` (91 RESULT) | REPRODUCE (máx 0.0, 0 discordantes) | REPRODUCE en los tres tramos de edad con el mismo universo (0.0, `-N` exacto); localidad, 60+ y nacional difieren por universo, como declaró la spec §3: ΔN −1/−9/+5/−10 (10 centinelas 98/99 y 5 personas de 97) | máx \|Δ\| **1.04e-3** | 8/8 |
| `CALC-ENVIPE2025-PISOS-EVADE-NORMA-SXD-0001--58a706285ac0` (114 RESULT) | REPRODUCE (0.0) | REPRODUCE (8 `-P` a 0.0, `-N` exacto) | máx \|Δ\| **1.10e-6** | 12/12 |

Guardias: ninguna agrupación de dos ejes; en ENVIPE, `cruce()` sobre la ola cargada como
reservada lanzó `ReservaRota` (`G-GUARDIA-CRUCE-DERIVADO = NO`). Asientos E.7 (verify aislado):
REPRODUCE · IDENTICO, 91/91 y 114/114, máx \|Δ\| 0.0.

## 3 · P3 · re-adjudicaciones -0002

Cada -0002 ejecuta **los bytes sellados** del medidor del -0001 (input `medidor_0001`, sha256) con
los mismos parámetros y la misma semilla (copiados verbatim; un test lo comprueba). Antes de
llamarlo sólo sustituye el C2 de las emisiones por el del piso, citado por id. COMMIT-3a
(`sha256` de los pisos) → preflight VERDE en los dos.

| CALC · corrida | veredicto (-0001 → -0002) | MAE C2 vs R (pp) | oro del -0001 |
|---|---|---|---|
| `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0002--2214ed984778` | SIN-CANDIDATO-SUPERIOR → **SIN-CANDIDATO-SUPERIOR** (C3 no vence en 8/8) | 1.466786 → 1.502959 | REPRODUCE (139 ids, 0.0) |
| `CALC-TRA-EVADE-NORMA-SXD-ARBITRO-CRUCE-0002--9fe8fe6e378e` | SIN-CANDIDATO-SUPERIOR → **SIN-CANDIDATO-SUPERIOR** (C6/C7 vencen a C2 en 0 celdas) | 1.568052 → 1.568030 | **NO-REPRODUCE, atribuido** (§5) |

Asientos E.7: REPRODUCE · IDENTICO, 208/208 y 425/425, máx \|Δ\| 0.0.

**Celdas-D.** `adjudicacion_por_celda` de las dos celdas apunta a `…-ARB2-C2-P/IC95INF/IC95SUP-*`
(copias por id del piso). El bloque anterior se conserva como `adjudicacion_por_celda_0001`.
`margen_material` es el MAE del -0002. `momentos_holdout_refs` conserva la R del -0001 y añade el
-0002. `champion_actual: C2` no cambia (piso no vencido, firma 17/sep). `decision_ref` sigue
siendo `adopcion:piso-C2-20-celdas`. `decisiones.tsv`: 4 filas `cuenta_gen2` y 40 filas
`origen_numerico=NUEVO` (20 del piso y 20 del -0002).

## 4 · P4 · hallazgo para el informe

Tabla «pisos por origen» (la que consume el marcador: celdas-D con C2 + pisos del árbitro):

| origen | antes | después |
|---|---:|---:|
| NUEVO (cadena termina en manifiesto) | 89 | **109** |
| HEREDADO-DE-LEGACY | 20 | **0** |

**Línea para el informe v1.3:** *«Los 109 pisos que consume el marcador ya se miden desde
microdato. Los últimos 20 con marginales tecleados de la propuesta legacy (ENIF 2024 localidad ×
edad, ENVIPE 2025 escolaridad × dominio) se re-midieron y se re-adjudicaron, y **ningún dictamen
cambió**. En ENIF el piso se movió hasta 0.10 pp por celda y su error medio contra el dato subió
de 1.47 a 1.50 pp. En ENVIPE se movió ~1e-6. En los dos, ningún retador vence al piso.»* Que
nada cambie también es noticia: el relevo de origen no se compró con un cambio de veredicto.

## 5 · Defectos y discrepancias declarados

- **Oro del -0002 de TRA: `NO-REPRODUCE` con máx \|Δ\| 0.0.** Discrepan 2 de 273 ids:
  `G-SKILL-C6-VS-C2` y `G-SKILL-C7-VS-C2`. Por construcción son `1 − MAE(retador)/MAE(C2)`
  (medidor del -0001, línea 204), así que dependen de C2. Quedaron fuera de la lista de exclusión
  porque el token se escribió `-VS-C2-`, con guion final, y esos dos ids terminan en `-VS-C2`.
  Recalculados con los MAE del propio -0002, cuadran a 0.0. Los otros 271 ids reproducen a 0.0.
  Es un defecto del control, no de la réplica. La corrida sellada no se reescribe (E.3).
  El dictamen del -0002 no depende del control de oro. Línea en `forense/hallazgos.md`.
- **Pin de la celda-D en `tests/test_celdas_d.py`** (`PILOTOS_POR_ID`): pasa al -0002 (3 líneas,
  D-21, adyacente e indispensable para terminar).
- **T25:** la spec del piso ENIF menciona los tramos de edad de la lxe8 como rótulos pelados; se
  censó en `_T25_ARCHIVOS_CONOCIDOS` con la misma razón que la lxe8 v1.2. La spec está sellada:
  su sha256 vive en el `spec.yaml` sellado.

## 6 · Auditoría (afirma sobre México)

Los pisos no identifican nada: acotan a los retadores. **ENIF:** son proporciones de personas de
18 años o más que ahorran sólo por vías informales, por tamaño de localidad × edad; el gradiente
describe acceso y oferta (sucursales, corresponsales, cuenta) antes que preferencia. **ENVIPE:**
son proporciones de **delitos** (no de víctimas) no denunciados por razones atribuibles a la
autoridad, por escolaridad proxy de la víctima × dominio; describen oferta institucional antes que
actitud. Las dos unidades no se promedian entre sí. **PROSPECTIVA vs RETROSPECTIVA:** el C2 de los
dos -0002 es RETROSPECTIVO (piso sellado después de R); C1, C3, C6 y C7 conservan su marca
PROSPECTIVA. **Cifra escrita a mano:** ninguna; los umbrales son los de los -0001 y las
tolerancias se declararon en COMMIT-1.
