# Cierre · `ACTO GEN2-FIRMAS-MESA-1` — propagar las 15 firmas del 15/sep

**15 de septiembre de 2026 · NUBE, Opus · `ADR-513`**
Encargo archivado verbatim por A.3 en
`forense/encargos/2026-09-15-GEN2-FIRMAS-MESA-1.md` (commit `6b47dc3`).

---

## 1 · Arranque y entorno (A.2, tres partes)

Salida cruda de `python3 tools/entorno.py`, al arrancar:

```
ENTORNO · commit=582d4e936654 · git_status=LIMPIO(0) · python=3.11.15 ·
numpy=AUSENTE pandas=AUSENTE scipy=AUSENTE yaml=6.0.1 pyreadstat=AUSENTE ·
CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default ·
red=no-ejecutada · raices=data_raw:NO · corpus=NO(examinados=0)
```

Las tres partes, dichas por separado: el **entorno** es nube
(`cloud_default`); la **red** no se sondeó porque este acto no descarga nada
(una sonda que nadie pidió es I/O que nadie declaró); el **dato** no está
montado (`corpus=NO`, `archivos_examinados=0`). `data/raw/` no existe. Es
exactamente lo que el encargo declara en su cabecera: **no abre microdato**.

Guard de arranque: base al día (`0` commits detrás de `origin/main`), árbol
limpio, sin duplicados de rótulo (rama remota, worktree y PR abiertos
comprobados), `limpia_arbol.py --reporta` sin hallazgos accionables.

## 2 · La compuerta mordió — y eso es el primer entregable

`COMPUERTA: merge de #779 y #781`.

Al abrir el encargo, `origin/main` era `81c7f63` y traía **sólo `#781`**:

```
$ git merge-base --is-ancestor 6e3591c origin/main
NO-ANCESTRO: #779 NO esta en origin/main
```

`#779` figuraba `state:"open"`, `merged:false`, y era el **único PR abierto**
del repo. **La sesión se negó con cero commits y reportó**, como el propio
encargo ordena («si no está, te niegas y reportas»).

No fue formalismo. `#779` escribe `data/corrida0/decisiones.tsv` (`4 ++++`) y
`forense/no-corrido.tsv` (`6 ++--`) — **los dos archivos exactos** donde caen
P1 y P4 — y su cuerpo declara que cierra `NC-0198`. Propagar antes habría (a)
censado la verificación A.8 contra un estado que caducaba en el merge, (b)
obligado a adivinar qué quedaba del OBJETO 1, que es reinterpretar un OBJETO,
y (c) producido conflicto mecánico garantizado al final de `decisiones.tsv`.

Fusionado `#779` (`582d4e9`), la compuerta se re-verificó por ancestría
(`COMPUERTA: #779 EN MAIN -- ABIERTA`) y el acto arrancó sobre esa base.

## 3 · Verificación de existencia A.8, re-derivada tras la compuerta

La cabecera del encargo ordenaba re-verificar `NC-0198`. Se hizo, y cambió el
plan:

| objeto | esperado por el encargo | real tras la compuerta |
|---|---|---|
| `NC-0198` | ABIERTA | **ya `CERRADA`** por `ACTO GEN2-MEDICION-DEMANDA-1` |
| `CALC-ENIGH-0001`, `CALC-ENFIH-0001`, `CALC-EDER-0003`, `CALC-ENUT-0001` | pendientes de fila | **las cuatro ya con `cuenta_gen2=SI`**, fecha 2026-09-15 |
| `FP-371`, `FP-372` | ABIERTA | ABIERTA ✔ |
| `NC-0086`, `NC-0125`, `NC-0160`, `NC-0142` | ya CERRADAS | ya CERRADAS ✔ |

Conclusión aplicada: **el OBJETO 1 ya estaba cumplido y no se duplicó.** «El
OBJETO 1 solo aplica a lo que falte», y no faltaba nada. No se reescribió
autoridad ajena ni se añadió una quinta fila redundante.

### A.8 sobre reglas citadas (`tools/ya_medido.py`)

El encargo cita siete ids de regla. `T-YAMEDIDO` los exige censados; el
encargo verbatim **no se edita** para complacer un test (misma regla que rige
T25), así que se corrió la herramienta y su salida se conserva aquí, y el
archivo se censó en `_T_YAMEDIDO_ARCHIVOS_CONOCIDOS` con esa razón:

```
familia.apoyo.recibe_dinero_familiares        MEDIDA-EN: tramite-ola5-propuesta-v0.yaml, tramite.yaml
familia.cuidado.recae_mujeres_40mas   (R5.2)  MEDIDA-EN: tramite.yaml
tramite.mordida.discrecional          (R3.1)  MEDIDA-EN: CALC-ENCIG-0001, CALC-ENCUCI-0001, tramite-ola5-propuesta-v0.yaml, tramite.yaml
tramite.mordida.con_registro          (R3.2)  MEDIDA-EN: CALC-ENCIG-0001, tramite.yaml
dinero.ahorro.horizonte_corto                 MEDIDA-EN: CALC-ENIF-0001, tramite.yaml
dinero.ahorro.horizonte_no_corto_con_seguridad_social  MEDIDA-EN: CALC-ENIF-0001, tramite.yaml
familia.corresidencia.adulto_familiar         MEDIDA-EN: CALC-EDER-0001, tramite-ola5-propuesta-v0.yaml
```

