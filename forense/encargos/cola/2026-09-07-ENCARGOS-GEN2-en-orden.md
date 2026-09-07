ESTADO: INDICE-DE-COLA — NO SE DESPACHA
ENTORNO: n/a (documento indice; cada encargo vive en su propio archivo de esta carpeta)
ENCOLADO: 2026-09-07 · ACTO GEN2-E0 · ENCOLA, skill `/encola`, PR [COLA]. Gesto de encolado: precedente §1c del transfer maestra-34 (firma D4-a, 1/sep/2026).
BITACORA:
- 2026-09-07 · INDICE · archivo entero de direccion, encolado verbatim por mandato de E0. No lleva estado LISTO-: `/despacha` busca `LISTO-NUBE` y este archivo no lo trae, a proposito. Los seis encargos ejecutables viven en `2026-09-07-GEN2-E1-LIMPIEZA-C1.md` … `2026-09-07-GEN2-E6-AUTOMATIZA-GEN2-2.md`, cada uno con su propio ESTADO y su compuerta.

──── CUERPO VERBATIM DEL ENCARGO (A.3) · el despachador NO lo edita ────

# ENCARGOS · GEN2 · EN ORDEN DE EJECUCIÓN
### dirección (Fable, Maestra 48) · 7/sep/2026 · redactados contra `origin/main = 03bcd6f6` (PR #597, GEN1 cerrado) · ADR máx 388 · FP máx 337 — **deriva, no heredes**: `cierre_acto.py` en cada 0-bis. Todos siguen `instrucciones-proyecto-v2_12.md` y la skill `/acto`. Firmas comunes, verbatim: mesa 6/sep «mi merge manual es la firma de las decisiones»; mesa 7/sep «Integra esto al plan final. Genera el plan final completo para Gen2 y dame los encargos en orden de ejecución». Cada encargo cita el PLAN-FINAL-GEN2 v2.0 por su ruta en `forense/notas/` una vez que E0 lo encole.

---

## E0 · ACTO GEN2-E0 · ENCOLA — el plan y los encargos entran al repo antes de ejecutarse

Cabecera: NUBE (`cloud_default`) · **Sonnet** · COMPUERTA: ninguna. NO se lanza en UBUNTU.
Qué hace: con `/encola` lleva al árbol, verbatim y con sidecar `.sha256` cada uno: `PLAN-FINAL-GEN2-v2_0-2026-09-07.md`, `PROPUESTA-CORRIDA-0-v1_1-2026-09-07.md`, `AUTOMATIZACION-GEN2-y-LIMPIEZA-2026-09-07.md` → `forense/notas/`; y este archivo entero → `forense/encargos/cola/2026-09-07-ENCARGOS-GEN2-en-orden.md`, más un archivo por encargo E1–E6 en `forense/encargos/cola/` (`2026-09-07-GEN2-E1-LIMPIEZA-C1.md` … `-E6-AUTOMATIZA-GEN2-2.md`), estado `LISTO-` salvo los gateados. Censa rótulos nuevos en `canon/registro-rotulos.tsv`: `GEN2`, `LEGACY-GEN1`, `CORRIDA0`, `CALC-`, `RESULT-`, `REPLAY-SMOKE`, `CANDIDATO-VENCIDO`. Suite VERDE. PR `[COLA]`.
A.8: `ls forense/encargos/cola/ | grep -c GEN2` → 0 de 7 archivos; `grep -rl "CORRIDA-0" forense/notas/` → 0. NO-ENCONTRADO en ambos, universo declarado.
Perímetro: `forense/notas/` (3 nuevos + sidecars) · `forense/encargos/cola/` (7 nuevos) · `canon/registro-rotulos.tsv` · cascada. Nada más. Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
Contador: cero, declarado. Lo que NO hace: no lanza nada, no edita ningún encargo.

---

## E1 · ACTO GEN2-E1 · LIMPIEZA-C1 — inventario de árboles, ramas y raíces (solo lectura)

