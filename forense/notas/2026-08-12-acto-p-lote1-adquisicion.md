# ACTO P·LOTE-1 · Las cinco fuentes firmadas

`ENCARGOS FINALES · PLAN DE DESCARGAS COMPLETO`, 12/ago/2026 (`forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md`), §2. Base declarada por el documento `origin/main = f8eb2e3`; base real de esta sesión `origin/main = e078e46` (merge de PR #183, posterior — `git merge-base --is-ancestor f8eb2e3 origin/main` confirma ancestro, sin deriva que re-derivar salvo la ya conocida: #183 pasó de abierto a fusionado entre la redacción del documento y esta sesión). Worktree `/home/pc0/mm-p-lote1-adquisicion`, rama `acto-p/lote1-adquisicion`.

## 0 · ARRANQUE

1. **REPO.** Clon existente `/home/pc0/Modelado-Mexicano`; worktree nuevo `/home/pc0/mm-p-lote1-adquisicion` (`git worktree add ... origin/main`). `git log -1`: `e078e46 Merge pull request #183 from Josanoforo/acto-o/cola-adquisicion`. `git status`: árbol limpio al abrir.
   - `git worktree add` emitió dos veces `error: could not write config file .git/config: Device or resource busy` — misma contención conocida ([[project-modelado-mexicano-git-config-contention]]). Verificado independientemente: `git log -1` quedó en `e078e46`, `git status` limpio, `git worktree list` lo lista — la creación no falló, solo la escritura de metadato de tracking.
2. **SHA.** `origin/main = e078e46`; `git merge-base --is-ancestor f8eb2e3 origin/main` → confirmado ancestro. Diferencia con la base declarada por el documento: exactamente el merge de PR #183 (esperado — el documento mismo anticipa este caso: "si tu fusión ya corrió, los gates de abajo lo confirmarán por comando").
3. **data/raw.** Ausente al crear el worktree (esperado, gitignorado). Enlazado: `ln -s /home/pc0/mm-corpus/raw data/raw` (mismo destino que la base clon y las demás worktrees). Corpus montado: `ls data/raw/ | wc -l` → 241 entradas. Este acto SÍ descarga — verificación de corpus compartido (defecto PR #77) obligatoria al cierre.
4. **ENTORNO.** `CLAUDE_CODE_REMOTE_ENVIRONMENT_TYPE` sin definir → `sin_variable`. `curl -s -o /dev/null -w "%{http_code}\n" --max-time 10 https://www.inegi.org.mx/` → `200`. Firma de caja confirmada — este acto exige caja y NO nube; entorno correcto.
   - Firma de tres partes (A.2, v2.5): tercera parte `ls data/raw/ | head -1` → no vacío (corpus montado, ver punto 3). Las tres partes coherentes: caja + red + corpus.
5. **ESPEJO.** No se usó. Toda cifra de esta nota sale de este worktree o de comandos de red corridos en esta sesión, con el comando a la vista.
5-bis. **REMOTO.** `git remote -v` → `origin  https://github.com/Josanoforo/Modelado-Mexicano.git` (fetch y push). Confirmado antes de cualquier push.

**Regla A.3 aplicada primero.** El texto completo del documento (los siete actos, §0-§8) se archivó en `forense/encargos/2026-08-12-encargos-finales-plan-descargas-completo.md` como *primer commit* de este acto, antes de lo que sigue.

**§0a/§1 (firma de corte) — verificados CONSUMIDOS antes de arrancar este acto.** `origin/main` en `e078e46`, mensaje `Merge pull request #183 from Josanoforo/acto-o/cola-adquisicion`. El texto de §1 de este documento ("FIRMA DE CORTE... entran ISSP(1)·WVS(3)·EARLY_CHILDHOOD_EDUCATION_2012_2014(4)·GPS(6)·CSES(7). Salen... BRASDEFER(2) y MOBILE_TUTORS(5)") coincide verbatim con lo ya registrado en memoria de sesiones previas sobre el merge de PR #183. Gate del acto (`ls data/cola-adquisicion-*.tsv`) verificado abajo.

```
$ ls data/cola-adquisicion-*.tsv | sort | tail -1
data/cola-adquisicion-2026-08-12.tsv
```

Coincide con lo esperado por el gate. Acto habilitado.

---

## 1 · El lote congelado (verbatim de `data/cola-adquisicion-2026-08-12.tsv`)

Extracción por comando (`awk -F'\t'` filtrando por `fuente_canonica` en las 5 firmadas), columnas completas:

| fuente_canonica | n_necesidades_servidas | destraba_sin_ruta | destraba_condicional_faltante | celda_piloto_FIN | url_conocida | clasificacion_a4_previa | palanca |
|---|---|---|---|---|---|---|---|
| ISSP | 7:N2,N3,N12,N13,N14,N28,N30 | SI (censo fila 12,13,14; N12,N13,N14) | *(21 condiciones individuales por necesidad, ver TSV crudo — resumen: falta verificar texto mexicano/dirección/condicionantes y monitoreo-sanción para N2,N12,N13,N14,N28,N30; N3 sin muestra México confirmada en release final 29 países, no se reabre ADR-54)* | SI | https://www.gesis.org/en/issp/data-and-documentation/social-networks/2017 | CANDIDATAx13+NEGATIVAx1 | 1 |
| WVS | 2:N5,N15 | SI (censo fila 15; N15) | N5/N15: WVS ya en catálogo v2.0, no es puerta nueva, mapeo México pendiente | SI | VACIO — derivado abajo (§4) | CANDIDATA(APERTURA_INDETERMINADA) | 3 |
| EARLY_CHILDHOOD_EDUCATION_PROGRAM_IMPACT_EVALUATION_2012_2014 | 1:N13 | SI (censo fila 13; N13) | N13: item explícito de deber/obligación y llaves cuidador-niño | SI | https://microdata.worldbank.org/catalog/2661/study-description | CANDIDATA(APERTURA_INDETERMINADA) | 4 |
| GPS | 5:N2,N4,N5,N6,N17 | NO | las 5: falta confirmar n de México, texto/codificación exactos y desenlace coobservado pertinente | SI | https://gps.econ.uni-bonn.de/home | CANDIDATA(APERTURA_INDETERMINADA) | 6 |
| CSES | 4:N17,N25,N26,N27 | NO | N17/N25: texto y codificación; N26/N27: no es panel ni padrón de beneficiarios, no identifica por sí solo tratamiento de Pensión del Bienestar | SI | https://cses.org/data-download/cses-module-5-2016-2021/ | CANDIDATA(APERTURA_INDETERMINADA) | 7 |

Texto crudo íntegro (las 21 condiciones de ISSP sin resumir) queda en `data/cola-adquisicion-2026-08-12.tsv`, filas correspondientes — no se transcriben completas aquí por longitud, se citan por referencia al TSV congelado (ya versionado desde PR #183, no cambia).

## 2 · Criterio de cierre, común a las 5 fuentes (A.4/A.5)

**EXISTE-SATISFACE para ESTA adquisición** (no para el modelo — eso es de M-APERTURA/mesa) exige las cuatro condiciones a la vez: (a) el payload se descargó íntegro y quedó en el corpus compartido (`data/raw` real, `/home/pc0/mm-corpus/raw`, no solo en este worktree — verificación PR#77 al cierre); (b) su sha256 quedó registrado en `data/manifiesto.yaml` vía `tests/manifiesto.py --registra`; (c) la decisión de adquisición pasó por la vía del motor (capa2 / `decisiones-adquisicion`) — el TSV de cola no se edita a mano, nunca; (d) se localizó al menos una ficha documental/puerta (RNM o equivalente) y se registró una fila en el conducto (ADR-70).

- Si (a)-(c) se cumplen pero (d) no: **EXISTE-NO-SATISFACE**, declarando qué ficha se buscó y no se encontró.
- Si el portal exige más que registro gratuito (pago, afiliación institucional, licencia restringida): **NO-ACCESIBLE**, con receta manual.
- Si el sondeo A.5 falla en sesión: **NO OBTENIDO POR ESTE AGENTE EN N INTENTOS**, con los N intentos y salida cruda, más receta manual ejecutable en navegador en <1 minuto.
- GESIS (ISSP) y WVS exigen registro gratuito conocido de antemano — se declara y se hace; registro gratuito no es NO-ACCESIBLE (A.4, v2.6).
- Ninguna fuente se abre a nivel variable en este acto — eso es acto posterior (M-APERTURA u otro), por demanda.

## 3 · Nota de contexto ISSP — los tres módulos (verbatim de `forense/notas/2026-08-12-acto-o-cola-adquisicion.md:101`)

> `ISSP` tiene tres URLs distintas (GESIS, tres módulos distintos) — la cola deja solo la primera (`.../social-networks/2017`, la que corresponde a N12/N13/N30) para que la columna quede usable por `curl` sin anotación; las otras dos (`.../social-inequality/2019`, `.../family-and-changing-gender-roles/2012`) quedan declaradas aquí, no en el TSV.

Este lote baja el módulo de la URL de la cola (`social-networks/2017`). Si el portal GESIS ofrece los otros dos módulos al mismo costo de sesión (mismo registro, sin paso adicional de licencia), se bajan y registran también, declarándolo en la ejecución (§ siguiente commit). URLs de los otros dos módulos derivadas por el mismo patrón de la nota de O (no verificadas aún, SIN-FETCH hasta sondear en el commit de ejecución): `https://www.gesis.org/en/issp/data-and-documentation/social-inequality/2019`, `https://www.gesis.org/en/issp/data-and-documentation/family-and-changing-gender-roles/2012`.

## 4 · WVS — portal oficial derivado (candidata SIN-FETCH, A.6)

La cola dejó `url_conocida=VACIO` para WVS. Derivación en esta sesión, por comando, sin usar conocimiento de entrenamiento para concluir nada sobre el portal (A.5, v2.6 — "si no se sondeó en esta sesión, no se sabe"):

```
$ curl -s -o /dev/null -w "%{http_code}\n" --max-time 15 https://www.worldvaluessurvey.org/wvs.jsp
200
```

La página principal es una SPA con navegación por `javaScript:SetContent(...)`, sin hrefs directos a documentación/datos. Localizado el endpoint AJAX real que alimenta el panel de documentación por ola: `src="AJDocumentation.jsp?CndWAVE=7&COUNTRY="` (visible en el HTML crudo de `WVSDocumentationWV7.jsp`, que sondeó `200`). Fetch de ese endpoint con `CndWAVE=7`:

```
$ curl -s --max-time 15 "https://www.worldvaluessurvey.org/AJDocumentation.jsp?CndWAVE=7&COUNTRY=" | grep -n -i mexico
169:    <td>Mexico 2018</td>
```

**Portal oficial declarado para este lote: `https://www.worldvaluessurvey.org/WVSDocumentationWV7.jsp`** (Wave 7, documentación y — según su propia pestaña "Data Download" — acceso a datos). Confirmado en esta sesión, por comando: (1) el portal responde `200`; (2) el levantamiento de México Wave 7 (2018) existe dentro de su panel de documentación (`tr id="3203"`, texto `Mexico 2018`). No confirmado aún: si el archivo de datos descargable (SPSS/dta/csv) está detrás de ese mismo ID o requiere un flujo de registro/solicitud separado — eso se abre en el commit de ejecución, no aquí. Candidata **SIN-FETCH** en el sentido de A.6 hasta ese momento: localizada por navegación de portal propio (no por buscador externo), pero el dato en sí — cuestionario, diccionario, microdato — no se ha abierto todavía.

---

El primer resultado que produzca este procedimiento es el que se reporta.
