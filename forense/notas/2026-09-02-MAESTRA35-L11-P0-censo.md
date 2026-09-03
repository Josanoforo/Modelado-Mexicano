# `ACTO MAESTRA35-L11 · ROBUSTECE-L9` — `P0` · censo `A.4`

> | | |
> |---|---|
> | **ACTO** | `MAESTRA35-L11 · ROBUSTECE-L9` |
> | **ENCARGO** | `forense/encargos/2026-09-02-MAESTRA35-L11-ROBUSTECE-L9.md` (A.3) |
> | **BASE** | specs heredadas de `forense/notas/2026-09-02-MAESTRA35-L9-spec.md` (§2.1, §3.1, §4.1, §5.1, §6.1) — **verbatim**, sólo cambia el instrumento |
> | **ENTORNO** | UBUNTU con corpus. `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` vacía · `data/raw` enlazada a `/home/pc0/mm-corpus/raw` (symlink) · `ls data/raw/ | head -1` → no vacío (examina el corpus completo, no cero archivos) |
> | **QUÉ ES** | El censo `A.4` de los dos instrumentos que este acto abre para robustecer (a), (b) y (c) — antes de cruzar nada contra el desenlace |
> | **VERIFICAS ASÍ** | `python3 tools/medidor_l11_encuci2020.py --censo` |

---

## §0 · Contaminación declarada (`ADR-46`), antes de la spec y no después

Esta sesión abrió **estructura, etiquetas de variable y marginales univariados**
de dos payloads del corpus: ENCUCI 2020 (`data/raw/BD_ENCUCI2020_dbf.zip`,
tablas `SEC_4_5`, `SEC_6_7_8`, `SD`) y Latinobarometro 2024
(`data/raw/latinobarometro2024_bd_stata.zip`, `Latinobarometro_2024_Stata_esp_v20250817.dta`,
332 columnas, metadatos únicamente). **No** se calculó ninguna tabla cruzada del
desenlace contra el moderador antes de este commit.

## §1 · Verificación de identidad de los payloads

| payload_id | sha256 (verificado) |
|---|---|
| `encuci2020_bd_dbf` | `0414fd59e2afcc36294530687c721e8e86bd04e76ad95bfce4b7b2e70853f283` — COINCIDE con `data/manifiesto.yaml:1004` |
| `latinobarometro2024_bd_stata` | `469a94c55395b36c4d1f013851a7e79d0619620640a64653eca79afce21f5e97` — COINCIDE con `data/manifiesto.yaml:9748` |

## §2 · Pieza (a) · `R7.7` — turnout ≠ vote-choice: ninguno de los dos instrumentos la satisface

**ENCUCI 2020 → `EXISTE-NO-SATISFACE`.** Sección 8 (Delitos electorales) trae
`AP8_1_1`/`AP8_1_2` («¿Usted conoce personalmente a alguien que haya recibido
dinero/regalos para votar por algún partido político?», elecciones de 2018,
6 673 / 13 754 sí, sobre 20 171 válidos) — es **exposición de red**, no
**recepción propia** de la dádiva, que es el antecedente exacto que `spec §2`
exige (`clien1na`: «LE ofrecieron un beneficio»). Y no hay ningún ítem de **por
quién votó** en 2018: `AP7_13`/`AP7_13A` preguntan simpatía de partido en 2020,
no el voto emitido en 2018. Los dos elementos que la spec exige —antecedente
personal y desenlace de elección— están ausentes. Se cierra aquí; no se fuerza
con exposición de red como sustituto de recepción personal, que sería medir
otra cosa y llamarla igual.

**Latinobarometro 2024 → `EXISTE-NO-SATISFACE`.** Búsqueda por etiqueta sobre
las 332 columnas de `Latinobarometro_2024_Stata_esp_v20250817.dta`: cero ítems
de compra de voto, oferta de dádiva o receptor de transferencia condicionada al
voto. La ola no trae la batería.

## §3 · Pieza (b) · `R7.3`/`R7.6` — ENCUCI sí la satisface; Latinobarometro no

**ENCUCI 2020 → `EXISTE-SATISFACE`, con dos sustituciones declaradas frente a
LAPOP 2023** (ninguna exige re-extracción, las dos son de la misma sección
6/7 ya abierta para R7.8 en `L9`):

- **Antecedente** `AP6_10` (beneficiario de programa social en últimos 12
  meses, `1=Sí` 5 789 / `2=No` 15 676 / `9` 54) — el **mismo** antecedente que
  `L9` usó para `R7.8`, y consistente con el antecedente literal de `R7.3`
  («transferencia directa universal no condicionada»), más cercano que la
  dádiva de `R7.7`.
- **Moderador** `AP7_15` («¿Usted cree que su voto es secreto o se puede
  descubrir por quién ha votado?»): `1=secreto` (14 630) · `2=se puede
  descubrir` (6 255) · `9=NS/NR` (634). Es el análogo exacto de `countfair3`
  de LAPOP 2023.
- **Desenlace** `AP7_13` («independientemente del partido por el que votó en
  2018, ¿con qué partido simpatiza más?», `07=MORENA` el partido en el
  gobierno desde dic-2018): marginal `{01:1580, 02:1948, 03:467, 04:100,
  05:118, 06:100, 07:4256, 08:116, 09:6716, 99:393, blanco:5725}`. Es el
  análogo declarado de `vb20` de LAPOP 2023 («votaría por el partido del
  presidente actual»): las dos son **prospectivas/actitudinales**, contemporáneas
  a la encuesta, no el voto emitido. `AP7_13A` (variante con un gate no
  documentado en el FD, sólo 5 725 casos) **no se usa**: cubre menos y el
  censo no explica la condición del gate.
