# Enlace M v1.1 — celda→(regla,conducta), TRA-M-02/03/07 re-apuntadas — `ACTO MAESTRA38-M13`

**Estado: re-sellado, 7/sep/2026.** Sustituye, para las tres celdas
`TRA-M-02`, `TRA-M-03`, `TRA-M-07`, el enlace v1.0 (26/ago/2026, `ADR-208`)
que `marco-M-sorteado-v1_2.tsv` seguía usando. El enlace v1.0 **no se
borra ni se edita** — sigue íntegro en `marco-M-sorteado-v1_2.tsv`,
registro de lo que el marco decía antes de esta re-sellada (A.10, corolario
1). Este documento y `marco-M-sorteado-v1_3.tsv` son la nueva capa: copia
byte a byte de `v1_2` con un solo cambio de columna (`conducta`) en tres
filas — verificado (`diff` por columna y por línea, ver A.8 abajo).

## 1 · Por qué el enlace v1.0 está vencido en alcance (A.10)

El enlace celda→(regla,conducta) de `marco-M-sorteado-v1_2.tsv` para
`TRA-M-02/03/07` apunta a `regla=tramite.mordida.discrecional,
conducta=paga_mordida` — la fila `ASIGNADO` (`p=0.62`,
`milpa/tramite.yaml:50`). Ese enlace se selló el 26/ago/2026, **cinco días
antes** de que la firma DM del 1/sep/2026 (`ADR-270`/`ADR-276`,
`milpa/tramite.yaml:44-49`) declarara: *"se conserva como historia — NO se
borra —, se sustituye por el MEDIDO de abajo en el cálculo del motor"* →
`paga_mordida_encig2025`, `p=0.085118`,
`clase: "MEDIDO·p(tasa base ponderada)"` (`milpa/tramite.yaml:60`). No hay
ruta causal por la que el enlace v1.0 pudiera haber leído una firma que
todavía no existía: no es un error del enlace v1.0, es que el universo
cambió debajo de él (A.10, "vencido en alcance", no "incorrecto al
sellarse").

Verificado hoy, sin re-derivar nada (A.8, comando a la vista):

```
$ grep -n "paga_mordida" milpa/tramite.yaml
50:      - {conducta: paga_mordida, p: 0.62, clase: ASIGNADO}
60:      - {conducta: paga_mordida_encig2025, p: 0.085118, clase: "MEDIDO·p(tasa base ponderada)"}
```

`milpa/src/emisor.py:emitir_binaria` recibe la `conducta` como argumento
explícito y devuelve la primera coincidencia de `regla.entonces` con ese
nombre exacto — no hay ambigüedad de cuál emite: el marco decide, columna
por columna, qué conducta se lee. Cambiar la columna es el único
mecanismo por el que el motor deja de leer `paga_mordida` y empieza a leer
`paga_mordida_encig2025`, para las mismas tres celdas, sin tocar
`milpa/tramite.yaml` ni `milpa/src/emisor.py`.

## 2 · El re-apuntado — exactamente tres filas, exactamente una columna

`marco-M-sorteado-v1_3.tsv` = `marco-M-sorteado-v1_2.tsv` byte a byte,
con la columna `conducta` cambiada de `paga_mordida` a
`paga_mordida_encig2025` en las filas `TRA-M-02`, `TRA-M-03`, `TRA-M-07`.
Ninguna otra columna de esas tres filas cambia — ni `regla`
(`tramite.mordida.discrecional`, sin cambio), ni `clase_procedencia`,
`ola_calibracion`, `grado_sellado`, `grado_transferencia`, `grado_DD`
declarados por v1.2 (que describen la fila ANTES del re-apuntado; se
declaran vencidos por el mismo A.10, no se re-derivan aquí — ver §3).

**Verificación (A.8):**

```
$ diff <(cut -f1-18,20- marco-M-sorteado-v1_2.tsv) <(cut -f1-18,20- marco-M-sorteado-v1_3.tsv)
(sin salida -- todas las columnas salvo `conducta` (col. 19) son idénticas)
$ diff marco-M-sorteado-v1_2.tsv marco-M-sorteado-v1_3.tsv
13,15c13,15  (3 líneas difieren -- exactamente TRA-M-02/03/07, exactamente el
              token `paga_mordida` -> `paga_mordida_encig2025`)
```

## 3 · Las 11 celdas restantes — por qué NO cambian

`diagnostico-14-celdas-v1_0.tsv` (Pieza 1, congelada antes de este
documento) censa, para las 14 celdas, si existe una enmienda MEDIDA
firmada de mesa sobre la misma conducta base. Resultado: **solo
`tramite.mordida.discrecional` (TRA-M-02/03/07) trae una enmienda MEDIDA
con firma de mesa citada explícitamente por este encargo** (DM,
1/sep/2026, `ADR-270`/`ADR-276`). `civico.denuncia.miedo_desconfianza`
(`CIV-M-*`), `familia.apoyo.recibe_dinero_familiares` (`FAM-M-01`) y
`familia.seguro.volatilidad_ausencia_estado` (`FAM-M-05/06/07`) no traen
ningún bloque `enmienda_*` en `milpa/tramite.yaml` — sus conductas ya son
`MEDIDO` sin sustituto en pugna, y no hay nada que re-apuntar.

**Hallazgo reportado, no aplicado (obligación de la Pieza 1, no decisión
de este documento).** `dinero.ahorro.tiene_ahorros` (`DIN-M-01`) **sí**
trae un bloque `enmienda_enif2024` (`milpa/tramite.yaml:623-651`:
`tiene_ahorros_enif2024`, `p=0.642080`, `MEDIDO`, campo `sustituye`:
*"MEDIDO ENNViH 2005-06 de arriba en el cálculo — se conserva íntegro, no
se borra (firma c1)"*, sellada por firma c1, mesa, 2/sep/2026, `ACTO
MAESTRA35-N1`) — misma forma que la enmienda de mordida (mismo verbo
"sustituye ... en el cálculo", misma firma de mesa citada por su propio
`sellada_por`). Este documento **no re-apunta `DIN-M-01`**: las firmas de
mesa que este encargo propaga (§ Firmas de mesa, cabecera) citan
`tramite.mordida.discrecional`, no `dinero.ahorro.tiene_ahorros` — aplicar
el re-apuntado de `DIN-M-01` sin una firma de mesa que lo cite sería una
decisión nueva, no la propagación de una ya firmada (SELLA-3: "el ejecutor
propaga, no decide"). Queda declarado aquí y en `diagnostico-14-celdas
-v1_0.tsv`, fila `DIN-M-01`, para que mesa decida si abre un acto sucesor
análogo a este.

`segmentacion_ejes_enif2024` (dentro del mismo bloque YAML de
`dinero.ahorro.tiene_ahorros`) declara `fuente_regla:
"dinero.ahorro.via_informal"` — una regla distinta — y sus ejes
(sexo/edad/escolaridad/formalidad/tiene_cuenta) no coinciden con el
estrato de `DIN-M-01` en el marco (`PENDIENTE`): no aplica a esta celda
bajo ningún re-apuntado.

## 4 · Limitación de escala/ola declarada (A-bis 3) — no se «ajusta»

El `MEDIDO` que sustituye está calibrado en **ENCIG 2025**
(`milpa/tramite.yaml:104`, campo `ola_calibracion` de
`enmienda_encig2025`). Los tres árbitros de estas celdas son de **olas
distintas**:

| celda | árbitro (encuesta, ola) | ola_calibracion del MEDIDO | coinciden |
|---|---|---|---|
| `TRA-M-02` | ENCUCI, 2020 | ENCIG 2025 | NO |
| `TRA-M-03` | ENCIG, 2013 | ENCIG 2025 | NO |
| `TRA-M-07` | ENCIG, 2021 | ENCIG 2025 | NO |

Se compara la **misma escala** — proporción de personas que declaran haber
pagado una mordida en un trámite discrecional, `[0,1]` en las tres filas,
`MEDIDO·p(tasa base ponderada)` en las tres — y se **declara el desfase de
ola**, tal como A-bis 3 exige. No se interpola, no se re-pondera y no se
promedia el `MEDIDO` de `ENCIG 2025` hacia `2013`/`2020`/`2021`: la serie
completa de 8 olas (`milpa/tramite.yaml:109-117`, `serie_olas`) ya existe
para quien quiera leer el punto de la ola específica en vez del más
reciente — este documento no la sustituye, solo declara que el `MEDIDO`
que Pieza 2 aplica es el de `2025`, la ola más reciente, por ser la que la
firma DM citó explícitamente (`ADR-270`/`ADR-276`).

Para `TRA-M-02`, la ola del árbitro (`ENCUCI 2020`) coincide exactamente
con la ola de una conducta MEDIDO **distinta** de la misma regla
(`paga_mordida_encuci2020`, `enmienda_encuci2020`, `FP-200=b`) — que
Pieza 2 **no** aplica (§3, `diagnostico-14-celdas-v1_0.tsv`, fila
`TRA-M-02`): aplicar esa conducta en vez de la de `2025` volvería la
celda `P0 VERIFICACION` (no puntúa bajo F-DD), un efecto ya declarado por
`corridas-M/M-TRA-M-02.json` (`aviso_F_DD_abierto_por_FP_200b`), sin
cambiar aquí — decisión de mesa, sucesor declarado.

## 5 · Efecto en `grado_DD` (F-DD, `ADR-237`) — declarado, no re-derivado en el marco

Bajo la conducta nueva, las tres celdas comparan `(encuesta,ola)` de la
celda contra `ola_calibracion=ENCIG 2025` del `MEDIDO`: en ningún caso
coinciden (tabla §4) → las tres siguen `P1 PUNTUA` bajo F-DD, igual que
bajo `paga_mordida` (que comparaba contra `ENCIG 2023`, también sin
coincidir). El veredicto F-DD no cambia de signo para ninguna de las tres
celdas — el re-apuntado mueve el punto `M` (`0.62` → `0.085118`) y la
`clase` (`ASIGNADO` → `MEDIDO`), no la exclusión de F-DD. Las columnas
`grado_DD`/`razon_DD` de `marco-M-sorteado-v1_3.tsv` **no se re-escriben**
(§2: un solo cambio de columna, `conducta`) — quedan con el texto de v1.2,
que cita la comparación contra `ENCIG 2023` (la ola del `ASIGNADO`
`paga_mordida` que ya no se lee); este párrafo es la corrección declarada
de esa columna para quien la lea después de este documento, sin tocar el
archivo.

## 6 · Qué NO hace este documento

No cambia `p` ni `clase` de ninguna regla en `milpa/tramite.yaml`. No
re-apunta `DIN-M-01` (§3 — reportado, no aplicado). No re-corre
`emite_m.py` ni escribe ningún `M-<id>.json` nuevo en
`corridas-M/` (fuera del perímetro de este acto) — el valor `M` para las
tres celdas re-apuntadas se deriva en `agregado_v1_3.py` (Pieza 3), en
memoria, vía `emitir_binaria(regla, 'paga_mordida_encig2025')`, el mismo
camino que `tools/emite_m.py` usa para escribir archivos. No abre `D1`
(corredor `P`). No decide si `DIN-M-01` se re-apunta en un acto sucesor.

---

## 6 · Reconciliación de columnas ejecutada — `ACTO MAESTRA38-M13 · M-POR-CELDA v1.3` (7/sep/2026)

**Este apartado se añade después de que `PR #592` fusionara.** No borra ni
reescribe nada de §1-§5: los deja fechados. Lo que cambia es que la
corrección que §5 dejó **declarada y sin tocar el archivo** ya está
**aplicada al archivo**, por mandato del §9 del encargo final
(`forense/encargos/2026-09-07-MAESTRA38-M13-M-POR-CELDA-v1_3.md`): «No
dejar columnas que contradigan el nuevo enlace».

**Qué queda vencido de este propio documento.** Tres afirmaciones de §2 y
§5 eran ciertas cuando se escribieron y dejan de serlo con la
reconciliación — se declaran aquí en vez de editarlas arriba:

1. §2 «`marco-M-sorteado-v1_3.tsv` = `marco-M-sorteado-v1_2.tsv` byte a
   byte, con la columna `conducta` cambiada» — ahora son **cinco**
   columnas en las tres filas TRA.
2. §2 «Ninguna otra columna de esas tres filas cambia» — cambian además
   `frase_discriminacion`, `ola_calibracion`, `razon` y `razon_DD`.
3. §5 «Las columnas `grado_DD`/`razon_DD` **no se re-escriben** … sin
   tocar el archivo» — `razon_DD` **sí** se re-escribe. `grado_DD` **no**:
   sigue `P1 PUNTUA` en las tres, que es lo que §5 predijo y lo que §9 del
   encargo final espera.

**Diff exacto sobre `marco-M-sorteado-v1_3.tsv` (5 columnas × 3 filas):**

| columna | qué decía | qué dice |
|---|---|---|
| `conducta` | `paga_mordida_encig2025` (ya re-apuntada por `PR #592`) | sin cambio en este acto |
| `frase_discriminacion` | `… -> paga_mordida (…` | `… -> paga_mordida_encig2025 (…` — sólo el prefijo; el paréntesis describe el desenlace de la celda y no se toca |
| `ola_calibracion` | `ENCIG 2023` (ancla del `ASIGNADO`) | verbatim de `milpa/tramite.yaml:104` (`enmienda_encig2025`) |
| `razon` | «`!= ola_calibracion ENCIG 2023 de la regla`» | «`… ENCIG 2025 de la conducta paga_mordida_encig2025 (enmienda_encig2025, milpa/tramite.yaml:104)`» — una cláusula; C1/C2, `grado_sellado` y la inconsistencia declarada de `cv_arbitro` no se tocan |
| `razon_DD` | comparaba contra `ENCIG 2023` por la conducta `paga_mordida` | compara contra `ENCIG 2025` por `paga_mordida_encig2025`, más una cláusula de linaje que conserva `0.62`/`ENCIG 2023` **como pasado explícito**, no como estado vigente |

**Lo que NO se movió**, verificado columna a columna: las 8 que el §9 del
encargo protege (`variable`, `ponderador`, `cv_arbitro`, `grado_sellado`,
`grado_transferencia`, `encuesta`, `ola`, `universo`) — **ninguna**; y
`clase_procedencia`, que describe el estimador del árbitro, no la clase
que emite el motor.

**Control mecánico (§9).** Las **11/11** celdas no afectadas son idénticas
entre `v1_2` y `v1_3`: mismo `sha256` de sus 11 filas
(`cd3f4401a6ba7d05…`), `diff` vacío. Universo, IDs, orden y 32 columnas
sin cambio.

**Lo que §5 no podía cerrar y este acto sí.** §5 declaraba el efecto F-DD
«sin tocar el archivo» porque el `M` de las tres celdas se calculaba **en
memoria**. El encargo final §2 corrige esa premisa: el agregado no consulta
el motor vivo, lee `corridas-M/M-<id>*.json`, así que *cambiar la conducta
en el marco sin reemitir M no tiene efecto en el agregado*. Por eso este
acto **materializa** el enlace en tres archivos nuevos —
`corridas-M/M-TRA-M-02__v1_3.json`, `…-03__v1_3.json`,
`…-07__v1_3.json` — emitidos por `tools.emite_m.emite_celda` con
`fuente_acto = ACTO MAESTRA38-M13 · EMITE-M-v1_3`. Los tres
`M-TRA-M-0*.json` históricos quedan intactos.

**`ola_calibracion` ahora se resuelve POR CONDUCTA.** §4 de este documento
leía la calibración del `MEDIDO` a mano; `tools/emite_m.py` no lo hacía —
resolvía por regla y devolvía el fijo `ENCIG 2023` para cualquier conducta
de `tramite.mordida.discrecional`. Corregido en el COMMIT 1 de este acto:
`paga_mordida → ENCIG 2023` (`:79`), `paga_mordida_encuci2020 → ENCUCI
2020` (`:86`), `paga_mordida_encig2025 → ENCIG 2025` (`:104`). Sin eso,
los tres JSON v1.3 habrían nacido citando el ancla equivocada.
