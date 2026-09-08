# GEN2-SONDA-2 · OPERACIONALIZA-SONDA-LATERAL

Convierte en capacidad reusable del proyecto la metodología de sonda que ya se
ejecutó con éxito en `PR #197` (`ACTO SONDA-1`), `PR #524`
(`ACTO MAESTRA38-A1 · SONDA-Y-DESCARGA-UNIVERSO-1` + su enmienda
`SONDA-LATERAL-PENDIENTES`) y `PR #542`
(`ACTO MAESTRA38-N12 · SONDA-INSTRUMENTOS-DE-PERCEPCION`). El entregable
principal es `.claude/commands/sonda.md`; el puente mínimo en
`.claude/commands/mapea.md`; este documento registra los tres pilotos reales
que validan que la interfaz funciona sobre huecos vigentes de `origin/main`,
no sobre huecos de juguete.

Base: `origin/main` en `d48014ed8da3879459aeb234de2addd5a8a83ad3` (verificado
con `git fetch --prune` + `git rev-parse origin/main` antes de tocar
archivos; el worktree de esta sesión ya estaba sincronizado a ese SHA, cero
commits de diferencia). Entorno: NUBE (`CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE=
cloud_default`), sin `data/raw`, sin CALC, sin descarga de payloads —
confirmado antes de sondear (§0 del encargo).

Baseline al arranque: `tests/check.py --baseline` → **LÍNEA BASE VERDE**
(3 FAIL · 211 WARN, sin diferencia frente a `tests/baseline.json` congelado en
`dee5fc5`).

---

## Precedentes — patrón extraído, no ceremonia copiada

- **`#197`**: sondear contra portal/fuente real, no solo contra tablas
  internas; distinguir barrera de ausencia de barrera de falta de obtención;
  no descargar por defecto.
- **`#524`**: "Universo desconocido" se explora con nombre propio; una ruta
  oficial fallida no agota una fuente — hay vías hermanas (repositorio,
  API, archivo histórico, mirror, replication package, formato alterno); un
  objeto encontrado se verifica por contenido, no por `HTTP 200`.
- **`#542`**: si NUBE no puede abrir una candidata, no se convierte en
  negativo — pasa a `SIN-FETCH`/CAJA con ficha; tres mecanismos de sonda de
  red independientes (`curl`, estado del proxy, `WebFetch`) es más fuerte que
  uno solo.

`.claude/commands/sonda.md` cita los tres verbatim en su cabecera y reusa,
sin duplicar: `tools/busca_reactivos.py` (búsqueda de reactivos, sin tocar),
`tools/curador_registro/tsv_crudo.py::upsert_fila` (escritor canónico de la
cola, mismo mecanismo que ya usa `tools/arbitra.py`),
`tools/vista_cola_adquisicion.py` (regeneración de la vista), y el
vocabulario A.4/A.5 ya vigente en `.claude/commands/mapea.md`/
`.claude/commands/adquiere.md`. No se creó
`tools/sonda_encola.py`, no se abrió una segunda cola, no se tocó
`tools/curador_registro/registra_cola_adquisicion.py` (migración legacy,
intacta).

---

## Piloto 1 — CONSTRUCTO · `civico.transferencia.atribucion_lider`

### SONDA · `civico.transferencia.atribucion_lider`
Definición: *"Atribución directa del apoyo (líder/presidente vs. gobierno vs.
partido vs. 'es un derecho, de nadie en particular'), en población
beneficiaria, aislada de aprobación presidencial e identidad partidista."*
(`milpa/tramite-ola5-propuesta-v0.yaml:3346-3369`, regla `R7.9`,
`condicion_no_medida` verbatim)

**Estado de entrada:** `HIPÓTESIS-SIN-INSTRUMENTO` desde `MAESTRA38-N5`
(`forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md#2.7`, aceptada por
mesa vía `FP-298`/`N6`, 4/sep/2026). El expediente ya declara la pieza que
falta: *"el falsador RDD (Pensión del Bienestar, efecto electoral
independiente de aprobación presidencial) ya está diseñado en canon; falta el
enlace padrón-beneficiarios/resultado-electoral por sección, **dato
administrativo, no un reactivo de opinión**"* — el propio expediente ya
apunta a que la vía de cierre no es un reactivo de encuesta.

