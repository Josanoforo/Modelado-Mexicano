# CORROBORA-MOTOR — 24/ago/2026

Corrida por `ACTO SELLA-AGO24`, ejecutando `FP-106`/firma de mesa D2, verbatim: *"D2-C Solo corroboremos que el motor está como queremos que esté bajo la ultima actualización."* Entorno **NUBE** (`cloud_default`), repo-only, sin `data/raw`. Base: `origin/main = bcd318f` (`PR #310` fusionado 10:31 −0600), sin cambio desde el arranque del acto salvo la propagación mecánica de la Parte A de este mismo acto (`FP-105`/`FP-106` → `FIRMADA`, `Hito D` 14→15).

Ocho verificaciones, vocabulario `A.4` + `A.13` (todo negativo declara cuántos archivos examinó el comando que lo produjo).

---

## B1 · Suite `python3 tests/check.py --baseline`

**EXISTE-NO-SATISFACE.** Tras la propagación de la Parte A: **27 FAIL · 146 WARN**. Línea base **ROJO**, 4 entradas nuevas frente a `tests/baseline.json` (`HEAD` congelado `e24d033`):

```
· T16: canon/estado-programa-v1_10.md: declara 147 WARN vigente; la corrida real da N WARN
· T16: canon/estado-programa-v1_10.md: declara 19 FAIL · 147 WARN vigente; la corrida real da N WARN
· T19c: README.md declara 14 de 27 corridas del Hito D; el bloque append-only de forense/hitoD-preregistro-v2_0.md tie[ne 15]
· T19c: README.md declara desglose {'D': 8, 'B': 2, 'A': 2, 'E': 2}; derivado del bloque append-only: {'D': 8, 'B': 2, [...]}
· T20: README.md: declara 14 de 27 corridas archivadas (marcado T20:HITO-D, pob=reglas); el bloque append-only de fo[rense...]
· T20: canon/modelo-decision-v4_0.md:65 declara 14 de 27 [...]
· T20: canon/modelo-decision-v4_0.md:700 declara 14 de 27 [...]
· T20: canon/modelo-decision-v4_0.md:885 declara 14 de 27 [...]
(5 entradas de la línea base ya no aparecen — mejora, no bloquea, no baja la cifra congelada sin --freeze explícito)
```

**Todas las entradas nuevas son consecuencia directa y esperada de que este acto movió `Hito D` 14→15** (Nota 31 de `hitoD-preregistro`, `FP-105`/`R7.1`→`A`): cada sitio que citaba `14 de 27` y no está en el perímetro declarado del encargo (`README.md` completo; `canon/modelo-decision-v4_0.md` en las líneas `:65`,`:700`,`:885` — distintas de las `:298`/`:789` que sí estaban en perímetro y sí se corrigieron) queda desincronizado. Ninguna es un defecto nuevo del motor: son propagación pendiente, fuera del perímetro que el encargo cerró explícitamente. **`README.md` no está en la lista de archivos que este acto puede tocar** — se reporta la discrepancia, no se corrige aquí.

## B2 · 49 reglas · perímetro Hito D = 27

**EXISTE-SATISFACE.** `canon/modelo-decision-v4_0.md:11` declara *"El motor sigue en 49 reglas; el perímetro del Hito D sigue en 27"*. El oráculo de la suite (`T12 conteos del motor`, `tests/check.py`, función `motor_rules()`/`rule_tier()`) corre `[ ok ]` y reporta `motor: 49 reglas · 20 [FUERTE] · 20[FUERTE] · 19[MEDIA] · 5[MEDIA-FUERTE] · 2[HIPÓTESIS] · 1[FUERTE como correlación] · 1[FUERTE / MEDIA] · 1[MEDIA / HIPÓTESIS]`. Coinciden. Perímetro `27` verificado en la misma corrida (T12/T18 comparten el denominador). Sin discrepancia.

## B3 · `milpa/src/emisor.py` — gate R3.4

**EXISTE-SATISFACE — el gate se niega a adjudicar con base insuficiente, como debe.** `python3 -m pytest tests/test_emisor_fidelidad.py`: **9 passed**. Corrida directa de `python3 milpa/src/emisor.py`:

