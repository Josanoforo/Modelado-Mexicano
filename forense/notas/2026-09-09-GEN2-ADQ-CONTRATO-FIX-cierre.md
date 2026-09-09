# ACTO GEN2-ADQ-CONTRATO-FIX — nota de cierre

**Fecha:** 2026-09-09 · **Entorno:** NUBE (encargo declara Opus; corrida real en Sonnet 5 — discrepancia reportada, no corregida en el registro) · **Redactado y ejecutado contra** `origin/main = cc1cfe2cf15f3abac8fcd64473531f7f99cb65d0` (al día, 0 commits detrás).

**Compuerta:** ninguna.

---

## 0 · Lo que no se pudo hacer, y por qué no bloqueó el resto

P0 del encargo pedía archivar verbatim `forense/notas/2026-09-09-REVISION-IMPLEMENTACION-PR660-666-astra.md` (insumo externo ChatGPT/Astra), con la cláusula «si falta, PARA». Ese documento **no llegó adjunto a esta sesión y no existe en el árbol** (`git grep -i "REVISION-IMPLEMENTACION-PR660"` sobre `origin/main` → 0 coincidencias). A diferencia de `ACTO GEN2-ADQ-VERIFICACION-CAJA` (`ADR-440`), donde el bloque ausente pudo reconstruirse de la propia enumeración del encargo, aquí el encargo **no** enumera el contenido del documento — solo cita sus conclusiones (H1/H2/H3/H5) de forma ya autocontenida y verificable contra el código.

La decisión tomada: el propio encargo declara que dirección **ya reverificó H1 textualmente** (cita exacta de la línea de código defectuosa) y **H5 «confirmado en clase»**, y pide explícitamente re-derivar H2/H3 contra el código como primer paso — es decir, el encargo mismo no depende de leer el documento ausente para ejecutar P1-P4. Se registra como `NC-0134` (`ABIERTA`, sucesor `DECISIÓN-DE-MESA-PENDIENTE`) en vez de parar el acto completo, siguiendo el principio de `AGENTS.md` («ante un defecto material, corrige, acota su efecto o pide decisión» — aquí el efecto se acota a la sola pieza de registro/procedencia, que no cambia ninguna medición ni comportamiento del ejecutable).

## 1 · Contraejemplos congelados en rojo antes de reparar

`tests/test_adq_contrato_fix.py`, 20 pruebas, corridas contra el código sin tocar:

```
FAIL prueba_h1_autorizada_fixtures_negativos_y_positivo: EXCEPCIÓN TypeError: _autorizada() takes 1 positional argument but 2 were given
FAIL H1: 'NO-AUTORIZADA' no debe leerse como autorizada; elegidos={'NEG_GUION', 'NEG_ESPACIO'}
FAIL H1: 'NO AUTORIZADA' no debe leerse como autorizada; elegidos={'NEG_GUION', 'NEG_ESPACIO'}
FAIL H1/P1: la invocación nominal no sustituye la autorización cuando el contrato exige ambas
FAIL H2: cita documental no debe leerse como intento, dio datetime.date(2026, 1, 1)
FAIL H2: cambiar la fecha de una cita documental no debe cambiar el cómputo
FAIL H2: una fecha dentro de un enlace no es un intento efectivo, dio datetime.date(2026, 8, 30)
FAIL prueba_h2_fecha_invalida_es_indeterminada_y_va_a_conciliacion: EXCEPCIÓN ValueError: month must be in 1..12
FAIL H2: debe tomar el intento MÁS RECIENTE, dio datetime.date(2026, 1, 1)
FAIL prueba_h3_recorrido_sonda_autorizacion_transformacion_seleccion: EXCEPCIÓN AttributeError: module 'adq_doctor' has no attribute 'transforma_sin_fetch_autorizada'
FAIL H5: tools/adquiere_cron.sh debe extraer la publicación inicial del censo a una función (publica_censo_manual) ...
FAIL H5: agente 0/publicación fallida no debe acreditar el día, dio 'COMPLETO' (...)
FAIL H5: el vigilante debe nombrar explícitamente la distinción terminar/publicar, dio 'COMPLETO' (...)
FAIL H5: el detalle debe citar publicacion=FALLIDA(2): '...'
FAIL H5: push fallido persistente no debe acreditar, dio 'COMPLETO'
FAIL H5: huella_adq con push fallido debe subir PUBLICACION_FALLIDA (...)
FAIL H5: el recibo local debe existir aunque el push falle
FAIL H5: el recibo debe declarar publicacion=FALLIDA(1): ''
FAIL H5: la señal REAL del vigilante sobre el recibo REAL del runner debe nombrar la distinción terminar/publicar; dio 'SIN-HUELLA' (...)

20 pruebas, 19 fallos
```

Solo `prueba_h3_pedida_no_salta_estado_sin_fetch_en_el_selector` daba ya el resultado correcto — por un efecto colateral del código anterior (la rama de `pedida` para `SIN-FETCH` caía siempre en el `catch-all` genérico, nunca en `candidatas`), no porque la excepción nominal funcionara. Se conserva como prueba de no-regresión.

