# ACTO GEN2-PREP-LOTE — identidad de demanda por consumidor: corrección de `_instrumento()` y tabla de correspondencia CORR viejo→nuevo

**Acto:** `ACTO GEN2-PREP-LOTE`, 9/sep/2026, NUBE. **Alcance:** solo la
resolución de identidad en `tools/corrida0.py:_instrumento()`/`_corridas()`
y la re-derivación mecánica de `data/corrida0/demanda-*.tsv` que resulta de
ese cambio. Cero microdato abierto, cero medición, cero sello tocado.

## 1 · El defecto y el arreglo (P1)

`_instrumento()`, para toda fila `conducta_*`, leía el `fuente:` de la
REGLA (agregado histórico, no actualizado cuando llegan mediciones nuevas
en otro instrumento) en vez del `payload` que la conducta misma ya declara
—correcto por conducta desde antes de este acto, vía `enmienda_*` en
`_consumidores_conductas()`. `demanda-corridas.tsv` etiquetaba `CORR-0002`
(payload `encig25_base_datos_csv`, en realidad **ENCIG 2025**) y
`CORR-0003` (payload `encuci2020_bd_dbf`, **otro programa**: ENCUCI 2020)
como `ENCIG2023` — el rastro de cuando `tramite.mordida.discrecional` era
solo `ASIGNADO` con `p: 0.62`. Diagnóstico completo, verificado sin abrir
microdato, en
`forense/notas/2026-09-09-identidad-encig-corr-0002-0003.md` (ACTO
GEN2-LOTE-ENVIPE-1, P4) y citado en `canon/gobernanza-v1_15.md` (entrada de
ese acto).

**Arreglo:** `_instrumento()` ahora resuelve, para `conducta_*`, primero el
payload propio de esa conducta (`fila["payload_ids_legacy"]`, ya correcto
por conducta) contra `data/manifiesto.yaml` — programa y año leídos de
`url_origen` (`/programas/<programa>/<año>/`), la misma evidencia 1 que
`2026-09-09-identidad-encig-corr-0002-0003.md` usó a mano. Solo cae al
`fuente:` de la regla cuando la conducta no declara payload propio (las
`ASIGNADO` sin medición). Los sufijos de nombre de conducta (`_encig2025`,
`_encuci2020`) siguen sin leerse como autoridad — son pista, nunca
corrección.

**Ambigüedad, ya no resuelta por "la primera".** Cuando el fallback a
`fuente:` de la regla encuentra **más de un** token con forma de
instrumento (caso real: `familia.seguro.volatilidad_ausencia_estado`,
seis fuentes `ENIGH2022/2012/2014/2016/2018/2020`, conductas `ASIGNADO`
sin payload propio), la corrida se etiqueta `AMBIGUA` y el caso se agrega
a la lista de "agrupaciones que el registro no decide" — antes se tomaba
la primera en silencio. Efecto real medido en esta re-derivación: `RES-0035`
y `RES-0036` (antes agrupados bajo `CORR-0013` como `ENIGH2022`) ahora
caen en la nueva `CORR-0011`, etiqueta `AMBIGUA`.

## 2 · Validaciones en fixture

`tests/test_corrida0.py` — `t_instrumento_no_agrupa_por_sufijo_de_regla`,
`t_instrumento_orden_de_fuente_no_cambia_identidad`,
`t_instrumento_fuente_ambigua_no_resuelve_por_primera`: una regla sintética
con conductas ENCIG2025+ENCUCI2020 no se agrupa bajo el `fuente:` de la
regla; invertir el orden de las fuentes en la regla no cambia la identidad
resuelta por payload; una regla con dos fuentes con forma de instrumento y
ninguna conducta con payload propio se etiqueta `AMBIGUA`, no la primera.

## 3 · Consecuencia mecánica: `demanda-corridas.tsv` se re-derivó

`data/corrida0/demanda-corridas.tsv` y `demanda-resultados.tsv` son
DERIVADOS — se re-generaron con `python3 tools/corrida0.py demanda`, el
comando de la casa, no se editaron a mano. La consecuencia esperada y
declarada aquí: al corregir la identidad, corridas que antes quedaban
separadas por una etiqueta de instrumento espuria (`report:politica`,
`validacion:SPEI`, o dos olas de la misma regla con `fuente:` distinto)
ahora comparten grupo, y **el número `CORR-NNNN` de todo lo que sigue en
el archivo se recorre** — es un id posicional, nunca un sello. Ningún
`RES-NNNN` cambia de identidad (el orden en que `_consumidores_conductas`
y las funciones hermanas producen `filas` no depende de `_instrumento()`,
así que `_asigna_ids` les da el mismo id de siempre).