**Modo:** CONSTRUCTO — la pregunta correcta no es "qué otra encuesta trae
esta pregunta" sino "qué otro TIPO de instrumento la mide", porque
`busca_reactivos.py` sólo indexa texto de reactivo/encuesta y es
estructuralmente ciego a un registro administrativo.

**Universo adicional sondeado:**

```
grep -i "atribuye\|credito\|merito\|responsable del apoyo" (busca_reactivos.py, 241 591 filas)
  -> 132 candidatas, las 20 primeras todas tablas CNBV de crédito financiero
     (ADQ15_CNBV_BDIF_inclusion_financiera) -- ruido, no señal política.
grep -i "padron.*bienestar\|pension.*bienestar" sobre
  data/manifiesto.yaml, cola-adquisicion-registro.tsv, aliases-fuentes.tsv,
  data/inventarios/*.md, data/curacion-registro/relaciones.tsv
  -> localiza PUB (Padrón Único de Beneficiarios) y la relación N25/SICEE +
     PREP-2024 (resultados electorales por sección).
```

| candidata | fuente/familia | evidencia de existencia | cobertura aparente | acceso | A.4/A.5 | siguiente paso |
|---|---|---|---|---|---|---|
| `PUB` — Padrón Único de Beneficiarios (Bienestar) | administrativo, `datos.gob.mx` CKAN | fila de cola `estado_A4A5=OBTENIDO`, CSV real en corpus (748 filas, 14 columnas) | **agregado ENTIDAD×TRIMESTRE**, no nominal ni por sección | ya `OBTENIDO`, no requiere adquisición nueva | `EXISTE-NO-SATISFACE` (granularidad insuficiente para el RDD por sección) | verificar si `pub.bienestar.gob.mx`/`cpid.bienestar.gob.mx` (portales de consulta nominal, `data/inventarios/inventario_fuentes_clase-fuente-mexico.md:104`, "no alcanzables en el sondeo" de Tarea B) sirven granularidad más fina — vía LATERAL, en un acto posterior |
| `PREP 2024`/Marco Geográfico Electoral (INE) | administrativo, INE | relación `REL-8b5abcdb9a618f64c2639477` (`EXISTE-NO-SATISFACE`) + `REL-60af9d4edd6d6f562a2f6cb1` (crosswalk sección→municipio, `INTEGRO`) ya en `relaciones.tsv` | resultados **por sección** ya en corpus | ya en corpus | `EXISTE-NO-SATISFACE` (es la mitad electoral del enlace, no mide N25/R7.9 por sí sola) | reusar como llave del lado electoral cuando exista spec que la necesite |

**NEGATIVO ACOTADO:** ningún reactivo de opinión mide esta atribución
(confirmado, universo ampliado: 241 591 filas de texto de reactivo, 4
formulaciones adicionales a las 5 de `N5`, 0 candidatas de opinión). Lo que
SÍ cambió: el tipo de instrumento correcto (enlace administrativo
padrón×resultado electoral por sección) ya tiene sus dos mitades
parcialmente en el corpus, ninguna a la granularidad nominal/seccional que
el enlace exige del lado del padrón. No sondeado: contenido nominal de
`pub.bienestar.gob.mx`/`cpid.bienestar.gob.mx` (red bloqueada, ver piloto 3
para el mismo patrón de bloqueo) ni si existe una versión seccional del PUB
publicada en otro canal.

**HANDOFF:** ninguno nuevo a la cola — `PUB` y `PREP 2024` ya tienen fila
(`OBTENIDO` ambas); un alta duplicaría. Reportado aquí como candidata para
un futuro `/sonda ... LATERAL` sobre los dos portales nominales, o para
quien diseñe la spec GEN2 de esta regla.

**RECOMENDACIÓN:** si un acto futuro necesita cerrar `R7.9`, la vía más
prometedora ya no es buscar más encuestas — es verificar si el padrón
nominal/seccional de Bienestar es alcanzable por alguna vía lateral distinta
del CSV agregado ya obtenido.

---

## Piloto 2 — HERMANAS · `familia.cortejo.urbano_joven_apps`

