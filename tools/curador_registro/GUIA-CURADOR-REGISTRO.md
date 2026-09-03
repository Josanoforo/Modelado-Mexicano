# Curador reusable del registro demanda-universo

Este directorio contiene utilidades generales para validar un baseline semántico
y derivar su cola de candidatas. El baseline es la fuente de verdad; la cola es
una vista reproducible y no debe versionarse.

```bash
python3 tools/curador_registro/baseline.py RUTA_AL_BASELINE
python3 tools/curador_registro/derive_queue.py RUTA_AL_BASELINE --output /tmp/cola.tsv
```

La identidad estable de una relación se construye con la terna
`(necesidad_id, fuente_canonica_normalizada, objeto_evidencia_id_canonico)`.
El validador comprueba hashes, conteos declarados, procedencias, fusiones,
decisiones y la proyección de utilidad sin depender de nombres o cantidades
particulares de una corrida.

## `via_capa2.py` — la vía de `capa2_manifiesto`

```bash
python3 tools/curador_registro/via_capa2.py --root .              # solo lectura (por defecto)
python3 tools/curador_registro/via_capa2.py --root . --escribe    # aplica los diffs propuestos
```

Deriva `capa2_manifiesto` por fila de `relaciones.tsv` contra `data/manifiesto.yaml`
real y reporta el diff propuesto. Solo promueve a `SI` cuando `id_manifiesto`
resuelve a una entrada con payload verificado — nunca por coincidencia de
nombre de fuente. Ver `forense/notas/2026-08-13-v2-via-capa2.md` para la
especificación completa (qué distingue `SI`/`SI_O_REFERENCIADO`/`NO_REFERENCIADO`,
y por qué esta vía no promueve las filas `SI_O_REFERENCIADO` automáticamente).

## alta de fuente nueva en tres tablas

**Por qué existe esta sección.** `ACTO MAESTRA34-A1` (1/sep/2026) paró al
intentar dar de alta SICEE en `relaciones.tsv`: las tres invariantes de
`baseline.py` están **acopladas** y una fila suelta rompe las tres a la vez.
Eso se levantó como `FP-230`; `ACTO MAESTRA34-N6 · CURADOR-Y-SUITE` lo ejecutó
y ésta es la vía que usó. `data/INFRAESTRUCTURA-v1_0.md` (D1) cita esta sección
en lugar de decir «SIN VÍA».

**No hay script que escriba estas tres tablas y esta sección no inventa uno.**
Lo que hay es un procedimiento con la derivación de ids fijada, para que dos
personas distintas produzcan los mismos ids a partir de los mismos insumos.

**Las tres invariantes que hay que satisfacer a la vez** (`validar_baseline()`):

1. toda relación de `relaciones.tsv` tiene ≥1 procedencia en `evidencias.tsv`;
2. `utilidad-modelo.tsv` es proyección **1:1** de `relaciones.tsv` (mismo
   conjunto de `relacion_id`, misma cardinalidad);
3. `len(evidencias) − len(relaciones) == len(fusiones-relaciones)`.

Por eso **un alta se escribe en las tres tablas en la misma operación**: +1
relación, +1 procedencia, +1 fila de utilidad. Si se añade más de una
procedencia por relación (una fusión), hay que declararla en
`fusiones-relaciones.tsv` o la invariante 3 se rompe.

**Derivación de ids — reproducible, nunca a mano:**

| id | derivación |
|---|---|
| `relacion_id` | `relacion_id(necesidad_id, fuente_canonica_normalizada, objeto_evidencia_id_canonico)` de `baseline.py` — `"REL-" + sha256("\x1f".join(terna))[:24]`. **Impórtala, no la reimplementes**: el validador la recomputa fila por fila y falla con `relacion_id no determinista`. |
| `objeto_evidencia_id_canonico` | `"OE-" + sha256("\x1f".join((fuente_canonica_normalizada, descripcion_del_objeto)))[:24]`. El validador no la comprueba (los `OE-` originales vienen del bulk-load `16180e6`); se fija aquí para que el mismo objeto dé el mismo id en altas futuras. Dos objetos distintos de la misma fuente → dos `OE-` distintos → dos relaciones. |
| `procedencia_id` | `"PROV-" + sha256("\x1f".join((relacion_id, procedencia_fuente, procedencia_objeto_evidencia_id, evidencia_ref)))[:24]`. Debe ser único en toda la tabla. |

**Procedimiento:**

1. **Necesidad.** Comprueba que la `necesidad_id` existe en
   `necesidad-objeto-modelo.tsv`. Si la regla del modelo no tiene `N` asignada,
   el alta empieza ahí (id nuevo derivado con
   `cut -f1 … | sort -V | tail -1`, sin heredar).