## 2 · P1 · H1 — `_autorizada()` exige token, no prosa

**El defecto, verbatim:** `tools/adq_doctor.py::_autorizada()` era `return "AUTORIZADA" in (nota or "")`. Una comprobación de subcadena acepta `"NO-AUTORIZADA"` y `"NO AUTORIZADA"` — la negación contiene la afirmación como texto.

**El arreglo:** autorización afirmativa e inequívoca como token — `AUTORIZADA:<quién>/<AAAA-MM-DD>/<objeto>` (A.16) —, con `<objeto>` verificado contra la `fuente_canonica` de la fila evaluada (`_autorizada(nota, fuente)`, nueva firma), de modo que una cita que nombra otra fila no autoriza ésta. La negación (`NO[-\s]+AUTORIZAD[AO]S?`) se comprueba **primero** y con prioridad sobre cualquier match del token — un límite de palabra por sí solo no basta, porque `"NO-AUTORIZADA"` contiene `"AUTORIZADA"` como palabra completa, igual que una autorización real. También se retiró el `and not pedida` que dejaba a la invocación nominal saltarse la falta de autorización en el handoff de `/sonda` (P1: «invocación nominal no sustituye autorización si el contrato exige ambas»).

La fixture `KAPPA_AUTORIZADA` de `tests/test_adq_cableado.py` (prosa: `"AUTORIZADA por firma de mesa 2026-09-09"`) se migró a `"AUTORIZADA:mesa/2026-09-09/KAPPA_AUTORIZADA"` — mismo significado, formato correcto; era el único caso de la suite existente que dependía de la prosa.

## 3 · P2 · H2 — el ÚLTIMO intento efectivo, nunca uno inferido

**El defecto:** `fecha_intento_efectivo()` usaba `.search()` (primer match textual, no el de mayor valor) y, si no encontraba `intento efectivo`, caía a un *fallback* de fecha suelta (`\d{4}-\d{2}-\d{2}` en cualquier parte del texto, tras solo quitar menciones de `descubrimiento de vía`) — una fecha dentro de una URL o de una cita documental se leía como intento de descarga.

**El arreglo:** `findall()` sobre todas las menciones **explícitas** `intento efectivo <fecha>` y `max()` sobre las fechas válidas — el orden textual deja de importar. El *fallback* de fecha suelta se elimina por completo: enlaces, citas documentales y descubrimientos de `/sonda` nunca entran al cómputo, por construcción del regex, no por un filtro adicional que podría fallar. Una mención con fecha de calendario inválida (p. ej. `2026-13-40`) ya no revienta con `ValueError` sin atrapar ni se descarta como si no existiera: nuevo centinela `FECHA_INDETERMINADA`, propagado por `_clave_orden()` y `selecciona_filas()` hasta una exclusión explícita («va a conciliación de mesa»). El tratamiento definitivo de esa indeterminación (¿reintento con receta manual? ¿mesa decide fecha por decreto?) queda **propuesto a mesa**, no decidido aquí — este acto no habilita reintentos automáticos.

## 4 · P3 · H3 — la excepción nominal de verdad

**El defecto real** no era el que parecía: el código *sí* excluía `SIN-FETCH` cuando se nombraba por `--nombrada`, pero por accidente — la rama `if base in _RAZON_POR_ESTADO and not pedida` se saltaba con `pedida=True`, y como ningún otro `if` de la función maneja `SIN-FETCH`, la fila caía siempre en el `catch-all` final («estado fuera del contrato de elegibilidad»). La «excepción nominal» que la skill documentaba (`.claude/commands/adquiere.md`: «el operador puede nombrar cualquiera de ellos por ID») **nunca tuvo código que la implementara**, para ningún estado de `_RAZON_POR_ESTADO`.

**El arreglo, alineando selector/skill/runbook con una sola conducta:** `SIN-FETCH` tiene ahora su propia rama en `selecciona_filas()`, **siempre** excluyente — con o sin `pedida` — porque «no hay rama de excepción que salte estados en el selector». La única puerta hacia `PENDIENTE` (su estado accionable) es la transformación CANÓNICA nueva: `adq_doctor.transforma_sin_fetch_autorizada(fuente, ruta)` (CLI: `python3 tools/adq_doctor.py --transforma-sin-fetch <ID>`), que exige la misma autorización de H1 ya asentada en la nota de esa fila y escribe con el escritor de siempre (`tools/curador_registro/tsv_crudo.py::upsert_fila`, clave `fuente_canonica`) — no reimplementa el TSV. `OBTENIDO-PARCIAL` se verificó explícitamente que sigue sin habilitar descarga completa por defecto, con o sin autorización/`pedida` (matriz de casos, sin código nuevo — ya estaba correctamente excluido, ahora hay una prueba que lo fija).