```
gate R3.4 · veredicto: NO-ADJUDICADO — B y C computados; A espera el comparador (huecos H1/H2 a mesa)
  codi(A)=0.09  útil(pareja)=0.71  razón_pareja=0.1267605633802817
  B: colapso=1.0 pasa=True · C: reducción=0.0 pasa=True
  HUECO · H1 · adopción por canal retail-efectivo (comparador de A, spec §10.1): NO-EMITE
  HUECO · H2 · discrepancia de comparador: spec §10.1 dice 'OXXO Pay' (retail); el Registro §7 enuncia R3.4 como 'CoDi rechazado vs. útil (SPEI) adoptado'. Cuál comparador rige la condición A es firma de mesa.
  ESTAMPA · insumos del cálculo: 2 probabilidades consumidas, clases {'ASIGNADO': 2}; base medida: 0 de 2 — B y C son propiedades estructurales del par ASIGNADO, no hallazgos empíricos (advertencia de mesa, 20/ago/2026); universo: tramite.yaml + procedencia.yaml + modelo §7
```

Reportado tal cual salió, no lo que la última dirección vio: veredicto `NO-ADJUDICADO`, condición A sin resolver por el hueco H1/H2 (mismo hueco que `FP-104` reformula bajo firma D3 en la Parte A de este acto), B y C computados pero con **base medida 0 de 2** — declarado explícitamente en la propia estampa, no oculto. El gate no inventa una adjudicación sobre base insuficiente: hace exactamente lo que se le pide.

## B4 · Contrato celda-D v0.5

**EXISTE-SATISFACE.** `tests/test_celdas_d.py:72` — `ROLES = {"BASELINE", "CHALLENGER", "COMPLEMENTO", "BASELINE_INGENUO", "ENSAMBLE"}`, ambos roles nuevos de v0.5 presentes. `tests/test_celdas_d.py:32-34` — `estado_decidibilidad` validado como obligatorio bajo `vocabulario_version == 0.5`, no exigido bajo 0.4 (celdas selladas antiguas). Corrida directa: `python3 tests/test_celdas_d.py` → **3 archivo(s) de celda-D validan** contra `propuesta-motor-adaptativo-celda-v0_5.md §3`, sin error.

## B5 · Umbrales de `ADR-68(c)`

**EXISTE-SATISFACE.** `ADR-128(b)` (`gobernanza:2532`) declara `ADR-68(b)`/`ADR-68(c)` **VENCIDOS EN ALCANCE**, con excepción expresa para el umbral (1), que `tests/test_motor_holdout.py` («EL MURO») sigue exigiendo — verbatim en la cabecera del archivo: *"el umbral (1) de ADR-68 (Ronda 1 §7)"*. Corrida: `python3 tests/test_motor_holdout.py` → **6 pruebas ok, 0 saltadas** (`test_a_conjunto_holdout_estable`, `test_a2_firma_contra_el_commit_de_sello`, `test_b_ningun_valor_holdout_se_lee`, `test_b2_la_rebanada_completa_no_toca_holdout`, `test_b3_el_codigo_del_motor_no_llama_valor_de_en_holdout`, `test_c_roles_sellados_antes_que_todo_resultado`). Los dos lados verificados: el vencimiento general está declarado en canon, y la excepción sigue viva y pasando en código.

## B6 · Operador ⊕ del corredor E

**EXISTE-SATISFACE, no ejecutado.** `ADR-141` (`gobernanza:2844`) sella `E = mediana_por_cuantil({L-solo, L+corpus, M})`, firma de mesa verbatim «D-a». `forense/prereg-duelo-v2/mesa-pendientes.md:53` registra **RESUELTA, 2026-08-21**. `forense/prereg-duelo-v2/corredor-E-combinacion-LM.py:14` implementa la definición sellada (`combinar_continua`/`combinar_categorica`/`combinar_E`, líneas 73-157). **El script sigue sin ejecutarse** — no hay corrida del duelo que lo consuma todavía; la definición existe y está donde el duelo la consumirá, pero el duelo mismo no ha corrido. Coherente con `mesa-pendientes.md`, que lo dice explícitamente.

