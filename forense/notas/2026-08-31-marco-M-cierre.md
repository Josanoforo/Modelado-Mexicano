# COMMIT-2 · cierre de MARCO-M-CONGELA (ACTO A′)

`ACTO MAESTRA32-E13 · MARCO-M-CONGELA`, 31/ago/2026. Corrida única siguiendo
exactamente la receta de `forense/notas/2026-08-31-marco-M-spec.md` (COMMIT-1),
sin reescribirla sobre la marcha.

## Reglas recorridas

`yaml.safe_load(open('milpa/tramite.yaml'))['reglas']` → **5 reglas**, todas
`dominio: tramite`: `tramite.mordida.discrecional`,
`tramite.mordida.con_registro`, `tramite.gobierno_digital.coercitivo`,
`tramite.gobierno_digital.util_sin_coercion`, `tramite.evasion_norma`.
`milpa/procedencia.yaml` recorrido completo con `yaml.safe_load` (18
secciones de nivel superior, ver spec (a) para el conteo por sección).

## Candidatos y elegibles

`forense/prereg-duelo-v2/candidatos-marco-M-v1_0.tsv` (A): **2 candidatos**
con `(regla_id real, desenlace MEDIDO, encuesta+variable citable)`:

| id | regla | encuesta/variable | base_medida | en_corpus | en_marco_60 | elegible |
|---|---|---|---|---|---|---|
| TRA-M-01 | tramite.mordida.discrecional | ENCIG/P8_3_1 | SI | SI | CIV-01 | SI |
| TRA-M-02 | tramite.mordida.discrecional | ENCUCI/AP5_1_1 | SI | SI | (vacío) | SI |

`forense/prereg-duelo-v2/marco-M-congelado-v1_0.tsv` (B): **2 filas**
(subconjunto elegible=SI == la tabla (A) completa en este barrido: ningún
candidato quedó excluido de (B) por `en_corpus` en este universo).

**N_elegibles = 2.**

Los 4 candidatos con regla real pero SOLO probabilidad `ASIGNADO` sin
encuesta/variable citada (`asignados_probabilidad`, líneas 782/788/793/799
de `milpa/procedencia.yaml`, uno por cada una de las otras 4 reglas de
`tramite.yaml`) NO entran a la tabla (A) — no hay `encuesta`/`variable` que
teclear sin inventarla (ver spec (a)). `tramite.evasion_norma` tiene **cero**
citas en `procedencia.yaml` (verificado, 0 líneas de 1944 examinadas) — no
genera ningún candidato, ni siquiera descartado.

## Desglose

**Por dominio**: `tramite` = 2 de 2 (100%). Los otros 9 dominios
conceptuales (`civico, dinero, salud, familia, tiempo, cooperacion, trabajo,
informacion, comunicacion`) aportan **0** candidatos — no porque
`procedencia.yaml` no tenga desenlaces medidos citables para ellos (los
tiene: p.ej. `G3.familismo_apoyo`, `G4.exposicion_violencia`,
`G4.confianza_institucional[justicia]`, todos con `valor_ejecutable`
sellado), sino porque **el motor real (`cargar_reglas()`, que solo lee
`milpa/tramite.yaml`) no tiene ninguna regla de esos dominios** — el criterio
EMITE exige `regla_id ∈ cargar_reglas()`, y esa función solo carga las 5
reglas de `tramite`. Este es el hallazgo estructural de este acto: **el
techo del criterio EMITE no es la disponibilidad de desenlaces medidos, es
la cobertura de dominios del motor mismo (1 de 10)**.

**Por `base_medida`**: `SI` = 2 de 2 (100%). `TRA-M-01`:
`G1.confianza_institucional`, `valor_ejecutable: -0.0645`. `TRA-M-02`:
`G1.radio_confianza`, `valor_ejecutable: -0.06626` — verificado con
`yaml.safe_load` sobre las 6 entradas de `coeficientes_generador_sellados`;
las 6 traen `valor_ejecutable` numérico (confirma la verificación previa
(ii) del encargo tal cual, 6 de 6, sin excepción).

## Control CIV-01