Probado como integración completa, no herramienta por herramienta (`prueba_h3_recorrido_sonda_autorizacion_transformacion_seleccion`): fila `SIN-FETCH` con recomendación de `/sonda` → sin autorización, `transforma_sin_fetch_autorizada` se rehúsa y la invocación nominal no la selecciona → nota recibe `AUTORIZADA:mesa/2026-09-09/PILOTO_H3` → transformación canónica pasa el `estado_A4A5` a `PENDIENTE` en el TSV real → la fila se selecciona por el camino normal de `PENDIENTE`, sin invocación nominal.

`.claude/commands/adquiere.md` §1 reescrito con la misma conducta (antigüedad+H2, autorización-token+H1, `SIN-FETCH`+H3).

## 5 · P4 · H5 — el vigilante distingue terminar de publicar

**El defecto que el encargo nombra:** `tests/check.py::_t_cron_exitosa()` acreditaba el día con `invocado=si exit=0`, sin mirar el campo `publicacion=` que `tools/adquiere_cron.sh` ya escribía desde `ADR-439` (`OK` / `FALLIDA(n)`). El vigilante nunca leía la señal que el runner ya emitía.

**El arreglo:** `t_cron_huellas_adq()` extrae `publicacion=`; `_t_cron_exitosa()` exige que sea `OK` o esté ausente (huella histórica — compatibilidad explícita, no se reinterpreta); nuevo estado `AGENTE-OK-PUBLICACION-FALLIDA` cuando el agente cerró limpio pero la publicación falló, distinto de `ARRANCO-FALLO` (que sería falla del agente mismo).

`tools/adquiere_cron.sh` ~527-556 (P4 lo señala explícitamente): la publicación inicial del censo (paso 2.5, `[CENSO]`) se extrajo a `publica_censo_manual()` — ejercitable con el seam `ADQ_CRON_SOLO_DEFINE` igual que `commit_censo_linea()` —, y su fallo de push ahora **sí** incrementa `PUBLICACION_FALLIDA` (antes solo se logueaba `PARO-CENSO-PUSH` sin tocar el contador: un censo que nunca llegó al remoto podía cerrar la corrida con `publicacion=OK`). `push-sin-PR` (rama empujada, `gh pr create` falló o `gh` no está disponible) se comprueba explícitamente que **no** cuenta como publicación fallida — el recibo sí llegó al remoto, el PR es trámite de mesa.

**Dos defectos adicionales, no citados por la revisión, encontrados al construir la prueba de runner completo** (salida+recibo+señal juntos, exigida por la aceptación de P4) — ninguno de los dos se pudo verificar el arreglo de H5 sin resolverlos primero:

1. `ramas_despues="$(git ls-remote --heads origin 2>/dev/null | wc -l || echo "$RAMAS_ANTES")"`, bajo `pipefail` (activo desde la línea 73): si `git ls-remote` falla, `wc -l` sobre su entrada vacía **igual** imprime `0` y sale `0`, pero `pipefail` hace que la canalización completa reporte el fallo de `git ls-remote`, así que el `|| echo` **también** se dispara — el resultado capturado son dos líneas concatenadas (`"0\n0"`), no una, y la aritmética siguiente revienta con `syntax error in expression`. Corregido separando la captura del respaldo con `set +e`/`set -e` para leer el código de salida real de la canalización.
2. `huella_adq()` calculaba `publicacion=` **antes** de llamar a `commit_censo_linea()` — el campo solo podía cargar fallos ANTERIORES de la misma corrida (2.5, PDN), nunca el fallo del propio push de esa huella, que es exactamente el caso que H5 pide distinguir. Corregido: se escribe en tentativa (arrastrando lo ya conocido) y, si el push de esa misma huella falla, se corrige el commit local recién hecho — nunca empujado todavía, así que corregirlo no reescribe nada compartido — antes de declarar cerrada la corrida.

## 6 · Suite

`python3 tests/check.py --baseline` → **VERDE**, sin `FAIL` nuevo (3 `FAIL`/1569 `WARN` heredados, ninguno de `TCRON`/`adq_doctor`/`adquiere_cron`). `tests/test_adq_contrato_fix.py`: 20/20. `tests/test_adq_cableado.py`: 27/27 (tras migrar `KAPPA_AUTORIZADA`). `tests/test_adq_doctor.py`: 5/5. `tests/test_adq_config.py`: 3/3.

## 7 · Reservas — lo que este acto no cierra

Ver `## NO-CORRIDO / RESERVAS` en `forense/encargos/2026-09-09-GEN2-ADQ-CONTRATO-FIX.md`. En breve: el registro verbatim de `REVISION-IMPLEMENTACION-PR660-666` (§0 de esta nota, `NC-0134`); reintentos automáticos para `FECHA-INDETERMINADA` (deliberadamente no habilitados); la primera corrida post-arreglo en producción (`NC-0114`, de caja, no de este acto). `NC-0119`/`NC-0115`/`NC-0120` se citan como frontera y no se tocan.

**Contador:** no se mueve. Este acto corrige el selector de adquisición y el vigilante de cron; ningún `CALC` nace, ningún sello se toca, ninguna fuente se descarga.