- **Universo**: `AP6_10 ∈ {1,2}`, `AP7_15 ∈ {1,2}`, `AP7_13 ∉ {blanco, 99}` →
  15 083 de 21 519 = **70.09 %**, bajo el 90 %: la pieza corre bajo **universo
  restringido** (`A-bis 4`), igual que la pieza homóloga de `L9` (87.18 %).
  Denominadores por celda (`AP6_10 × AP7_15`, sin tocar `AP7_13`):
  transferencia-sí×secreto 4 164, transferencia-sí×descubrible 1 447,
  transferencia-no×secreto 10 441, transferencia-no×descubrible 4 803.

**Latinobarometro 2024 → `EXISTE-NO-SATISFACE`.** Cero ítems de secreto del
voto, cero ítems de recepción de transferencia gubernamental. Se buscaron por
etiqueta `voto`, `secreto`, `corrup`, `transferenc`, `beneficio`, `programa
social`: nada que sirva de moderador ni de antecedente para este par.

## §4 · Pieza (c) · `R7.4` — ENCUCI la satisface con dos sustituciones; Latinobarometro no

**ENCUCI 2020 → `EXISTE-SATISFACE`, con dos sustituciones declaradas frente a
LAPOP 2019:**

- **Agravio**: no existe ítem de **victimización personal** (el `vic1ext` de
  LAPOP). El más cercano es `AP4_3_2` («en su colonia/localidad han tenido
  problemas de pandillerismo, robos o delincuencia», sección 4, tabla
  `SEC_4_5.dbf`) — **percepción de inseguridad en el entorno**, no
  victimización personal. Marginal: `1=sí` 11 008 / `2=no` 10 428 / `9` 83.
  Sustitución declarada porque es lo único en el corpus que se acerca a
  «agravio» sin exigir re-extracción de texto.
- **Entorno**: `DOMINIO` (`U`=Urbano 10 308, `C`=Complemento urbano 5 295,
  `R`=Rural 5 916) del diseño muestral (`ENCUCI_2020_SD.dbf`). Se agrupa
  **urbano = U+C**, **rural = R** — la misma partición que el marco muestral
  del INEGI usa, no idéntica a `ur` de LAPOP pero del mismo tipo.
- **Desenlace**: `AP7_3_5` («alguna vez en su vida, ¿ha participado en una
  protesta?»): `1=sí` 1 748 / `2=no` 18 506 / `9` 67 / blanco 1 198. **No** se
  usa `AP7_4_5` («en los últimos 12 meses…»): está **gateada dentro de
  `AP7_3_5 == 1`** (sólo 1 748 de 21 519 = 8.1 % la responden), así que no
  sirve como desenlace de población — sería medir protesta reciente **sólo
  entre quienes ya protestaron alguna vez**, un universo distinto y sesgado.
  `AP7_3_5` es de por vida, no de una ventana de 12 meses como `prot3` de
  LAPOP: la ventana temporal difiere, declarado.
- **Universo**: `AP7_3_5 ∈ {1,2}` ∧ `AP4_3_2 ∈ {1,2}` → 20 187 de 21 519 =
  **93.80 %**, sobre el 90 %: **no** corre bajo universo restringido (a
  diferencia de la pieza (b) de este mismo acto). Denominadores del eje
  (`DOMINIO agrupado × AP4_3_2`, sin tocar `AP7_3_5`): urbano-agravio 8 817,
  urbano-sin-agravio 6 723, rural-agravio 2 191, rural-sin-agravio 3 705 — las
  cuatro celdas muy por encima de la guardia de numerador de 10.

**Latinobarometro 2024 → `EXISTE-NO-SATISFACE`.** Cero ítems de protesta,
manifestación, huelga o bloqueo; cero ítems de victimización o percepción de
inseguridad en la colonia; sólo trae victimización general (`P50ST.A`, sin
desagregar urbano/rural en el cuestionario de esta ola) y nada de agravio
localizado. No se sustituye con `P50ST.A`: mediría otra cosa (victimización
nacional autoreportada, sin el eje de entorno).

## §5 · La pieza (d) — `R1.5` — NO-LANZADA, y no se examina aquí

El encargo declara la sub-compuerta de la pieza (d) (ICPSR 35024 en
`data/manifiesto.yaml` con formato stata/dta/delimited/csv) verificada por el
orquestador **antes** de arrancar este acto: `grep -c` da `0`. Esta sesión no
re-verifica ni re-busca ICPSR 35024: la pieza (d) queda `NO-LANZADA` desde el
arranque, sin censo propio.

## §6 · Reproducción

```
python3 tools/medidor_l11_encuci2020.py --censo
```

Los dos payloads viven en `data/raw` (symlink al corpus compartido): no
requiere `data/raices.local.yaml`.

## §7 · Contador de este commit

Piezas censadas: 3 (a, b, c) × 2 instrumentos (ENCUCI 2020, Latinobarometro
2024) = 6 celdas instrumento×regla. **`EXISTE-SATISFACE`: 2** (b y c sobre
ENCUCI). **`EXISTE-NO-SATISFACE`: 4** (a sobre ENCUCI, a/b/c sobre
Latinobarometro). Ningún cruce del desenlace contra el moderador se calculó
todavía; eso es `COMMIT-1` / `P1`, que sigue a este commit.