**PRESENTE.** `TRA-M-01` cumple la condición exacta: `encuesta=ENCIG`,
`variable=P8_3_1`, `en_marco_60=CIV-01` — misma cita
(`milpa/procedencia.yaml:937`) que usa `enlace-M-v1_0.md` para sellar el
único EMITE de las 60 originales. **Control PASA, sin forzar.**

## B-bis · interpretación (adjudicada aquí, sobre el resultado real)

`N_elegibles=2 < 15` → **"<15: viable sin sorteo (todas las elegibles)"**,
la lectura (f) del pre-registro de COMMIT-1. Si el acto B′ (`MAESTRA32-E14`)
se lanza sobre este marco-M, entra directo con las 2 filas, sin correr
`sorteo_v2.py` (que además, por regla explícita de este acto, no se editó ni
se usó — sigue con su `assert n=50` contra el marco de 60/50 original,
intacto). No es el resultado `0` que habría sido "hallazgo de que el
criterio EMITE no alcanza ni los 6 pares medidos" — sí alcanza, pero solo a
2, y solo dentro de un único dominio, por la razón estructural documentada
arriba (motor de 1 dominio de 10).

## Marco original — intacto

`marco-congelado-piloto-v1_0.tsv` (60 filas / 50 puntuables) queda **sin
tocar** como benchmark L-vs-R, verificado con `git diff --stat` (ver abajo).
El marco-M de este acto es un hermano nuevo, no un reemplazo.

## INTOCABLES — verificación final

```
$ git diff --stat main -- forense/prereg-duelo-v2/marco-congelado-piloto-v1_0.tsv \
    forense/prereg-duelo-v2/CONGELADO-v1_0.sha256 \
    forense/prereg-duelo-v2/sorteo_v2.py \
    forense/prereg-duelo-v2/tests_sorteo_v2.py \
    forense/prereg-duelo-v2/enlace-M-v1_0.md \
    forense/prereg-duelo-v2/corridas-* \
    forense/prereg-duelo-v2/scoring-adv1-m3.py \
    milpa/
(sin salida -- ninguno de estos archivos cambió)
```

## Tests

`python3 forense/prereg-duelo-v2/tests_sorteo_v2.py` → VERDE (ver salida en
el commit; el mecanismo del sorteo no se tocó, por lo que no hay razón de
diseño para que cambie, y se confirma corriéndolo).
`python3 tests/check.py --baseline` → VERDE tras registrar en `_T25_
ARCHIVOS_CONOCIDOS` los archivos nuevos de este acto que citan rótulos
pelados ya conocidos del espacio E/M en prosa narrativa (`E4`, `E6`, `E11`
— todos habitantes ya censados, ninguno nuevo).

## Discrepancias documentadas de este acto (no forzadas)

1. **`grado_dependencia` P0 vs. P1** — la regla real y sellada
   (`forense/notas/2026-08-20-act-pil-2-marco.md`) clasificaría ambos
   candidatos como `P0` (parametrizan directamente al generador `G1` del
   motor); el encargo pide `P1/P2, nunca P0`. Se resolvió con `P1` declarado
   explícitamente como desviación, no como redescubrimiento de la regla —
   ver spec (b).
2. **`ponderador` de `TRA-M-02` no encontrado** — 1944 líneas de
   `milpa/procedencia.yaml` y 46 líneas de `milpa/tramite.yaml` revisadas, 0
   coincidencias de un nombre de variable de ponderador para ENCUCI/AP5_1 —
   se deja `NO_ENCONTRADO_1944_LINEAS_REVISADAS`, no se inventa un nombre de
   variable.
## PROPAGA-3 · IDs de firma usados

El encargo pre-asignó `FP-190`, `FP-191`, `FP-192` para la fila-grito
`PROGRAMA-(i′)` y el recibo de este acto. Se usan **dos** de los tres:
`FP-190` → fila-grito `PROGRAMA-(i′)`; `FP-191` → recibo de este acto
(`MARCO-M-CONGELA`, N_elegibles=2, hallazgo estructural del motor de 1
dominio). `FP-192` queda **sin usar, reservado** — no se necesitó una
tercera fila.

el primer resultado que produjo este procedimiento es el que se reporta.