2. **Alias.** Si la fuente es nueva, dale fila en `aliases-fuentes.tsv` y decide
   explícitamente si se fusiona con una fuente canónica existente. Por defecto
   **no** se fusiona: misma institución no es mismo objeto.
3. **Escribe las tres filas** con los ids derivados como arriba.
   `clasificacion_relacion` sólo admite `CONFIRMADA` · `NEGATIVA` · `CANDIDATA` ·
   `NO_ACCESIBLE`. `capa2_manifiesto` = `SI` sólo si `id_manifiesto` resuelve
   contra `data/manifiesto.yaml`; `capa3_disco_real` afirma el disco, así que en
   un entorno sin corpus montado se **cita** su medición (con el acto que la
   hizo) y se dice que no se reverificó — no se afirma haber tocado el disco.
   Nunca se rellena un campo por estimación: `NO_DETERMINADO` es una respuesta.
4. **Recifra** `data/curacion-registro/baseline.json`: `archivos[*].sha256` y
   `archivos[*].filas` de las tres tablas tocadas, más los `conteos` derivados
   (`relaciones_activas`, `procedencias_aceptadas`, y el conteo por estado). Los
   `sha256` quedan inválidos en cuanto se escribe, así que el recifrado no es
   opcional: es parte del alta. Anota en `procedencia.origen` qué acto recifró y
   por qué.
5. **Valida en verde**, sin excepciones:

```bash
python3 tools/curador_registro/baseline.py data/curacion-registro   # "ok": true, "errores": []
python3 tools/curador_registro/via_capa2.py --root .                # lectura: 0 diffs propuestos
```

`via_capa2.py` **nunca degrada** una fila (`derivado = "SI" if estado ==
"COINCIDE" else actual`): «0 diffs» no confirma un `capa2 = SI`, sólo dice que
no lo contradice. Sin `data/raw` montada devuelve `AUSENTE`/
`RAIZ_NO_CONFIGURADA` y la confirmación positiva queda pendiente de un acto en
caja. Decirlo es parte del alta.

---

## Enmienda de dirección a ACTO MAESTRA35-L3 (2/sep/2026)

Todo payload nuevo se registra por la infraestructura del curador (Codex,
A5/`PR #441`), en este orden y sin reinventar:

1. **Capa payload.** Archivo en el corpus compartido +
   `tests/manifiesto.py --registra --id … --usado-para … --url-origen …
   --descargado-por … --fecha-descarga …`, una invocación por `--id`; sha y
   tamaño los deriva el script.
2. **Capa cola del registro.** Fila por `fuente_canonica` en
   `data/curacion-registro/cola-adquisicion-registro.tsv`
   (`estado_A4A5`, `ids_manifiesto`, nota con fecha y comando). Fuente nueva
   = fila en `aliases-fuentes.tsv` + fila en la cola citando la receta.
   Después, `python3 tools/vista_cola_adquisicion.py`
   (`data/cola-adquisicion-v1_0.tsv` es VISTA GENERADA, `T26` falla si no se
   regenera).
3. **Capa relación.** `relaciones.tsv` (`necesidad_id` /
   `fuente_canonica_normalizada` / `objeto_evidencia_id_canonico`) +
   `necesidad-objeto-modelo.tsv`; `python3 tools/curador_registro/via_capa2.py
   --root .` en lectura, y `--escribe` solo cuando el id resuelve a payload
   verificado.

Cierre con `tools/curador_registro/baseline.py` si el validador lo exige
(este archivo, §1). Raíz `descargas_mx` en `data/raices.local.yaml`.

---

## `estado_A4A5` — el token `OBTENIDO-PARCIAL` (3/sep/2026, ACTO MAESTRA37-N3)

`OBTENIDO-PARCIAL` entra al vocabulario de `estado_A4A5` de
`data/curacion-registro/cola-adquisicion-registro.tsv` como estado válido.
Estrenado por `ACTO MAESTRA36-A2` (fila 63, `EXT_OF_07_CATALOGO_PROVEEDORES_S1_S3_S6`):
se llegó a un payload verificado por `A.7` (sha256, estructura legible) que
NO es el objeto que la fila describe — es contenido adyacente de la misma
plataforma (los datos, no los diccionarios que el encargo pedía). Distinto de
`OBTENIDO` (el objeto pedido, completo) y de `NO-OBTENIDO-POR-ESTE-AGENTE`
(nada llegó). Verificado en `ACTO MAESTRA36-A2` y reconfirmado por
`ACTO MAESTRA37-N3`: ningún script de `tools/` ni `tests/` cuenta
`estado_A4A5 == OBTENIDO-PARCIAL` como `OBTENIDO`, así que el token no voltea
ningún contador en silencio.
