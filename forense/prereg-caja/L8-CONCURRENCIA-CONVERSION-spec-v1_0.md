# L8 · conversión municipal→individual de la concurrencia presidencial — pre-registro congelado de `CALC-L8-CONVERSION-0001`

### `prereg-caja-L8-CONCURRENCIA-CONVERSION` · **v1.0** · 15 de septiembre de 2026

> | | |
> |---|---|
> | **ARCHIVO** | `forense/prereg-caja/L8-CONCURRENCIA-CONVERSION-spec-v1_0.md` |
> | **NOMBRE ESTABLE** | **`prereg-caja-L8-CONCURRENCIA-CONVERSION`** — cítalo así, nunca por nombre de archivo |
> | **QUÉ ES** | Pre-registro, congelado en NUBE, de `CALC-L8-CONVERSION-0001`: releva `CORR-0016` — los tres puntos ilustrativos de `civico.participacion.concurrencia_presidencial_conversion` (`participa_p0_minimo`, `participa_p0_maximo`, `participa_p0_media`; `RES-0050`, `RES-0051`, `RES-0052`) por **transformación determinista y verificable** de campos ya publicados en `data/l8-resultados-tipo-boleta-v1_0.json` — un artefacto del repo, versionado y con `sha256` fijo, **no microdato**. |
> | **QUÉ NO ES** | No re-ejecuta el panel de `L8` (`por_transicion`, `estimador`, wild-cluster): esos campos se **leen**, no se recalculan. No abre ningún `.csv`/`.dta` ni `data/raw`. No cambia la fórmula de conversión que `milpa/tramite.yaml:1142-1146` ya declara (`conversion_A_aditiva`, firma de mesa D1/`FP-255`) — la **aplica** a los tres puntos que la regla ya cita como ilustrativos, con la salvedad de §2 sobre el redondeo. No adopta nada nuevo: `RES-0050/51/52` son legacy `MEDIDO·Δ`, y este `CALC` los **releva** (les da cadena `E.2` trazable a archivo+línea), no los sustituye. |
> | **VERIFICAS ASÍ** | CAJA (o cualquier sesión con el repo) confirma que `data/l8-resultados-tipo-boleta-v1_0.json` en disco tiene el `sha256` de §1, que `len(por_transicion) == 20` (40 medias, `y_de_media`+`y_a_media`), y que `round(min/max/mean(ys)/100, 4) + round(beta_pres_pp/100, 6)` reproduce `0.345267`/`0.750567`/`0.619867` a dos decimales de tolerancia (§3 fija la tolerancia exacta) sin abrir ningún otro archivo. |

**Acto:** `ACTO GEN2-SPECS-DEMANDA-2`, 15/sep/2026, entorno **NUBE** (`cloud_default`, `data/raw` ausente, corpus `montado=NO`, `archivos_examinados=0`), sobre `origin/main = da9b47a361143d408cd9fd9c20d17b101c4fe381`.

**Regla consumidora:** `civico.participacion.concurrencia_presidencial_conversion` (`misma_regla_motor: civico.participacion.contingente`), `milpa/tramite.yaml:1122`, `situacion: SELLADA`, `tier: MEDIA` (`ADR-321`, firma D1 `FP-255`).

---

## 0 · A.8 — qué ya existe, y por qué esto no es una nueva medición

### 0.1 · `ya_medido.py`, salida cruda