### SONDA · `familia.cortejo.urbano_joven_apps`
Definición: *"Cómo se conoció a la pareja actual/más reciente, con opción
explícita 'por internet/aplicación', en población joven urbana conectada."*
(`milpa/tramite-ola5-propuesta-v0.yaml:3371-3395`, regla `R5.4`,
`condicion_no_medida` verbatim)

**Estado de entrada:** `HIPÓTESIS-SIN-INSTRUMENTO` desde `MAESTRA38-N5`
(`forense/notas/2026-09-04-MAESTRA38-N5-diseno-9-reglas.md#2.9`, mismo
`FP-298`/`N6`). Universo citado por `N5`: **7 formulaciones, 0/42 536**
filas — el propio expediente ya sugiere el hueco natural: *"módulo de
nupcialidad tipo ENADID o de una ronda de ENDIREH"*.

**Modo:** HERMANAS — ENADID es exactamente la familia que el propio
expediente nombra; falta confirmar si ya está indexada y si el módulo trae
el ítem.

**Universo adicional sondeado:**

```
python3 tools/busca_reactivos.py --palabra "aplicacion" --palabra "internet" \
    --palabra "tinder" --palabra "conocieron" --limite 20
  -> universo declarado: v1_2=178246, ext=63345 (241 591 filas) -- 5.7x más
     ancho que las 42 536 que N5 citó el 4/sep. ENADID2023 SÍ aparece
     indexada (candidatas de "internet", ninguna de cortejo).

python3 tools/busca_reactivos.py --encuesta "enadid" --regex "conoc|nupcia|union" --limite 30
  -> 7 candidatas: TMUJER1.csv, variables conoce/conoce_1..conoce_6.
     texto_reactivo VACÍO en las 7 (limitación declarada, no oculta).
```

| candidata | fuente/familia | evidencia de existencia | cobertura aparente | acceso | A.4/A.5 | siguiente paso |
|---|---|---|---|---|---|---|
| `enadid2023:TMUJER1.csv:conoce_1..6` | ENADID 2023 (INEGI), ya `OBTENIDO` | 7 filas en `v1_2`, `en_corpus=SI` | **incierta** — nombre de variable compatible tanto con "conoce métodos anticonceptivos" (batería típica de encuestas de fecundidad) como con "cómo conoció a su pareja"; `texto_reactivo` vacío impide decidir | payload ya en corpus, cuestionario PDF (`mujer_enadid23.pdf`) también ya `OBTENIDO` en manifiesto | **candidata localizada, no verificada** (ni `EXISTE-SATISFACE` ni `NO-ENCONTRADO` — clasificación pendiente de abrir el cuestionario) | abrir `mujer_enadid23.pdf` (ya en corpus) o el `.dta`/`.sav` de `TMUJER1` y leer la etiqueta real de `conoce_1..6` — operación de CAJA (o NUBE si INEGI deja de estar bloqueado, ver piloto 3) |

**NEGATIVO ACOTADO:** ningún candidato con texto confirmado de cortejo/app en
el universo ampliado (241 591 filas, hoy 5.7× más ancho que cuando `N5`
clasificó la regla). No se pudo abrir ningún payload para leer la etiqueta
real de `conoce_1..6` (NUBE, sin `data/raw`) — la incertidumbre queda
declarada, no resuelta a favor de ninguna lectura.

**HANDOFF:** ninguno a la cola — `ENADID 2023` ya está `OBTENIDO`, no hay
adquisición pendiente. CAJA/manual: abrir `TMUJER1` y el cuestionario para
resolver si `conoce_1..6` es la batería de anticoncepción o algo distinto.

**RECOMENDACIÓN:** antes de reafirmar `HIPÓTESIS-SIN-INSTRUMENTO` en la
próxima revisión de esta regla, alguien con `data/raw` debería leer
`conoce_1..6` de `enadid2023:TMUJER1` — es la primera vez que esta variable
se cruza contra esta regla desde que ENADID entró al corpus.

---

## Piloto 3 — LATERAL · `RUPC` (Registro Único de Proveedores y Contratistas)

### SONDA · `RUPC`
Definición: pieza del hueco "persona + sanción" que la fila `EXT_OF_07`
nombra (`data/curacion-registro/cola-adquisicion-registro.tsv`, fila
`forense/notas/2026-09-06-MAESTRA38-A6-reconciliacion.md#RUPC`).