**Candado de migración — ningún id citado se resignifica en silencio.**
Tres citas verbatim en actos sellados usan un número `CORR-*` como parte
de su identidad:

| cita sellada | CORR viejo | CORR nuevo | qué no cambió |
|---|---|---|---|
| `forense/prereg-caja/ENVIPE-DENUNCIA-spec-v1_0.md` (releva `CALC-ENVIPE-0001`) | `CORR-0009` | `CORR-0007` | mismos `RES-0027/RES-0028` (+ `RES-0039..42`, `## NO-CORRIDO` de ese acto) — instrumento sigue `ENVIPE2025`, ahora también absorbe el par que colgaba bajo la etiqueta espuria `report:politica` (viejo `CORR-0008`) |
| `forense/prereg-caja/R-ENVIPE-SERIE-spec-v1_0.md` (releva `CALC-R-CIV-M-10/-12/-13`) | `CORR-0036`/`CORR-0040`/`CORR-0044` | `CORR-0032`/`CORR-0036`/`CORR-0040` | mismos `RES-0108`/`RES-0113`/`RES-0118`, mismo instrumento (`ENVIPE 2021/2023/2024`) — el corrimiento es puramente posicional (el bloque ENCIG/ENCUCI de más arriba en el archivo se contrajo) |
| `canon/gobernanza-v1_15.md` (entrada de `ACTO GEN2-LOTE-ENVIPE-1`, P4) | `CORR-0002`/`CORR-0003` | `CORR-0002`/`CORR-0003` (sin corrimiento) | el número no cambia; lo que cambia es la columna `instrumento`, de `ENCIG2023` (defecto ya documentado por esa misma entrada) a `ENCIG2025`/`ENCUCI2020` — es la corrección que esa entrada pedía |

Ninguna de las tres queda huérfana: la fila vieja de cada tabla de abajo
trae su puntero de sucesión (columna "CORR nuevo"). Ningún sello ni
`CALC-*/` se tocó — esto es re-derivación de la DEMANDA (lo que se pide
medir), no de la OFERTA (lo ya medido).

**Tabla de correspondencia completa** (86 `CORR-*` viejos → 82 nuevos; la
reducción neta de 4 es la suma de los tres pares/tríos que colapsan por
compartir instrumento real una vez corregida la derivación: ENCIG2025,
ENCUCI2020, ENVIPE2025):