**Las siete `MEDIDA-EN`, ninguna `NUNCA-MEDIDA`.** Este acto no mide ninguna:
las cita como los **consumidores** cuyas glosas de prosa enmienda.

## 4 · Contador, sin disfraz

**Cero mediciones propias. Cero adopciones.**

| contador | antes | después |
|---|---|---|
| `N_corridas_selladas` | 72 | **72** |
| `N_resultados_gen2_sellados` | 3 255 | **3 255** |
| `N_resultados_gen2_adoptados_activos` | 16 | **16** |
| `dependencias_numericas_legacy_activas` | 191 | **191** |
| `N_resultados_gen2_pendientes_adopcion` | 5 | 3 |
| `N_resultados_gen2_vetados_por_decision` | — | **2** (categoría nueva) |
| NC abiertas | 69 | 60 (14 cerradas, 5 nuevas) |
| FP abiertas | 3 | **1** (`FP-374`) |

Los cuatro contadores de **medición y adopción no se movieron un bit**, que es
lo que el encargo prometió. Lo que se movió es **contabilidad**: la cola
aparente de adopción deja de contar dos RESULT que una decisión vigente
prohíbe adoptar.

## 5 · Las cuatro glosas — la prueba de que sólo cambió prosa

```
$ git diff --stat milpa/tramite.yaml
 milpa/tramite.yaml | 94 ++++++++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 94 insertions(+)

$ git diff milpa/tramite.yaml | grep -E "^-" | grep -v "^---"
(sin salida)
```

**94 inserciones, 0 borrados.** Ni un `tier`, ni una `p`, ni un `ic95`, ni un
`n`, ni un `sha256_payload` se tocó. La forma es la del precedente único del
propio archivo (clave hermana `*_enmienda_fechada: >`, `milpa/tramite.yaml:339`),
que abre con fecha + ACTO y cierra declarando que el texto previo no se edita
ni se borra.

Dos de las cuatro valen más que su tamaño:

- **`NC-0195`** escribe la identidad `enif_2024_enif_2024_bd_csv` que el
  propio `sha256_payload` de la regla ya probaba. **Desbloquea `CORR-0010`
  sin descargar nada.** El acto que escribió «NO-LOCALIZADO» buscó el id
  `enif2024_csv`, que es otro ZIP: el defecto era de búsqueda, no de corpus.
- **`NC-0196`** fija que `FAC_HOG` vive en `tsdem.csv`, no en `tvar_crea.csv`
  (que trae `FAC_PER`), con la guarda `G-FAC-HOG-TSDEM-IGUAL-THOGAR` de
  `CALC-ENUT-0001`. La propia fila lo decía: «no bloquea la corrida; bloquea
  la lectura».

## 6 · Lo que no se pudo aplicar — y por qué no se estiró

**`CORR-0004` sigue `BLOQUEADA`.** El OBJETO 3 dice «Aplica a
CORR-0004/0005/0006/0019», pero la opción (a) es **precedencia del MEDIDO**, y
`tramite.gobierno_digital.coercitivo:adopta` (ASIGNADO 0.09) **no tiene
MEDIDO de su regla**. La propia nota de mesa que armó D2 lo dice con todas sus
letras:

> «`CORR-0004` queda fuera de (a) —no tiene medido— y se resuelve por
> separado.»