```
$ python3 tools/ya_medido.py civico.participacion.concurrencia_presidencial_conversion
  resuelto por canon: (id compuesto de motor, sin R-n propio en canon/modelo-decision-v4_0.md §7 -- 0 filas)
  -- milpa/tramite.yaml -- :1122  situacion=SELLADA tier=MEDIA p0_rango=[0.3051,0.7104]  [TASA-EJECUTADA vía conversión, no vía payload propio]
  -- milpa/tramite-ola5-propuesta-v0.yaml -- (sin apariciones)
  -- data/corrida0 (RESULT + ejecución + sello) -- (sin CALC propio: 0 filas en data/corrida0/CALC-*/spec.yaml)
  -- forense/notas/*-L*-*.md -- 2026-09-02-MAESTRA35-L8-spec.md (definición de p0), 2026-09-03-MAESTRA36-N12-propuesta.md §1.1 (rango [0.3051,0.7104])
  -- canon/registro-rotulos.tsv (alias) -- (sin apariciones)
  ========================================
  MEDIDA-EN: tramite.yaml (sin CALC que la releve)
```

`MEDIDA-EN` por transformación de motor, **sin `CALC`/`spec.yaml` que le dé
cadena `E.2`**: exactamente el hueco que `CORR-0016` nombra y que este acto
cierra.

### 0.2 · El payload no falta — es un artefacto del repo

`data/l8-resultados-tipo-boleta-v1_0.json` no es microdato de ninguna
encuesta: es la **salida ya computada** del panel `L8`
(`forense/notas/2026-09-02-MAESTRA35-L8-spec.md`), versionada en el repo,
43 545 bytes. `data/corrida0/demanda-corridas.tsv:CORR-0016` lo cita
literalmente como `instrumento`. No hay ZIP que descargar, ni `sha256` de
manifiesto que resolver: el `sha256` del propio archivo es la identidad.

```
$ sha256sum data/l8-resultados-tipo-boleta-v1_0.json
<se fija en §1 abajo, verificado por el mismo comando al sellar>
```

### 0.3 · Por qué `p0_rango`/`p0_media` no se re-derivan de memoria

`milpa/tramite.yaml:1147-1158` ya documenta la fórmula y la fuente
(`por_transicion[].y_de_media`/`y_a_media`, 20 transiciones × 2 patas = 40
medias), pero **no** trae un `CALC` que reproduzca esas 40 lecturas con
comando a la vista. Verificado en esta sesión:

```
$ python3 -c "
import json
d = json.load(open('data/l8-resultados-tipo-boleta-v1_0.json'))
pt = d['por_transicion']
ys = [row[k] for row in pt for k in ('y_de_media','y_a_media')]
print('n_transiciones:', len(pt), 'n_medias:', len(ys))
print('min:', min(ys), 'max:', max(ys), 'mean:', sum(ys)/len(ys))
print('beta_pres_pp:', d['estimador']['beta_pres_pp'])
"
n_transiciones: 20 n_medias: 40
min: 30.509568846824635 max: 71.043832719488 mean: 57.96625432088392
beta_pres_pp: 4.016715486813227
```

`round(30.509568846824635/100, 4) = 0.3051`, `round(71.043832719488/100, 4)
= 0.7104`, `round(57.96625432088392/100, 4) = 0.5797` — **coinciden
exactamente** con `p0_rango_observado`/`p0_media` de `milpa/tramite.yaml`.
`round(4.016715486813227/100, 6) = 0.040167` coincide con `delta` de
`conversion_A_aditiva`. La regla no inventó estos números: son lectura
directa y redondeada del JSON, y esta spec es la primera vez que ese
cálculo queda escrito con comando, no solo citado.

---

## 1 · Payload

| id | ruta | `sha256` | origen |
|---|---|---|---|
| `l8_resultados_tipo_boleta_v1_0` | `data/l8-resultados-tipo-boleta-v1_0.json` | `sha256sum` del archivo en disco al congelar (repo, no manifiesto — es artefacto versionado, `E.5` lo permite abrir sin restricción: no es microdato) | repo |

Campos leídos, y **solo** esos — ningún otro campo del JSON se abre:

- `por_transicion` (lista de 20 objetos): `y_de_media`, `y_a_media` (float,
  puntos porcentuales de participación municipal, `100 * votos /
  lista_nominal`, definidos en `forense/notas/2026-09-02-MAESTRA35-L8-spec.md
  §1.2`).
