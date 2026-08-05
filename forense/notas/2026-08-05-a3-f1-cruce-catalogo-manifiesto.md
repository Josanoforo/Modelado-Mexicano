Contadores movidos: 0. (Este acto es de instrumento — repara la cadena
`tests/catalogo.py` → `tests/dedup.py` → `tests/cruce_operables.py` — no de
evidencia; no toca Hito D, `data/manifiesto.yaml` ni ningún veredicto `RX.Y`.)

# A3 · F1 — reparar la cadena del cruce catálogo × manifiesto

*5 de agosto de 2026.* Rama `claude/bloque-arranque-verificacion-n1byxs`
(clon existente, no nuevo). HEAD al abrir y al escribir esta nota:
`32d9321` (== `origin/main`, sin divergencia — `git fetch` confirmado).
Encargo declaraba base `9729894`; es ancestro de HEAD (main avanzó por
PR #97–#100 mientras tanto, refresco reportado antes de editar, sin volver
a derivar nada del perímetro porque este acto no toca canon/perímetro).

**Los tres defectos que mesa reprodujo, verificados aquí antes de tocar
código** (protocolo del encargo: reproducir antes de arreglar).

---

## Defecto 1 · dependencia no documentada

`python3 tests/cruce_operables.py`, en un `data/` sin `catalogo_unico.json`
(el gitignorado, ausente en cualquier clon fresco), fallaba:

```
Traceback (most recent call last):
  File ".../tests/cruce_operables.py", line 77, in <module>
    op = [r for r in json.load(open(os.path.join(RAIZ, 'data', 'catalogo_unico.json')))
FileNotFoundError: [Errno 2] No such file or directory: '.../data/catalogo_unico.json'
```

**Diagnóstico, no typo.** `catalogo_unico.json` no es un nombre mal escrito
de `catalogo_derivado.json`: es un derivado real y distinto, que produce
`tests/dedup.py` (línea 83) a partir de `catalogo_derivado.json` (que a su
vez produce `tests/catalogo.py`). La diferencia importa — `catalogo_unico.json`
trae las 131 filas ya deduplicadas por acrónimo+título y el campo `en_disco`
que `cruce_operables.py` necesita; `catalogo_derivado.json` todavía tiene las
~201 entradas crudas, con duplicados como "LAPOP" y "AMERICASBAROMETER /
LAPOP" contados como dos filas separadas (ver Defecto 2). Sustituir uno por
otro no haría pasar el script correctamente — produciría un `op_acr` con
ruido, no el problema que el guard debía resolver.

**Arreglo:** guarda de archivo ausente (mismo patrón ya usado en
`catalogo.py`/`dedup.py` para `data/inventarios/`), con el porqué en el
docstring del módulo, y `Uso:` actualizado a la cadena completa de tres
comandos. No se auto-invoca `dedup.py` desde `cruce_operables.py` — la
cadena se mantiene explícita y visible (así es como el propio encargo pide
reportarla), no oculta detrás de un subproceso.

---

## Defecto 2 · el cruce no cerraba (`MAPA incompleto`)

Tras `dedup.py`, `cruce_operables.py` terminaba en:

```
MAPA incompleto, falta(n): {'LATINOBARÓMETRO', 'INE', 'CLUES', 'CONEVAL', 'LAPOP'}
```

**Diagnóstico.** Las cinco son filas reales, limpias, operables (`micro=sí`,
`libre=sí`) de `catalogo_unico.json` — no artefactos de dedup ni fuentes
ausentes del catálogo. `MAPA` (el diccionario cerrado, mantenido a mano en
`cruce_operables.py`) simplemente nunca les asignó clave: tenía 38 de las 43
operables reales (`dedup.py` ya derivaba 43 antes de este acto).

La pista del encargo — "LAPOP aparece a la vez como registrada y como
faltante" — es real pero apunta a un señuelo, no al defecto en sí. Verificado
en `catalogo_unico.json`:

```
acronimo: 'LAPOP'                      micro=sí libre=sí   n_dom=4   en_disco=True   ← operable real
acronimo: 'AMERICASBAROMETER / LAPOP'  micro=sí libre=?    n_dom=1   en_disco=True   ← NO operable (libre≠sí, nunca entra a `op`)
```

Son dos filas separadas porque el dedup por título de `dedup.py` no las
fusionó: el inventario que solo dice "AmericasBarometer / LAPOP" (sin
descriptor en español) no comparte título normalizado con el que sí lo
tiene. La que aparece "registrada" en la lista cruda de `dedup.py` (que
opera sobre las 131 filas, no solo las 43 operables) es la fila compuesta,
no operable — un lector apurado podría "arreglar" esto añadiendo
`'AMERICASBAROMETER / LAPOP'` a `MAPA`, y esa clave nunca se usaría (no
está en `op_acr`). El arreglo real es más simple: `MAPA['LAPOP']`, la fila
que sí importa. Comentario dejado en el código para que el próximo que lea
esto no repita el señuelo.

**Arreglo:** 5 claves añadidas a `MAPA`, en su posición alfabética (el
diccionario ya estaba ordenado así):