La segunda casilla que esa nota abrió para esa fila (buscar instrumento de
unidad persona **/** rotular `ASIGNADO·SIN-INSTRUMENTO`) **no viene firmada**
en la hoja. El ejecutor propaga, no decide: va a `NC-0206` con la razón
escrita, no se reinterpreta.

Las otras tres sí se propagaron, con el MEDIDO citado fila por fila, y
`CORR-0019` celda por celda (5 de 21 retiradas, 16 conservadas), derivado
mecánicamente de `milpa/` y no a ojo.

## 7 · Reservas que la firma *crea* (y que no se barren)

Firmar `FP-371` y `FP-372` **caduca premisas escritas en otros archivos**:

- `data/diseno-muestral.yaml:504-515` todavía dice «mientras `FP-371` siga
  ABIERTA» y «`FP-372` decide su uso inferencial».
- `forense/prereg-caja/S6-L16-spec-v1_5.md` remite a `FP-372` como decisión
  pendiente — y esa spec está **sellada** con `.sha256`, así que pediría
  sucesora v1_6.

Ninguno de los dos está en el perímetro. Lo que **sí** estaba
(`milpa/tramite-ola5-propuesta-v0.yaml`, bloque
`enmienda_alcance_inferencial_2026_09_10`, que declaraba «FP-372 ABIERTA;
esta enmienda no firma opción A ni B») **se enmendó**. El resto va a
`NC-0209`: mientras no se propague, el árbol dice dos cosas sobre el mismo
objeto, y eso se declara en vez de disimularse.

## 8 · Las dos specs de munición — auditadas, no aceptadas de palabra

`CALC-ENCIG-2023-0001` (59 RESULT) y `CALC-ENVIPE-DENUNCIA-SEGURO-0001`
(57 RESULT), cada una en **dos capas (D-15)**: spec humana sellada +
sidecar `.sha256` en `forense/prereg-caja/`, y cara mecánica `spec.yaml` +
`spec.md` en `data/corrida0/`.

Verificado por comando, no por declaración:

- esquema y orden de claves idénticos a `CALC-ENFIH-0001` (0 claves faltantes);
- los cuatro `sha256` cruzados (`spec_md_sha256`, `spec_sellada_sha256`)
  cuadran con los archivos reales;
- `cuenta_gen2: PENDIENTE-DE-MESA` en ambas — la firma autoriza **medir**, no
  declara OBJETO sobre el contador (estándar FP-367/368 no satisfecho), y se
  dice en vez de darse por concedido;
- **sin `medidor.py`** en ninguna de las dos;
- **las 29 variables declaradas entre ambas existen**, auditadas contra
  `data/inventario-reactivos-v1_2.tsv` por archivo + columna: **ninguna
  inventada**.

Dos hechos quedaron como PARÁMETRO y no como detalle, porque resolverlos por
nombre tomaría el objeto equivocado sin avisar: `FAC_TRA` vive en `sec_7`
mientras `sec_8` trae `FAC_P18` (otro ponderador, otro universo), y el join
`sec_7 × sec_8` lleva llave declarada con guardia
`NO-ESTIMABLE-LLAVE-NO-UNICA`, sin deduplicar sobre la marcha.

La spec ENCIG-2023 es además el vehículo que corrige, **sin reescribir el
sello** (E.3), la frase «ENCIG2023, sin payload» de
`ENCIG-MORDIDA-spec-v1_0.md:142`, falsa en la letra desde el 29/jul/2026.

**Ninguna de las dos se corre aquí** (`NC-0207`): `preflight` reportará
`BLOQUEADO:script_ausente` para ambas hasta que CAJA escriba los medidores, y
eso es correcto, no un defecto.

## 9 · El verificador F5 — qué cierra `NC-0178` y qué no

`F5-documental-ejecucion-v1_2.md`, sucesión; v1.1 y v1.0 **intactos**.

El defecto medido: `--verify` hasheaba `data/manifiesto.yaml` **entero**, que
crece con cada adquisición (1 599 → 1 608 filas por seis commits ajenos). El
verificador no detectaba alteración de la evidencia del duelo: detectaba
**actividad de adquisición**. Un verificador que falla por algo que no es su
objeto enseña a ignorarlo.

v1.2 lo acota a las 8 entradas que el duelo usa, **derivadas** de la
materialización congelada (5 de `DIN-M-01`, 3 de `TRA-M-07`), con la
serialización canónica **declarada** —orden por `id`, `json.dumps` con
`sort_keys`, separadores fijos, UTF-8—, porque un hash sobre un subconjunto
sin orden fijado no es reproducible.

**`NC-0178` cierra por el contrato, no por la ejecución.** Su sucesor pedía
literalmente «fija `sha256_manifiesto_fuentes` a las 8 filas del contrato, no
al archivo entero», y eso es lo que v1.2 fija. Pero `tools/f5_documental.py`
está **fuera de perímetro**, así que el runner sigue implementando la versión
de archivo completo y **`--verify` sigue sin imprimir `OK`**. Eso va a
`NC-0208`, para que el cierre de `NC-0178` no se lea como más de lo que es.

## 10 · Cascada y suite

`tools/cierre_acto.py --aplica`:

```
APLICADO: gobernanza 512->513 · L0 512->513 · tabla estado 512->513
```

Rótulo `GEN2-FIRMAS-MESA-1` censado en `canon/registro-rotulos.tsv` (D-6).

`tests/check.py --baseline`: un único `FAIL` nuevo apareció durante el acto,
`T-YAMEDIDO` sobre el encargo archivado, y se resolvió **censando el archivo
con su razón** (§3), nunca editando el encargo verbatim. `T06` y `T08` son
entradas de línea base preexistentes, ajenas a este acto.
`tests/test_corrida0.py` 91/91 · `tests/test_motor_usos_complementos.py` 16/16
· `tests/test_emite_m_calibracion.py` 16/16 (incluye la regresión P2 que cita
conductas de `tramite.mordida.*` por texto exacto de línea).

## 11 · Falsador de este acto

Si en el siguiente acto de CAJA alguna de las dos specs congeladas resulta
**no ejecutable por una razón visible desde el metadato que había aquí** —una
columna que el inventario declaraba y no existe, una llave de join que no es
única sin guardia, un ponderador resuelto al archivo equivocado—, entonces la
disciplina de congelar en nube contra inventario de columna no está pagando lo
que dice pagar, y la pieza que falló se revierte y se anota.

**Sucesor:** `ACTO GEN2-MEDICION-DEMANDA-2` (CAJA), con las dos specs de P3.