**Estado de entrada:** `NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)` desde
`ACTO MAESTRA38-A6` (6/sep/2026) — 4 rutas oficiales agotadas (host viejo,
ruta `/norah/`, backend `/backends/rose`, `/whitney/`), razón
`EXIGE-SESION-NAVEGADOR` (control positivo: el host responde a otros
backends de la misma familia, sólo RUPC exige sesión). Receta de navegador
ya en `PAQUETE-RECETAS-11`.

**Modo:** LATERAL — la fuente es conocida, las 4 rutas oficiales ya fallaron
por la misma razón (sesión), la pregunta es si existe una vía distinta al
mismo objeto (folio RUPC por proveedor) que no dependa de esa sesión.

**Universo adicional sondeado:**

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/
000
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://web.archive.org/
000 (connect_rejected)
$ curl -sS "$HTTPS_PROXY/__agentproxy/status"
recentRelayFailures: www.inegi.org.mx:443 connect_rejected (403 a CONNECT,
  policy denial); mismo patrón repetido para datos.gob.mx, archive.org,
  google.com
```

Tres dominios de prueba (INEGI, Wayback Machine, datos.gob.mx) devuelven la
misma firma de bloqueo — **el bloqueo de esta sesión NUBE es de política de
egreso general, no específico de `buengobierno.gob.mx`**: ni siquiera la vía
Wayback/mirror (la que resolvió `CSES`/`Pew` en la enmienda de `#524`) es
alcanzable hoy desde este entorno.

| candidata | fuente/familia | evidencia de existencia | cobertura aparente | acceso | A.4/A.5 | siguiente paso |
|---|---|---|---|---|---|---|
| API pública de contratos adjudicados de CompraNet (folio RUPC del proveedor ganador) | mismo host, endpoint distinto al ya probado | conceptual — no confirmada | desconocida | `SIN-FETCH` (red bloqueada) | candidata sin verificar | probar sin sesión desde CAJA/NUBE con red |
| Plataforma Nacional de Transparencia (PNT/INAI), solicitudes resueltas con RUPC adjunto | repositorio institucional distinto | conceptual — no confirmada | desconocida | `SIN-FETCH` | candidata sin verificar | buscar solicitudes ya resueltas sobre RUPC |
| CKAN `datos.gob.mx`, query `RUPC`/`Registro Único de Proveedores` (distinta de `q=compranet`, ya probada para `DD_COMPRANET`) | catálogo abierto | conceptual — no confirmada | desconocida | `SIN-FETCH` | candidata sin verificar | repetir la consulta CKAN con el término específico |

**NEGATIVO ACOTADO:** las 4 rutas oficiales siguen bloqueadas por la misma
razón que `A6` ya midió (sesión de navegador) — no re-probadas hoy porque el
mecanismo de bloqueo no cambió. 3 rutas laterales nuevas identificadas por
razonamiento, **ninguna verificada por ejecución**: la red de esta sesión
NUBE bloquea de forma general (INEGI, Wayback, datos.gob.mx, Google — no
sólo `buengobierno.gob.mx`), confirmado por 2 mecanismos independientes
(`curl` → `000` en los 4 hosts; `$HTTPS_PROXY/__agentproxy/status` → 403 a
CONNECT, policy denial, en los mismos 4). No sondeado: si las 3 rutas
laterales propuestas existen realmente como dataset — eso exige red
funcional, no disponible hoy.

**HANDOFF:** adquisición — actualizado (no duplicado) el registro existente.
`data/curacion-registro/cola-adquisicion-registro.tsv`, fila `RUPC`
(clave `fila_origen`, mismo mecanismo `upsert_fila` que ya usa
`tools/arbitra.py`): se añadió a la `nota` existente las 3 rutas laterales
propuestas, declaradas `SIN-FETCH`/sin verificar, sin tocar ningún otro
campo ni ninguna otra fila (`git diff --numstat`: 1 línea). Vista
regenerada con `python3 tools/vista_cola_adquisicion.py` (134 filas, mismo
diff de 1 línea, reflejando exactamente el cambio del registro).

**RECOMENDACIÓN:** quien retome `RUPC` debería probar las 3 rutas laterales
antes de recurrir a la receta de sesión de navegador de `PAQUETE-RECETAS-11`
— si cualquiera funciona sin sesión, es más barata.