```
'CLUES': [], 'CONEVAL': [], 'INE': [],
'LAPOP': ['lapop'], 'LATINOBARÓMETRO': ['latinobarometro'],
```

Verificado entrada por entrada contra `data/manifiesto.yaml` (no aceptado
de memoria): CLUES/CONEVAL/INE — cero ids con esos prefijos en el
manifiesto (`grep -in` sin resultados) → `[]`, mismo estado que la mayoría
de `MAPA`. LAPOP → `lapop_abmex2023_cuestionario_mexico` (con `sha256`,
así que entra a `con_payload`) — es un cuestionario PDF de Vanderbilt, no
microdato, así que se agregó también a `SOLO_INSTRUMENTO` (ver más abajo;
primera pasada de este arreglo lo dejó fuera y `cruce_operables.py` lo
reportaba "EN MANIFIESTO", falso — corregido antes de cerrar el acto).
LATINOBARÓMETRO → dos ids (`latinobarometro2024_cuestionario_esp`,
`latinobarometro2024_fichas_tecnicas`), ambos con `sha256`, ambos PDF
(cuestionario y fichas técnicas, no microdato) — igual, a
`SOLO_INSTRUMENTO`. Resultado real tras el arreglo: LAPOP y LATINOBARÓMETRO
→ **PARCIAL** (documentación real en disco, microdato no), no "EN
MANIFIESTO". `docstring` y el print de "38 operables" corregidos a 43 en
el mismo cambio (quedaban desincronizados del `MAPA` ya completo).

---

## Defecto 3 · subconteo por prefijo en `dedup.py`

`dedup.py` reportaba `OPERABLES ya en disco: 15`. Verificado entrada por
entrada contra el manifiesto (no aceptado del encargo): son **17**.

**Diagnóstico, dos bugs independientes en la misma función** (líneas
62-82 de la versión previa):

1. **Prefijo numérico.** `pref = {m.group(0).upper() for i in ids if (m :=
   re.match(r'^[a-z]+', i))}` exige que el id empiece con letras. Los 5 ids
   de ENSANUT en el manifiesto empiezan con un ordinal de documento
   multi-parte (`1_vfinal_..._ensanut_2024_...` … `5_vfinal_...`) —
   `re.match` devuelve `None` y esos ids no aportaban NINGÚN prefijo.
   Verificado que simplemente saltarse el número tampoco alcanzaba: el
   siguiente token es `vfinal`, no `ensanut` — la palabra significativa no
   está al inicio. El arreglo prueba todas las palabras del id (no solo la
   primera) cuando el id no tiene letras iniciales.
2. **Acento sin normalizar.** El acrónimo `LATINOBARÓMETRO` se comparaba
   con `.upper()` pero sin plegar a ASCII, contra ids del manifiesto que sí
   son ASCII (`latinobarometro2024_...`) — "Ó" ≠ "O" a nivel de byte, nunca
   iba a calzar aunque el id existiera. El arreglo pliega el acrónimo con
   el mismo patrón NFKD que el archivo ya usa en `norm()`/`akey()`.

**La receta se probó contra el caso conocido antes de confiar en ella**
(disciplina explícita del encargo, y la razón de la sección siguiente): la
primera versión del arreglo (extraer TODAS las palabras de TODOS los ids,
no solo de los que empiezan con dígito) dio **19**, no 17 — con dos falsos
positivos (`ENCUESTA NACIONAL DE BIENESTAR`, `ENCUESTA NACIONAL PARA EL
SIST`, `GLOBAL FINDEX DATABASE` entraban por palabras genéricas como
"nacional"/"global") y una regresión (`CPV` se perdía, porque el filtro
`len>3` que antes solo aplicaba a la comparación por substring quedó mal
puesto también en la construcción del set, y `"cpv"` tiene 3 letras). Es
exactamente el defecto que el encargo cita del reparto del cruce v2.0: un
conteo por ocurrencias sobre un archivo entero miente. La versión final
—fallback a todas las palabras SOLO para los ids que no empiezan con
letra, filtro de longitud solo en la comparación, igual que antes— da
**17**, con el delta exacto esperado (`ENSANUT` y `LATINOBARÓMETRO`
pasan a `True`, nada más se mueve, nada se pierde). Verificado con un
script de comparación ad-hoc antes de tocar `dedup.py`, no después.

**Efecto colateral, verificado y benigno:** el mismo pliegue de acento
también activa un match para la fila no-operable "ÍNDICES DE INTENSIDAD
MIGRATORIA" (México-Estados Unidos) en la lista cruda de "ya registradas"
de `dedup.py` (16→19, no 16→17 — el 19 cuenta las 131 filas, no las 43
operables). Es esperable y correcto dejarlo así: `micro=no` para esa fila,
así que nunca puede entrar a `op`/las 43 operables ni al conteo de 17
verificado arriba; y el pliegue de acento no se puede aplicar solo a
LATINOBARÓMETRO sin reintroducir el mismo tipo de parche-por-síntoma que
este acto existe para evitar.

---