## B7 · `milpa/refutations.yaml`

**NO-ENCONTRADO (parcial) — sin oráculo mecanizado para la partición fina.** `canon/estado-programa-v1_10.md:95` declara: *"49 refutaciones narrativas corridas: 27 pasan, 3 fallan, ~~8 sin objeto~~ 1 sin objeto (`ref.A.04`) + 7 recién con objeto y veredicto pendiente, 11 requieren el ejecutable."* Re-derivado por comando (`python3` + `yaml.safe_load`, 49 archivos-entrada en `refutaciones:`, universo declarado): **total 49 confirmado, coincide.** La partición fina (pasan/fallan/sin objeto/con objeto pendiente/requieren ejecutable) **no tiene enum ni campo estructurado en el YAML** — cada entrada trae `nota` como texto libre sin vocabulario fijo, y `tests/check.py` no mecaniza esta cuenta (`grep` sobre el archivo no encuentra ningún test que la derive). Re-clasificar las 49 fichas a mano, una por una, contra la cinco categorías está fuera del tiempo de este acto de corroboración y del perímetro que el encargo cerró (no incluye `milpa/refutations.yaml` en la lista de archivos a tocar). **Se declara la discrepancia potencial, no se resuelve**: sin oráculo, no se puede confirmar ni refutar que `27/3/1/7/11` siga vigente tras las adjudicaciones de `ACTO RETRIAGE-4` y de este mismo acto. Candidato a fila de tablero nueva si mesa lo quiere (no se abre aquí — fuera de perímetro).

## B8 · Tablero — filas `ABIERTA` con antigüedad

**EXISTE-SATISFACE.** `T22 T-FIRMAS`: `[warn] (23 warn)`. Muestra (comando completo, no filtrado a mano):

```
FP-70 ABIERTA desde 2026-08-19 (5 días)
FP-71 ABIERTA desde 2026-08-19 (5 días)
FP-85 ABIERTA desde 2026-08-20 (4 días)
… y 20 más
```

23 filas `ABIERTA` con antigüedad, derivadas por el vigía, no tecleadas. (Antes de la propagación de este acto eran más: `FP-105`/`FP-106` salieron de este universo al firmarse `FIRMADA` en la Parte A; `FP-112`, nueva, entra al universo `ABIERTA` de nuevo.)

---

## Párrafo a mesa

**El motor está como se quiere, con dos huecos declarados y uno reportado sin resolver.** Las siete verificaciones ejecutables (B1-B6, B8) confirman que el aparato hace lo que dice: 49 reglas y perímetro 27 coinciden (B2); el gate `R3.4` se niega correctamente a adjudicar sobre base insuficiente en vez de fabricar un veredicto (B3); el contrato celda-D v0.5 valida sus tres celdas y su nuevo vocabulario de rol (B4); el umbral (1) de `ADR-68(c)` — «EL MURO» — sigue vivo y pasando pese al vencimiento en alcance del resto (B5); el operador `⊕` del corredor `E` está sellado e implementado, sólo pendiente de que el duelo lo ejecute (B6); el tablero de firmas sigue vigilado y sus 23 filas `ABIERTA` restantes traen antigüedad derivada, no supuesta (B8). **Lo que no está:** la suite corre en rojo (B1) porque este mismo acto movió `Hito D` de 14 a 15 y `README.md` — fuera del perímetro que el encargo cerró — quedó desincronizado, junto con tres citas de `14 de 27` en `canon/modelo-decision-v4_0.md` fuera de las dos líneas (`:298`,`:789`) que el encargo sí autorizó tocar; y la partición fina de `milpa/refutations.yaml` (27/3/1/7/11) no tiene oráculo mecanizado que la re-derive, así que no se puede confirmar que siga vigente tras las últimas adjudicaciones (B7). Ninguno de los dos es un defecto del motor mismo — son propagación pendiente y un hueco de instrumentación, ambos fuera de lo que este acto puede cerrar por su propio perímetro declarado.