---

## Medición operativa del acto (punto 9)

| contador | valor |
|---|---|
| `N_huecos_sondeados` | **3** (`civico.transferencia.atribucion_lider`, `familia.cortejo.urbano_joven_apps`, `RUPC`) |
| `N_candidatas_nuevas` | **2** — (a) enlace administrativo padrón-Bienestar×resultado-electoral-por-sección, conectado por primera vez a `civico.transferencia.atribucion_lider`; (b) `enadid2023:TMUJER1:conoce_1..6`, nunca antes cruzado contra `familia.cortejo.urbano_joven_apps`. Las 3 rutas laterales conceptuales de `RUPC` NO se cuentan aquí — no verificadas por ejecución, serían inflar el número con nombres sin confirmar (§9 del encargo) |
| `N_candidatas_ya_conocidas_redescubiertas` | **2** — `PUB` (Padrón Único de Beneficiarios, ya `OBTENIDO`) y `PREP 2024`/Marco Geográfico Electoral (ya en `relaciones.tsv`), ambas ya existían en el repo para otro propósito y se re-surfacearon para el piloto 1 |
| `N_handoffs_adquisicion` | **1** — actualización (no alta) de la fila `RUPC` en `cola-adquisicion-registro.tsv`, vía `upsert_fila`, vista regenerada |
| `N_negativos_que_siguieron_negativos` | **3** — las tres reglas/filas de entrada conservan su clasificación previa (`HIPÓTESIS-SIN-INSTRUMENTO` ×2, `NO-OBTENIDO-POR-ESTE-AGENTE(4 rutas)` ×1); ningún piloto sella ni reclasifica una regla — fuera del perímetro de esta skill |
| `N_negativos_reclasificados_por_nueva_evidencia` | **0** — ninguna reclasificación: esta skill propone, mesa/DIRECCIÓN decide |

El éxito de este acto no es que los tres pilotos encontraran algo — dos
produjeron candidatas concretas sin resolver el hueco (granularidad
insuficiente, texto vacío sin verificar) y uno confirmó un negativo más
acotado (bloqueo de red general, no específico de la fuente). Los tres
dejan un siguiente paso nombrado y accionable, que es el criterio de
aceptación real.

---

## Validación funcional de `/sonda` (punto 12)

1. `/sonda` corrió conceptualmente sobre los 3 pilotos sin inventar universo
   ni estado — cada universo adicional citado arriba trae su comando.
2. Un fallo de fetch (piloto 3, política de egreso NUBE) no terminó como "no
   existe" — quedó `SIN-FETCH`/candidata sin verificar, con el mecanismo de
   bloqueo declarado dos veces (`curl`, `$HTTPS_PROXY/__agentproxy/status`).
3. Una candidata pendiente (`RUPC`) produjo handoff sin duplicar cola —
   `git diff --numstat` confirma 1 línea tocada, la misma en registro y
   vista, mismo escritor canónico que ya usa `tools/arbitra.py`.
4. `/mapea` no se tocó en su función — sólo se le añadió el puente
   `SONDA-RECOMENDADA` como texto opcional al final de su recomendación,
   sigue proponiendo, no decidiendo.
5. `/sonda` tampoco decide ni adopta nada: ninguna fila de `milpa/*.yaml` se
   tocó, ninguna relación se selló, ninguna candidata se declaró
   `EXISTE-SATISFACE` sin verificación de contenido.

## Perímetro respetado

Tocado: `.claude/commands/sonda.md` (nuevo) · `.claude/commands/mapea.md`
(puente mínimo) · este documento ·
`data/curacion-registro/cola-adquisicion-registro.tsv` (1 línea, `RUPC`) ·
`data/cola-adquisicion-v1_0.tsv` (vista regenerada, 1 línea). No tocado:
`milpa/**`, canon sustantivo, `data/manifiesto.yaml`, microdato, specs/
resultados GEN2, medidores, GitHub Actions, Despacha/Revisa/Trámite/Pulso.

## Verificación

`python3 tests/check.py --baseline` corrido al arranque (LÍNEA BASE VERDE,
3 FAIL · 211 WARN) y al cierre de este acto (ver `## CONSUMIDO`/commit de
cierre para la segunda corrida) — sin regresión material nueva.