## Cadena completa, salida cruda (estado final, tras los tres arreglos)

```
$ rm -f data/catalogo_derivado.json data/catalogo_unico.json   # limpio, sin ellos data/raw tampoco se usa (premisa 1)

$ python3 tests/catalogo.py
VERIFICACIÓN DE RECETA (parser vs. conteo crudo de encabezados numerados)
  ok        credito-ahorro-finanzas-hogar    crudo= 15  parseado= 15
  ok        migracion                        crudo= 27  parseado= 27
  ok        tecnologia-digital               crudo= 16  parseado= 16
  ok        capital_social                   crudo= 14  parseado= 14
  ok        clase-fuente                     crudo= 18  parseado= 18
  ok        cultura_valores_opinion          crudo= 20  parseado= 20
  ok        salud                            crudo= 18  parseado= 18
  ok        seguridad_justicia               crudo= 12  parseado= 12
  ok        trabajo_ingreso_formalidad       crudo= 21  parseado= 21
  ok        tramites_estado                  crudo= 23  parseado= 23
  ok        uso_del_tiempo_cuidados_hogar    crudo= 17  parseado= 17
RECETA: consistente

ARCHIVOS: 11   ENTRADAS (con repetición): 201
FUENTES ÚNICAS (dedup por acrónimo): 151
[...]

$ python3 tests/dedup.py
ENTRADAS: 201    FUENTES ÚNICAS tras dedup por acrónimo+nombre: 131
MICRODATOS sí=55 no=34 ?=42
OPERABLES (microdatos + acceso libre): 43
TRANSVERSALES (3+ dominios): 17   mono-dominio: 97
[...]
CRUCE CONTRA data/manifiesto.yaml
  fuentes del catálogo ya registradas: 19 (AMERICASBAROMETER / LAPOP, CPV, ENADID, ENCIG,
  ENCUCI, ENCUP, ENDIREH, ENDUTIH, ENIF, ENIGH, ENNVIH, ENOE, ENSANUT, ENUT, ENVIPE, LAPOP,
  LATINOBARÓMETRO, MOCIBA, ÍNDICES DE INTENSIDAD MIGRATOR)
  OPERABLES ya en disco:      17
  OPERABLES sin bajar:        26

$ python3 tests/cruce_operables.py
ACRONIMO                         ESTADO         PAYLOADS  (sin-payload)
[... 43 filas ...]
CPV                               EN MANIFIESTO    8       (0)
ENSANUT                           EN MANIFIESTO   24       (0)
LAPOP                             PARCIAL          1       (0)
LATINOBARÓMETRO                   PARCIAL          2       (0)
CLUES / CONEVAL / INE             SIN PAYLOAD      0       (0)   (las tres)

RESUMEN: {'EN MANIFIESTO': 11, 'PARCIAL': 2, 'SIN PAYLOAD': 30}
OPERABLES SIN PAYLOAD DE VERDAD: 30 de 43
```

Salida completa (sin recortar) archivada junto con esta sesión; lo de
arriba es la forma legible. Los 43 renglones íntegros de `cruce_operables.py`
se reproducen corriendo la cadena — ese es el punto de este arreglo.

---

## Suite

```
$ python3 tests/check.py --baseline     # ANTES de tocar código
  18 FAIL · 95 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe5)

$ python3 tests/check.py --baseline     # DESPUÉS de los tres arreglos + doc
  18 FAIL · 95 WARN
  LÍNEA BASE: VERDE — nada nuevo frente a tests/baseline.json (HEAD congelado 837d5fe5)
```

Idéntico antes/después — esperable: `check.py` vigila `canon/`, `corpus/`,
`README.md`, `milpa/` y refs colgantes/duplicados en todo el árbol; este
acto no toca ninguno de esos, solo `tests/dedup.py`, `tests/cruce_operables.py`
y el bloque de cifras de `data/catalogo-fuentes-v2_0.md`.

---

## Lo que este acto no hace

No toca `data/manifiesto.yaml` (lo escribe P-B en paralelo). No descarga
nada — cero llamadas de red fuera de `git fetch`. No sella ADR. No toca
`canon/` ni `forense/hitoD-preregistro`. No re-deriva ni sustituye las
cifras de `data/catalogo-fuentes-v2_0.md` — las re-etiqueta como
históricas/congeladas y apunta al comando (verificadas iguales hoy a las
que ya tenía, no reemplazadas por eso).

## Hallazgos fuera de perímetro, reportados no resueltos

- `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=cloud_default` al abrir — el
  protocolo de arranque de este encargo esperaba `sin_variable`. No es
  `ubuntu` (la prohibición explícita), así que se interpretó como cloud
  válido y se continuó; queda declarado por si el protocolo de arranque
  necesita ese valor específico documentado en algún lado.
- Sonda de red a `https://www.inegi.org.mx/` (paso 4 del arranque):
  `curl` no conectó (exit 56, código 000) incluso con `HTTPS_PROXY`
  configurado — consistente con que este acto declaró de entrada que su
  red es solo git (premisa 1); no se investigó más porque no bloqueaba
  nada de este encargo.