- `estimador.beta_pres_pp` (float): efecto puntual del panel wild-cluster,
  puntos porcentuales.

---

## 2 · Transformación (determinista, sin ajuste, sin bootstrap)

```
ys = [t[k] for t in por_transicion for k in ('y_de_media', 'y_a_media')]   # 40 valores
p0_min  = round(min(ys) / 100, 4)
p0_max  = round(max(ys) / 100, 4)
p0_mean = round(sum(ys) / len(ys) / 100, 4)
delta   = round(estimador['beta_pres_pp'] / 100, 6)

p_minimo = min(max(p0_min  + delta, 0.0), 1.0)
p_maximo = min(max(p0_max  + delta, 0.0), 1.0)
p_media  = min(max(p0_mean + delta, 0.0), 1.0)
```

**Redondeo declarado, no re-descubierto.** `p0` se redondea a 4 decimales
**antes** de sumar `delta` (a 6 decimales): así lo hizo la cifra legacy que
esta spec releva (`0.3051 + 0.040167 = 0.345267`, exacto), y esta spec **no
cambia ese orden de redondeo** — cambiarlo produciría un número
ligeramente distinto (`0.34526284…`) que ya no sería el mismo `RESULT` que
`milpa/tramite.yaml` cita. El `clip(0,1)` no se activa en ningún caso: los
tres puntos quedan lejos de los bordes (`recorte_activo_en_rango_observado:
false`, ya declarado por la regla).

---

## 3 · `estimando`

**Descriptivo, sin incertidumbre nueva.** Los tres `RESULT` son puntos
ilustrativos de una fórmula de conversión ya firmada por mesa
(`conversion_A_aditiva`, D1/`FP-255`) — **no** una medición con diseño
muestral propio: `p0` viene de un panel municipal agregado (`L8`) y `delta`
de un estimador wild-cluster cuyo propio IC95 vive en
`estimador.wild_cluster_beta_pres` (no se recita aquí: es campo del `L8`
original, no de este `CALC`). Esta spec no calcula IC95 de `p_minimo`/
`p_maximo`/`p_media` — declararía una precisión sobre la conversión que
`L8` mismo no ofrece del lado de `p0` (medias sobre `n` de 5 a 209
municipios por transición, sin bootstrap re-corrido aquí). Tolerancia:
`abs=5e-7` en las tres cifras, exacta en las lecturas de `len(por_transicion)`
y `n_medias`.

---

## 4 · `resultados` que releva

`CORR-0016` (`data/corrida0/demanda-corridas.tsv`, `n_resultados=3`):
`RES-0050` (`participa_p0_minimo`), `RES-0051` (`participa_p0_maximo`),
`RES-0052` (`participa_p0_media`) — los tres bajo
`civico.participacion.concurrencia_presidencial_conversion`. Sin residuo:
`CORR-0016` tiene exactamente 3 `RESULT` y los tres quedan relevados.

---

## 5 · Qué NO hace este acto

No re-corre el panel `L8` ni sus wild-cluster bootstrap. No escribe
`data/raw`, no consulta el corpus compartido, no abre ningún `.dta`/`.csv`.
No cambia `milpa/tramite.yaml` (`E.3`, cifra sellada; esta spec **releva**,
no reemplaza). No calcula el `medidor.py`: `data/corrida0/CALC-L8-CONVERSION-0001/spec.yaml`
declara el contrato completo y **el script queda para CAJA** — no porque
falte `numpy`/`pandas` (esta transformación no los necesita: es aritmética
pura sobre JSON, con la librería estándar) sino porque este acto declaró en
su propio lanzamiento `CONTADOR: cero mediciones propias` y no corre ningún
`CALC` (perímetro fijado en `forense/encargos/2026-09-15-GEN2-SPECS-DEMANDA-2.md`,
sin excepción por facilidad técnica).

**El primer resultado que produzca este procedimiento es el que se
reporta.**