Cabecera: **UBUNTU (caja)** · **Sonnet** · COMPUERTA: ninguna. NO se lanza en NUBE: el terreno que inventaría es la máquina local.
Firmas: mesa 7/sep «quiero un plan de limpieza de worktrees o cualquier rama o branch que pueda quedar volando localmente, no me gustaría que se jalara info o data de otros trabajos en la máquina local».
Qué hace, sin ninguna acción de borrado:
1. Clones: `find "$HOME" -maxdepth 4 -type d -name .git 2>/dev/null` (declara `$HOME`, profundidad, directorios examinados). Por clon: `git worktree list --porcelain`; por árbol: ruta · rama · `HEAD` · `git merge-base HEAD origin/main` y cuántos commits atrás · `git status --porcelain | wc -l` · `git log --branches --not --remotes --oneline | wc -l` (commits no empujados) · `data/raw`: symlink (a dónde) o directorio real (tamaño, n archivos).
2. Raíces: `data/raices.local.yaml` de cada clon (raíces lógicas y si están configuradas; **no pegar rutas físicas en la nota**, solo `raiz_logica · configurada · sha256 del archivo de config`). Por cada raíz real: `python3 tools/barrido_descargas_vs_manifiesto.py` → presentes-no-registrados (candidatos PR #77) y registrados-ausentes, con conteo.
3. Remoto: `git ls-remote --heads origin`; por rama: fusionada en `main` (`git branch -r --merged origin/main`) · PR abierto · trabajo vivo · PARO · sin utilidad aparente. Hoy se espera una: `claude/encargo-maestra38-sello-3-6y5e0z` (PARO).
4. Entregable: `forense/notas/2026-09-07-GEN2-E1-limpieza-arboles.md` con las tres tablas y la **lista propuesta de poda** para firma de mesa (E4), cada fila con su evidencia. Recibo `RECIBO — no requiere firma`; fila `ABIERTA` solo si aparece un payload no registrado o un commit no empujado (eso sí es decisión).
Perímetro: `forense/notas/` (1) · `forense/firmas-pendientes.tsv` · cascada. **No borra, no mueve, no empuja nada.** Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
Contador: cero directo; nace `arboles_fuera_de_politica` con su primer valor medido.

---

## E2 · ACTO GEN2-E2 · C0-A DEMANDA — qué hay que volver a medir, derivado

Cabecera: NUBE · **Opus** · COMPUERTA: E0 fusionado (el plan y la propuesta están en `forense/notas/`; se cita su sha). NO se lanza en UBUNTU: solo lee el repo.
Firmas: propuesta v1.1 §17.5 «El perímetro se deriva desde consumidores activos, no desde inventarios históricos» y §17.10 «Primer acto: C0-A».
COMMIT-0: si E0 aún no fusionó, PARA.
Qué hace: `tools/corrida0.py` nace aquí con **un solo subcomando**, `demanda` (los demás los añade E3; el archivo se crea con la estructura de subcomandos vacía y declarada). `demanda` recorre, en este orden y por lectura: (a) cada conducta con `p:` de cada regla que `milpa.src.emisor.cargar_reglas()` devuelve — MEDIDO y ASIGNADO; (b) coeficientes que `B` lee por `valor_ejecutable` y pares que caen a `asignados_coeficiente` (misma resolución que `tests/test_matriz_sellados.py`); (c) `asignados_probabilidad`; (d) cada celda del marco sorteado vigente (v1.3) con su R, M, L y el agregado como derivado. Emite `data/corrida0/demanda-resultados.tsv` (`resultado_id · consumidor · tipo · valor_legacy · escala_legacy · clase_legacy · acto_legacy · fecha_legacy · payload_ids_legacy · sha256_legacy · script_legacy · spec_legacy · spec_sha_legacy · receta_legacy (OK|PARCIAL:<falta>|SIN-RECETA) · depende_de · corrida_natural · estado=PENDIENTE · vigencia=PENDIENTE · validacion_independiente=NO-HECHA`) y `demanda-corridas.tsv` (`corrida_id · instrumento · payload_ids · medidor_o_spec_candidato · n_resultados · resultados_ids · entorno_requerido · receta · orden_causal 1–7`), determinista (ids por orden de consumidor; dos corridas sobre el mismo SHA = bytes idénticos), grafo acíclico (falla si no), cabecera `# DERIVADO — NO EDITAR`. **No reconstruye recetas desde notas; no escribe `valor_gen2`; no decide agrupaciones ambiguas: las lista.** Nota `forense/notas/2026-09-07-GEN2-E2-C0A.md` con `N_resultados_activos · N_corridas_requeridas · N_resultados_pendientes · N por receta · N por entorno · N por orden causal · clausura activa de payloads (derivada; contrastar con la estimación ~24) · lista SIN-RECETA activos · lo que queda fuera como histórico, contado · lo que el registro no puede decidir`.
A.8: `ls data/corrida0 tools/corrida0.py` → no existen (7/sep). Cifras previas (21 reglas, 50 conductas, 7 coeficientes, 13 asignados, 14 celdas, ~24 payloads) son **estimaciones** que este acto puede contradecir.
Perímetro: `tools/corrida0.py` (nuevo) · `data/corrida0/demanda-*.tsv` (nuevos) · `forense/notas/` (1) · `forense/firmas-pendientes.tsv` (recibo + fila ABIERTA para lo indecidible, si hay) · cascada. **No toca `milpa/**`, canon, `prereg-duelo-v2/`, manifiesto ni specs.** Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
Contador: cero medición; nacen `N_resultados_activos`, `N_corridas_requeridas`, `dependencias_numericas_legacy_activas = N_resultados_activos`.

---

## E3 · ACTO GEN2-E3 · AUTOMATIZA-GEN2-1 — núcleo de `corrida0.py`, `spec-check`, `negativo`, `entorno`, guard en `/acto`, smoke

Cabecera: NUBE · **Opus** · COMPUERTA: E2 fusionado (`tools/corrida0.py` con `demanda` en `main`; `git show origin/main:tools/corrida0.py | grep -c "def demanda"` → 1). NO se lanza en UBUNTU: no necesita corpus; el smoke corre sobre insumos versionados.
Firmas: plan v2.0 §4 y §8 Fase I; propuesta externa aprobada: «El humano decide qué medir. La máquina registra, verifica y conecta mecánicamente lo que efectivamente ocurrió».
Piezas (un PR, un ADR, cuatro piezas — D-11):
**P1 · `corrida0.py preflight / run / verify`.** `preflight CALC-X`: spec.md y spec.yaml existen y están commiteados; sha del md en `main` == el citado en yaml; ids únicos; script existe; inputs en manifiesto con hash; `tests/manifiesto.py --verifica --id …` (todos los ids en una invocación; salida cruda; tres estados A.1 sin colapsar); parámetros, tolerancia y seed declarados; `git status --porcelain` vacío (si no: `PRE-FLIGHT: BLOQUEADO working_tree_dirty=SI`); sin sello incompatible previo. `run CALC-X`: captura `corrida_id · spec_id · fecha · git_commit · script_path · script_blob_sha256 · input_ids · input_sha256 · parametros · seed · python_version · dependencias_materiales · firma_entorno (P3) · exit_code · resultado_ids`; ejecuta el medidor con interfaz estable (`medir(inputs, params) -> {"RESULT-…": valor}`); escribe `ejecucion.json`, `resultados.json`, `sello.sha256` (vía `tools/sella_sha256.py`, no reimplementa). `verify CALC-X`: verifica inputs e identidad de código, reejecuta, compara con la tolerancia declarada → `REPRODUCE / NO-REPRODUCE / NO-EJECUTABLE` con `delta`. Tolerancias por tipo: enteros exactos; flotantes `abs(delta) <= 1e-10` por defecto; bootstrap exacto solo con seed+RNG+código fijados.
**P2 · `spec-check CALC-X`.** Para cada `(archivo, variable)` del yaml consulta **solo los inventarios canónicos vigentes** (`inventario-reactivos-v1_2`, `-descargas-mx-v1_2`, `-ext-v1_0`; nunca `v1_0/v1_1` superados): FAIL si no existe en ese archivo exacto; muestra etiqueta, sección, patrón y filas examinadas; WARN con la etiqueta más cercana (distancia de edición ≤ 2) **sin darla por hallada ni editar la spec**; lista todas las secciones del instrumento presentes en el inventario. Caso de prueba obligatorio: `iiib_hs.dta` con `hs02g` (b3b) vs `p_hs.dta` con `hs02g` (bx) → etiquetas distintas detectadas; `IMMS` → WARN «¿IMSS?».
**P3 · `negativo --patron … --archivos …`** (generaliza `tools/barrido_negativos_m38.py`): imprime patrón, universo, archivos y filas examinadas, aciertos con contexto y la línea para el recibo. **`tools/entorno.py`**: JSON + una línea con `git_commit · git_status · python · dependencias materiales · variables de entorno relevantes · sonda de red (si aplica) · raíces lógicas (`raiz_logica · configurada · config_sha256`, sin rutas físicas) · acceso a corpus`; `run` la incorpora a `ejecucion.json`.
**P4 · guard mínimo en `.claude/commands/acto.md`.** ARRANQUE: `git fetch --prune`; base = `origin/main` HEAD (si no: `git merge` antes de nada; no es PARO); árbol limpio; **duplicado**: rama remota, PR abierto o worktree con el mismo rótulo de acto → `PARA / RESUELVE DUPLICADO` antes del 0-bis; `tools/entorno.py` pegado. Y `limpia_arbol.py --reporta` **mínimo** (worktrees, ramas fusionadas vivas, base atrasada) — el `--aplica` es E4/Fase IV.
**Smoke (P1 sobre GEN1, declarado):** `CALC-SMOKE-0001` = `agregado_v1_3.py` con `spec.yaml` derivada del procedimiento v1.2 y tolerancia `1e-10`; `preflight` VERDE, `run`, `verify` → esperado `REPRODUCE` (precedente: 7/sep, diferencia `3·10⁻¹⁵` en `ic_hi`). Etiquetas: `generacion = LEGACY-GEN1 · tipo = REPLAY-SMOKE · cuenta_gen2 = NO · validacion_independiente = NO-HECHA`. Tests: `tests/test_corrida0.py` (unidad de preflight/verify/spec-check con fixtures pequeños, sin corpus) llamado desde `tests/check.py`.
A.8: `grep -c "def preflight\|def run\|def verify\|def spec_check\|def negativo" tools/corrida0.py` → 0; `ls tools/entorno.py tools/limpia_arbol.py` → no existen; `grep -n "duplicado\|mismo rótulo" .claude/commands/acto.md` → 0.
Perímetro: `tools/corrida0.py` · `tools/entorno.py` · `tools/limpia_arbol.py` · `tests/test_corrida0.py` · `tests/check.py` (llamada + exenciones del encargo verbatim) · `.claude/commands/acto.md` · `data/corrida0/CALC-SMOKE-0001/` · cascada. **No toca `milpa/**`, canon, manifiesto, specs ni `corridas-M/`.** Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
Contador: cero GEN2 (el smoke no cuenta). Sucesores: E5 (primeras corridas), E6 (registro/status/T-REPRO).

---

## E4 · ACTO GEN2-E4 · LIMPIEZA-C2 PODA — con la lista firmada de E1

Cabecera: **UBUNTU (caja)** · **Sonnet** · COMPUERTA: E1 fusionado **y** la lista de poda de su nota lleva la firma de mesa (fila FIRMADA en el tablero, o el merge de un PR que la marque). NO se lanza en NUBE.
Qué hace, solo lo que la lista firmada diga y en este orden: (1) ramas remotas fusionadas/consumidas/PARO → `git push origin --delete` (hoy `sello-3-6y5e0z`); (2) ramas locales fusionadas → `git branch -d`; con commits únicos → **empujar o reportar, nunca borrar**; (3) worktrees de actos CONSUMIDO → antes: `git status`, commits únicos, `barrido_descargas_vs_manifiesto.py` sobre su `data/raw` si es real; lo no registrado se mueve al corpus compartido y se registra en el manifiesto **antes** de `git worktree remove` + `prune`; (4) clones extra con 0 commits únicos, 0 payloads únicos, 0 trabajo útil → borrar; (5) en GitHub: activar *Automatically delete head branches* (mesa lo hace; el acto lo verifica en una rama de prueba). Salida cruda de cada comando en la nota; `limpia_arbol.py --reporta` antes y después, pegado.
Perímetro: sistema de archivos local y remoto según la lista; en el repo solo `forense/notas/` (1), manifiesto **solo si aparece un payload huérfano** (append), tablero, cascada. Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: `arboles_fuera_de_politica → 0`; `ramas_consumidas_vivas → 0`. Lo que NO hace: C-4 íntegro.

---

## E5 · ACTO GEN2-E5 · CALC-0001..0003 — L19, L20 y L21 como primeras corridas GEN2

Cabecera: **UBUNTU (caja, corpus montado)** · **Opus** · COMPUERTA, por producto: E3 fusionado (`corrida0.py` con `preflight/run/verify` en `main`) **y** los tres gates de spec: `git show origin/main:forense/prereg-caja/S12-CSES-spec-v1_0.md | sha256sum` → `870522a34d9538454b5b774ddc33e46f9cd8e8d62a20f31b2d972f9755447336`; `S13-R10-3-spec-v1_0.md` → `c41235b804b0834881b7d3467e25ab0b74946fc03ba14245918e9c7a2e69a515`; `S6-L16-spec-v1_2.md` → `c1cd3b6367d4edc4…` (los 64 caracteres se pegan del sidecar en `main`). Si cualquiera difiere, PARO. NO se lanza en NUBE.
Firmas: plan v2.0 §12.6; plan CORRIDA-0 v1.1 §2 (frontera temporal: la cadena completa existe **antes** de ejecutar o la corrida es legacy).
Sustancia (lote de tres corridas coherentes; una pieza que PARA no tumba a las otras; PARO de entorno A.2 detiene todo):
**CALC-0001 · L19 · CIDE-CSES 2015 contra S12.** `spec.yaml` extraída de S12 (tres brazos POR SEPARADO: zanahoria `pcyc13`, garrote `pcyc14`, experimento `pvoto1/2/3`; desenlace de §2 o `NO-CONSTRUIBLE` declarado; `NO-ESTIMABLE` si numerador `<10`); `spec-check` VERDE; `preflight` VERDE; `run`; `verify`. Outputs `RESULT-` por brazo (n, numeradores, proporciones ponderadas, IC95, veredicto por la escala §4). Registra si el instrumento trae asistencia electoral cruzable con `pcyc13` (insumo de la cláusula de R7.7), sin medirlo salvo que S12 lo pre-registre.
**CALC-0002 · L20 · R10.3 en LAPOP 2019/2021/2023 contra S13.** Una ola, un veredicto; batería y dicotomizaciones idénticas a 2004 según la spec (nombres reales por ola: la spec ya corrigió que dos de cuatro no existen bajo el nombre de D2-h); ponderador por archivo, verificado al abrir; `NO-ESTIMABLE` por numerador. Lectura D2-h en `veredicto`, sin tocar tier.
**CALC-0003 · L21 · Rama A′ de R4.4 en ENNViH 2002 contra S6 v1.2.** Dos disparadores POR SEPARADO (T1 `es09`; T2 crónicas `ec01a-g, ec01h_1, ec01i_1`, solo brazo `b3b`), dos desenlaces POR SEPARADO (D-HS primario con **Tabla A** para `b3b` y **Tabla B** para `bx`; D-CE secundario con su tabla única), variable `LUGAR` de cuatro niveles excluyentes con `AMBOS` y `SOLO-OTRO` fuera del cociente y contados, sensibilidad `AMBOS→PÚBLICO` pre-declarada, ventanas de `es09`/`ce01` leídas del cuestionario en corpus (`ennvih1_2002_hogar_q`) y citadas con página **antes** de la primera celda, ponderadores del `bx` en pareja (`fac_3b_px` y `fac_3a_px`, ambos reportados; el brazo adjudica solo si coinciden en signo), `fac_3b` para `b3b`, llave `folio/ls` a entero, chequeo de consistencia como diagnóstico reportado (no `assert`), 8 filas de contraste (6 estimables como máximo; las `T2 × ·` de `bx` con razón escrita), IC95 por diferencia con bootstrap por hogar dentro de estrato y semilla declarada, escala §4 con `NO-CONCLUYENTE-POR-PONDERADOR`. Codebook `ehh02cb_all.zip` con `zipfile-deflate64` y firma `%PDF` verificada.
Común: COMMIT-1 por corrida (spec.yaml + `spec-check` + `preflight` VERDE + «el primer resultado que produzca este procedimiento es el que se reporta») **antes** de abrir dato; COMMIT-2 con `run` + `verify` + `ejecucion.json`/`resultados.json`/`sello.sha256`; entradas nuevas en la propuesta como `PENDIENTE-DE-MESA` (tokens; prosa en comentario) citando `corrida0_resultado_id`; un tercer commit si una spec estaba mal contra el dato — nunca se corrige hacia atrás.
A.8: `ls data/ | grep -E "^l19|^l20|^l21"` → 0; `ls data/corrida0/ | grep -c CALC-000` → 0 (7/sep). Payloads: ids y sha256 en las specs §6.
Perímetro: `data/corrida0/CALC-000{1,2,3}/` · `forense/notas/2026-09-0X-GEN2-E5-*.md` · `milpa/tramite-ola5-propuesta-v0.yaml` (solo `append`) · `forense/firmas-pendientes.tsv` (recibo) · cascada. **No toca `tramite.yaml`, canon ni specs.** Si te encuentras escribiendo fuera de esta lista, PARA — el perímetro estaba mal calculado y saberlo vale más que el atajo.
Contador: **medición: sí** — hasta 3 corridas y ~14 resultados GEN2 sellados; `N_corridas_selladas 0→3`, `N_resultados_sellados 0→k`. Sucesor: `SELLO-4` (mesa) sobre lo que dejen; E6.

---

## E6 · ACTO GEN2-E6 · AUTOMATIZA-GEN2-2 — registro, status, tablero, T-REPRO

Cabecera: NUBE · **Opus** · COMPUERTA: E5 fusionado (≥2 carpetas `CALC-000*` selladas en `main`; `ls data/corrida0/ | grep -c "^CALC-000"` ≥ 2). NO se lanza en UBUNTU.
Qué hace: `corrida0.py registro` (une demanda de E2 y oferta de `CALC-*/` → `corridas.tsv · resultados.tsv · usos.tsv` con `# DERIVADO — NO EDITAR` y las validaciones de §5 del plan: paran ids duplicados, RESULT sin CALC, uso a RESULT inexistente, CALC sin spec, RESULT sin sello, hash ausente, ciclo, consumidor activo apuntando a LEGACY; avisan RESULT sin consumidor, CALC sin consumidor activo, legacy sin sucesor); `corrida0.py status` (§9 del plan); `tools/tablero_programa.py` deriva los contadores GEN2 de `status`; **T-REPRO** como test dentro de `tests/check.py`: cada RESULT activo GEN2 con id, CALC, spec, script, código fijado, inputs, hashes, parámetros, sello, consumidor; consumidor→RESULT→CALC resolubles; `valor materializado == RESULT` dentro de tolerancia para todo valor de `tramite.yaml` que lleve `corrida0_resultado_id`; línea base congela GEN1. Se activa solo si las corridas de E5 atraviesan el formato completo; si el esquema necesita cambios, se declaran y **no se congela** el gate antes.
A.8: `grep -c "def registro\|def status" tools/corrida0.py` → 0 tras E3; `grep -n "T-REPRO\|corrida0" tests/check.py` → solo la llamada al smoke.
Perímetro: `tools/corrida0.py` · `tools/tablero_programa.py` · `tests/check.py` · `data/corrida0/{corridas,resultados,usos}.tsv` · cascada. Si te encuentras escribiendo fuera de esta lista, PARA.
Contador: cero directo; el tablero pasa a mostrar los contadores GEN2 derivados.

---

## Después de E6 (no se redactan ahora)
`C0-B` lotes sobre `demanda-corridas.tsv` de E2 (specs nuevas para lo `SIN-RECETA` activo, empezando por los coeficientes) · `SELLO-4` · `C0-C` · `C0-D` (M → R → L → marcador v2.0, con el paso 3 del marco) · B-6/B-7 al primer caso · B-8 con dos corridas `ci_replayable` · Fase IV (B-5, B-9 con el dato medido: 63 MB del checkout, pack 38 MB, B-10 en cron).

**Contadores movidos por este documento: cero.** Declarado.
