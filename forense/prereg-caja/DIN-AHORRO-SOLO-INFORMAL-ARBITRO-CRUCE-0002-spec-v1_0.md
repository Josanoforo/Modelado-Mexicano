# Re-adjudicación de DIN.ahorro_solo_informal.enif2024.localidad_x_edad con piso de cadena limpia · CALC -0002 · spec v1.0

**Pre-registro de caja.** `ACTO GEN2-PISOS-GEN2-2`, 24/sep/2026, CAJA, rama `acto/gen2-pisos-gen2-2`,
0-bis `25185b7e`. Encargo: `forense/encargos/2026-09-24-GEN2-PISOS-GEN2-2.md` (P3). Congelada en el
COMMIT-1, antes de sellar el piso (P2) y antes de correr este árbitro.

Firma que la ordena (encargo §2, verbatim): Decisión 1 de ADOPCION-2 — «…hasta que un acto en caja
re-mida el piso … desde microdato y re-adjudique el cierre con un CALC sucesor -0002 que cite ese
piso por id…»; INTERPRETACIÓN-DECLARADA del encargo: se extiende a todas las celdas-D. Regla 6
(sin retadores nuevos) y PARO d (no cambiar umbral, contendientes ni agregador).

**Nombre.** El encargo escribe `…-ADJUDICACION-000N+1`; la adjudicación original de esta celda-D
se llama `CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001`, así que su sucesor es `…-ARBITRO-CRUCE-0002`
(cláusula 1, declarada).

## 1 · Herencia por identidad de archivo

| pieza | archivo sellado | cómo se hereda |
|---|---|---|
| medidor | `data/corrida0/CALC-DIN-AHORRO-SOLO-INFORMAL-ARBITRO-CRUCE-0001/medidor.py` | input `medidor_0001` (`funcion: CODIGO`, sha256 en el `spec.yaml`); **se ejecuta su `medir`, sin editar** |
| spec humana | `…-ARBITRO-CRUCE-0001/spec.md` (= `DIN-ahorro-solo-informal-lxe8-spec-v1_2`) | sha256 en `etiquetas.hereda_por_sha` |
| parámetros y semilla | `…-ARBITRO-CRUCE-0001/spec.yaml` | copiados verbatim (el test `test_c_…` lo comprueba); se añade sólo `tol_oro_0001` |

Mismos: R (cruce de ENIF 2024, bootstrap del CALC de emisiones, `PCG64(42)`, 10 000), soporte
(`n ≥ 200`), criterio por celda («INDECIDIBLE si ambos caen dentro del IC de R o si
|d_1-d_2| < 0.5·EE(R)»), umbrales de celdas (gana ≥ 6 de ≥ 6 PUNTUADA), paradas, B-bis y
**contendientes: C1 y C2 pisos, C3 challenger**. C1 y C3 siguen siendo los de las emisiones
selladas (PROSPECTIVA): no se re-emiten.

## 2 · El único cambio, y lo que se añade

**Cambio:** antes de llamar al `medir` del -0001, en la copia en memoria de las emisiones selladas
se sustituye `RESULT-DIN-LXE8-C2-P-{celda}` por
`RESULT-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-C2-P-{celda}` del piso sellado
`CALC-ENIF2024-PISOS-AHORRO-INFORMAL-LXE-0001`, **por id**. Ningún otro id de las emisiones cambia.

**Se añade:** ids renombrados `RESULT-DIN-LXE8-ARB-*` → `…-ARB2-*`; `-C2-P/IC95INF/IC95SUP-{celda}`
(copia del piso: lo que cita la celda-D); `-C2-P-EMISION-0001-{celda}` (el legacy, descriptivo);
`G-FUENTE-C2`, `G-PISO-C2-SHA256`; **oro del -0001 (E.5)**: todo id del -0001 que no depende de C2
(`-D-C2-`, `-VEREDICTO-C3-VS-C2-`, `-VEREDICTO-CELDA-`, `-G-C3-GANA-A-AMBOS-PISOS`,
`-G-C3-INDECIDIBLES`, `-G-MAE-C2`, `-G-SKILL-C3-VS-C2`, `-G-VEREDICTO-CELDA-D`) reproduce el
`resultados.json` sellado a `1e-10` (`G-CTRL-ORO-0001-*`); `G-DICTAMEN-0001` y
`G-DICTAMEN-CAMBIA`. Guardia: sellos de emisiones, -0001 y piso por sha; el piso debe declarar
`G-ORIGEN` NUEVO, `CTRL-EMISIONES-VEREDICTO = REPRODUCE` e IC `EMITIDO`; si no, **PARA**.

## 3 · Qué se espera y qué no se decide aquí

El C2 legacy y el medido difieren hasta ~1e-3 (las emisiones lo midieron: Δ máx 1.04e-3). **No se
predice el dictamen**: el -0002 corre y su primer resultado es el que se reporta, aunque difiera
del -0001 (`SIN-CANDIDATO-SUPERIOR`). Registro: `champion_actual: C2` y
`adjudicacion_por_celda` → ids `-ARB2-C2-*` si el piso no fue vencido y el oro reproduce; si C3
vence a los dos pisos, el veredicto se reporta y la adopción es de mesa. **Este acto no adopta
retadores.**

## 4 · Secuencia (heredada de #1116)

COMMIT-1 specs+código+D-22 → COMMIT-2 piso sellado → COMMIT-3a sha256 del piso en este `spec.yaml`
(`preflight` antes: BLOQUEADO **sólo** por esos dos inputs) → COMMIT-3 `run`, sello, celda-D,
`decisiones.tsv`, asientos.

## 5 · Auditoría (afirma sobre México)

Hereda la del -0001: proporciones de personas de 18+ que ahorran sólo informalmente, por tamaño de
localidad × edad; acceso y oferta antes que preferencia. **C2 RETROSPECTIVA** (piso sellado después
de R); C1/C3 PROSPECTIVA; ninguna frase las mezcla. Contadores: una corrida sellada;
`celdas_validadas` no cambia de número.

El primer resultado que produzca este procedimiento es el que se reporta.