| CORR viejo (instrumento) | CORR nuevo (instrumento) | nota |
|---|---|---|
| `CORR-0001` (ENCIG2023) | `CORR-0001` (ENCIG2023) | |
| `CORR-0002` (ENCIG2023) | `CORR-0002` (ENCIG2025) **(instrumento corregido)** | |
| `CORR-0003` (ENCIG2023) | `CORR-0003` (ENCUCI2020) **(instrumento corregido)** | |
| `CORR-0004` (validacion:CoDi) | `CORR-0004` (validacion:CoDi) | |
| `CORR-0005` (validacion:SPEI) | `CORR-0005` (validacion:SPEI) | |
| `CORR-0006` (validacion:SPEI) | `CORR-0002` (ENCIG2025) **(instrumento corregido)** | |
| `CORR-0007` (report:politica) | `CORR-0006` (report:politica) | |
| `CORR-0008` (report:politica) | `CORR-0007` (ENVIPE2025) **(instrumento corregido)** | |
| `CORR-0009` (ENVIPE2025) | `CORR-0007` (ENVIPE2025) | |
| `CORR-0010` (ENNViH/MxFLS_olas2-3) | `CORR-0008` (ENNViH/MxFLS_olas2-3) | |
| `CORR-0011` (ENNViH/MxFLS_olas2-3) | `CORR-0009` (ENIF2024) **(instrumento corregido)** | |
| `CORR-0012` (ENIF2024) | `CORR-0010` (ENIF2024) | |
| `CORR-0013` (ENIGH2022) | `CORR-0011` (AMBIGUA) **(instrumento corregido)** | |
| `CORR-0014` (ENFIH2019) | `CORR-0012` (ENFIH2019) | |
| `CORR-0015` (EDER2017) | `CORR-0013` (EDER2017) | |
| `CORR-0016` (ENUT2024) | `CORR-0014` (ENUT2024) | |
| `CORR-0017` (ENIF2024) | `CORR-0009` (ENIF2024) | |
| `CORR-0018` (data/l8-resultados-tipo-boleta-v1_0.json) | `CORR-0015` (data/l8-resultados-tipo-boleta-v1_0.json) | |
| `CORR-0019` (ENIF2024) | `CORR-0016` (ENIF2024) | |
| `CORR-0020` (ENCUCI2020) | `CORR-0003` (ENCUCI2020) | |
| `CORR-0021` (forense/prereg-caja/S7-L17-spec-v1_0.md) | `CORR-0017` (forense/prereg-caja/S7-L17-spec-v1_0.md) | |
| `CORR-0022` (NO-DECLARADO-EN-EL-REGISTRO) | `CORR-0018` (NO-DECLARADO-EN-EL-REGISTRO) | |
| `CORR-0023` (NO-DECLARADO-EN-EL-REGISTRO) | `CORR-0019` (NO-DECLARADO-EN-EL-REGISTRO) | |
| `CORR-0024` (ENVIPE 2012) | `CORR-0020` (ENVIPE 2012) | |
| `CORR-0025` (ENVIPE 2012) | `CORR-0021` (ENVIPE 2012) | |
| `CORR-0026` (ENVIPE 2012) | `CORR-0022` (ENVIPE 2012) | |
| `CORR-0027` (ENVIPE 2012) | `CORR-0023` (ENVIPE 2012) | |
| `CORR-0028` (ENVIPE 2013) | `CORR-0024` (ENVIPE 2013) | |
| `CORR-0029` (ENVIPE 2013) | `CORR-0025` (ENVIPE 2013) | |
| `CORR-0030` (ENVIPE 2013) | `CORR-0026` (ENVIPE 2013) | |
| `CORR-0031` (ENVIPE 2013) | `CORR-0027` (ENVIPE 2013) | |
| `CORR-0032` (ENVIPE 2015) | `CORR-0028` (ENVIPE 2015) | |
| `CORR-0033` (ENVIPE 2015) | `CORR-0029` (ENVIPE 2015) | |
| `CORR-0034` (ENVIPE 2015) | `CORR-0030` (ENVIPE 2015) | |
| `CORR-0035` (ENVIPE 2015) | `CORR-0031` (ENVIPE 2015) | |
| `CORR-0036` (ENVIPE 2021) | `CORR-0032` (ENVIPE 2021) | |
| `CORR-0037` (ENVIPE 2021) | `CORR-0033` (ENVIPE 2021) | |
| `CORR-0038` (ENVIPE 2021) | `CORR-0034` (ENVIPE 2021) | |
| `CORR-0039` (ENVIPE 2021) | `CORR-0035` (ENVIPE 2021) | |
| `CORR-0040` (ENVIPE 2023) | `CORR-0036` (ENVIPE 2023) | |
| `CORR-0041` (ENVIPE 2023) | `CORR-0037` (ENVIPE 2023) | |
| `CORR-0042` (ENVIPE 2023) | `CORR-0038` (ENVIPE 2023) | |
| `CORR-0043` (ENVIPE 2023) | `CORR-0039` (ENVIPE 2023) | |
| `CORR-0044` (ENVIPE 2024) | `CORR-0040` (ENVIPE 2024) | |
| `CORR-0045` (ENVIPE 2024) | `CORR-0041` (ENVIPE 2024) | |
| `CORR-0046` (ENVIPE 2024) | `CORR-0042` (ENVIPE 2024) | |
| `CORR-0047` (ENVIPE 2024) | `CORR-0043` (ENVIPE 2024) | |
| `CORR-0048` (ENNViH/MxFLS 2002 (ola 1)) | `CORR-0044` (ENNViH/MxFLS 2002 (ola 1)) | |
| `CORR-0049` (ENNViH/MxFLS 2002 (ola 1)) | `CORR-0045` (ENNViH/MxFLS 2002 (ola 1)) | |
| `CORR-0050` (ENNViH/MxFLS 2002 (ola 1)) | `CORR-0046` (ENNViH/MxFLS 2002 (ola 1)) | |
| `CORR-0051` (ENNViH/MxFLS 2002 (ola 1)) | `CORR-0047` (ENNViH/MxFLS 2002 (ola 1)) | |
| `CORR-0052` (ENIF 2018) | `CORR-0048` (ENIF 2018) | |
| `CORR-0053` (ENIF 2018) | `CORR-0049` (ENIF 2018) | |
| `CORR-0054` (ENIF 2018) | `CORR-0050` (ENIF 2018) | |
| `CORR-0055` (ENIF 2018) | `CORR-0051` (ENIF 2018) | |
| `CORR-0056` (ENIGH 2016) | `CORR-0052` (ENIGH 2016) | |
| `CORR-0057` (ENIGH 2016) | `CORR-0053` (ENIGH 2016) | |
| `CORR-0058` (ENIGH 2016) | `CORR-0054` (ENIGH 2016) | |
| `CORR-0059` (ENIGH 2016) | `CORR-0055` (ENIGH 2016) | |
| `CORR-0060` (ENIGH 2018) | `CORR-0056` (ENIGH 2018) | |
| `CORR-0061` (ENIGH 2018) | `CORR-0057` (ENIGH 2018) | |
| `CORR-0062` (ENIGH 2018) | `CORR-0058` (ENIGH 2018) | |
| `CORR-0063` (ENIGH 2018) | `CORR-0059` (ENIGH 2018) | |
| `CORR-0064` (ENIGH 2020) | `CORR-0060` (ENIGH 2020) | |
| `CORR-0065` (ENIGH 2020) | `CORR-0061` (ENIGH 2020) | |
| `CORR-0066` (ENIGH 2020) | `CORR-0062` (ENIGH 2020) | |
| `CORR-0067` (ENIGH 2020) | `CORR-0063` (ENIGH 2020) | |
| `CORR-0068` (ENCUCI 2020) | `CORR-0064` (ENCUCI 2020) | |
| `CORR-0069` (ENCUCI 2020) | `CORR-0065` (ENCUCI 2020) | |
| `CORR-0070` (ENCUCI 2020) | `CORR-0066` (ENCUCI 2020) | |
| `CORR-0071` (ENCUCI 2020) | `CORR-0067` (ENCUCI 2020) | |
| `CORR-0072` (ENCIG 2013) | `CORR-0068` (ENCIG 2013) | |
| `CORR-0073` (ENCIG 2013) | `CORR-0069` (ENCIG 2013) | |
| `CORR-0074` (ENCIG 2013) | `CORR-0070` (ENCIG 2013) | |
| `CORR-0075` (ENCIG 2013) | `CORR-0071` (ENCIG 2013) | |
| `CORR-0076` (ENCIG 2021) | `CORR-0072` (ENCIG 2021) | |
| `CORR-0077` (ENCIG 2021) | `CORR-0073` (ENCIG 2021) | |
| `CORR-0078` (ENCIG 2021) | `CORR-0074` (ENCIG 2021) | |
| `CORR-0079` (ENCIG 2021) | `CORR-0075` (ENCIG 2021) | |
| `CORR-0080` (NO-DECLARADO-EN-EL-REGISTRO) | `CORR-0076` (NO-DECLARADO-EN-EL-REGISTRO) | |
| `CORR-0081` (NO-DECLARADO-EN-EL-REGISTRO) | `CORR-0077` (NO-DECLARADO-EN-EL-REGISTRO) | |
| `CORR-0082` (NO-DECLARADO-EN-EL-REGISTRO) | `CORR-0078` (NO-DECLARADO-EN-EL-REGISTRO) | |
| `CORR-0083` (NO-DECLARADO-EN-EL-REGISTRO) | `CORR-0079` (NO-DECLARADO-EN-EL-REGISTRO) | |
| `CORR-0084` (ENIGH 2022 nueva serie, registro PERSONA (modelo §1.1.A)) | `CORR-0080` (ENIGH 2022 nueva serie, registro PERSONA (modelo §1.1.A)) | |
| `CORR-0085` (POR DECLARAR -- el pre-registro fija instrumento por ficha) | `CORR-0081` (POR DECLARAR -- el pre-registro fija instrumento por ficha) | |
| `CORR-0086` (NO-DECLARADO-EN-EL-REGISTRO) | `CORR-0082` (NO-DECLARADO-EN-EL-REGISTRO) | |

