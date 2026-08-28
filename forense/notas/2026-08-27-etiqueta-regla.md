# COMMIT-1 — Regla congelada de etiqueta de instrumento para payloads de raíz

`ACTO MAESTRA31-E7 · ETIQUETA`, 27/ago/2026. Congelada ANTES de aplicarla a `data/inventario-reactivos-v1_0.tsv`. Universo: `main = 9578ee6` (rama `claude/etiqueta-inventario-raiz-luzdef` arrancó ya sobre este SHA — el encargo se redactó contra `f1b0d79`; `main` se movió porque `E6` fusionó en paralelo, PR #387; confirmado `git merge-base HEAD origin/main == 9578ee6 == HEAD`, sin diferencia adicional que resolver).

## 0 · El mecanismo, citado (no editado)

```
tools/inventario_reactivos.py:125
    instrumento = rel.split("/", 1)[0] if "/" in rel else "(raiz)"
```

Confirmado contra el archivo: `awk -F'\t' 'NR>1 && $3=="(raiz)"' data/inventario-reactivos-v1_0.tsv | wc -l` → **103302**; distintos: `... | awk '{print $1}' | sort -u | wc -l` → **119**; ENCUCI: `awk -F'\t' 'NR>1 && tolower($1) ~ /encuci/' data/inventario-reactivos-v1_0.tsv | wc -l` → **458**. Coincide exacto con lo que dirección declaró en el encargo.

**Corrección a una cifra del encargo, verificada por comando, antes de tocar nada más:** el encargo afirma "16 de los 20 veredictos `EXISTE-NO-SATISFACE` citan un payload de `(raiz)`". Comando:

```
$ awk -F'\t' 'NR>6 && $2=="EXISTE-NO-SATISFACE"{n=split($6,a,";"); found=0; for(i=1;i<=n;i++) if(a[i]=="(raiz)") found=1; print found}' data/cruce-inverso-v1_0.tsv | sort | uniq -c
     20 1
```

Son **20 de 20**, no 16 de 20. Se reporta la cifra correcta; no cambia la lectura del encargo (el veredicto sigue significando "existe, pero bajo otro instrumento", y el otro instrumento sigue siendo el cubo en todos los casos, no menos).

## 1 · Observación de las familias (antes de escribir la regla)

Los 119 payloads de `(raiz)` se listaron y se agruparon a mano por patrón visible en el nombre. No hay un patrón único — hay varias familias reales y varias que no traen ningún dato de instrumento en el nombre:

- **Familia `<familia><año>_<sufijo>`** (mayoría): `encig2015_csv.zip`, `envipe2018_csv.zip`, `enigh2012_nc_csv.zip`, `enif2018_csv.zip`, `enut2019_bd_csv.zip` — la familia y el año están pegados o con un separador simple, exactamente el mismo patrón `familia+año` que ya usan los 74 instrumentos no-raíz del inventario (`encig2023`, `envipe2025`, …). Esta familia se resuelve.
- **Familia `<prefijo>_<familia>_<año>_<sufijo>` o `<familia>_<año>_<sufijo>`**: `BD_ENCUCI2020_dbf.zip`, `ejemplobd_enestyc_1992_dbf.zip`, `bases_enif2012_dbf.zip`, `fd_enif2012.xlsx`, `base_datos_enadid23_csv.zip`, `inegi_encoap_2023_csv.zip`, `conjunto_de_datos_enoe_2018_4t_csv.zip` — el nombre de la encuesta está en mayúsculas o rodeado de texto descriptivo, pero el token de familia+año sigue siendo extraíble con una regex por familia.
- **Familia `<timestamp>trim<N>_csv.zip` / `<timestamp>.export.CSV.zip`**: `2005trim1_csv.zip`, `20260813130000.export.CSV.zip` — el nombre es una fecha o un timestamp de exportación, sin ningún token alfabético de encuesta. **No hay instrumento derivable del nombre solo** — se sabe por contexto de dominio (son trimestres de ENOE) pero eso no es "derivar del payload_id", es adivinar; la regla no lo fuerza.
- **Residual sin patrón reconocible**: `DescargaMasivaOD_*.xml` (nombre de sistema, no de encuesta), `cses5_*` (identifica una ronda numerada, no un año, y `cses` no tiene análogo en los 74 instrumentos del corpus), `banxico_encuesta_competencias_financieras_*.xlsx` (nombre descriptivo completo, sin acrónimo establecido en el corpus — no es lo mismo que ENIF aunque comparta dominio temático, y no hay base para inventar un acrónimo), `ucdp_ged261_csv.zip` (versión de dataset, no año de ola), `zenodo_electoral_precinct_level_mexico_municipal.zip` (repositorio genérico, no instrumento).

## 2 · Regla congelada

Para cada `payload_id` cuyo `instrumento` actual es `(raiz)`, aplicar en orden la primera regex de familia que haga match (case-insensitive) sobre el propio `payload_id`; el año de 2 dígitos se expande a 4 asumiendo `20YY` si `YY<50`, si no `19YY` (mismo rango que ya usan los 74 instrumentos existentes: nada antes de 1990 ni futuro más allá del año en curso):

| familia | patrón |
|---|---|
| encig | `encig(\d{2,4})` |
| envipe | `envipe(\d{4})` |
| enigh | `enigh(\d{4})` |
| enif | `enif_?(\d{4})` |
| enadid | `enadid(\d{2})` |
| enestyc | `enestyc_(\d{4})` |
| enut | `enut(\d{4})` |
| encup | `encup_?(\d{4})` |
| encoap | `encoap_(\d{4})` |
| encuci | `encuci(\d{4})` |
| cpv | `cpv(\d{4})` |
| censo | `censo(\d{4})` |
| enoen | `enoen_(\d{4})` |
| enoe | `enoe_(\d{4})` (sin casar dentro de `enoen`) |
| iter | `iter_nal_(\d{4})` |

Salida: `familia + año4`. Si ninguna regex casa, `instrumento = (sin-instrumento-derivable)` — no se fuerza ninguna otra heurística (ni acrónimo inventado, ni "vecino más parecido", ni conocimiento externo de qué encuesta es).

Este criterio es deliberadamente conservador: solo se acepta una familia cuando su token aparece **literal** en el nombre del payload, con **año explícito** adjunto. `cses5` no entra porque "5" es un número de ronda, no un año — inventar `cses2022` sería adivinar, no derivar. Los `trimN`/timestamp no entran porque el nombre no lleva ningún carácter alfabético identificable como encuesta.

## 3 · Resultado de aplicar la regla (primera y única corrida, antes de ver el efecto en el cruce)

```
$ python3 deriva_instrumento_raiz.py   (script de scratch, no forma parte del repo -- no toca tools/)
total payloads raiz: 119
resueltos: 80  no-resueltos: 39
```

**39 de 119 (32.8%) van a `(sin-instrumento-derivable)`.** Está bajo la mitad — la regla de tope de "una vuelta" (§4 del encargo) no se dispara; no hubo necesidad de ajustar nada tras ver este número, y no se ajustó. El listado completo de las dos clases queda en el commit de datos (`data/inventario-reactivos-v1_1.tsv`) y es auditable por instrumento.

Los 39 no resueltos, por motivo:
- 16 archivos `<año>trim<N>_csv.zip` — sin token alfabético de encuesta en el nombre (son ENOE por contexto de dominio, no por el nombre).
- 13 archivos `<timestamp>.export.CSV.zip` — timestamp de exportación, sin nombre de encuesta.
- 2 `DescargaMasivaOD_*.xml` — nombre de sistema descargador, no de encuesta.
- 3 `banxico_encuesta_competencias_financieras_*.xlsx` — nombre descriptivo sin acrónimo establecido en el corpus.
- 3 `cses5_*` — ronda numerada, no año.
- 1 `ucdp_ged261_csv.zip` — versión de dataset, no ola.
- 1 `zenodo_electoral_precinct_level_mexico_municipal.zip` — repositorio genérico.

## 4 · La trampa de `ola`

`ola` **no se toca, y no puede romperse**, porque no se deriva de la ruta en absoluto: es una constante. Confirmado citando el propio código (`tools/inventario_reactivos.py:110`, dentro de `filas_desde_objetos`): `"ola": "NO_DETERMINADO"` — literal, sin condicional, para toda fila que produce el extractor. Confirmado también contra el dato:

```
$ awk -F'\t' 'NR>1{print $4}' data/inventario-reactivos-v1_0.tsv | sort -u
NO_DETERMINADO
```

Un solo valor en las 178,246 filas. La premisa del encargo ("`ola` se deriva hoy del mismo lugar [que `instrumento`]") no se sostiene contra el archivo: `ola` no se deriva de nada, ni de la ruta ni de otra columna — es un valor fijo del extractor, independiente de si el payload vive en raíz o en carpeta. Por construcción, ninguna corrección a `instrumento` puede romper `ola`, porque `ola` no varía con `instrumento` hoy. Esto ya lo sabía la propia spec congelada de E5 (`forense/notas/2026-08-27-cruce-inverso-spec.md`, §2): declaró que `n_olas_distintas` se calcula sobre el conjunto de valores distintos de `instrumento`, precisamente porque `ola` es inservible. Esta corrección hereda esa misma decisión sin reabrirla: al arreglar `instrumento`, `n_olas_distintas` (que ya se apoyaba en `instrumento`, no en `ola`) se recalcula correctamente sin que la spec de E5 cambie una palabra.

## 5 · Control positivo (obligatorio)

Los payloads que hoy tienen instrumento correcto deben conservarlo byte a byte. Verificado tras generar `v1_1` (no antes de congelar la regla, porque el archivo aún no existía; se declara aquí como parte de COMMIT-1 y se re-verifica en COMMIT-2):

```
$ diff <(grep $'encig2023/encig23_base_datos_dbf.zip\t' data/inventario-reactivos-v1_0.tsv) \
       <(grep $'encig2023/encig23_base_datos_dbf.zip\t' data/inventario-reactivos-v1_1.tsv)
(sin salida -- identicas)
$ diff <(grep $'envipe2025/bd_envipe_2025_csv.zip\t' data/inventario-reactivos-v1_0.tsv) \
       <(grep $'envipe2025/bd_envipe_2025_csv.zip\t' data/inventario-reactivos-v1_1.tsv)
(sin salida -- identicas)
```

Y a nivel de tabla completa (no solo muestra): las 74,944 filas cuyo `instrumento` en `v1_0` ya era distinto de `(raiz)` se comparan línea completa contra `v1_1` (excluyendo únicamente filas que hoy son `(raiz)` o `(sin-instrumento-derivable)`):

```
$ python3 -c "... comparación línea a línea por multiconjunto ..."
matched original non-raiz lines byte-for-byte: 74944 de 178247
original non-raiz lines NOT found unchanged in v1_1: 0
```
Las 74,944 filas no-raíz de `v1_0` están, sin excepción, byte a byte idénticas en `v1_1`. La regla no toca lo que ya estaba bien.

## 6 · B-bis — qué significaría el delta, antes de correr el cruce

- **Si muchos veredictos `EXISTE-NO-SATISFACE` pasan a `EXISTE-SATISFACE`:** la contaminación de etiqueta era la causa real de gran parte del "no satisface" — el motor citaba bien, el corpus lo tenía, y solo el cubo lo escondía. Esto es lo que predice el diagnóstico del encargo para el caso ENCUCI.
- **Si casi ninguno se mueve:** la contaminación de etiqueta existía (58% de filas) pero no era la causa de los veredictos concretos publicados — la mayoría de los `EXISTE-NO-SATISFACE`/`NO-ENCONTRADO` tendría otra causa (instrumento genuinamente ausente del corpus, o token que de verdad no es una variable). Esto **corrobora** a E5, no lo contradice: significa que E5 midió bien a pesar del defecto de etiqueta, porque el defecto no tocaba las filas que E5 estaba mirando. Se reportaría así, sin maquillaje, como resultado tan publicable como el contrario.

Frase de sello, verbatim: «El primer resultado que produzca este procedimiento es el que se reporta.»