## 4 · Lo que este acto NO hizo

No corrigió `milpa/tramite.yaml:tramite.mordida.discrecional`'s `fuente:`
(cosmético, y fuera de perímetro — tocaría el motor y exige firma de
mesa). No re-clasificó la nueva `CORR-0011` (`AMBIGUA`,
`familia.seguro.volatilidad_ausencia_estado`) — la ambigüedad se declara,
no se resuelve por este acto. No relanzó `GEN2-LOTE-ENCIG-1` ni ningún
lote que consuma estos ids.

## 5 · P3 · destrabe del lote ENCIG (línea para que dirección propague)

Con P1 fusionable, la identidad de `CORR-0002`/`CORR-0003` (`ENCIG2025`/
`ENCUCI2020`, antes `ENCIG2023` para ambas) ya no depende de una cirugía
pendiente: **el encargo `GEN2-LOTE-ENCIG-1` pierde su P0** (la corrección
de identidad que traía como prerrequisito queda `SUPERSEDED-POR:
ACTO GEN2-PREP-LOTE`, cita al PR de este acto) y **su compuerta pasa de
"P0 de este mismo encargo" a "DBF y PREP-LOTE fusionados"** — el acto DBF
en CAJA (paralelo a este) y este mismo acto son ahora sus dos únicas
condiciones de arranque. Este acto no edita `GEN2-LOTE-ENCIG-1` ni lo
lanza: la propagación de esta línea a ese encargo queda en manos de
dirección, como el encargo pidió.
